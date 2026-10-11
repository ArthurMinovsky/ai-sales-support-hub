# PLAN-003 — FastAPI Registration, JWT and Protected Routes

> **PROPOSAL R2 — NOT APPROVED.** Action-only amendment of approved upstream OUTCOME/CONSTITUTION/PRD/ARCHITECTURE/TEST R1. The proposal corrects Plan readiness/verification sequencing and shared-file ownership only; no API, Architecture or TEST contract change. Batch review is planning approval only, never permission to create source, execute tests, commit or deploy.

- **Plan ID:** PLAN-003
- **Dependencies:** PLAN-002 IR, not its deferred auth-dependent FV.
- **Classifications copied from PRD:** CORE-001
- **Outcomes:** OUT-003, OUT-007
- **Architecture modules:** MOD-002
- **Linked TEST obligations:** TEST-001..004 for auth IR; TEST-005 full protected `/api/suggestions` coverage deferred to PLAN-006 IR and PLAN-007 run; TEST-023 all-repo secrets audit deferred to PLAN-008.
- **Owner:** implementation coordinator; optional isolated worker only after approved contracts and separate permission.
- **Parallelism:** Independent writers possible only when dependencies and file ownership do not overlap; default serialize shared main.py/CI/runtime.

## Dependency checkpoints — initial-batch exception

- **Implementation Ready (IR)** = the named interface, source composition and prerequisite behavior are ready for a dependent Plan to integrate. This is **not** TEST PASS, project acceptance, or permission for source mutation/test execution. For a new project, the initial approved create batch contains all source/test files before any test runs; IR is the logical integration/readiness order after that batch exists.
- **Fully Verified (FV)** = every linked mandatory TEST obligation assigned to this Plan has current PASS evidence on the integrated build; `UNVERIFIED`, `BLOCKED`, RED and `FAILED` never count as PASS. Cases requiring later modules/harnesses are explicitly deferred to their named owner and retain pending status until execution.
- **Dependency edges below refer to IR, not FV**, unless an explicit FV prerequisite is named. A later Plan may finish the earlier Plan's deferred verification; no circular edge is introduced. New Core edits and individual Core TEST runs still require their own User permissions.

## Exact file operations

| Operation | Exact path | Owner |
|---|---|---|
| CREATE | `backend/app/core/security.py` | PLAN-003 |
| CREATE | `backend/app/schemas/auth.py` | PLAN-003 |
| CREATE | `backend/app/api/deps.py` | PLAN-003 |
| CREATE | `backend/app/api/routes/auth.py` | PLAN-003 |
| CREATE | `backend/tests/test_auth.py` | PLAN-003 |
| EDIT (initial-batch contribution) | `backend/app/api/routes/products.py` | PLAN-002 final integrator; PLAN-003 supplies bearer enforcement requirement only |
| EDIT (initial-batch contribution) | `backend/app/main.py` | PLAN-001 final integrator; PLAN-003 provides auth router requirement only |
| EDIT (initial-batch contribution) | `backend/tests/conftest.py` | PLAN-002 final integrator; PLAN-003 provides auth fixture requirement only |

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

### PLAN-003-A01 — Action 1

- **Do:** Author test slices for registration uniqueness/password hash, login 3600s, forged/expired bearer and protected CRUD.
- **Done when:** Given/When/Then HTTP assertions map to TEST-001..004 and protect current `me`/products; suggestion subset of TEST-005 is recorded for later PLAN-006 IR.
- **Verify:** Run authorized expected RED for missing behavior.
- **Checkpoint:** No tests run from Plan approval.
- **Evidence:** record `PLAN-003-A01` in `evidence/plans/plan-003.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-003-A02 — Action 2

- **Do:** Add Argon2id hashing, JWT issue/verify, security dependency and auth API.
- **Done when:** No plaintext passwords; 3600s exp enforced; invalid tokens 401.
- **Verify:** TEST-001..004.
- **Checkpoint:** Only configured JWT secret; never log access token.
- **Evidence:** record `PLAN-003-A02` in `evidence/plans/plan-003.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-003-A03 — Action 3

- **Do:** Protect products and reserve server-side reusable dependency for suggestion route.
- **Done when:** Direct API bypass of browser does not bypass auth.
- **Verify:** Direct FastAPI unauthorized/expired access on current `/api/auth/me` and products; complete TEST-005 PASS deferred until `/api/suggestions` exists after PLAN-006 IR.
- **Checkpoint:** Any user/role change beyond shared catalog is PRD amendment.
- **Evidence:** record `PLAN-003-A03` in `evidence/plans/plan-003.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-003-A04 — Action 4

- **Do:** Run approved pytest tests, record evidence and fix failures through fresh Core permissions.
- **Done when:** Security endpoints and product access match fixed contracts.
- **Verify:** TEST-001..004 (and partial TEST-005) for PLAN-003 IR. Complete TEST-005 in PLAN-007 once PLAN-006 IR; complete TEST-023 in PLAN-008 when all source/CI files exist.
- **Checkpoint:** Critical failures in TEST-001..004 block auth IR and dependent UI; deferred TEST-005 suggestion/TEST-023 whole-repo checks do not create a false dependency cycle. FV waits for their actual separate approved runs.
- **Evidence:** record `PLAN-003-A04` in `evidence/plans/plan-003.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

## Approval and stop conditions

- The complete source-create batch is prepared only after all governing sources and this Plan batch have their exact-revision User approvals. Initial create permission must enumerate every named file and intended content. Additional library-generated files require prior enumeration and approval.
- Ask separately before linked Core test executions. If a test fails, inspect and request fresh permission for any Core edit; don't redefine TEST expectations.
- Stop and request a higher-contract amendment if approved scope, interface, auth/security boundary, classification, or verification seam must change. Record actual evidence separately.
- **This proposal is not permission to execute commands, mutate a repository, or claim any test passed.**
