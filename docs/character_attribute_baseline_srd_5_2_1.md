# Character Attribute Baseline (SRD v5.2.1 + Product Context)

Date: March 8, 2026

## Scope
This baseline uses SRD v5.2.1 as the canonical rules source and layers in product constraints from Elarion research (collaboration-first, not VTT-first).

## What the SRD implies belongs on a character

### 1) Identity and origin attributes
- Character name
- Level and XP
- Class (and subclass when applicable)
- Background
- Species
- Alignment
- Languages
- Size and Speed
- Feat(s) and class features selected

Rationale: SRD character creation explicitly has you record these during steps 1-5 and level advancement.

### 2) Core mechanical stats
- Six ability scores: STR, DEX, CON, INT, WIS, CHA
- Ability modifiers (derived)
- Proficiency bonus
- Saving throw proficiencies and totals
- Skill proficiencies and totals
- Passive Perception

Rationale: SRD step 5 calls out filling these numbers from ability modifiers and proficiency.

### 3) Combat and survivability state (highly mutable)
- Armor Class (AC)
- Initiative
- Hit Point max
- Current HP
- Temporary HP
- Hit Dice type and spent count
- Death saving throws (successes/failures)
- Conditions (including stack-aware Exhaustion)

Rationale: SRD character sheet guidance and rules glossary define these as active play state.

### 4) Attack and spellcasting attributes
- Weapon entries (name/type, attack bonus, damage expression, properties)
- Spell save DC
- Spell attack bonus
- Spell slots by level
- Known cantrips
- Prepared spells / available spell list

Rationale: SRD step 5 gives formulas and requires these to be recorded.

### 5) Equipment and economy
- Starting equipment and ongoing inventory
- Currency balances
- Equipped vs carried distinctions

Rationale: SRD has you record starting equipment/coins and references equipment properties.

## Product-layer attributes (from market/competitor analysis)
These are not rules primitives but are needed for Elarion’s value proposition:
- Ownership and visibility: player owner, GM visibility, campaign membership
- Permission model per field (e.g., HP player+GM editable; XP/level GM-only)
- Change audit for shared mutable stats (who changed what and when)
- Dice event linkage (roll -> affected attribute)
- World-scoped reusable character identity across campaigns

Inference from research: tools win by reducing prep friction and preserving continuity; shared state + auditability are core differentiators for collaboration-first products.

## Recommended implementation baseline for first character epic

### MVP Character Core (build first)
- Identity: name, class, species, background, level, XP
- Core stats: six abilities + modifiers, proficiency bonus
- Mutable combat state: AC, initiative, HP max/current/temp, death saves, exhaustion level
- Inventory: item name, quantity, equipped flag, notes
- Permissions: per-field edit policy (player/GM)
- Audit fields: updated_by, updated_at

### Next increment (after core)
- Full skill/saving throw matrix with proficiency toggles
- Hit Dice spend/recovery flows
- Spellcasting panel (save DC, attack bonus, slots, prepared spells)
- Condition engine with rule-aware effects display

## Sources
1. SRD landing and official download links: https://www.dndbeyond.com/srd
2. SRD v5.2.1 PDF (English): https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf
3. D&D Beyond character creation page (2024 basic rules): https://www.dndbeyond.com/sources/dnd/br-2024/creating-a-character/
4. D&D Beyond character origins page: https://www.dndbeyond.com/sources/dnd/br-2024/character-origins
5. Internal project market synthesis: /Users/jason/projects/elarion/docs/market-competitor-research.md
