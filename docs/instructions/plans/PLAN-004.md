# PLAN-004 — Next.js Session BFF, Registration and Login UI

> **PROPOSAL R2 — NOT APPROVED.** Action-only amendment of approved upstream OUTCOME/CONSTITUTION/PRD/ARCHITECTURE/TEST R1. The proposal corrects Plan readiness/verification sequencing and shared-file ownership only; no API, Architecture or TEST contract change. Batch review is planning approval only, never permission to create source, execute tests, commit or deploy.

- **Plan ID:** PLAN-004
- **Dependencies:** PLAN-003 IR (signed backend session works); PLAN-007 IR is required only for final browser E2E verification, NOT to start implementation.
- **Classifications copied from PRD:** CORE-001
- **Outcomes:** OUT-003, OUT-007
- **Architecture modules:** MOD-006
- **Linked TEST obligations:** TEST-006/007/014 E2E verification when PLAN-007 fixture/Playwright harness IR; TEST-023 whole-repo secrets review when PLAN-008 runs.
- **Owner:** implementation coordinator; optional isolated worker only after approved contracts and separate permission.
- **Parallelism:** Independent writers possible only when dependencies and file ownership do not overlap; default serialize shared main.py/CI/runtime.

## Dependency checkpoints — initial-batch exception

- **Implementation Ready (IR)** = the named interface, source composition and prerequisite behavior are ready for a dependent Plan to integrate. This is **not** TEST PASS, project acceptance, or permission for source mutation/test execution. For a new project, the initial approved create batch contains all source/test files before any test runs; IR is the logical integration/readiness order after that batch exists.
- **Fully Verified (FV)** = every linked mandatory TEST obligation assigned to this Plan has current PASS evidence on the integrated build; `UNVERIFIED`, `BLOCKED`, RED and `FAILED` never count as PASS. Cases requiring later modules/harnesses are explicitly deferred to their named owner and retain pending status until execution.
- **Dependency edges below refer to IR, not FV**, unless an explicit FV prerequisite is named. A later Plan may finish the earlier Plan's deferred verification; no circular edge is introduced. New Core edits and individual Core TEST runs still require their own User permissions.

## Exact file operations

| Operation | Exact path | Owner |
|---|---|---|
| CREATE | `web/src/lib/session.ts` | PLAN-004 |
| CREATE | `web/src/app/api/auth/register/route.ts` | PLAN-004 |
| CREATE | `web/src/app/api/auth/login/route.ts` | PLAN-004 |
| CREATE | `web/src/app/api/auth/logout/route.ts` | PLAN-004 |
| CREATE | `web/src/app/api/backend/[...segments]/route.ts` | PLAN-004 |
| CREATE | `web/src/app/login/page.tsx` | PLAN-004 |
| CREATE | `web/src/app/register/page.tsx` | PLAN-004 |
| CREATE | `web/src/app/(app)/layout.tsx` | PLAN-004 |
| CREATE | `web/tests/e2e/auth.spec.ts` | PLAN-004 |

## Ordered actions (no source code)

### PLAN-004-A01 — Action 1

- **Do:** Define browser auth tests for register/login, logout, expiry/guard and unsafe Origin.
- **Done when:** Browser-visible behaviors and BFF public seams mapped.
- **Verify:** Review test assertions and browser seams; Playwright RED/GREEN invocation only after PLAN-007 IR sets up real web/API/browser/fixture. Earlier syntax/harness absence is not meaningful RED.
- **Checkpoint:** Core mutation/test approvals separate.
- **Evidence:** record `PLAN-004-A01` in `evidence/plans/plan-004.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-004-A02 — Action 2

- **Do:** Implement BFF HTTP-only cookie session endpoints, backend bearer forwarding and whitelist.
- **Done when:** Token never exposed to browser script; 401 from FastAPI fails closed.
- **Verify:** BFF/API response and cookie/security behavior at real HTTP seam where ready; full E2E TEST-006/007 follows PLAN-007 IR; secrets TEST-023 finalized in PLAN-008.
- **Checkpoint:** CSRF protection on all mutation BFF routes.
- **Evidence:** record `PLAN-004-A02` in `evidence/plans/plan-004.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-004-A03 — Action 3

- **Do:** Implement Register/Login and server-side protected layout with recoverable validation errors.
- **Done when:** Navigation matches US-001/002, direct protected navigation redirects.
- **Verify:** UI navigation/guard source and real HTTP behavior; automated browser TEST-014 only after PLAN-007 IR.
- **Checkpoint:** Do not rely on page redirect for backend authorization.
- **Evidence:** record `PLAN-004-A03` in `evidence/plans/plan-004.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-004-A04 — Action 4

- **Do:** Hand complete browser-auth scenarios and expected screenshots to PLAN-007 harness owner; after PLAN-007 IR request explicit Core TEST run and execute auth E2E on real Web + API.
- **Done when:** Auth UI/BFF is implementation-ready and later approved Playwright TEST-006/007/014 evidence demonstrates authorized and unauthorized flows; retain `DEFERRED` state until that later proof exists.
- **Verify:** TEST-006/007/014.
- **Checkpoint:** PLAN-004 IR lets PLAN-005/006 integrate UI; its FV waits for PLAN-007 IR and authorized TEST-006/007/014. This is a deferred verification obligation, not an implementation cycle PLAN-007→PLAN-004→PLAN-007.
- **Evidence:** record `PLAN-004-A04` in `evidence/plans/plan-004.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

## Approval and stop conditions

- The complete source-create batch is prepared only after all governing sources and this Plan batch have their exact-revision User approvals. Initial create permission must enumerate every named file and intended content. Additional library-generated files require prior enumeration and approval.
- Ask separately before linked Core test executions. If a test fails, inspect and request fresh permission for any Core edit; don't redefine TEST expectations.
- Stop and request a higher-contract amendment if approved scope, interface, auth/security boundary, classification, or verification seam must change. Record actual evidence separately.
- **This proposal is not permission to execute commands, mutate a repository, or claim any test passed.**

## Current repair execution

The User-approved PLAN-010 supersedes email-registration and retained-volume assumptions in this historical plan. See revised PRD-001/008, Architecture and TEST-001/002/010. Unaffected implementation responsibilities remain valid.
