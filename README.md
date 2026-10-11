# AI Sales Support Hub

A small, demo-oriented product catalog and AI recommendation workspace for Sales Support Hub's Forward Deployed AI Engineer project.

> **Source status (12 October 2026):** TEST-019 passed locally with complete scan reports and reviewed findings. Fresh backend tests passed 11/11, Playwright 17/17, scan-evaluator tests 10/10, TypeScript and production Web build passed. Committed baseline `c9b5610` has successful GitHub Actions evidence; new security fixes are uncommitted and have not run remotely. Live AI has separate historical evidence; manual acceptance and external hosting remain pending.

## Stack and features

- Python FastAPI + Swagger at `/docs` with user registration/login, backend JWT verification (3600s) and Product CRUD.
- SQLAlchemy and persistent named-volume SQLite database seeded with **ten realistic fictional products** across Demo Sensors (VisionScan, VibeSense, ThermoNode, GateLink) and Demo Automation (FlowBridge, DocuMind, AssistDesk, PredictIQ) families. They are synthetic examples, not real offerings.
- Authenticated `POST /api/suggestions`: lexical candidate shortlist → OpenRouter Chat Completions → strict catalog Product-ID allowlist. Missing/broken provider returns explicit `503 AI_UNAVAILABLE`, never fabricated AI success.
- Next.js 15 TypeScript web, server-side BFF HttpOnly cookie, Origin checks on mutation requests, protected pages.
- Pytest, Playwright, Docker Compose, GitHub Actions, four scanner configurations and evidence matrix prepared for separately authorized execution.

## Reviewer launch (local Docker verified)

**Prerequisites:** Docker Engine + Docker Compose v2, network access for pulling images/dependencies, and a strong local JWT key. AI inference requires separately configured OpenRouter API key; catalog CRUD does not.

1. Copy `.env.example` to `.env` (do not commit). Set `JWT_SECRET` to 32+ random characters. Optionally set `OPENROUTER_API_KEY` and `OPENROUTER_MODEL`.
2. Build and start both services with **one command**:

   ```sh
   ./start
   ```

   The command runs Docker Compose, waits until both services are healthy, then automatically prints the actual allocated Web, API and Swagger URLs. No separate status command is required.

   ```text
   AI Sales Support Hub is ready
   Web:     http://localhost:<allocated-web-port>
   API:     http://localhost:<allocated-api-port>
   Swagger: http://localhost:<allocated-api-port>/docs
   ```

   Ports are assigned by Docker after the containers are created; they are not fixed in the launcher. To inspect an already running stack later, `./scripts/status.sh` remains available. An optional `COMPOSE_PROJECT_NAME` selects a different isolated stack.

   The underlying plain Docker launch remains `docker compose -p saleshub-implementation-check up --build --detach --wait --wait-timeout 180`. The `start` entry point adds automatic URL reporting after this succeeds. It uses the host's POSIX shell and standard tools and requires no additional package installation.
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

- Backend: fresh Pytest 11/11; `evidence/security/runs/20261011213538Z/pytest-regression.xml`.
- Frontend: TypeScript and production Docker build passed; isolated actual Web/API browser suite 17/17 (15 existing plus 2 security checks), recorded in `evidence/security/runs/20261011213538Z/playwright-final.json`. Start a fixture with `docker compose -f compose.yaml -f compose.e2e.yaml -p saleshub-e2e up --build -d`, then run `COMPOSE_PROJECT_NAME=saleshub-e2e npm run test:e2e` from `web/`. `PLAYWRIGHT_BASE_URL` overrides dynamic target discovery.
- Mock OpenRouter in E2E verifies deterministic UI/error behavior only. A real, redacted live provider inference also passed (TEST-018); see `evidence/openrouter/live-inference-redacted.json`.
- TEST-019 **PASS locally with reported findings**: pip/npm 0 advisories; Semgrep 23 files/0 findings; Checkov 294 passed/0 failed; ZAP 0 high, 0 low, 1 medium and 3 informational alert types. Actual ZAP exit **2** (warnings); JSON/HTML retained. Medium `img-src https:` preserves approved external product images and has a documented review/remediation. See `evidence/security/runs/20261011213538Z/summary.json` and `review.json`.
- Historical local TEST-020/021 passed: Compose API and Web became healthy, Swagger and OpenAPI returned HTTP 200 on fixed test host ports. Dynamic-port verification is recorded separately in `evidence/dynamic-ports/`; discover the current URLs with `docker compose port`.
- CI baseline: [38157463221](https://github.com/ArthurMinovsky/ai-sales-support-hub/actions/runs/38157463221), commit `c9b5610`, all six jobs succeeded with an image archive. Its historical DAST artifact lacked usable reports. The new local fix collects nonroot ZAP reports, fails on missing reports/tool errors/high findings and gates release jobs on security. The modified workflow has **not** run on GitHub.

More detailed procedures: `tests/verification/README.md`; evidence sources: `docs/verification/EVIDENCE-MATRIX.md`.

For scanner runs, set `COMPOSE_PROJECT_NAME` to an isolated running stack; `scripts/security/run-scans.sh` discovers ports and verifies Web/API readiness before DAST. It creates a fresh `evidence/security/runs/<UTC timestamp>/` directory; `SECURITY_EVIDENCE_DIR` overrides it and `SECURITY_CATEGORIES=sca,sast,iac,dast` selects scope. On Docker Desktop use `DAST_DOCKER_NETWORK=<project>_default` and `DAST_DOCKER_TARGET=http://web:3000`. ZAP writes inside its own nonroot container, reports are copied before cleanup and raw scanner exits remain visible. Passive DAST does not authenticate CRUD routes.

## demonstration materials and constraints

- `docs/presentation/PITCH.md` covers As Is/To Be, Architecture, System Features, User Stories and UI Flow in <=10 minutes. Rehearsal pending.
- The app is designed for a single-host small catalog; no enterprise RBAC, RAG/vector DB or full analytics dashboard.
- Public source: [ArthurMinovsky/ai-sales-support-hub](https://github.com/ArthurMinovsky/ai-sales-support-hub). A securely configured key was used for the retained TEST-018 record. Independent review, TEST-025 rehearsal and TEST-026 acceptance remain pending.

## Project governance

`docs/instructions/` contains the approved OUTCOME, CONSTITUTION, PRD, ARCHITECTURE pair, TEST and PLAN-001..009 contracts (source hashes in HANDOFF). Approved document headers may retain historical PROPOSAL language; the separate User decision is authoritative. Code changes, tests, builds, commits and publication have independent gates.

> **Dependency status:** `web/package-lock.json` was regenerated using the declared dependency ranges; `npm ci`, TypeScript checks and Next.js build passed. A scoped Next.js PostCSS override pins the patched 8.5.23 release; npm audit reported zero advisories.
