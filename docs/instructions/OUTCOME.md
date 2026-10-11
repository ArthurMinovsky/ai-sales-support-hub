# OUTCOME — AI Sales Support Hub

> PROPOSAL ONLY — Not approved. Do not promote to `docs/instructions/OUTCOME.md` without explicit User approval of this exact review revision.

**Project:** Sales Support Hub — Forward Deployed AI Engineer project  
**Source of requirements:** `ข้อสอบ.pdf`, pages 1–3, plus User-provided project email  
**Proposal date:** 2026-10-10 (Asia/Bangkok)  
**Current lifecycle state:** `OUTCOME_REVIEW_REQUIRED`

## 1. Intent / Mission

Deliver an demo-ready **AI Sales Support Hub** enabling a Business Unit sales/product specialist to manage a product catalog and obtain AI-assisted suggestions matched to a customer's stated needs, through a working, protected Next.js web application and a documented FastAPI backend. Demonstrate engineering ownership end-to-end: functionality, reproducible Docker launch, verification, secure defaults, CI, and demonstration-ready evidence.

## 2. Desired End State

A reviewer with Docker can obtain the source from a Git repository, follow a concise README, run one Docker Compose command to start the web application and backend, register/log in, manage products, describe a customer's need, and receive product recommendations grounded in the current catalog through a working OpenRouter integration when a valid API key and connectivity are supplied. The reviewer can inspect Swagger, test and scanning evidence, and a concise presentation in no more than ten minutes.

## 3. Mandatory Observable Outcomes

### OUT-001 — Usable Product Suggestion Journey

A logged-in user can provide customer needs in natural language and receive relevant recommended products from the persisted product catalog, along with comprehensible reasons for the match. The system does not present invented product records as if present in the catalog. The Product Suggestion journey is usable from the web interface and exposed via REST API.

**Proof:** Web flow from input through returned suggestion cards and product identifiers that resolve to persisted records; one actual OpenRouter-backed inference demonstrated with valid credentials.

### OUT-002 — Required AI Backend and API Contract

Backend is implemented in Python with FastAPI. It exposes a Product Suggestion endpoint plus REST endpoints supporting the web application, publishes a usable Swagger/OpenAPI specification, and performs AI inference through OpenRouter for the recommendation capability.

**Proof:** Swagger accessible; documented endpoint exercises; captured OpenRouter integration evidence with sensitive values redacted.

### OUT-003 — Protected Next.js Web and Product Management

Web Application is implemented in TypeScript with Next.js. It provides user registration with Username, Email, and Password stored only as a secure one-way hash; login with username and password; an authenticated response/session valid for **one hour**; protection of restricted application routes and API access via token validation; and the ability to create, list, update, and delete product records.

**Proof:** Register/login flow, CRUD state surviving a page reload/restart consistent with the selected persistence design, and unauthorized/expired token access rejected by the backend.

### OUT-004 — Automated Test Evidence

Backend has runnable Unit Tests; frontend has runnable End-to-End tests for the core user journeys. Important negative states, especially unauthorized access and provider errors, are represented in the verification contract.

**Proof:** Test commands, reproducible results, and reports/logs tied to the final tested revision.

### OUT-005 — Docker, Git, CI and Four Scan Categories

Source history is managed with Git and includes a working CI/CD workflow: automated validation on code changes and a reproducible build/release artifact step. Actual deployment to external infrastructure is not required unless separately approved. The reviewable application can be started by **one Docker Compose command** from a documented clean setup on a machine with Docker/Compose; Docker presence is non-negotiable. Security scanning covers **SCA, SAST, DAST, and IaC** with evidence of real tool execution, observed findings, and remediation/known limitations.

**Proof:** Clean-launch `docker compose up --build` smoke test, service readiness and UI/API visit, CI/CD pipeline run and build/release artifact evidence, and one report per required scanner category. No claim of perfect security without evidence.

### OUT-006 — Handover and demonstration Package

Deliver a Git repository URL suitable for inclusion in an email to **[removed-contact]** and **[removed-contact]**. Provide README instructions, environment configuration guidance with no checked-in secrets, product sample data marked as demo data, endpoint docs, test/scan proof, and presentation material for a **maximum 10-minute** local walkthrough containing: **As Is vs To Be, System Architecture, System Features, User Stories, UI Flow**.

**Proof:** Repository URL available, documented setup/review checklist, presentation content and 10-minute rehearsal/demo path.

### OUT-007 — Explicit Failure, Security, and Trust Behavior (Proposed Quality Guardrail)

Invalid/expired credentials fail closed; secrets are not emitted into application output or committed source; product input is validated. An absent/invalid OpenRouter key, timeout, or provider failure is shown as an honest, non-success state while the web application and catalog management remain reviewable. Any fallback suggestion mode must be explicitly labeled as non-OpenRouter behavior, not counted as successful AI inference.

**Proof:** Reproducible negative tests and visibly differentiated success vs AI-unavailable states.

### OUT-008 — Reviewer-Reproducible Outcome Verification

