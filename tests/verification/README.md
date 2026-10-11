# Verification Recipe

> Follow the current execution grant recorded in HANDOFF.md. The User's explicit Fast Mode grant covers the scoped local edits, builds, tests and debug loop. Never call a configured scan/test PASS until actual results exist; manual acceptance and external prerequisites remain explicit.

## Environment and source identity

- Pin the approved repository revision/working tree; preserve source file digests.
- Copy `.env.example` to `.env`, set a 32+ character JWT_SECRET, no real credentials committed.
- Run in isolated Docker Compose project and preserve all `evidence/*` outputs after cleanup.
- Use `docker compose -f compose.yaml -f compose.e2e.yaml -p saleshub-e2e up --build -d` for the isolated fixture. Leave `WEB_PORT=0`, `API_PORT=0`, `APP_ORIGIN=` to let Docker allocate unused host ports and enforce the actual browser origin.
- Discover the published endpoints and verify readiness before browser tests:

  ```sh
  export COMPOSE_PROJECT_NAME=saleshub-e2e
  web_port="$(docker compose port --index 1 web 3000 | sed -n '1s/.*://p')"
  api_port="$(docker compose port --index 1 api 8000 | sed -n '1s/.*://p')"
  export PLAYWRIGHT_BASE_URL="http://localhost:$web_port"
  export API_BASE_URL="http://localhost:$api_port"
  curl -fsS "$API_BASE_URL/health"
  curl -fsS "$PLAYWRIGHT_BASE_URL/login"
  ```

  Playwright also discovers its Web URL automatically when `PLAYWRIGHT_BASE_URL` is unset and `COMPOSE_PROJECT_NAME` identifies the running stack. Rediscover ports after container recreation. Explicit `WEB_PORT`/`API_PORT` overrides are optional.

## Scoped TEST operations

1. Backend: create `evidence/backend/`, install test dependencies, and run `pytest -q --junitxml=../evidence/backend/pytest-results.xml` from `backend/` (TEST-001..005,008..009,011..013,024).
2. Frontend: `cd web && npm ci --no-audit --no-fund && npx playwright install --with-deps chromium && npm run test:e2e` against e2e stack (TEST-006/007/014..017).
3. Persistence TEST-010: from plain Compose only, create user/product through authorized REST; record ID; `docker compose down` **without -v**; `docker compose up --build -d`; login and GET record; save IDs/times/status to `evidence/docker/persistence.json`; teardown preserves volume.
4. TEST-020/021: plain `docker compose up --build`, discover Web/API host ports with `docker compose port web 3000` and `docker compose port api 8000`, then verify Web `/login`, API `/health` and Swagger paths; save `evidence/docker/smoke.json` with source identity, discovered URLs and timestamps. Internal ports remain 3000/8000.
5. TEST-018: with real OpenRouter key in runtime only, submit actual query, redact logs, record model/status/provider metadata and resulting DB-known IDs to `evidence/openrouter/live-inference-redacted.json`. If missing key, report BLOCKED.
6. TEST-019: start live ready stack, run scripts/security/run-scans.sh with required tool dependencies; capture four tools' exit/status/severity and reports, do not claim unauthenticated ZAP baseline covers authenticated endpoints. Stop stack created by run only; preserve reports.
7. TEST-022: after authorized Git push, GitHub Actions execution and actual image artifact evidence.

## Cleanup and collision prevention

Only one runtime owner should control each Compose project and writable DB at a time. Automatic published host ports let separate projects run without port collisions; each project must use its own named volume. Capture logs/screenshots/evidence **before** cleanup; never use `docker compose down -v` on user data. Do not kill other programs by name. A single successful fixture pilot does not complete all TEST cases. Save failures with source digest and observed vs expected rather than changing approved criteria.

> **Lockfile status:** `web/package-lock.json` contains the npm-resolved dependency graph derived from the declared ranges. Historical clean `npm ci`, TypeScript checks and production build passed; current dynamic-port validation is recorded separately under `evidence/dynamic-ports/`.
