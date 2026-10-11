# PRD — AI Sales Support Hub

> **PROPOSAL R1 — NOT APPROVED.** Derive from approved OUTCOME R1 `801acfc6…334bbb1`. Constitution R1 is a *proposal*, not governing law yet; PRD R1 is conditional on its approval without material amendments.

## 1. Business problem and scope

A BU Product/Sales Specialist must identify matching items from an editable catalog for a prospect. Today the concept relies on manual interpretation/search; target is secure web-enabled catalog administration and AI-backed suggestion within a reproducible demonstration demonstration. Primary actor: registered BU staff user. Secondary actor: technical reviewer testing Docker, Swagger, auth, scans and CI.

**Required MVP:** register/login, 60-minute token, authenticated search and product CRUD, FastAPI Swagger, real OpenRouter call, Next.js TypeScript REST web, persisted local catalog, unit/E2E, Docker one-command, Git+CI/CD build, SCA/SAST/DAST/IaC, README and 10-minute pitching content. **Deferred:** full analytics, document ingestion/RAG, cross-selling engine, history/template, ERP/CRM, production cloud deployment.

## 2. Stable user stories and acceptance scenarios

| Story | Scenario | Given / When / Then | Outcome |
|---|---|---|---|
| US-001 Registration | US-001.SC-001 | Given a new username/email and strong password, when registering, then the user is persisted with a one-way password hash and can log in. | OUT-003 |
| US-001 Registration | US-001.SC-002 | Given an already registered username/email or invalid fields, when registering, then a safe validation/conflict response occurs; no duplicate inserted. | OUT-003/007 |
| US-002 Sign-in | US-002.SC-001 | Given valid username/password, when logging in, then session authenticates and expires at 3600 seconds. | OUT-003 |
| US-002 Sign-in | US-002.SC-002 | Given no/bad token, when calling protected REST endpoints or viewing protected pages, then access is denied or redirected without leaking data. | OUT-003/007 |
| US-002 Sign-in | US-002.SC-003 | Given expired token, when performing privileged requests, then server rejects it and the user must log in again. | OUT-003/007 |
| US-003 Manage products | US-003.SC-001 | Given authorized user, when adding/editing/listing/deleting a product, then changes reflect in the UI and REST responses. | OUT-003 |
| US-003 Manage products | US-003.SC-002 | Given persisted catalog, when containers restart using retained volume, then saved products/users remain. | OUT-003/005 |
| US-003 Manage products | US-003.SC-003 | Given invalid mandatory product fields, when submitting, then validation prevents malformed persistence. | OUT-007 |
| US-004 Find products | US-004.SC-001 | Given valid key and products, when searching in natural language, then OpenRouter is actually called and response recommends only catalog IDs with meaningful reasons. | OUT-001/002 |
| US-004 Find products | US-004.SC-002 | Given a provider response citing unknown IDs or malformed output, when post-processing, then unknown records are not presented as catalog products. | OUT-001/007 |
| US-004 Find products | US-004.SC-003 | Given missing key/timeout/provider error, when requesting inference, then service returns a clearly non-success AI error and catalog UI still works. | OUT-007 |
| US-004 Find products | US-004.SC-004 | Given empty catalog, when searching, then the UI states there are no products and does not present fabricated suggestions. | OUT-001/007 |
| US-005 Technical review | US-005.SC-001 | Given Docker/Compose and documented environment, when running `docker compose up --build`, then Web+API start and readiness checks succeed. | OUT-005/008 |
| US-005 Technical review | US-005.SC-002 | Given running API, when visiting `/docs`, then the Product Suggestion and CRUD/auth schemas are visible and actionable with authorization. | OUT-002 |
| US-005 Technical review | US-005.SC-003 | Given reviewed Git revision, when running CI, then tests/build and SCA/SAST/DAST/IaC produce actual evidence artifacts and actionable findings. | OUT-004/005/008 |
| US-006 Pitch | US-006.SC-001 | Given a reviewer demo, when presenting within ten minutes, then As Is/To Be, Architecture, Features, User Stories and UI Flow are clearly covered. | OUT-006 |

## 3. Requirements — function and interfaces

