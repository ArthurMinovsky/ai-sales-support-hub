# TEST — AI Sales Support Hub (Verification Contract)

> **PROPOSAL R1 — NOT APPROVED.** Source: approved OUTCOME `801acfc6…334bbb1`, conditional Constitution/PRD/Architecture R1 proposals. No tests have been run. PASS is never inferred from an approved test definition.

## 1. Definitions and ownership

- **Automated** = agent executes approved test and evaluates output under execution permission. **Manual** = User examines actual output after independent code review and decides PASS/FAIL.
- **Code verification** (isolated pytest/typecheck), **system verification** (containers/browser/Swagger/external API/CI/scans), and **Outcome verification** (all mandated proof) are separate levels.
- Where applicable, test through public FastAPI HTTP REST, Next.js visible UI, Compose launch, GitHub Action job output. Mock only the OpenRouter external boundary for deterministic unit/E2E; live provider smoke remains separately required.
- Approved TEST is static; `evidence/*.json`, CI logs, screenshots, reports capture mutable observations. All are currently `UNVERIFIED`.
- TDD applicable to behavior cases exposing public response or browser-visible state; no TDD for artifact structure/manual pitching/scanner setup, with justification.

## 2. Test cases — contract table

| ID | Seam / method | Precondition and procedure | Expected observation | Mode / level | PRD/OUT/CORE |
|---|---|---|---|---|---|
| TEST-001 | `POST /api/auth/register` pytest HTTP (TDD) | Fresh temp DB; submit valid username/email/password | 201, persisted password_hash != password, can subsequently login | Auto/code | PRD-001; OUT-003/007; CORE-001 |
| TEST-002 | Registration negative HTTP (TDD) | Attempt username/email duplicate and malformed fields | 409/422, no duplicated user, no password in response/log | Auto/code | PRD-001; OUT-007; CORE-001 |
| TEST-003 | `POST /api/auth/login` HTTP JWT (TDD) | Sign in with valid credentials; inspect decoded signed token exp and expires_in | 200; expiration 3600s after issuance within clock tolerance; never plaintext | Auto/code | PRD-001; OUT-003; CORE-001 |
| TEST-004 | Invalid login/expired JWT HTTP (TDD) | Wrong password, forged signature, expired JWT | 401; backend protected call denied | Auto/code | PRD-001/002; OUT-003/007; CORE-001 |
| TEST-005 | `GET /api/auth/me`, CRUD, Suggestion (TDD) | No token then valid bearer then expired token | All protected surfaces reject missing/expired bearer regardless of Next.js | Auto/API | PRD-002; OUT-003/007; CORE-001 |
| TEST-006 | BFF mutation routes `Origin` check (TDD) | Malicious Origin submits POST/PUT/DELETE with cookie; allowed Origin control | Wrong Origin denied; allowed origin can progress; no wildcard trust | Auto/system | PRD-NFR-001; OUT-007; CORE-001 |
| TEST-007 | `POST /api/auth/logout`, UI guard (TDD) | Sign in, logout, refresh protected page | Cookie cleared; protected page reroutes to login; API 401 | Auto/E2E | PRD-002/007; OUT-003; CORE-001 |
| TEST-008 | `/api/products` HTTP CRUD (TDD) | Authorized create/list/get/update/delete on temp DB | 201,200,200,200,204; persisted DB reflects expected rows | Auto/API | PRD-003; OUT-003; CORE-002 |
| TEST-009 | Product validation HTTP (TDD) | Missing name or description under 10 chars, malformed HTTPS URL, unknown ID | 422 for invalid, 404 for nonexistent; no malformed writes; no server-fetch URLs | Auto/API | PRD-003; OUT-007; CORE-002 |
| TEST-010 | SQLite named-volume restart (not TDD: runtime) | From clean Compose start create user/product, `docker compose down` (without `-v`), re-up | Saved credentials/products still exist | Auto/system | PRD-003/008; OUT-003/005; CORE-002/004 |
| TEST-011 | Suggestion HTTP with mocked adapter (TDD) | Seed known catalog; mocked provider returns 2 known and 1 invented ID | 200 suggestions contain known IDs only, max 3, reasons, DB product details | Auto/API | PRD-004/005; OUT-001/007; CORE-003 |
| TEST-012 | OpenRouter error surfaces (TDD) | Missing key, timeout, 429, schema-malformed mocked provider response | Typed 503 AI_UNAVAILABLE, no fabricated success, other endpoints healthy | Auto/API | PRD-005; OUT-007; CORE-003 |
| TEST-013 | Empty catalog suggestion (TDD) | Empty SQLite products, authorized suggest request | 200 empty list and notice, no provider success claim | Auto/API | PRD-004/005; OUT-001; CORE-003 |
| TEST-014 | Login E2E in browser (TDD) | Playwright register/login, wrong password and guarded direct navigation | Correct authenticated transition and safe errors | Auto/E2E | PRD-001/007/012; OUT-003; CORE-001 |
| TEST-015 | Catalog E2E in browser (TDD) | Playwright add/edit/delete; reload; attempt form validation | Visible product and status updates, stable after reload; no hidden unauth mutation | Auto/E2E | PRD-003/007/012; OUT-003; CORE-002 |
| TEST-016 | Search E2E with provider fixture (TDD) | Fixture returns known product IDs; Playwright search UI | Loading → known recommendations with reasons; no fabricated entries | Auto/E2E | PRD-004/007/012; OUT-001; CORE-003 |
| TEST-017 | Search provider error E2E (TDD) | Fixture returns timeout/invalid schema; Playwright search | Explicit unavailable state, retry action, catalog remains accessible | Auto/E2E | PRD-005/012; OUT-007; CORE-003 |
| TEST-018 | Actual OpenRouter HTTPS (not TDD: live external) | Runtime provided valid OPENROUTER_API_KEY, deployed catalog; submit a real search; capture redacted request/response metadata | Proves provider sent response and known-ID suggestions; no mock; without credentials record BLOCKED | Auto/system requiring User permission and key | PRD-005; OUT-001/002; CORE-003 |
| TEST-019 | SCA/SAST/DAST/IaC run evidence (not TDD) | Execute pip-audit/npm audit, Semgrep, ZAP baseline against running stack, Checkov; collect versions/target/findings | Four real reports with exit, severity, scope, remediation or accepted gaps; never assume clean | Auto/system | PRD-009; OUT-005/008; CORE-006 |
| TEST-020 | Clean Docker build and readiness (not TDD: runtime) | Isolated clean checkout, valid documented env; run `docker compose up --build`, request `http://localhost:3000`, `http://localhost:8000/health` | Single launch command starts both; accessible UI and API ready; no hidden manual install | Auto/system | PRD-008; OUT-005; CORE-004 |
| TEST-021 | Swagger REST schema (not TDD: contract) | Running API `/docs` and `/openapi.json`; verify suggestion CRUD auth endpoints | Interactive docs and accurate OpenAPI path/authorization schema | Auto/system | PRD-006; OUT-002; CORE-002/003 |
| TEST-022 | CI/CD on pinned git revision (not TDD) | GitHub Actions run from reviewed commit; inspect job logs and image artifact | Real tests/scans/build and retained build image or publishable artifact; failures visible | Auto/system | PRD-009/010; OUT-004/005/008; CORE-005/006 |
| TEST-023 | Secrets review (not TDD: static) | Inspect versioned tracked files + reports for token/OpenRouter key/private env; verify container env segregation | No real secrets committed or browser exposed; `.env.example` placeholders only | Auto/static + human spot check | PRD-NFR-001/006; OUT-007; CORE-001/006 |
| TEST-024 | API provider allowlist integrity (TDD) | AI responds with injection instruction and unknown ID, valid product catalog contains others | Drop unknown entries, disregard model's suggested altered product fields | Auto/API | PRD-004/005; OUT-001/007; CORE-003 |
| TEST-025 | 10-minute pitch / 5 sections (not TDD) | Review actual slides/script and run timed walkthrough | < =10 minutes; As Is/To Be, Architecture, Features, User Story, UI Flow covered | Manual/Outcome | PRD-011; OUT-006/008; CORE-007 |
| TEST-026 | Reviewer end-to-end acceptance (not TDD) | User opens repository and docs, performs recorded Docker/auth/catalog/AI/scan evidence review | User decides verified vs blocked/unverified on OUT-001..008; authorized final release only after acceptance | Manual/Outcome | PRD-001..012; OUT-001..008; CORE-001..007 |

