# Character-Focused Epic Set and Sprint-Ready User Stories

Date: March 8, 2026

## Confirmed Product Decisions (from clarification)
- Character-rules scope is at the **World** level (not Campaign).
- New world creation starts from selectable SRD 5.2.1 baseline concepts, then world-specific edits are allowed.
- World-rule changes apply **immediately** and must resolve character state immediately.
- Player can mutate play-state/loadout fields (equip/swap/use), but not core build attributes during campaign play.
- GM can make all player-permitted edits plus higher-authority edits.
- MVP homebrew scope includes species, classes/subclasses, spells, items/weapons, backgrounds.
- Spell rules require **full custom progression tables** in MVP.
- World rules changes are visible to all via a shared change log.
- MVP uses **live edits** (no draft/publish).
- World supports **co-GMs**; each campaign has a single GM.
- Top first-sprint priorities: world rules catalog management; constrained character creation; inventory/equipment overrides.

## Epic Set

### Epic CHR-EPIC-1: World Rules Catalog Management
Build world-scoped rules catalogs seeded from SRD baseline with include/exclude/add/edit for species, classes/subclasses, spells, items/weapons, and backgrounds.

### Epic CHR-EPIC-2: Character Creation Constrained by World Rules
Build character creation and edit flows that only allow world-approved options and enforce mutability policies.

### Epic CHR-EPIC-3: Inventory and Equipment Overrides
Enable world-specific inventory/equipment definitions and player/GM equip/use behavior within permission rules.

### Epic CHR-EPIC-4: Character Revalidation and Change Propagation
Ensure immediate revalidation/propagation when world rules change and surface impact to players/GM.

### Epic CHR-EPIC-5: Full Custom Spell Progressions
Provide world-managed class/subclass spell progressions, available spell sets, and automatic character spellbook recalculation.

### Epic CHR-EPIC-6: Shared World Rules Change Log
Provide visible-to-all change feed for world-rule updates and resulting character-impact events.

## Sprint-Ready User Stories (initial backlog)

### Sprint 1 (Top priority implementation order)

#### CHR-US-01: Create world from selectable SRD baseline
**As** a GM, **I want** to initialize a world by selecting SRD concept sets, **so that** I start from a curated baseline.

**Acceptance Criteria**
- World creation UI allows selecting baseline concept groups (species, classes/subclasses, spells, items/weapons, backgrounds).
- Selected concepts are copied into world-scoped catalogs.
- Unselected concepts are unavailable in that world.

#### CHR-US-02: World rules catalog CRUD for top entities
**As** a GM/co-GM, **I want** to include/exclude/add/edit catalog entries, **so that** world rules match setting lore.

**Acceptance Criteria**
- CRUD supported for species, classes/subclasses, items/weapons, backgrounds.
- Co-GM can edit world catalogs; non-GM cannot.
- Edits are immediately live.

#### CHR-US-03: Character creation constrained by world catalogs
**As** a player, **I want** only world-allowed options during creation, **so that** my character is valid for that world.

**Acceptance Criteria**
- Character creation pickers only show world-allowed catalog entries.
- Submit fails with validation error if payload includes excluded options.
- Created character stores world linkage for reuse across campaigns in that world.

#### CHR-US-04: Enforce mutable vs non-mutable character fields
**As** a player/GM, **I want** field-level permissions, **so that** campaign play changes are controlled.

**Acceptance Criteria**
- Base build fields (e.g., ability scores) are not player-editable in campaign play.
- Loadout/session fields (equipped weapon/armor, spell-use tracking) are player-editable.
- GM can edit all player-editable fields and GM-authority fields.

#### CHR-US-05: World equipment overrides in character inventory
**As** a GM/player, **I want** world-specific item/equipment definitions reflected in inventory, **so that** equipment choices fit world rules.

**Acceptance Criteria**
- World item catalog supports custom add/edit and SRD item exclusion.
- Character inventory only allows world-approved items.
- Equip/unequip actions follow mutability permissions.

### Sprint 2 (next-high-value)

#### CHR-US-06: Immediate character revalidation on rules edits
**As** a GM/player, **I want** character data to update/flag immediately when world rules change, **so that** no stale invalid state remains.

**Acceptance Criteria**
- Rules changes trigger synchronous/near-real-time revalidation of impacted characters.
- Invalid references are removed, replaced, or flagged according to configured behavior.
- Impact summary is visible to GM and affected players.

#### CHR-US-07: Full custom spell progression tables
**As** a GM/co-GM, **I want** custom spell progression by class/subclass/level, **so that** magic systems match world design.

**Acceptance Criteria**
- GM can edit progression tables per class/subclass.
- Character spell availability recalculates immediately on table changes.
- Excluded spells become unavailable in character selection/play state.

#### CHR-US-08: World rules change log visible to all
**As** a player/GM, **I want** to see world rules changes, **so that** everyone stays aligned.

**Acceptance Criteria**
- Change log records actor, timestamp, entity, and change summary.
- Log is visible to all world participants.
- Character-impact events are linked from the same feed.

### Optional stretch (if capacity permits)
- CHR-US-09: Link character background entries to wiki pages.
- CHR-US-10: Co-GM invitation/role management for world administration.

## Recommended Implementation Order
1. CHR-US-01
2. CHR-US-02
3. CHR-US-03
4. CHR-US-05
5. CHR-US-04
6. CHR-US-06
7. CHR-US-08
8. CHR-US-07
9. CHR-US-09
10. CHR-US-10
