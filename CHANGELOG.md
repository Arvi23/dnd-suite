# Changelog

## Unreleased
From the first look by other DMs.
- **Movement fixes.** Large and bigger tokens were placed from their top-left corner, so their range, path and click target were off by a square or more; they're now centred on the pointer, the range shows their whole footprint, and you can click inside your own big token to shuffle it. Tokens could slip diagonally between two walls that touch at a corner; they can't now. Stunned or paralysed enemies no longer let you walk through them; the dead don't block. Creatures two sizes apart can pass each other, and halflings can pass anything bigger. Prone means crawling at double cost, with a **Stand up** button. Drag your own token to move. The path preview takes the straightest route and shows a ghost, the cost, and amber/red when it's over your movement.
- **Dying and death are obvious.** Dying, stable and dead states on the map, in the initiative list, in the player's banner and action panel, with death-save pips and flashes. One death save per turn; the dead and stable are skipped in the turn order; healing doesn't work on the dead, Revivify and friends do; stable characters taking damage start dying again; monsters at 0 HP die.
- **Undo / redo.** The DM can undo anything, across turns (sheet slots and resources included); players can undo their own actions until they end their turn, without re-rolling dice by default (⚙ setting). Ctrl+Z / Ctrl+Y.
- **Class action economy.** Thief: Fast Hands, Thief's Reflexes. Rogue: Steady Aim. Monk: Martial Arts bonus strike, Unarmored Movement. Barbarian: Fast Movement, Frenzy. Fighter: Action Surge once per turn, Eldritch Knight War Magic. War Cleric: War Priest. Moon Druid: bonus-action Wild Shape. Gloom Stalker: Dread Ambusher. Sorcerer: Quickened Spell. Haste and Slow. The bonus-action spell rule.
- The top bar names whose turn it is; players get a "Your turn" flash.

## 1.0.0 — 2026-10-13
- **Wider sheet panels**: every character-sheet panel has a ↔ button that cycles one column → two columns → full width (saved per character). Widened panels sit in a band above the columns; **Reset Layout** puts everything back.
- Click a truncated spell description in the spell list to show it in full.
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
- **1.1** — reaction prompts (Shield, opportunity attacks), shared dice from the sheet, effect durations and repeat saves, multiple live maps, legendary/lair actions, editable player sheets, HTTPS.