The delivered package identifies which mandatory results are verified, blocked, or unverified; distinguishes automated code checks from runtime/system verification and local manual acceptance; and makes unsupported claims visible rather than silently marking them passed.

**Proof:** Final evidence matrix mapping `OUT-*` to tests, CI/scans, Docker smoke, and manual presentation/demo evidence, tied to an identifiable source revision.

## 4. Direction and Priorities

1. Mandatory compliance: Docker one-command, security/auth, AI backend/inference, CRUD, tests and four scan categories.
2. A coherent end-to-end customer-needs-to-product journey that can be reproduced by the reviewer.
3. Explicit failure handling and honest evidence of what ran, what failed, and what was mocked.
4. Polished but lean UI, concise presentation and README.
5. Optional extension only after core delivery evidence is complete.

Time budget is constrained; treat **Sunday 2026-10-11 evening (Asia/Bangkok)** as a *provisional internal target based on the User's estimate*, not as a deadline confirmed by Sales Support Hub.

## 5. Constraints and Boundaries

- Respect all required frameworks/interfaces: Python/FastAPI; TypeScript/Next.js; REST; Swagger/OpenAPI; OpenRouter.
- Register/Login uses Username and Password; Email is captured at registration; passwords are not plaintext at rest.
- One-hour session/token validity must be enforced at the backend trust boundary, not only with UI redirection.
- Docker startup may require ordinary runtime secret configuration to exercise the **actual** OpenRouter call; application launch itself must remain one documented Compose command. Never commit a real API key.
- Demonstration catalog records must be clearly labeled sample/seed data, not asserted to represent Sales Support Hub's actual products.
- The choice of SQLite vs PostgreSQL, cookie vs header transport, exact OpenRouter model, ranking algorithm, frontend design library and scan tooling is deferred to later PRD/ADR/Architecture decisions, provided these outcomes remain satisfied.

## 6. Out of Scope Unless Separately Approved

- Full Analytics Dashboard or sales attribution/forecasting.
- Cross-selling optimization, supporting-document ingestion or RAG, vector search, history/templates, external ERP/CRM integration.
- Multi-tenant roles, SSO, enterprise infrastructure, cloud hosting, public production hardening or payment workflows.

These may appear in illustration/concept mockups but are not treated as mandatory from the written minimum requirements.

## 7. Failure / Compatibility Expectations

- Invalid or expired session/token: access refused with a clear re-login path; no bypass of protected Backend API.
- Product suggestion failure: no fabricated “AI success”; capture/log a bounded error without leaking secrets, show recoverable UI messaging.
- Invalid product fields: predictable client error response; avoid silent corruption.
- Docker restart: stored users/products persist per the architecture's documented storage choice and volume semantics; persistency proof must be performed rather than presumed.
- Browser/API consumers: no undocumented requirement for other clients; REST contract remains clearly inspectable via Swagger.

## 8. Expected Deliverables

1. Source repository + README + environment example, no secrets.
2. Runnable Docker Compose project with Next.js app and FastAPI backend and persistent catalog.
3. Swagger/OpenAPI and OpenRouter-backed suggestion flow.
4. Backend Unit Tests and Frontend E2E tests with execution evidence.
5. CI/CD with a reproducible build/release artifact, and executed SCA/SAST/DAST/IaC scanning evidence.
6. Demo/presentation package covering all five mandated topics in ten minutes.
7. Final traceability/evidence of verified, blocked and unverified outcomes.

## 9. Outcome-Level Definition of Done

**OUTCOME PASS requires all mandatory evidence, not only generated files:**

- A clean Docker Compose build/start and browser/API readiness demonstrated from the reviewed revision.
- Register/login, protected Product CRUD and suggestion journeys verified; token lifetime/security negative cases checked.
- At least one **real** OpenRouter inference with a valid configured key (a mocked call alone cannot satisfy OUT-002).
- Backend Unit Tests and Frontend E2E Tests executed and results reported honestly.
- Git+CI/CD evidence exists (including build/release artifact); SCA, SAST, DAST and IaC each actually executed with accessible report/finding summary.
- Repo URL and reviewer instructions are ready for delivery; 10-minute presentation has the five required sections.
- Outstanding failures/risks are explicit. No unchecked outcome can be marked PASS.

**Release decision remains with the User:** Passing automated checks does not itself confer final manual acceptance or authorize submitting the repository link/email.

## 10. Pending User Decisions

- **D-OUT-01:** Approve this exact Outcome proposal revision or request edits.
- **D-OUT-02:** Confirm or modify provider-unavailable behavior: prefer application boots and explicitly reports AI unavailable rather than failing to boot altogether.
- **D-OUT-03:** If known, confirm actual release deadline/time; current Sunday evening is User estimate.
- **D-OUT-04:** Choose execution harness before source creation: ChatGPT deliverable ZIP or a specified external/local repository workflow.

**No PRD feature's official `CORE-*` or `MINOR-*` classification is assigned by this Outcome.** The approved PRD owns that classification.
