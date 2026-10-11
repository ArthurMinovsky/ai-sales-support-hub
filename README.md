# AI Sales Support Hub

A small, demo-oriented product catalog and AI recommendation workspace for Sales Support Hub's Forward Deployed AI Engineer project.

> **Source status:** Backend tests (11/11), browser tests (15/15), TypeScript checks, reproducible npm installation, Docker image builds, local Compose readiness, all four scanner categories and a redacted live OpenRouter inference have been executed — most recently against the realism-upgraded source (realistic 10-product catalog, professional UI). GitHub Actions, external hosting and manual acceptance remain pending. See the evidence matrix for exact scope and findings.

## Stack and features

- Python FastAPI + Swagger at `/docs` with user registration/login, backend JWT verification (3600s) and Product CRUD.
- SQLAlchemy and persistent named-volume SQLite database seeded with **ten realistic fictional products** across Demo Sensors (VisionScan, VibeSense, ThermoNode, GateLink) and Demo Automation (FlowBridge, DocuMind, AssistDesk, PredictIQ) families. They are synthetic examples, not real offerings.
- Authenticated `POST /api/suggestions`: lexical candidate shortlist → OpenRouter Chat Completions → strict catalog Product-ID allowlist. Missing/broken provider returns explicit `503 AI_UNAVAILABLE`, never fabricated AI success.
- Next.js 15 TypeScript web, server-side BFF HttpOnly cookie, Origin checks on mutation requests, protected pages.
- Pytest, Playwright, Docker Compose, GitHub Actions, four scanner configurations and evidence matrix prepared for separately authorized execution.

## Reviewer launch (LOCALLY VERIFIED; LIVE AI AND CI PENDING)

**Prerequisites:** Docker Engine + Docker Compose v2, network access for pulling images/dependencies, and a strong local JWT key. AI inference requires separately configured OpenRouter API key; catalog CRUD does not.

1. Copy `.env.example` to `.env` (do not commit). Set `JWT_SECRET` to 32+ random characters. Optionally set `OPENROUTER_API_KEY` and `OPENROUTER_MODEL`.
2. Start both services with **one command**:

   ```sh
   docker compose -p saleshub-implementation-check up -d --build
   ```

3. Docker automatically allocates an unused host port for Web and API — no fixed port to collide with anything else on the machine. Get the current URLs with one command:

   ```sh
   ./scripts/status.sh
   ```

   Or discover them manually:

   ```sh
   docker compose -p saleshub-implementation-check port --index 1 web 3000
   docker compose -p saleshub-implementation-check port --index 1 api 8000
   ```

TEST-010 verified user and product persistence across `docker compose down` (without `-v`) and re-up. The evidence records the named volume and persisted product. **Never run `docker compose down -v` on data you wish to retain.**

Host port allocation avoids collisions with existing containers on each machine. Internal container ports stay `3000` and `8000`; allocated host ports can change when containers are recreated. Leave `WEB_PORT=0`, `API_PORT=0` and `APP_ORIGIN=` for direct Docker access. Set `WEB_PORT` or `API_PORT` to a chosen host port when a stable mapping is needed. If an override is occupied, Docker reports an error; use `0` to restore automatic allocation.

The browser's mutation Origin must match the actual request Host and scheme in direct Docker mode. Behind a reverse proxy, configure `APP_ORIGIN` as the exact public URL (for example `https://sales.example`) so the configured origin stays strict and session cookies use HTTPS. Forwarded host headers do not authorize browser mutations.

## Suggested user walkthrough

Register a new user (username/email/password 10+ chars) → Log in (one-hour JWT) → Manage Products (add/edit/delete) → Product Search (customer needs) → recommendation cards linked to known catalog IDs. The seed catalog is a realistic fictional Sales Support Hub-style product set; it is not Sales Support Hub's real catalog. The UI uses self-contained system fonts — no remote font or CDN requests.

## API endpoints

