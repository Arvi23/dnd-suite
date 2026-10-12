# D&D Suite — `dnd-suite.html`

**One file, three tabs: 🗺 Map, 📜 Characters, ⚔ Encounter.** Double-click it like before. The old `editor.html`, `character-creator.html` and `encounter.html` still work, but the suite is now the main app.

- **One character roster for everything.** The Map's party (⚔️ button and player export) and the Encounter's **+ Party** both use the current roster from the Characters tab. The first time the suite opens, the map's old party list moves into a roster called *Map party*.
- **🧙 Party drawer.** On the Map and Encounter tabs, character sheets slide in from the right. In an encounter, select a party member and press **📜 Sheet**.
- **Encounter ↔ sheet sync.** Damage, healing, temp HP and death saves in combat are written to the character sheet, and edits on the sheet show up in the encounter.
- **⋯ menu:**
  - *Back up everything* saves the map, characters, encounter and settings in one `.json`.
  - *Restore* loads a backup, e.g. on another browser or PC.
  - *Import a file from the old apps* accepts a map **Export JSON**, character files or rosters, and saved encounters, and sends each to the right tab.

**Moving your data in.**
- **Edge/Chrome:** your existing map and characters usually show up on their own.
- **Floorp/Firefox:** these keep storage separate per file, so the suite may start empty. In the old apps, export the map with **Export JSON** and your characters, then use **⋯ → Import a file**.

Under the hood each app runs in its own same-origin frame built from a `<template>` inside the file. They share storage but never clash on styles, IDs or hotkeys. The bridge between them is `window.SUITE` in the shell.


## ⚔ Encounter — combat at the table

**Turns.** Each combatant gets an action, a bonus action, a reaction and their movement every turn, shown as chips at the top of the action bar. Extra Attack and monster Multiattack are counted, so the attack buttons stay live until all attacks are used. **Start Combat** begins round 1 and **Next Turn** (or Space) moves on. Players end their own turn with **End Turn**. **■ End** stops combat.

**Legal moves only (⚙ → Rules).** This is off by default.
- When it is on, players can act only on their own turn and only with what they have left. Buttons they can't use are greyed out, and hovering one shows why.
- Reactions such as Shield work outside your turn.
- Outside combat everyone moves freely.
- The DM can always do anything, for any combatant.

**Casting from the sheet.**
- Spells, slots and class resources come live from the character sheet. Casting spends the slot on the sheet.
- Pick a slot level to upcast.
- Targeting depends on the spell:
  - **Single-target spells** (Healing Word, Hold Person, …) need a click on the target.
  - **"Up to N targets"** spells (Bless, Bane, Mass Healing Word…) take that many clicks.
  - **Magic Missile:** click once per dart. It needs line of sight only, so creatures in the way don't matter.
  - **Scorching Ray and Eldritch Blast:** click once per ray or beam.
  - **Areas** (Fireball, Burning Hands, Thunderwave, Spirit Guardians…): on the grid, aim the template and click. Everyone inside is hit automatically, and walls stop the area.
- Rolls, saves, half damage, resistances, concentration (with the CON save when hit) and conditions are applied for you and written to the log.
- Sneak Attack, Divine Smite, maneuver dice, Rage, Second Wind, Ki, Lay on Hands and Bardic Inspiration are on the action bar or the attack options.

**🗺 Grid (battle map).**
- Map basics:
  - 5-ft squares, with an optional background image.
  - **✏ Edit map** paints walls, wooden walls, wooden or iron doors, windows, difficult terrain, water, pits and fog. **Erase** makes any square passable again.
  - **⤢ Fit**, wheel to zoom, right-drag to pan.
- Moving:
  - Click a square to move. The green area shows how far you can go, and hovering shows the path and its cost.
  - Difficult terrain costs double. Enemies block your path. Allies can be passed but you can't stop on them.
  - Leaving an enemy's reach logs an opportunity-attack hint.
- Doors and objects:
  - Click a door next to you to open or close it.
  - Doors, wooden walls and windows have AC and HP. Attack them, and once broken they let creatures and line of sight through.
- Seeing and covering:
  - Line of sight and range are checked when you pick a target.
  - Creatures in the way give half cover (+2).
- DM controls: drag tokens when out of combat (or with Shift held), and use **📍 Place unplaced**.

