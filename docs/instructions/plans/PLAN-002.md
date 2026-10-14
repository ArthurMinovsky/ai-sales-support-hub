# PLAN-002 — Catalog Models and REST CRUD

> **PROPOSAL R2 — NOT APPROVED.** Action-only amendment of approved upstream OUTCOME/CONSTITUTION/PRD/ARCHITECTURE/TEST R1. The proposal corrects Plan readiness/verification sequencing and shared-file ownership only; no API, Architecture or TEST contract change. Batch review is planning approval only, never permission to create source, execute tests, commit or deploy.

- **Plan ID:** PLAN-002
- **Dependencies:** PLAN-001 IR; do not await deferred full TEST-021 (PLAN-001 FV).
- **Classifications copied from PRD:** CORE-002
- **Outcomes:** OUT-003, OUT-007
- **Architecture modules:** MOD-003
- **Linked TEST obligations:** TEST-008/009 after PLAN-003 IR (auth-protected requests can use real tokens); TEST-021 full Swagger schema after PLAN-006 IR, verified in PLAN-007.
- **Owner:** implementation coordinator; optional isolated worker only after approved contracts and separate permission.
- **Parallelism:** Independent writers possible only when dependencies and file ownership do not overlap; default serialize shared main.py/CI/runtime.

## Dependency checkpoints — initial-batch exception

- **Implementation Ready (IR)** = the named interface, source composition and prerequisite behavior are ready for a dependent Plan to integrate. This is **not** TEST PASS, project acceptance, or permission for source mutation/test execution. For a new project, the initial approved create batch contains all source/test files before any test runs; IR is the logical integration/readiness order after that batch exists.
- **Fully Verified (FV)** = every linked mandatory TEST obligation assigned to this Plan has current PASS evidence on the integrated build; `UNVERIFIED`, `BLOCKED`, RED and `FAILED` never count as PASS. Cases requiring later modules/harnesses are explicitly deferred to their named owner and retain pending status until execution.
- **Dependency edges below refer to IR, not FV**, unless an explicit FV prerequisite is named. A later Plan may finish the earlier Plan's deferred verification; no circular edge is introduced. New Core edits and individual Core TEST runs still require their own User permissions.

## Exact file operations

| Operation | Exact path | Owner |
|---|---|---|
| CREATE | `backend/app/db/models.py` | PLAN-002 |
| CREATE | `backend/app/schemas/product.py` | PLAN-002 |
| CREATE | `backend/app/api/routes/products.py` | PLAN-002 final integrator; includes PLAN-003 protected-route guard in initial creation |
| CREATE | `backend/app/seed.py` | PLAN-002 |
| CREATE | `backend/tests/conftest.py` | PLAN-002 final integrator; includes PLAN-003/007 fixture requirements at initial creation |
| CREATE | `backend/tests/test_products.py` | PLAN-002 |
| EDIT (initial-batch contribution) | `backend/app/main.py` | PLAN-001 creates final integrated file; PLAN-002 owns product-router/DB requirement, not a second write |

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

### PLAN-002-A01 — Action 1

- **Do:** Write linked REST acceptance tests for create/list/get/update/delete and validation against temporary DB.
- **Done when:** Tests exist at public HTTP seam and assert DB side effect.
- **Verify:** Approved RED/GREEN for TEST-008/009 only when PLAN-003 IR provides working authorized HTTP seam; otherwise mark pending integration, not failed/passed.
- **Checkpoint:** Test execution separately approved.
- **Evidence:** record `PLAN-002-A01` in `evidence/plans/plan-002.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-002-A02 — Action 2

- **Do:** Implement SQLAlchemy User/Product models, Pydantic product schemas and routes, seed only empty catalog.
- **Done when:** Endpoints expose specified typed statuses and no unauthenticated write is allowed.
- **Verify:** Catalog response/schema and DB behavior can be inspected; TEST-008/009 protected full-path PASS is deferred until PLAN-003 IR.
- **Checkpoint:** PLAN-002 IR = product model/router/schema/data access and integration contribution available. Auth-dependent TEST-008/009 remain `DEFERRED` to PLAN-003 IR/PLAN-007 full run; do not block PLAN-003 on their PASS.
- **Evidence:** record `PLAN-002-A02` in `evidence/plans/plan-002.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-002-A03 — Action 3

- **Do:** Connect catalog router and database lifecycle to FastAPI app.
- **Done when:** OpenAPI contains catalog routes; seed idempotency and persistence semantics documented.
- **Verify:** Product route appears in partial OpenAPI inspection; TEST-021 PASS deferred until complete auth/suggestion routes exist after PLAN-006 IR and PLAN-007 execution.
- **Checkpoint:** At initial creation PLAN-001 owns `main.py` complete content; outside that batch, any EDIT still requires fresh explicit Core permission.
- **Evidence:** record `PLAN-002-A03` in `evidence/plans/plan-002.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-002-A04 — Action 4

- **Do:** Run linked tests and capture expected code/data evidence.
- **Done when:** Catalog behavior and schema match PRD-003.
- **Verify:** TEST-008/009 after PLAN-003 IR; TEST-005 covering suggestion remains deferred to PLAN-006 IR and PLAN-007 verification. No TEST-021 final assertion until PLAN-007.
- **Checkpoint:** Gate PLAN-003 on PLAN-002 IR (typed models, router, known HTTP contract), NOT PLAN-002 FV. Final FV waits for deferred full auth and OpenAPI evidence.
- **Evidence:** record `PLAN-002-A04` in `evidence/plans/plan-002.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

## Approval and stop conditions

- The complete source-create batch is prepared only after all governing sources and this Plan batch have their exact-revision User approvals. Initial create permission must enumerate every named file and intended content. Additional library-generated files require prior enumeration and approval.
- Ask separately before linked Core test executions. If a test fails, inspect and request fresh permission for any Core edit; don't redefine TEST expectations.
- Stop and request a higher-contract amendment if approved scope, interface, auth/security boundary, classification, or verification seam must change. Record actual evidence separately.
- **This proposal is not permission to execute commands, mutate a repository, or claim any test passed.**

## Current repair execution

The User-approved PLAN-010 supersedes email-registration and retained-volume assumptions in this historical plan. See revised PRD-001/008, Architecture and TEST-001/002/010. Unaffected implementation responsibilities remain valid.
