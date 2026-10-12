# Changelog

## 0.9.0 — 2026-10-13 · first public release
The suite as it stands before 1.0.

**Suite**
- Map editor, character creator and encounter tracker merged into a single `dnd-suite.html` with three tabs, one shared character roster and a slide-in character drawer.
- Backup / restore everything in one `.json`; import files from the old standalone apps.

**Map**
- Sync from an Obsidian vault (places, NPCs, rumours, hooks; per-item export toggles; conflict policy; wanderers list).
- Fogging a kingdom fogs everything inside it.

**Characters**
- Full class spell lists with prepare checkboxes; class resource trackers (rage, ki, superiority dice, Lay on Hands…).

**Encounter**
- Host-authoritative rules engine: action economy, optional legal-moves enforcement, attacks and spellcasting from the sheet (targets, darts, area templates, saves, concentration, conditions, riders, smites, sneak attack).
- Battle grid: walls, doors and windows with HP, difficult terrain, line of sight, cover, movement paths; six texture packs; auto-revealing fog of war.
- Spell areas follow the DMG grid rule (or grid distance, optional); spell metadata audited.
- 54 SRD monsters checked against the SRD 5.1, with icons, multiattack, on-hit riders, save abilities and recharge; custom token pictures; party tokens use sheet portraits.
- Prepped encounters library (build before the session, run in one click).
- Seats and control requests, health hints, hidden monsters, turn timer, public/private dice.

**Online**
- `dnd-server.py`: standard-library relay server; players join by address and screen name, see a filtered view and their read-only character sheet.

## Planned
- **1.0** — players roll their own initiative; darkvision and light-aware vision.
- **1.1** — DM undo, reaction prompts (Shield, opportunity attacks), shared dice from the sheet, effect durations and repeat saves, multiple live maps, legendary/lair actions, editable player sheets, HTTPS.
