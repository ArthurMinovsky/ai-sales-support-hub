# PLAN-007 — Complete Automated Tests and Verification Harness

> **PROPOSAL R2 — NOT APPROVED.** Action-only amendment of approved upstream OUTCOME/CONSTITUTION/PRD/ARCHITECTURE/TEST R1. The proposal corrects Plan readiness/verification sequencing and shared-file ownership only; no API, Architecture or TEST contract change. Batch review is planning approval only, never permission to create source, execute tests, commit or deploy.

- **Plan ID:** PLAN-007
- **Dependencies:** PLAN-004/005/006 IR, not their E2E FV. After PLAN-007 harness IR, execute deferred browser/Swagger/DB restart cases.
- **Classifications copied from PRD:** CORE-005
- **Outcomes:** OUT-004, OUT-008
- **Architecture modules:** MOD-009
- **Linked TEST obligations:** TEST-001..017, TEST-020/021, TEST-024, explicitly TEST-010 named-volume down/re-up persistence. TEST-018 remains real-provider credential-gated under PLAN-006; TEST-019 scanning under PLAN-008.
- **Owner:** implementation coordinator; optional isolated worker only after approved contracts and separate permission.
- **Parallelism:** Independent writers possible only when dependencies and file ownership do not overlap; default serialize shared main.py/CI/runtime.

## Dependency checkpoints — initial-batch exception

- **Implementation Ready (IR)** = the named interface, source composition and prerequisite behavior are ready for a dependent Plan to integrate. This is **not** TEST PASS, project acceptance, or permission for source mutation/test execution. For a new project, the initial approved create batch contains all source/test files before any test runs; IR is the logical integration/readiness order after that batch exists.
- **Fully Verified (FV)** = every linked mandatory TEST obligation assigned to this Plan has current PASS evidence on the integrated build; `UNVERIFIED`, `BLOCKED`, RED and `FAILED` never count as PASS. Cases requiring later modules/harnesses are explicitly deferred to their named owner and retain pending status until execution.
- **Dependency edges below refer to IR, not FV**, unless an explicit FV prerequisite is named. A later Plan may finish the earlier Plan's deferred verification; no circular edge is introduced. New Core edits and individual Core TEST runs still require their own User permissions.

## Exact file operations

| Operation | Exact path | Owner |
|---|---|---|
| CREATE | `web/playwright.config.ts` | PLAN-007 |
| CREATE | `compose.e2e.yaml` | PLAN-007 |
| CREATE | `tests/fixtures/openrouter_mock.py` | PLAN-007 |
| CREATE | `tests/verification/README.md` | PLAN-007 |
| EDIT (initial-batch contribution) | `web/package.json` | PLAN-001 final integrator; PLAN-007 defines Playwright/test scripts and dependencies |
| EDIT (initial-batch contribution) | `web/package-lock.json` | PLAN-001 final integrator; PLAN-007 defines matching resolved dependency lock |
| EDIT (initial-batch contribution) | `backend/tests/conftest.py` | PLAN-002 final integrator; PLAN-007 defines test isolation fixtures |

## Integrated initial-batch file ownership

Shared paths are each **created exactly once** with their complete final content in the User-reviewed initial source batch. Other Plans provide integration requirements but do **not** independently overwrite that file during initial creation. Later corrections remain separate permissioned Core edits.

| Shared path | Final file owner / integrator | Contributors / required merged scope |
|---|---|---|
| `backend/app/main.py` | PLAN-001 | PLAN-002 product router and DB bootstrap; PLAN-003 auth router; PLAN-006 suggestion router; health and OpenAPI intact |
| `backend/app/api/routes/products.py` | PLAN-002 | PLAN-003 backend JWT guard requirement, merged at initial creation |
| `backend/tests/conftest.py` | PLAN-002 | PLAN-003 auth fixture requirements; PLAN-007 deterministic fixture/session isolation; no divergent DB ownership |
| `web/package.json` | PLAN-001 | PLAN-007 Playwright/test commands and exact dev dependencies; existing Next.js runtime/build intact |
| `web/package-lock.json` | PLAN-001 | PLAN-007 matching resolved dependencies; regenerate/verify against final `web/package.json`, both shipped as one coherent pair |

**Initial code draft reviewer gate:** list each path once, show full final content and all contributing PRD/CORE/TEST IDs. Before any source write, obtain distinct User approval of the exact initial-create batch; after creation, request separate approval for each Plan's actual linked Core TEST execution. All shared-file integration is serialized under the named owner.