**👥 Players and control.**
- Add a seat for each player. A seat controls a character plus any familiar or companion. Add a monster or custom combatant as a *companion of* a party member and it follows that character's controller.
- Players can **ask to control** a character. With *Ask me first* on (the default) you get "X wants to control Y — Accept / Deny".
- The DM can also hand control over directly.
- **as: [name]** at the top previews exactly what that player sees and can click:
  - Monsters show *healthy / hurt / bloodied* instead of numbers.
  - Hidden monsters, DM-only log lines and anything under fog are left out.

**Table extras.**
- 👻 **Hidden combatants:** add monsters hidden, then **Reveal** them when they appear.
- ⏱ **Turn timer (⚙):** for example 30 s, either flag the turn when time runs out or end it automatically.
- 🎲 **Dice:** the box under the log rolls dice that everyone sees. Tick **🔒 to DM** for a private roll.

**📚 Preps (prepped encounters).** Build combat maps before the session and run them with one click.
- **+ New prep** opens an editor that sets your live table aside; nothing on it changes.
  - Use everything as usual: paint walls, doors, difficult terrain and fog, and set a background image.
  - Add monsters, hidden ones too, and drag or place them.
  - Tweak any token's name, AC, max HP, speed or side.
  - Add party members, or paint **▶ Party start** squares, where the heroes come in.
  - **📝 Notes** holds tactics and treasure.
- **Save**, or **Save & close**, to return to your table. If you close the browser mid-edit, you're back in the editor next time.
- **▶ Run** puts it on the table:
  - The map goes up with the monsters at full HP in their spots; hidden ones stay hidden.
  - The party lands on the start squares, each character on their own square when they were placed in the prep. Familiars stay with their owner.
  - You can keep the party already in the tracker, with their HP intact, and add anyone missing from the roster.
  - Seats and control carry over, and your notes go to the DM-only log.
- **Edit, duplicate, rename, export and import**: each prep is its own `.prep.json`. **⋯ → Import a file** recognises it too. Suite backups include the whole library.

**❤ Health hints.** Players see exact HP and AC only for what they control. Everyone else, other players' characters included, shows a hint: *Unhurt / Damaged / Heavily damaged / Critical condition / Down*.
- **Table default (⚙):** by % of max HP (damaged below 100%, heavily damaged below 50%, critical below 25%), manual, or show nothing.
- **Per creature (its card → *What players see*):**
  - **% thresholds** or **HP thresholds**, e.g. a boss that looks "Damaged" below 150 HP;
  - **Manual**: one click on a hint sets it;
  - **Show nothing**.
- Hover a creature's HP bar on the left to see what players see right now. Attack lines in the players' log leave out the target's AC.

## 🌐 Online play — `dnd-server.py`

A small Python server (standard library only, nothing to install). It serves the suite to players and passes messages along. The rules, the encounter, your notes and every hidden thing stay in **your** browser, which acts as the host. Each player only ever receives their own filtered view.

1. **Start it**, in the folder that holds `dnd-suite.html`:
   `python3 dnd-server.py` (Windows: `py dnd-server.py`)
   It prints a **DM key** and the addresses players can use.
   - `--dm-key mysecret` fixes the key;
   - `--password goblins` adds a room password;
   - `--port 9000` changes the port (default 8765);
   - `--file path\to\dnd-suite.html` points it at the suite file.
2. **Connect as DM:** open your own `dnd-suite.html` as usual, then go to **Encounter → 🌐 Online**. Enter server `localhost:8765` (or `pi-address:8765`) and the DM key, then **Connect**. Keep that tab open while you play; if it closes, players see "DM is offline" and everything resumes when you reconnect.
3. **Players** open the address the server printed and type a screen name. Then they go to **👥 Players → Ask to control** their character and you accept.
   - They see the battle map, the initiative order (their own HP/AC, health hints for everyone else) and their **full character sheet, read-only**, under *📜 My character*.
   - Refreshing or reconnecting puts them back in the same seat.
4. **Over the internet:** forward the TCP port on your router to the machine running the server. Players then use `http://<your public IP>:8765`, which the server prints when it can look it up. If your router's WAN IP differs from that public IP, you're behind carrier-grade NAT (CGNAT), and port forwarding won't reach you.

Safety:
- Players can't send DM actions.
- Their attacks and spells are re-checked on your side (turn, action economy, range, line of sight, dart counts) when *Enforce legal moves* is on.
- Messages are size- and rate-limited.
- The connection is plain `http`/`ws` (no TLS). That's fine for dice and goblins; don't reuse a real password as the room password.

