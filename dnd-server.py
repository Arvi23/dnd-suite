#!/usr/bin/env python3
"""
dnd-server.py — the online table for dnd-suite.html.  Standard library only (Python 3.8+).

It is deliberately dumb: it serves the suite to players and relays messages.
The rules, the encounter and every secret stay in the DM's browser, which connects as the host.
Each player only ever receives their own filtered view from the DM's browser.

    python3 dnd-server.py                        # port 8765, suite file next to this script
    python3 dnd-server.py --port 9000 --password goblins
    python3 dnd-server.py --file /path/to/dnd-suite.html --dm-key mysecret

Then: DM opens their own dnd-suite.html → Encounter → 🌐 Online → server "localhost:8765" + the DM key.
Players open http://<your public IP>:<port>  (forward that TCP port on the router).
"""
import argparse, asyncio, base64, hashlib, hmac, json, os, secrets, socket, struct, sys, time, urllib.request

GUID = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
MAX_FROM_PLAYER = 64 * 1024          # a player's message is small: an intent or a join
MAX_FROM_HOST = 24 * 1024 * 1024     # the DM sends map images and views
RATE = 40                            # messages per second a player may send before being throttled


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


class Conn:
    def __init__(self, reader, writer, cid):
        self.r, self.w, self.id = reader, writer, cid
        self.role = None          # 'host' | 'player'
        self.name = ''
        self.closed = False
        self.lock = asyncio.Lock()
        self.bucket, self.bucket_t = RATE, time.monotonic()
        self.peer = (writer.get_extra_info('peername') or ('?',))[0]

    async def send(self, obj):
        if self.closed:
            return
        data = json.dumps(obj, separators=(',', ':')).encode()
        n = len(data)
        if n < 126:
            head = struct.pack('!BB', 0x81, n)
        elif n < 65536:
            head = struct.pack('!BBH', 0x81, 126, n)
        else:
            head = struct.pack('!BBQ', 0x81, 127, n)
        try:
            async with self.lock:
                self.w.write(head + data)
                await self.w.drain()
        except Exception:
            self.closed = True

    async def send_raw(self, opcode, payload=b''):
        try:
            async with self.lock:
                self.w.write(struct.pack('!BB', 0x80 | opcode, len(payload)) + payload)
                await self.w.drain()
        except Exception:
            self.closed = True

    def allow(self):
        now = time.monotonic()
        self.bucket = min(RATE, self.bucket + (now - self.bucket_t) * RATE)
        self.bucket_t = now
        if self.bucket < 1:
            return False
        self.bucket -= 1
        return True

    async def recv(self, limit):
        """One complete text message (handles fragmentation, ping/pong, close). None when the socket is done."""
        parts, total = [], 0
        while True:
            b1, b2 = await self.r.readexactly(2)
            fin, op, masked, ln = b1 & 0x80, b1 & 0x0F, b2 & 0x80, b2 & 0x7F
            if ln == 126:
                ln = struct.unpack('!H', await self.r.readexactly(2))[0]
            elif ln == 127:
                ln = struct.unpack('!Q', await self.r.readexactly(8))[0]
            if not masked:                     # clients must mask
                return None
            total += ln
            if total > limit:
                log('message too large from', self.name or self.peer, '- dropping connection')
                return None
            mask = await self.r.readexactly(4)
            raw = await self.r.readexactly(ln)
            payload = bytes(b ^ mask[i & 3] for i, b in enumerate(raw)) if ln < 4096 else _unmask(raw, mask)
            if op == 0x8:
                await self.send_raw(0x8)
                return None
            if op == 0x9:
                await self.send_raw(0xA, payload[:125])
                continue
            if op == 0xA:
                continue
            if op in (0x1, 0x2, 0x0):
                parts.append(payload)
                if fin:
                    return b''.join(parts).decode('utf-8', 'replace')

    def close(self):
        self.closed = True
        try:
            self.w.close()
        except Exception:
            pass