## 3. Public observation seams and quality of RED/GREEN

- `backend/tests/test_auth.py` → FastAPI TestClient with disposable DB (TEST-001..005). Unit tests verify public HTTP statuses and signed expiry, not implementation helper call counts.
- `backend/tests/test_products.py` → HTTP/DB state (TEST-008/009).
- `backend/tests/test_suggestions.py`, `backend/tests/test_openrouter_adapter.py` → HTTP DTO and provider adapter stubbed **only at HTTPS external seam** (TEST-011..013/024).
- `web/tests/e2e/*.spec.ts` → Playwright with real Next.js/FastAPI and an isolated fake OpenRouter endpoint, browser visible and accessible state (TEST-007/014..017). Test env keys distinct from production credentials.
- A behavior test's RED must be from approved missing behavior, not test harness syntax/config failure. Re-run GREEN and capture evidence. The full initial source batch (when approved) includes both implementation and test files; no test invocation without a separate Core execution approval.

## 4. Verification recipe and evidence mapping

Plan must create `tests/verification/README.md` describing exact commands, environment, health polling, test fixture startup, teardown (never `down -v` except approved destructive reset), evidence capture and shared instance ownership. Recipe pilot = launch → readiness → one mapped case → evidence → cleanup; pilot is not full coverage. Evidence paths:

