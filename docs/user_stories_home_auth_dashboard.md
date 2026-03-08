# User Stories: Home, Authentication, and Post-Login Experience

## Scope
These stories cover:
- Anonymous (logged-out) home screen
- Login process
- First screen for authenticated users

## Epic A: Anonymous Home Screen

### US-A1: Understand product purpose quickly
**As** an anonymous visitor, **I want** to see a clear explanation of what Elarion does, **so that** I can decide if it fits my tabletop campaign needs.

**Acceptance Criteria**
- Home page includes a concise product value statement.
- Page highlights player and GM benefits.
- Primary call-to-action buttons are visible above the fold: `Log in` and `Create account`.

### US-A2: See trust and expectations before signup
**As** an anonymous visitor, **I want** to understand what Elarion is and is not (not a VTT replacement), **so that** I have correct expectations.

**Acceptance Criteria**
- Home page includes a short "what Elarion focuses on" section.
- Home page includes out-of-scope clarification (for example, no heavy map/VTT replacement in MVP).
- A link to product overview or docs is available.

### US-A3: Navigate to authentication paths
**As** an anonymous visitor, **I want** direct access to login and account creation, **so that** I can start quickly.

**Acceptance Criteria**
- `Log in` and `Create account` routes are accessible from home.
- If user is already authenticated, home route redirects to authenticated landing page.

## Epic B: Login and Authentication

### US-B1: Log in with local credentials
**As** a returning user, **I want** to log in with username and password, **so that** I can access my worlds and campaigns.

**Acceptance Criteria**
- Login form accepts username and password.
- Valid credentials create an authenticated session.
- Invalid credentials show a non-revealing error message.
- CSRF protection is enabled.

### US-B2: Stay secure during login
**As** a user, **I want** secure handling of credentials, **so that** my account is protected.

**Acceptance Criteria**
- Passwords are hashed using Django’s default password hashing system.
- Rate limiting/lockout strategy is defined (MVP can start with basic throttling or logging hooks).
- Session cookie settings are secure-by-default for the environment.

### US-B3: Prepare for future external sign-on
**As** a product owner, **I want** auth routes and account model decisions that can support Apple/Google/Microsoft later, **so that** we avoid a rewrite.

**Acceptance Criteria**
- Local auth flow is encapsulated in a dedicated auth app/module.
- User identity remains one-account-per-human.
- Auth integration points are documented for future OAuth/OIDC providers.

## Epic C: Authenticated User Landing Experience

### US-C1: See my campaign context immediately
**As** an authenticated user, **I want** a landing screen that shows worlds, campaigns, and my role in each, **so that** I can resume play quickly.

**Acceptance Criteria**
- Landing page lists memberships grouped by world and campaign.
- Each campaign shows role label (`GM` or `Player`).
- Quick action buttons are present: `Enter campaign`, `Create world`, `Create campaign`.

### US-C2: Handle invite-only collaboration workflow
**As** an authenticated user, **I want** to view and act on invitations, **so that** I can join campaigns cleanly.

**Acceptance Criteria**
- Pending invites are shown on landing page.
- User can accept or decline invite.
- Accepting invite adds membership and campaign appears in active list.

### US-C3: Respect role permissions from first screen
**As** an authenticated user, **I want** role-appropriate options, **so that** I only see controls I can use.

**Acceptance Criteria**
- GM sees roster/invite management links for GM-owned campaigns.
- Players do not see GM-only management actions.
- Unauthorized route access returns 403 or redirect with message.

## Non-Functional Stories (cross-cutting)

### US-N1: Responsive web experience
**As** a user on laptop/tablet, **I want** pages to render cleanly, **so that** I can use Elarion at the table.

**Acceptance Criteria**
- Home, login, and landing pages are usable at common tablet/laptop widths.
- Navigation and primary actions remain visible without horizontal scrolling.

### US-N2: Audit-friendly authentication events
**As** a GM/product owner, **I want** authentication events logged, **so that** troubleshooting and security review are possible.

**Acceptance Criteria**
- Successful login, failed login, and logout events are logged.
- Logs avoid storing raw passwords or sensitive secrets.

## Suggested MVP Build Order
1. Anonymous home page and route guards.
2. Local login/logout and session flow.
3. Authenticated landing page skeleton.
4. Invite list UI placeholders.
5. Role-aware action visibility.
