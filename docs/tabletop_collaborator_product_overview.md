# Elarion - Executive Overview of a Tabletop Collaborator Product

## Product Vision
Elarion is a web-based tabletop RPG collaborator for in-person play groups. It is not a Virtual Tabletop replacement. The product focuses on helping players and Game Masters stay synchronized on character state, inventory, and campaign context while preserving the physical tabletop experience.

## Product Direction
- Primary MVP optimization target: player experience.
- Rules strategy: D&D 5e (2024) first, while keeping architecture simple and extensible for future systems.
- Product style: lightweight, not graphics-heavy, and not mini-map/token driven in early releases.
- Delivery philosophy: hobby project, iterative MVP releases, working software over process overhead.

## MVP 1 Scope
### Player-facing priorities
- Character sheet as the default screen on tablet/laptop.
- Fixed character attributes: name, class, race, core stats (for example Strength, Intelligence).
- Mutable character attributes with live updates.
- Character portrait support.
- Inventory visibility and updates.

### GM-facing priorities
- Real-time visibility into player character status.
- GM timeline and story notes.
- Control of world-specific inventory, classes, races, and related reference data.
- Dice rolling and roll log visibility.

### Session collaboration
- Real-time synchronization between player and GM views.
- Dice log entries should capture actor + roll expression + result (example: `GM Samantha rolled d20 = 8`; `Player Rob rolled 2d8+1 = 12`).

## Permissions and Data Rules
- Players can edit their own mutable attributes such as hit points.
- GMs can also edit mutable player attributes.
- Experience and level are GM-managed fields.
- Any update by player or GM is reflected to both sides in real time.

## Account, Roles, and Access
- One account per human user.
- MVP authentication: simple in-app username/password.
- Invite-only collaboration by default.
- Any user may create a world and campaign; for that context they act as GM/owner.
- GMs manage campaign roster (invite existing users or new users who must sign up).
- Players may accept invites and may leave campaigns.

## Authentication Strategy
- Start with local authentication (username/password) to minimize MVP complexity.
- Design identity internals to allow future external auth providers without account resets.
- Target future external sign-on options: Apple, Google, Microsoft.
- Preserve a single human identity model regardless of auth method (local or external).

## Domain Model
- Rules System: game mechanics definition (MVP baseline is D&D 5e 2024).
- World: setting container linked to one Rules System.
- Campaign: story arc within a World.
- Session: play event within a Campaign.
- Character: belongs to a World and may be reused across multiple campaigns in that World.
- Player-to-Character: one player may own multiple characters.

## Non-Functional Requirements
- Web-delivered application (HTML/JavaScript frontend, Python backend, SQLite in early stages).
- No offline support required for MVP.
- Prefer proven open-source components over custom rebuilds.
- Keep auth architecture migration-friendly (provider abstraction, linkable external identities).
- Wiki capability preference:
  - First choice: integrated open-source wiki package embedded into the stack.
  - Second choice: side-by-side "mash-up" with a mature open-source wiki if that accelerates capability.

## Out of Scope (Early MVP)
- Full VTT battlemap replacement.
- Heavy graphics/3D interaction.
- Monetization features (subscriptions, payments, tier gating).

## Success Intent
Build a useful, cool product for real play groups while learning modern AI-assisted software development workflows.