## Ordered actions (no source code)

### PLAN-007-A01 — Action 1

- **Do:** Specify Playwright browser base URL/session isolation and deterministic mock-provider fixture.
- **Done when:** Playwright runner/config, isolated Compose overlay, disposable account/catalog fixtures and deterministic mock external-provider endpoint are specified; source batch includes all files needed to run later TEST-014..017.
- **Verify:** PLAN-007 IR requires working harness readiness and one separately approved representative browser case; full TEST-014..017 PASS waits for the complete run.
- **Checkpoint:** No tests executed by plan drafting.
- **Evidence:** record `PLAN-007-A01` in `evidence/plans/plan-007.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-007-A02 — Action 2

- **Do:** Configure e2e Compose overlay, mock server, stable Playwright/pytest dependencies.
- **Done when:** Test overlay points backend to deterministic fake provider only in the isolated Compose project; production/provider env unchanged; Playwright runner, packages and fixture preconditions are wired.
- **Verify:** TEST-011..017 after harness readiness with authorized invocation; TEST-018 requires independent real OpenRouter HTTPS and MUST NOT reuse mock evidence.
- **Checkpoint:** Never allow fake provider fixture to count as live AI evidence.
- **Evidence:** record `PLAN-007-A02` in `evidence/plans/plan-007.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-007-A03 — Action 3

- **Do:** Create verification recipe; pilot isolated Compose launch → poll Web/API readiness → execute one approved representative test → save evidence → stop only test-owned processes, without removing named volumes.
- **Done when:** Pilot preserves evidence, exact command IDs documented.
- **Verify:** TEST-020 + representative test.
- **Checkpoint:** A single run owner serializes use of shared port/SQLite state and preserves evidence before cleanup; failed readiness is `BLOCKED/FAILED`, not a passed harness.
- **Evidence:** record `PLAN-007-A03` in `evidence/plans/plan-007.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-007-A04 — Action 4

- **Do:** Execute TEST-010 *explicitly* with an isolated named-volume Compose project: clean start → create test account and product through protected API → record IDs → `docker compose down` **without `-v`** → `docker compose up --build` → login and verify the same product/user persist → save `evidence/docker/persistence.json` → `down` without volume deletion.
- **Done when:** TEST-010 evidence records exact Compose project, volume name, user/product IDs (no secrets), restart commands, post-restart authenticated reads, timestamp and source revision; no `-v` destructive cleanup has occurred.
- **Verify:** TEST-010 expected rows survive restart; confirm `evidence/docker/persistence.json` exists after teardown and distinguish restart persistence from browser refresh TEST-015.
- **Checkpoint:** Use test-only catalog/database; do not destroy persistent volume with `down -v`. If disposable test-volume removal is needed later, request explicit destructive cleanup permission; record retained volume or planned cleanup.
- **Evidence:** record `PLAN-007-A04` in `evidence/plans/plan-007.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-007-A05 — Action 5

- **Do:** Run full separately authorized backend API/pytest and browser Playwright suites after PLAN-007 IR; include deferred TEST-005, TEST-006/007, TEST-008/009, TEST-014..017 and full TEST-021 OpenAPI routes, collect reports and screenshot evidence.
- **Done when:** Every currently runnable mandatory automated case has a revision-bound PASS record or an explicit truthful FAILED/BLOCKED/UNVERIFIED status; no pending case silently treated as PASS.
- **Verify:** TEST-001..017/020/021/024, especially separately persisted TEST-010; save `evidence/backend/pytest-results.xml`, `evidence/frontend/playwright-report/`, `evidence/docker/smoke.json`, `evidence/docker/persistence.json`.
- **Checkpoint:** Each Core TEST invocation requires separate User approval. No Core code correction without fresh permission; TEST-018 live provider handled separately, TEST-019/022 in PLAN-008.
- **Evidence:** record `PLAN-007-A05` in `evidence/plans/plan-007.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

## Approval and stop conditions

- The complete source-create batch is prepared only after all governing sources and this Plan batch have their exact-revision User approvals. Initial create permission must enumerate every named file and intended content. Additional library-generated files require prior enumeration and approval.
- Ask separately before linked Core test executions. If a test fails, inspect and request fresh permission for any Core edit; don't redefine TEST expectations.
- Stop and request a higher-contract amendment if approved scope, interface, auth/security boundary, classification, or verification seam must change. Record actual evidence separately.
- **This proposal is not permission to execute commands, mutate a repository, or claim any test passed.**
