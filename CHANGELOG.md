# Changelog

## 1.0.1 — 2026-10-13
- **Wider sheet panels**: every character-sheet panel has a ↔ button that cycles one column → two columns → full width (saved per character). Widened panels sit in a band above the columns; **Reset Layout** puts everything back.
- Click a truncated spell description in the spell list to show it in full.

## 1.0.0 — 2026-10-13
- **Players roll their own initiative**: optional (on by default). The DM's roll skips player-controlled characters; players roll in-app or type their table roll; the DM sees who's missing and can roll for stragglers.
- **Light & darkvision**: ambient light per map (bright / dim / dark), painted light sources and carried lights, darkvision and blindsight for PCs (by race) and monsters (from their senses). The party's shared vision drives what players see, which monsters appear for them, auto-revealed fog, and advantage or disadvantage for unseen attackers and targets.

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
- **1.1** — DM undo, reaction prompts (Shield, opportunity attacks), shared dice from the sheet, effect durations and repeat saves, multiple live maps, legendary/lair actions, editable player sheets, HTTPS.