**🎨 Map textures.** In **✏ Edit map**, the 🎨 picker sets the texture pack for that map:
- **Dungeon stone**
- **Wilderness**
- **Cave**
- **Interior / tavern**
- **Classic (flat)**
- **High contrast**

Each pack draws its own floor, walls, wooden walls, doors (wooden and iron), windows, rubble or brush, water and pits. Every exposed wall face gets a bright outline so rooms read at a glance. If the map has a background image, it replaces the floor texture. The pack is saved with preps.

**👁 Auto-reveal fog (⚙ or the map toolbar, off by default).**
- Squares the party has line of sight to are uncovered as they move, and stay uncovered. Walls and closed doors block sight; opening a door reveals the room behind it.
- **Party sight range** limits how far they see; 0 means unlimited.
- Tip: **Fog all**, then turn auto-reveal on.

**Spell areas.**
- Cones and lines start on the caster's edge. A square counts when at least half of it is inside the area (the DMG grid rule).
- ⚙ can switch to *grid distance* instead: spheres become squares and diagonal lines count 5 ft per square, matching movement.
- Walls and closed doors stop areas.
- The spell list was audited: areas, real ranges, multi-damage spells (Flame Strike, Ice Storm, Meteor Swarm), riders and self-buffs. Walls and waves let you pick the creatures caught in them. Spells the table resolves by hand (Booming Blade, Geas…) are just logged.

**Monsters.** The built-in stat blocks were checked against the 5.1 SRD.
- **Multiattack** is counted from each creature's Multiattack trait.
- **Thrown weapons** (dagger, javelin, spear) are melee within reach and ranged beyond it.
- **Riders on a hit** are rolled and applied: extra damage (*plus 1d6 fire*), and saves with damage or conditions (wolf → prone, ghoul → paralyzed, assassin → poison).
- **Save abilities** get their own buttons, aimed on the map like spells: Fire Breath, Frightful Presence, Horrifying Visage, Engulf. **Recharge** is rolled at the start of the monster's turn and logged for you only, and **↻ Recharge** resets it by hand.
- Imported 5e-database packs get the same treatment.

**🖼 Token art.**
- Every built-in monster has its own silhouette icon, shown in its side's colour on the map, in the initiative list and in the monster picker. Duplicates get a small number badge.
- Imported monsters get a matching icon by name (dragon, goblin, vampire, golem…) when one fits, otherwise their initials.
- **Your own pictures:**
  - In **+ Monster**, the 🖼 next to a monster sets its picture for every future one of that kind.
  - On a creature's card, 🖼 sets the picture for that token. You can apply it to all of that kind at once, and ✕🖼 goes back to the icon.
  - Pictures are shrunk to small JPEGs.
- Party tokens use the portrait from the character sheet.
- Online players receive each picture only once.
- *Monster icons by Cathelineau, DarkZaitzev, Delapouite, Lorc, Skoll and Sparker from game-icons.net, licensed CC BY 3.0. This credit is also shown in the monster picker.*

**🎲 Players roll their own initiative** (⚙ → on by default).
- **Roll Initiative** rolls for monsters and NPCs, and skips characters a player controls.
- Each player gets a banner: **Roll d20+mod**, or type the total they rolled with real dice. Everyone sees the result in the log.
- You see who you're still waiting for. **Start Combat** offers to roll for the stragglers.

**🌑 Light & darkvision.**
- The map toolbar sets the **ambient light**: ☀ Bright, 🌗 Dim or 🌑 Dark.
- In dim light or darkness, a creature sees a square only if it's lit, or within its **darkvision** or **blindsight**:
  - Darkvision comes from the character's race (elves, dwarves, half-orcs, tieflings…) or the monster's senses, and can be edited on the card.
  - Light comes from **🔥 Light source** squares painted in ✏ Edit map (bright 20 ft + dim 20 ft), or a creature that **🔥 carries a light** (torch, lantern or the Light cantrip; players toggle their own).
- The party shares what it sees:
  - Players' screens shade squares the party can't currently see.
  - Monsters standing in darkness nobody can see into are left off the players' map and initiative list.
  - Auto-reveal only lifts fog the party can actually see.
- Attacks follow the rules: attacking a target you can't see is at disadvantage, and attacking one that can't see you is at advantage.

*Server-ready:* every click is sent as an intent to one rules engine (`Host.handle`). Each player's screen is built from their own redacted view (`redact(state, seat)`), which `dnd-server.py` carries over the network.

---

# D&D Map Editor