| ID | Requirement | Classification | Story | Outcome |
|---|---|---|---|---|
| PRD-001 | Register (username/email/password), reject duplicates, hash password; authenticate username/password and enforce JWT lifetime exactly 3600 seconds. | CORE-001 | US-001, US-002 | OUT-003,007 |
| PRD-002 | Require signed valid bearer JWT for FastAPI product CRUD and suggestions, no authorization solely in browser; frontend protected pages redirect when session absent. | CORE-001 | US-002 | OUT-003,007 |
| PRD-003 | Persist product catalog with name, brand, description (10+ chars), category, type, subtype, image URL; create/list/get/update/delete and input validation. | CORE-002 | US-003 | OUT-003,007 |
| PRD-004 | Provide customer-needs text input and return at most three suggestions anchored to known product IDs, with reason and product detail in typed REST response. | CORE-003 | US-004 | OUT-001 |
| PRD-005 | Invoke OpenRouter for inference when properly configured; validate LLM output and refuse to masquerade mocked/fallback behavior as a genuine AI success. | CORE-003 | US-004 | OUT-001,002,007 |
| PRD-006 | Python FastAPI with Swagger/OpenAPI, typed request/response and actionable error contracts. | CORE-002/003 | US-005 | OUT-002 |
| PRD-007 | Next.js TypeScript web with Register/Login, product management and suggestion flows communicating via JSON REST. | CORE-001/002/003 | US-001–004 | OUT-003 |
| PRD-008 | Docker Compose starts Next.js + FastAPI in one command after documented local configuration; database state survives Compose restart. | CORE-004 | US-005 | OUT-005 |
| PRD-009 | GitHub Actions automates checks and build/release image artifact; runs SCA/SAST/DAST/IaC and publishes logs/reports. | CORE-006 | US-005 | OUT-005,008 |
| PRD-010 | Backend pytest unit tests and frontend Playwright E2E for happy/error security paths with result evidence. | CORE-005 | US-001–005 | OUT-004,008 |
| PRD-011 | README, `.env.example`, Git URL, reproducible verification checklist and 10-minute pitch covering five mandated topics. | CORE-007 | US-005–006 | OUT-006,008 |
| PRD-012 | Empty/error/loading/re-login UI states and accessible labels; responsive layout adequate for desktop demonstration. | CORE-001/002/003 | US-001–004 | OUT-003,007 |
| PRD-013 | Cosmetic polish (spacing, icons, small-screen refinements) beyond functional accessibility, with no changed contract or data flows. | MINOR-001 | US-001–004 | OUT-006 |

**PRD is the sole classification authority.** `CORE-001` Authentication; `CORE-002` Catalog+API; `CORE-003` Recommendation+OpenRouter; `CORE-004` Container/restart; `CORE-005` Tests; `CORE-006` CI/scans; `CORE-007` Handover/pitch. `MINOR-001` strictly visual styling-only; no autonomous auth/API, permissions, data, scan, infrastructure or protected-asset changes.

## 4. Nonfunctional requirements

- **PRD-NFR-001 Security:** Secure hash Argon2id; JWT signed with confidential server secret; TTL 3600s; deny missing/invalid/expired tokens; HttpOnly SameSite Lax cookie for BFF login, and Origin check for mutating BFF requests; never expose token or OpenRouter key in browser JS. Secret present only server-side. Applies to OUT-003/007.
- **PRD-NFR-002 Integrity:** Products and users persist across restarts with documented named volume. Product recommendation IDs must match catalog rows. OUT-001/003/005.
- **PRD-NFR-003 Operability:** `/health` API endpoint, human-readable failure messages, configurable timeouts to OpenRouter. Missing OpenRouter key must not make catalog/admin unusable. OUT-005/007.
- **PRD-NFR-004 Scale:** demo/demo: one BU team, up to roughly 100–1,000 seeded/catalog items, low concurrency, one backend process. These are *design assumptions*, not employer-provided workload targets. No production HA/SLA promise. OUT-005/008.
- **PRD-NFR-005 Verification:** Every mandatory outcome must have an executable or manual verification seam, evidence path, revision binding, and `PASS/FAIL/BLOCKED/UNVERIFIED` classification. OUT-004/008.
- **PRD-NFR-006 External data:** Provider payload contains minimum product fields needed to rank, never username/password, access token or internal secrets. OUT-007.

## 5. Explicit API contract proposal

