# Elarion Style Playbook v0

## Purpose
Create a clear visual direction for an RPG collaboration app that feels imaginative and fantastical while staying clean, readable, and fast for in-session play.

## Design Principles
- Prioritize readability and low cognitive load during live play.
- Add fantasy atmosphere through texture, motifs, and typography accents, not clutter.
- Keep Player UI lighter and calmer; allow higher information density in GM UI.
- Use a consistent token system so UI polish work remains coherent.

## Mood Direction A: Scholarly Arcana
**Vibe:** Arcane academy, spellbooks, observatory charts.
**Best for:** Knowledge-rich worlds, spell-heavy campaigns.

**Color Tokens**
- `bg`: `#F7F4EC`
- `surface`: `#FFFDF8`
- `ink`: `#1F2A44`
- `accent`: `#2E5B9A`
- `accent-2`: `#B68A3C`
- `danger`: `#B23A48`

**Typography**
- Headings: `Cinzel` (or `Cormorant Garamond`)
- Body/UI: `Source Sans 3`

**Motifs**
- Star charts, constellation lines, margin annotations, thin gold separators.

## Mood Direction B: Rugged Expedition
**Vibe:** Frontier travel kit, field journal, weathered maps.
**Best for:** Adventure-focused and survival-leaning tables.

**Color Tokens**
- `bg`: `#F1ECE2`
- `surface`: `#FAF7F0`
- `ink`: `#2A241E`
- `accent`: `#556B2F`
- `accent-2`: `#8C5A2B`
- `danger`: `#9C2F2F`

**Typography**
- Headings: `Alegreya SC`
- Body/UI: `Work Sans`

**Motifs**
- Topographic lines, compass marks, leather/linen texture.

## Mood Direction C: Candlelit Chronicle
**Vibe:** Tavern table, parchment notes, warm lantern light.
**Best for:** Character drama, lore, narrative campaigns.

**Color Tokens**
- `bg`: `#2B211A`
- `surface`: `#3A2D23`
- `surface-light`: `#F6E7C9`
- `ink`: `#1B140F`
- `accent`: `#C17C2E`
- `danger`: `#A94438`

**Typography**
- Headings: `IM Fell English SC`
- Body/UI: `Noto Sans`

**Motifs**
- Wax seal marks, ink blot corners, subtle paper grain.

## Mood Direction D: High Mythic
**Vibe:** Heroic banners, monumental fantasy, sacred geometry.
**Best for:** Epic campaigns and high-drama encounters.

**Color Tokens**
- `bg`: `#EAF0F8`
- `surface`: `#F8FBFF`
- `ink`: `#12223A`
- `accent`: `#2D6CDF`
- `accent-2`: `#D4AF37`
- `danger`: `#B02A37`

**Typography**
- Headings: `Marcellus`
- Body/UI: `Inter` (or `Public Sans`)

**Motifs**
- Heraldic dividers, sigils, vaulted-arch framing.

## Player vs GM Application Rules
- **Player Screen:** larger stat cards, calmer backgrounds, fewer simultaneous callouts.
- **GM Screen:** denser tables, stronger section boundaries, high contrast for scanning.
- Keep decorative texture opacity under 8%.
- Never place ornament behind critical numeric values (HP, AC, roll totals).

## Do / Don’t
**Do**
- Use one dominant accent and one secondary accent per theme.
- Reserve high-saturation color for alerts and key actions.
- Keep spacing predictable (`8px` base scale).

**Don’t**
- Mix multiple fantasy motifs in one screen.
- Use distressed textures where form readability drops.
- Add animation to live-updating combat metrics.

## Recommended Initial Candidate
Start with **Scholarly Arcana** as primary and **Rugged Expedition** as fallback. Both balance fantasy tone with clean operational UX for MVP.