A two-part map annotation tool for tabletop RPG dungeon masters. Draw regions, place named pins, trace roads, attach lore and NPCs to locations, and export a polished self-contained handout your players can open in any browser.

**No installation. No server. No dependencies.** Just open `editor.html`.

---

## Getting Started

1. Download `editor.html` from the [latest release](https://github.com/Arvi23/dnd-map-tool/releases/latest)
2. Open it in any modern browser (Chrome, Firefox, Edge, Safari)
3. Click **Load Image** or drag a map image onto the window
4. Start annotating

All data is auto-saved to your browser's IndexedDB. Use **Export JSON** to back up your work or move it to another device.

---

## The Two Files

### `editor.html` — DM Editor

The full editing environment. Never share this file with players — it contains DM notes, fog of war state, and unexplored lore.

### `world-map.html` — Player Export

Generated by clicking **Export Player Map**. A completely self-contained file (image + data + styles all embedded) that players can double-click and open offline. Share this freely.

---

## Features

### Map & Navigation
- Load any PNG, JPG, or WebP map image — stored as base64 in localStorage
- Mouse wheel to zoom, middle-click or right-click drag to pan
- Right-click on empty space to deselect and pan simultaneously

### Drawing Tools

**Polygon regions** (`P` key or toolbar)
- Click to place vertices; near the first point a gold snap ring appears to close
- Double-click or `Enter` to close; `Esc` to cancel
- Minimum 3 points

**Road tool** (drag from pin palette)
- Drag the Road tile from the sidebar palette onto the map to start tracing
- Click to add waypoints, `Enter` or double-click to finish, right-click to finish, `Esc` to cancel
- While drawing, endpoints **snap to nearby pins** (gold ring preview) and remember what the route connects
- **Six road types**, each with its own look and legend entry: *Path / Trail* (thin, faint), *Road* (dotted, default), *King's Road / Highway* (thick cased stroke), *River* (smooth blue, draws beneath terrain), *Sea Route* (dashed), and *Wall / Border* (solid with crenellation ticks)
- **Smooth / curved** toggle bends the road naturally through its points (auto-on for rivers and sea routes)
- **Path-following name label** (off by default, per-road toggle) writes the road's name along the curve — "The King's Road", "River Vael". Drag the label on the map to reposition it, or fine-tune with the Position / Straighten / Vertical-offset / Flip controls

**Pins** (drag from pin palette)
- 10 types with distinct icons: City, Town, Village, Dungeon, Ruin, Wilderness, POI, Road, Water, Other (the Road tile drags out the road tool — see above)

**Kingdom / Territory border** (`K` key or 👑 toolbar button)
- Draws a polygon border that's automatically marked as a Kingdom — no extra steps
- Three border display styles: filled, border-only (click-through interior), or hidden (name label only — handy for subtle realm outlines over a detailed map)
- Click-through by design: pins and regions inside a kingdom's border stay individually selectable; clicking empty space inside selects the kingdom
- Auto-detects and lists every settlement, NPC, and building found within its borders
- Existing polygons can also be converted to/from a Kingdom via the toggle in their edit panel
- Each type remembers the last size you used

### Editing
| Action | How |
|--------|-----|
| Select anything | Single click (selects on press — pins, roads, polygons, outlines, labels) |
| Move a pin | Drag it directly |
| Move a region or road | `Ctrl` + drag |
| Move a vertex | Drag the gold handle (visible when region selected) |
| Insert a vertex | Click the faint midpoint diamond between two handles |
| Delete a vertex | Right-click a vertex handle |
| Resize a pin or road | Select it, then scroll wheel |
| Delete a region | `Delete` key, or right-click → Delete |
| Extend a road | Select it, click **Continue Road from End** in the edit panel |

### Per-Location Data

Every region, road, and pin has:
- **Name** and **Type tag**
- **Color** with per-type swatches
- **Fill opacity** slider (0% = border only, useful for territory outlines over detailed maps)
- **Pin size** slider (pins) / **Road size** slider (roads)
- **Fog of War** toggle — unexplored regions render greyed-out in the player export and hide all lore
- **Cover image** — upload a photo or illustration shown at the top of the popup
- **Public Lore** — visible to players in the export
- **DM Notes** — shown only in the editor, never exported (marked with 🔒)
- **Rumours** — short whispers attached to a location (or world-wide). Each has a 👁/🚫 **export toggle**: only 👁 rumours are written into the player handout, so a location being on the map no longer leaks its secrets — flip a rumour to 👁 when the party actually *hears* it (then re-export). DM details/notes on a rumour never export. Manage them per-location or all at once in the **💬 Rumor Tracker**.

All lore, notes, and descriptions support **Markdown** — headers, **bold**/*italic*, lists, and `[[wikilinks]]` to other regions, NPCs, or buildings. Fields render as formatted text wherever they appear (edit panel, lore browser, player popups); click a rendered field to flip it back to a plain-text editor, and it re-renders when you click away. A `[[wikilink]]` becomes a clickable jump straight to its target the moment a matching name exists anywhere in the world.

**NPCs tab** — Add as many NPCs as needed, each with name, portrait image, public description, and private DM notes.

**Buildings tab** — Same structure for inns, shops, temples, dungeons, etc.

**Kingdom Details** (territories only) — Ruler, Government, and Capital fields. Ruler can be linked to any existing NPC and Capital to any existing location; linked entries appear as clickable chips that jump straight to (and expand) the target — in the editor, the lore browser, and the player export alike.

### Sidebar
- Search regions by name
- Filter by type chip (City, Town, Dungeon, etc.)
- Click any entry to select it on the map
- **📍 Places to add** — appears when an imported note mentions a place that doesn't exist yet; drag a chip straight onto the map to drop a pre-named pin there (see Importing from Markdown below)

### Importing from Markdown (Obsidian-friendly)

Already keep your world in Obsidian or another Markdown notebook? Skip retyping it:

| Button | Where | What it does |
|--------|-------|--------------|
| **Import from Markdown** (NPCs tab) | NPC edit panel | Creates a new NPC from a `.md` file's title and body |
| **Import from Markdown** (Buildings tab) | Building edit panel | Creates a new building the same way |
| **Import Lore from Markdown** (Info tab) | Region edit panel | Overwrites the region's Public Lore / DM Notes from a `.md` file |

The importer reads the file's title/heading as the name, the main body as Public Lore, and a "DM Notes"-style section as private notes — a typical Obsidian export drops in with no reformatting.

**Auto-detecting new references** — if the imported note contains `[[wikilinks]]` to entities that don't exist in your world yet, a dialog lets you classify each one:
- **🧑 Person** — stubbed immediately as an empty NPC in the region you imported into, ready to flesh out
- **📍 Place** — too important to guess a location for; instead it's queued in the sidebar's "Places to add" list as a chip you can drag onto the map exactly where it belongs
- **— Skip** — leave it alone; the link will resolve automatically once you create a matching entity by hand

Either path makes the original `[[link]]` clickable the instant a matching name exists.

### Sync from Obsidian (⟳ Sync Vault)

Pick your campaign folder (or the whole vault) and the editor reads every note under `Locations/`, `NPCs/` and `Factions/`. Nothing is written back to Obsidian. You get a preview of what will change, then **Apply** (Ctrl+Z undoes the whole sync). Edge and Chrome remember the folder, so a re-sync is one click; Firefox and Floorp ask for it each time.

| In the vault | On the map |
|---|---|
| `Locations/<Kingdom>/<Town>/<Town>.md` | Settlement pin. `**Tier:**` picks the type (4–5 City, 3 Town, 2 Town/Village, 1 POI; *Fortified / Port / Dungeon* in the tier text override it) |
| Other notes in that town's folder | Its **buildings**, unless they have a Tier ≥ 2, in which case they're settlements too (e.g. the Southern Bastions) |
| `Roman Landmarks (Tier 1).md`-style notes | One POI per `##` section that has a Faction/Region line |
| `NPCs/.../<Town>/<Name>.md` | NPC in the place named by `**Location:** [[Town]]`, otherwise by its folder |
| `Factions/X.md`, region overview notes | Fill the kingdom/faction **shape with the same name**. The "At a Glance" table sets ruler / capital / government. Borders can't be guessed: draw the shape, name it, sync again |

**Sections.** Every heading in a place note becomes a section with its own 👁 export toggle. *Public Knowledge*, *Myths* and *What Outsiders Know* start revealed; everything else starts DM-only. `DM Notes` always goes to the private notes. For NPCs and buildings, only their *Appearance / Description / Public Knowledge / Myths* sections become the public description. Header lines like Role, Status and Aliases (often the spoiler) and everything else go to DM notes.

**🌍 World — wanderers.** NPCs with no place on the map (e.g. `NPCs/Major/Unlocated/`) go to the World list instead of being skipped. Each has a kingdom/faction dropdown (or stays *World*) and a 👁 toggle. In the player Compendium, affiliated wanderers appear under their kingdom's Notable People and the rest under *Wanderers of the World*. A `**Faction:**` or `**Affiliation:**` line in the note pre-selects the kingdom. If a note gains a `**Location:**` that's on the map, the NPC moves into that town on the next sync, and back to World if it loses it.

**Hooks, rumours and tensions.** Each bullet under `Hooks`, `Rumours` or `Current Tensions` becomes a rumour:

```
- [x] **The destroyed cargo manifest.** Someone made a copy before the fire. #true %%Varro's clerk has it%%
```

`[x]` = exported, `[ ]` = DM-only, no box = leave it to the map (new ones start DM-only). The **bold part** is the title and the rest is the detail players can expand. `#true` / `#false` set the truth marker, and `%%…%%` (an Obsidian comment) becomes the rumour's DM note.

**Export toggles.** Every place has an *Included in player export* switch, and every NPC and building has a 👁. Anything new from the vault starts hidden. New places are staged as 📥 pins in the top-left corner and never export until you drag them into position.

**Editing on both sides.** Sync is a per-field 3-way merge: whatever changed since the last sync wins. If the same field changed in Obsidian *and* on the map, the setting in the sync dialog decides (*Obsidian wins* by default). Notes deleted from the vault are flagged, never deleted from the map. Every synced item has an **Open in Obsidian ↗** link.

### Undo / Redo
- `Ctrl+Z` — undo
- `Ctrl+Y` (or `Ctrl+Shift+Z`) — redo
- 100-step history

### Import / Export
| Action | Result |
|--------|--------|
| Export JSON | Full backup including image, all regions, NPCs, buildings, images |
| Import JSON | Restore from backup (merges image if current map is empty) |
| Export Player Map | Generates `world-map.html` — fully self-contained, works offline |

---

## Player Export (`world-map.html`)

- **Parchment aesthetic** — dark background, aged gold palette, Georgia serif font
- Zoom and pan (mouse wheel, right-click drag, pinch-to-zoom on touch)
- Hover glow on clickable regions and pins
- Click any explored location to open a popup:
  - Cover image (if set)
  - Public lore
  - NPCs with portraits (collapsible list)
  - Buildings with images (collapsible list)
- Click a **road** to see its type and the locations it connects; named roads also get a **Routes** section in the Compendium
- Clicking a location that's already open just brings its popup forward — no duplicate windows
- **Party marker** (if placed): players can drag it to move, and resize *only that pin* with the scroll wheel or the −/+ buttons in its popup; their size + position are remembered per browser
- **Per-location notes** — every location popup has a **✎ Your notes** box players can write in; saved in their browser, keyed to that place
- **💬 Rumors tracker** — lists every revealed rumour grouped by location. Players mark each **Known / Tracking / Finished** and keep their own expandable **Notes** under each rumour
- **⤓ Save Notes / ⤒ Load Notes** (toolbar) — one button backs up **everything the player has written** — their journal, rumour statuses, rumour notes, and per-location notes — to a single JSON file. Because the DM re-sends a fresh `world-map.html` whenever the world changes, players **⤒ Load** that backup into the new map (or on another device) and all their tracking carries over (imported entries win; the journal is appended). It all stays in the player’s browser; nothing returns to the DM
- Fog of war regions show *"Unexplored territory — venture forth to reveal its secrets"*
- Collapsible sidebar listing all explored locations, searchable by name
- **Zero external requests** — works completely offline

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `P` | Polygon tool |
| `K` | Kingdom / Territory border tool |
| `Esc` | Cancel drawing / close edit panel |
| `Enter` | Close polygon or road |
| `Delete` | Delete selected region |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl` + drag | Move selected region |
| Right-click (map) | Deselect + pan |
| Right-click (drawing) | Finish road / cancel polygon |
| Scroll wheel | Zoom map (or resize if pin/road is selected) |

---

## Data & Privacy

- All data lives in your browser's IndexedDB — nothing is sent anywhere
- The JSON export is the only way to move data between browsers or devices
- DM notes are stripped from the player export at export time — they never touch the generated file
- Player rumour statuses & notes live only in the player’s browser (and their optional Save/Load JSON) — the DM never sees them

---

## Browser Support

Any modern browser released after 2020. Tested on Chrome, Firefox/Floorp, and Edge. Requires JavaScript enabled.

Hover and selection are handled without re-rendering the map, so interaction stays smooth and clicks register reliably even on large maps with many regions.

---

## License

MIT