def _unmask(raw, mask):
    # fast path for big frames: XOR with a repeated mask via int arithmetic
    n = len(raw)
    m = (mask * (n // 4 + 1))[:n]
    return (int.from_bytes(raw, 'big') ^ int.from_bytes(m, 'big')).to_bytes(n, 'big')


class Table:
    def __init__(self, args):
        self.args = args
        self.host = None
        self.players = {}       # conn id -> Conn
        self.next_id = 0
        self.urls = []

    # ---------------- HTTP ----------------
    async def handle(self, reader, writer):
        try:
            head = await asyncio.wait_for(reader.readuntil(b'\r\n\r\n'), 15)
        except Exception:
            writer.close()
            return
        lines = head.decode('latin-1').split('\r\n')
        try:
            method, path, _ = lines[0].split(' ', 2)
        except ValueError:
            writer.close()
            return
        hdr = {}
        for ln in lines[1:]:
            if ':' in ln:
                k, v = ln.split(':', 1)
                hdr[k.strip().lower()] = v.strip()
        path = path.split('?', 1)[0]
        if path == '/ws' and hdr.get('upgrade', '').lower() == 'websocket':
            await self.websocket(reader, writer, hdr)
            return
        if method != 'GET':
            await self.reply(writer, 405, b'Method not allowed', 'text/plain')
            return
        if path in ('/', '/index.html', '/play'):
            try:
                with open(self.args.file, 'rb') as f:
                    html = f.read()
            except OSError as e:
                await self.reply(writer, 500, ('Cannot read the suite file: %s' % e).encode(), 'text/plain')
                return
            inject = b'<script>window.NET_CLIENT=true;</script>'
            i = html.find(b'<head>')
            html = html[:i + 6] + inject + html[i + 6:] if i >= 0 else inject + html
            await self.reply(writer, 200, html, 'text/html; charset=utf-8')
            return
        if path == '/health':
            await self.reply(writer, 200, json.dumps({'host': bool(self.host), 'players': len(self.players)}).encode(), 'application/json')
            return
        await self.reply(writer, 404, b'Not found', 'text/plain')

    async def reply(self, writer, code, body, ctype):
        msg = {200: 'OK', 404: 'Not Found', 405: 'Method Not Allowed', 500: 'Server Error'}.get(code, 'OK')
        writer.write(('HTTP/1.1 %d %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nCache-Control: no-store\r\nConnection: close\r\n\r\n'
                      % (code, msg, ctype, len(body))).encode() + body)
        try:
            await writer.drain()
        finally:
            writer.close()

    # ---------------- WebSocket ----------------
    async def websocket(self, reader, writer, hdr):
        key = hdr.get('sec-websocket-key', '')
        accept = base64.b64encode(hashlib.sha1(key.encode() + GUID).digest()).decode()
        writer.write(('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                      'Sec-WebSocket-Accept: %s\r\n\r\n' % accept).encode())
        await writer.drain()
        self.next_id += 1
        c = Conn(reader, writer, 'c%d' % self.next_id)
        pinger = asyncio.ensure_future(self.keepalive(c))
        try:
            while not c.closed:
                text = await c.recv(MAX_FROM_HOST if c.role == 'host' else MAX_FROM_PLAYER)
                if text is None:
                    break
                try:
                    msg = json.loads(text)
                except ValueError:
                    continue
                if not isinstance(msg, dict):
                    continue
                await self.route(c, msg)
        except (asyncio.IncompleteReadError, ConnectionError, OSError):
            pass
        finally:
            pinger.cancel()
            c.close()
            await self.gone(c)

    async def keepalive(self, c):
        try:
            while not c.closed:
                await asyncio.sleep(25)
                await c.send_raw(0x9, b'k')
        except asyncio.CancelledError:
            pass

    async def route(self, c, msg):
        t = msg.get('t')
        if c.role is None:
            if t == 'host':
                if not hmac.compare_digest(str(msg.get('key', '')), self.args.dm_key):
                    await c.send({'t': 'denied', 'why': 'Wrong DM key'})
                    log('rejected a DM login from', c.peer)
                    return
                if self.host and self.host is not c:
                    await self.host.send({'t': 'denied', 'why': 'Another DM window took over'})
                    self.host.close()
                c.role, c.name = 'host', 'DM'
                self.host = c
                log('DM connected from', c.peer)
                await c.send({'t': 'hostOk', 'info': {'urls': self.urls, 'password': bool(self.args.password)}})
                for p in list(self.players.values()):          # re-introduce everyone already waiting
                    await c.send({'t': 'join', 'conn': p.id, 'name': p.name, 'token': p.token})
                return
            if t == 'join':
                if self.args.password and not hmac.compare_digest(str(msg.get('pass', '')), self.args.password):
                    await c.send({'t': 'denied', 'why': 'Wrong room password'})
                    return
                c.role = 'player'
                c.name = str(msg.get('name', 'Player'))[:30]
                c.token = str(msg.get('token', ''))[:64]
                self.players[c.id] = c
                log('%s joined from %s' % (c.name, c.peer))
                if self.host:
                    await self.host.send({'t': 'join', 'conn': c.id, 'name': c.name, 'token': c.token})
                else:
                    await c.send({'t': 'wait', 'why': 'Connected — waiting for the DM to come online.'})
                return
            return
        if c.role == 'host':
            if t == 'to':
                p = self.players.get(msg.get('conn'))
                if p and isinstance(msg.get('msg'), dict):
                    await p.send(msg['msg'])
            elif t == 'kick':
                p = self.players.pop(msg.get('conn'), None)
                if p:
                    log('DM removed', p.name)
                    p.close()
            return
        if c.role == 'player':
            if not c.allow():
                return
            if self.host:
                await self.host.send({'t': 'from', 'conn': c.id, 'msg': msg})
            else:
                await c.send({'t': 'hostGone'})

    async def gone(self, c):
        if c.role == 'host' and self.host is c:
            self.host = None
            log('DM disconnected')
            for p in list(self.players.values()):
                await p.send({'t': 'hostGone'})
        elif c.role == 'player' and self.players.get(c.id) is c:
            del self.players[c.id]
            log(c.name, 'left')
            if self.host:
                await self.host.send({'t': 'leave', 'conn': c.id})


def lan_ips():
    ips = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        ips.add(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ips.add(info[4][0])
    except OSError:
        pass
    return sorted(i for i in ips if not i.startswith('127.'))


def public_ip():
    for url in ('https://api.ipify.org', 'https://ifconfig.me/ip'):
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                ip = r.read().decode().strip()
                if ip and len(ip) < 40:
                    return ip
        except Exception:
            pass
    return None


async def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description='Online table for dnd-suite.html')
    ap.add_argument('--port', type=int, default=8765)
    ap.add_argument('--bind', default='0.0.0.0', help='address to listen on (default: all)')
    ap.add_argument('--file', default=os.path.join(here, 'dnd-suite.html'), help='path to dnd-suite.html')
    ap.add_argument('--dm-key', default=os.environ.get('DND_DM_KEY') or '', help='secret the DM types to connect (random if omitted)')
    ap.add_argument('--password', default=os.environ.get('DND_ROOM_PASSWORD') or '', help='optional password players must type')
    ap.add_argument('--no-public-ip', action='store_true', help="don't look up the public IP")
    args = ap.parse_args()
    if not os.path.isfile(args.file):
        sys.exit('Cannot find the suite at %s — pass --file /path/to/dnd-suite.html' % args.file)
    if not args.dm_key:
        args.dm_key = secrets.token_urlsafe(6)

    table = Table(args)
    server = await asyncio.start_server(table.handle, args.bind, args.port, limit=1 << 16)
    pub = None if args.no_public_ip else await asyncio.get_event_loop().run_in_executor(None, public_ip)
    urls = [{'url': 'http://localhost:%d' % args.port, 'note': 'this computer'}]
    urls += [{'url': 'http://%s:%d' % (ip, args.port), 'note': 'same Wi-Fi / LAN'} for ip in lan_ips()]
    if pub:
        urls.append({'url': 'http://%s:%d' % (pub, args.port), 'note': 'over the internet (needs the port forwarded)'})
    table.urls = urls
    print('\n  ⚔  D&D table is up — serving %s' % args.file)
    print('  DM: open your dnd-suite.html → Encounter → 🌐 Online → server  localhost:%d   DM key:  %s' % (args.port, args.dm_key))
    for u in urls:
        print('  Players: %-34s %s' % (u['url'], u['note']))
    if args.password:
        print('  Room password is on.')
    print('  Ctrl+C to stop.\n', flush=True)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nTable closed.')