- `evidence/backend/pytest-results.xml` and `evidence/backend/summary.json`
- `evidence/frontend/playwright-report/` and `evidence/frontend/screenshots/`
- `evidence/docker/smoke.json`, `evidence/docker/persistence.json`
- `evidence/openrouter/live-inference-redacted.json`
- `evidence/security/{sca,sast,dast,iac}/` (raw scanner outputs and triage summaries)
- `evidence/ci/workflow-run.json`, `evidence/release/image-artifact.json`
- `evidence/review/outcome-matrix.json`, `evidence/manual/user-acceptance.md`

Each record must refer to exact source revision, command/target/environment, timestamp, evaluator, expected vs observed and PASS/FAIL/BLOCKED/UNVERIFIED; retain raw logs/screenshots as permitted and redact secrets.

## 5. Run-loop thresholds and severity

- **Plan checkpoint PASS** only when each linked Automated case has an authorized current successful result; required blocked evidence keeps checkpoint unverified/blocked. Flaky or inconclusive observations are not PASS.
- **Release-critical gates:** TEST-005 auth, TEST-008 CRUD, TEST-011 known-ID integrity, TEST-018 real OpenRouter, TEST-019 four scans, TEST-020 Docker, TEST-022 CI and TEST-025/026 Manual acceptance.
- SAST/SCA/DAST/IaC findings classified by severity and exploitability; critical/high issues relevant to demo trust boundary must be resolved or presented for explicit User risk acceptance before release. Report lower severities and coverage. Scanner network errors do not count as successful scanning.
- **Manual** TEST-025 and 026 remain pending until after walkthrough, local Git commit, independent code review and the User's post-review direction.
- If a required case is impossible due to unprovided key/Git remote/time, state BLOCKED with exact unblock condition rather than weakening a test.

## 6. Traceability and proposal approval

- Map all 16 stable `US-*.SC-*` scenarios to tests; PRD-001..012 are covered by TEST-001..026; MINOR-001 appearance work only requires existing visible E2E regression.
- Current results: NONE EXECUTED; no PASS claimed.
- No tests are implemented by drafting this `TEST.md`; next artifact must be action-only Plan packages. Any behavior seam change returns to TEST approval.
