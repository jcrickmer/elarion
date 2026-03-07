# Python Framework Options for Elarion (Research Summary)

Date: March 7, 2026

## Requirements recap (from current product docs)
- Web app with HTML/JavaScript frontend.
- Python 3.12+ backend.
- SQLite-first data layer.
- Real-time sync between player and GM.
- Local username/password auth now, clean path to Apple/Google/Microsoft later.
- Invite-only worlds/campaigns, role-aware permissions.
- Prefer integration of existing wiki capability over building one from scratch.

## Option 1: Django (+ Channels + allauth)
### Pros
- Strongest batteries-included stack for your needs: auth, sessions, admin, ORM, templating are built in.
- Native fit for local username/password auth now (Django auth system).
- Clean social-login path with mature provider ecosystem (allauth supports Apple/Google/Microsoft providers).
- SQLite is first-class and default in Django setup.
- Good domain-model ergonomics for world/campaign/character relationships.
- Mature ecosystem for embedding or tightly integrating a Django-based wiki app.

### Cons
- Real-time at scale needs extra moving parts (Channels + Redis channel layer in production).
- More framework conventions than microframeworks; some initial learning/config overhead.
- Async is strong but not as “async-native everywhere” as lighter ASGI-first stacks.

### Fit assessment
Best overall fit for Elarion MVP + near-term roadmap.

## Option 2: FastAPI (+ SQLAlchemy/Alembic + Authlib)
### Pros
- Excellent async ergonomics and straightforward WebSocket support.
- Very strong for real-time features and API-first architectures.
- Good future external auth path via OAuth/OIDC integrations (commonly with Authlib).
- Fast iteration if you want explicit control over architecture.

### Cons
- Not batteries-included for web app concerns: auth flows, admin UI, permissions framework, and sessions require assembly.
- More integration work to reach the same “out-of-the-box” productivity for invite flows and back-office management.
- Wiki integration is possible but typically less turnkey than Django ecosystem options.

### Fit assessment
Great technical choice if you prioritize async/API control and accept more up-front composition work.

## Option 3: Flask (+ Flask-Login + Flask-SocketIO + extensions)
### Pros
- Minimal, flexible, easy to start.
- Solid extension ecosystem for auth, admin, and OAuth clients.
- SQLite patterns are simple and well-documented.

### Cons
- Real-time story usually means Socket.IO extension and additional deployment complexity.
- You compose many critical pieces yourself (auth, permissions, admin, migrations, policy structure).
- Risk of architecture drift over time in a feature-rich collaborative product.

### Fit assessment
Viable for prototypes, but likely higher long-term maintenance burden than Django for this product shape.

## Option 4: Litestar (+ plugins)
### Pros
- Modern ASGI framework with strong typing, WebSocket support, and high performance.
- Good if you want a modern, explicit, API-centric architecture.

### Cons
- Smaller ecosystem and fewer battle-tested “drop-in” solutions for your exact stack (wiki/auth/admin workflows) compared to Django.
- More design/assembly decisions early in the project.

### Fit assessment
Promising technically, but higher product-delivery risk for a hobby MVP unless you want to invest in framework decisions.

## Recommendation
Choose **Django 6.x** as the primary framework, with:
- `django.contrib.auth` for local username/password now.
- `django-allauth` staged later for Apple/Google/Microsoft.
- `Django Channels` only where needed for real-time character/inventory sync.
- SQLite for MVP, keeping ORM models migration-safe for later PostgreSQL.

Inference: Given your stated preference for fast delivery, minimal reinvention, invite/role workflows, and possible wiki integration, Django minimizes integration risk while still supporting real-time collaboration.

## Suggested implementation sequence
1. Core Django app with users, worlds, campaigns, characters, invites.
2. Role/permission rules (GM vs player mutable-field policy).
3. Real-time updates for character state (Channels on targeted endpoints).
4. Dice roll service + persistent roll log events.
5. Add social sign-on (allauth providers) after core UX is stable.
6. Add embedded or adjacent wiki integration.

## Sources
- Django auth: https://docs.djangoproject.com/en/6.0/topics/auth/
- Django + SQLite default/support: https://docs.djangoproject.com/en/6.0/faq/install/
- Django 5.2 LTS Python compatibility: https://docs.djangoproject.com/en/6.0/releases/5.2/
- Django Channels channel layers: https://channels.readthedocs.io/en/latest/topics/channel_layers.html
- FastAPI WebSockets: https://fastapi.tiangolo.com/advanced/websockets/
- FastAPI security (username/password + JWT example): https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- FastAPI features (includes Starlette capabilities): https://fastapi.tiangolo.com/features/
- Flask installation (Python support): https://flask.palletsprojects.com/en/stable/installation/
- Flask SQLite pattern: https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
- Flask-SocketIO intro/deployment: https://flask-socketio.readthedocs.io/en/latest/
- django-allauth providers index: https://docs.allauth.org/en/latest/socialaccount/providers/index.html
- django-allauth Google: https://docs.allauth.org/en/latest/socialaccount/providers/google.html
- django-allauth Apple: https://docs.allauth.org/en/latest/socialaccount/providers/apple.html
- django-allauth Microsoft: https://docs.allauth.org/en/dev/socialaccount/providers/microsoft.html
- FastAPI PyPI metadata: https://pypi.org/project/fastapi/
- Django PyPI metadata: https://pypi.org/project/Django/
- Flask PyPI metadata: https://pypi.org/project/Flask/
- Litestar PyPI metadata: https://pypi.org/project/litestar/
