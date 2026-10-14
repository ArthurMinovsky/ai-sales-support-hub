# AI Sales Support Hub

A protected product catalog and AI recommendation workspace for sales teams.

## Features

- FastAPI REST API with Swagger, username/password authentication and signed one-hour JWTs.
- Next.js TypeScript Web with registration, product CRUD, search and clear provider-error states.
- Registration uses Username, Password and Confirm password. Email is neither collected nor stored. Passwords use Argon2id hashing.
- Ten fictional demo products use the neutral Demo Sensors and Demo Automation brands.
- OpenRouter ranks a catalog shortlist. The backend resolves returned IDs against stored products and returns up to three suggestions. Missing/broken inference returns 503 AI_UNAVAILABLE.
- HttpOnly browser sessions, mutation Origin checks and backend bearer validation.

## One-command Docker startup

Requires Docker Engine with Compose v2, OpenSSL and network access to pull/build images.

```sh
git clone https://github.com/ArthurMinovsky/ai-sales-support-hub.git && cd ai-sales-support-hub && (umask 077; printf 'JWT_SECRET=%s\n' "$(openssl rand -hex 32)" > .env) && export COMPOSE_PROJECT_NAME=saleshub-implementation-check && docker compose up --build --force-recreate -d --wait --wait-timeout 180 && ./scripts/status.sh
```

From an existing checkout with its private .env configured, use `./start`. It builds and force-recreates the services, waits for health and prints the actual Web, API and Swagger URLs. Docker assigns available host ports. Internal ports stay Web 3000/API 8000.

**Disposable data:** every API container start/restart/recreation starts with zero accounts and ten demo products. All registrations and product edits from the previous container run disappear. Page reloads preserve edits while the API is running. An unchanged `docker compose up` may leave running containers untouched and therefore does not reset them. Use the documented fresh-start command or `docker compose -p saleshub-implementation-check restart api` for a clean API run.

SQLite uses a bounded 64 MiB tmpfs owned by the non-root API user. The old named volume is not mounted. Earlier JWTs are rejected after an API restart even if account IDs are reused. This configuration is for disposable testing, not durable business storage.

Live AI requires an OPENROUTER_API_KEY in the ignored local .env. The Web and CRUD start without that key. Keep JWT_SECRET and provider credentials private. Leave API_PORT=0, WEB_PORT=0 and APP_ORIGIN blank for direct Docker access. Behind an HTTPS reverse proxy, configure APP_ORIGIN as the exact public origin.

## API

Registration: POST /api/auth/register with {username, password, confirm_password}. Success returns {id, username, created_at}. Mismatched passwords or invalid fields return 422. Duplicate usernames return 409.

Login: POST /api/auth/login with {username, password}. The direct API returns a bearer token with expires_in=3600. The Web BFF stores it in an HttpOnly cookie and returns no bearer token to browser JavaScript.

Protected endpoints: GET /api/auth/me, product CRUD at /api/products and POST /api/suggestions. Public readiness: GET /health. Swagger: /docs.

## Verification

See tests/verification/README.md for isolated backend, browser, reset, security and CI checks. Current repair evidence is summarized in docs/verification/REPAIR-REPORT.md. Mock-provider tests verify UI/API behavior; they do not constitute a new live AI call. Historical evidence remains tied to its original execution and does not prove this revision.

The demo has a shared catalog. Enterprise roles, tenant isolation, durable storage and external hosting are future work.