| Verb/path (FastAPI) | Request | Success | Failure |
|---|---|---|---|
| `POST /api/auth/register` | `{username,email,password}` | `201 UserPublic` | 422/409 |
| `POST /api/auth/login` | `{username,password}` | `200 {access_token,token_type,expires_in:3600}` | 401/422 |
| `GET /api/auth/me` | Bearer token | `200 UserPublic` | 401 |
| `GET /api/products` | token, optional search | `200 Product[]` | 401 |
| `POST /api/products` | token, ProductCreate | `201 Product` | 401/422 |
| `GET /api/products/{id}` | token | `200 Product` | 401/404 |
| `PUT /api/products/{id}` | token, ProductUpdate | `200 Product` | 401/404/422 |
| `DELETE /api/products/{id}` | token | `204` | 401/404 |
| `POST /api/suggestions` | token, `{query}` | `200 {suggestions: Suggestion[]}` | 401/422/503 AI unavailable |
| `GET /health` | none | `200 {status:ok}` | 503 readiness failure |

`Suggestion` includes `product_id`, `product` (catalog snapshot), `reason`; empty catalog => 200 with empty list and `notice`. `503` includes sanitized `{code,message}`. Product IDs opaque numeric primary keys in MVP; precise typed schemas in Architecture. Swaggers at `/docs` and `/openapi.json`. No hard-coded success fallback pretending OpenRouter worked.

## 6. Security/acceptance decisions (proposed inline ADRs)

- **ADR-001 — Database:** SQLite via SQLAlchemy and Docker named volume for a single-host demo. Why: deterministic single-command deployment; cost: concurrent-write limit and no horizontal HA; revisit at real multi-user production scale.
- **ADR-002 — Session boundary:** FastAPI signed JWT 3600s; Next.js BFF route handlers store token in HttpOnly SameSite=Lax cookie and add Authorization to internal API requests; server validates token on every protected API call. Why: avoid JS token exposure and browser cross-origin problem; cost: BFF code and CSRF/origin checks. Public FastAPI docs available separately for reviewer.
- **ADR-003 — Recommendation:** Deterministic candidate shortlist, up to 20 known items; OpenRouter models rank/reason over shortlist; strict JSON/Pydantic validation and ID allowlist. Reason: reduce hallucination/cost; limitation: lexical shortlist may miss semantic matches; no vector DB for initial demo.
- **ADR-004 — OpenRouter failure:** API missing key/timeout/invalid schema returns typed 503 and web displays provider unavailable; no silent model replacement. Why: genuine evidence and honest UX.
- **ADR-005 — DevSecOps:** GitHub Actions + pytest + Playwright + npm audit/pip-audit (SCA) + Semgrep (SAST) + ZAP baseline (DAST) + Checkov (IaC); artifacts/logs retained. Authenticated DAST coverage may be limited; label it honestly and add manual authorized API tests.
- **ADR-006 — Image URL:** Treat product image as external display URL, apply validation and browser CSP; do not server-fetch image from arbitrary URLs (avoid SSRF). On failure show placeholder. No upload/storage requirement.

## 7. Risk register

| Risk | Trigger | Response |
|---|---|---|
| RISK-001 | Docker containers fail to boot | Gate first with clean `docker compose up --build` smoke; STOP optional polish |
| RISK-002 | OpenRouter key unavailable | Keep Web/CRUD working; mark real inference `BLOCKED`, never `PASS` |
| RISK-003 | CI scans present but never run | Produce actual run URLs/logs/exit code and report limitations |
| RISK-004 | JWT leakage / unauthorized data | HttpOnly BFF boundary, server authorization, negative tests, redact evidence |
| RISK-005 | Single-person deadline | Freeze optional feature; critical P0 before UX flourishes |
| RISK-006 | Upstream amendment invalidates plans | Stable ID trace map, source hashes, only scoped downstream re-review |

## 8. Scope and evidence assumptions

- Employer PDF pages 1–3 establish required technologies/tests/scans and image concepts, but **do not** require a full analytics dashboard, cross-selling engine, detailed product schema, cloud deployment or RAG.
- The due time of Sunday 11 October 2026 evening remains a User estimate and is not claimed employer-confirmed.
- The current workspace contains the attached PDF and approved Outcome HTML; no user Git repository URL, live OpenRouter key, ClickUp task or external execution harness was supplied. Code/CI execution remains unverified.
- UI can use simple accessible components rather than extensive design system dependencies; seed catalog contains explicitly fictional demo products.

## 9. Exit / handoff to Architecture and TEST

Architecture must map CORE-001..007 and MINOR-001 to modules/trust boundaries and chosen ADRs; TEST must cover every `US-*.SC-*`, mandatory PRD ID, negative/operational flows; Plans must bind exact filenames to TEST IDs. Acceptance requires OUT-001..008 evidence, not merely page renders. No Plan may introduce features absent from PRD.