| Method | Path | Auth |
|---|---|---|
| POST | `/api/auth/register` | Public |
| POST | `/api/auth/login` | Public |
| GET | `/api/auth/me` | Bearer JWT |
| GET/POST | `/api/products` | Bearer JWT |
| GET/PUT/DELETE | `/api/products/{id}` | Bearer JWT |
| POST | `/api/suggestions` | Bearer JWT |
| GET | `/health` | Public |

Swagger login returns an access token for direct API testing; the browser does not read that token. Backend enforces bearer checks on its own even when called outside Next.js.

## Verification / security status

- Backend command: `cd backend && pip install -e '.[test]' && pytest -q`. Latest run: 11 passed; XML is in `evidence/backend/pytest-results-post-origin-fix.xml`.
- Frontend commands: `cd web && npm ci && npm run typecheck && npm run build`. Start an isolated fixture with `docker compose -f compose.yaml -f compose.e2e.yaml -p saleshub-e2e up --build -d`, then run `COMPOSE_PROJECT_NAME=saleshub-e2e npm run test:e2e` from `web/`; Playwright discovers its published Web port. `PLAYWRIGHT_BASE_URL` can override discovery for an existing test target. Final run: 15 passed (4 journeys + origin-policy suite); see `evidence/frontend/playwright-execution.json` and `evidence/frontend/playwright-report/`.
- Mock OpenRouter in E2E verifies deterministic UI/error behavior only. A real, redacted live provider inference also passed (TEST-018); see `evidence/openrouter/live-inference-redacted.json`.
- SCA, SAST, DAST and IaC scans were executed; raw outputs and reviewed findings are in `evidence/security/`. SCA reported zero advisories, Semgrep reported zero findings, Checkov completed with one documented false-positive skip, and ZAP completed with eight warning categories. See `evidence/security/scan-review.json`; these results do not mean zero security risk.
- Historical local TEST-020/021 passed: Compose API and Web became healthy, Swagger and OpenAPI returned HTTP 200 on fixed test host ports. Dynamic-port verification is recorded separately in `evidence/dynamic-ports/`; discover the current URLs with `docker compose port`.
- CI: `.github/workflows/ci.yml` includes tests, builds, scans and an image artifact. TEST-022 has not run because there is no GitHub remote or push yet (the verified state is committed locally).

More detailed procedures: `tests/verification/README.md`; evidence sources: `docs/verification/EVIDENCE-MATRIX.md`.

For scanner runs, set `COMPOSE_PROJECT_NAME` to the running stack; `scripts/security/run-scans.sh` discovers Web/API host ports and verifies both before DAST. `DAST_TARGET` and `API_BASE_URL` support explicit target URLs. On Docker Desktop, the scanner can use the Compose network with `DAST_DOCKER_NETWORK=<project>_default` and `DAST_DOCKER_TARGET=http://web:3000`; on Linux its default host network reaches the discovered URL.

## demonstration materials and constraints

- `docs/presentation/PITCH.md` covers As Is/To Be, Architecture, System Features, User Stories and UI Flow in <=10 minutes. Rehearsal pending.
- The app is designed for a single-host small catalog; no enterprise RBAC, RAG/vector DB or full analytics dashboard.
- There is no GitHub repository URL or live OpenRouter key. TEST-025 pitch rehearsal and TEST-026 reviewer acceptance remain pending. Local Compose verification is not external hosting.

## Project governance

`docs/instructions/` contains the approved OUTCOME, CONSTITUTION, PRD, ARCHITECTURE pair, TEST and PLAN-001..009 contracts (source hashes in HANDOFF). Approved document headers may retain historical PROPOSAL language; the separate User decision is authoritative. Code changes, tests, builds, commits and publication have independent gates.

> **Dependency status:** `web/package-lock.json` was regenerated using the declared dependency ranges; `npm ci`, TypeScript checks and Next.js build passed. A scoped Next.js PostCSS override pins the patched 8.5.23 release; npm audit reported zero advisories.
