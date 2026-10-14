# PLAN-006 — OpenRouter Recommendation and Search UI

> **PROPOSAL R2 — NOT APPROVED.** Action-only amendment of approved upstream OUTCOME/CONSTITUTION/PRD/ARCHITECTURE/TEST R1. The proposal corrects Plan readiness/verification sequencing and shared-file ownership only; no API, Architecture or TEST contract change. Batch review is planning approval only, never permission to create source, execute tests, commit or deploy.

- **Plan ID:** PLAN-006
- **Dependencies:** PLAN-003/004/005 IR (not their deferred E2E FV). PLAN-007 IR is a *verification* prerequisite only.
- **Classifications copied from PRD:** CORE-003
- **Outcomes:** OUT-001, OUT-002, OUT-007
- **Architecture modules:** MOD-004, MOD-005, MOD-008
- **Linked TEST obligations:** TEST-011/012/013/024 API with mock HTTPS seam; TEST-016/017 browser E2E deferred until PLAN-007 IR; TEST-018 live provider remains separate credential-gated verification.
- **Owner:** implementation coordinator; optional isolated worker only after approved contracts and separate permission.
- **Parallelism:** Independent writers possible only when dependencies and file ownership do not overlap; default serialize shared main.py/CI/runtime.

## Dependency checkpoints — initial-batch exception

- **Implementation Ready (IR)** = the named interface, source composition and prerequisite behavior are ready for a dependent Plan to integrate. This is **not** TEST PASS, project acceptance, or permission for source mutation/test execution. For a new project, the initial approved create batch contains all source/test files before any test runs; IR is the logical integration/readiness order after that batch exists.
- **Fully Verified (FV)** = every linked mandatory TEST obligation assigned to this Plan has current PASS evidence on the integrated build; `UNVERIFIED`, `BLOCKED`, RED and `FAILED` never count as PASS. Cases requiring later modules/harnesses are explicitly deferred to their named owner and retain pending status until execution.
- **Dependency edges below refer to IR, not FV**, unless an explicit FV prerequisite is named. A later Plan may finish the earlier Plan's deferred verification; no circular edge is introduced. New Core edits and individual Core TEST runs still require their own User permissions.

## Exact file operations

| Operation | Exact path | Owner |
|---|---|---|
| CREATE | `backend/app/schemas/suggestion.py` | PLAN-006 |
| CREATE | `backend/app/services/openrouter.py` | PLAN-006 |
| CREATE | `backend/app/services/recommendation.py` | PLAN-006 |
| CREATE | `backend/app/api/routes/suggestions.py` | PLAN-006 |
| CREATE | `backend/tests/test_suggestions.py` | PLAN-006 |
| CREATE | `backend/tests/test_openrouter_adapter.py` | PLAN-006 |
| EDIT (initial-batch contribution) | `backend/app/main.py` | PLAN-001 final integrator; PLAN-006 supplies suggestion router wiring |
| CREATE | `web/src/app/(app)/search/page.tsx` | PLAN-006 |
| CREATE | `web/src/components/RecommendationResults.tsx` | PLAN-006 |
| CREATE | `web/tests/e2e/search.spec.ts` | PLAN-006 |

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

### PLAN-006-A01 — Action 1

- **Do:** Define suggestion API tests for valid IDs, max three, empty catalog, bad provider JSON/timeouts, unknown IDs.
- **Done when:** Public HTTP DTO tests and fake external HTTP boundary.
- **Verify:** TEST-011/012/013/024 expected RED.
- **Checkpoint:** Test execution requires Core approval.
- **Evidence:** record `PLAN-006-A01` in `evidence/plans/plan-006.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-006-A02 — Action 2

- **Do:** Implement lexical shortlist, provider adapter and strict ID whitelist; integrate protected API router.
- **Done when:** Response always uses DB fields; provider failure never masquerades as successful inference.
- **Verify:** TEST-011..013/024.
- **Checkpoint:** No provider key in client bundle; timeout handling.
- **Evidence:** record `PLAN-006-A02` in `evidence/plans/plan-006.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-006-A03 — Action 3

- **Do:** Implement search page with loading/reason/error/empty product states.
- **Done when:** Authenticated user can submit need and inspect known product match reasons.
- **Verify:** Search UI and public JSON/error states can be inspected; browser TEST-016/017 waits for PLAN-007 IR with a deterministic fake external provider and a running real Web + API.
- **Checkpoint:** OpenRouter mock only used in isolated test stack.
- **Evidence:** record `PLAN-006-A03` in `evidence/plans/plan-006.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-006-A04 — Action 4

- **Do:** Hand search scenarios to PLAN-007 for deterministic Playwright execution after harness IR; separately run one authorized *real* OpenRouter HTTPS integration with redacted evidence when a valid key and execution permission are present.
- **Done when:** PLAN-006 IR proves suggestion route/UI/provider handling are integrated; FV requires separately authorized TEST-016/017 E2E after PLAN-007 IR and TEST-018 real provider evidence (or remains blocked, never PASS).
- **Verify:** TEST-016/017 under PLAN-007 managed harness, separate TEST-018 real HTTPS against real OpenRouter, and TEST-011/012/013/024 unit/API suite.
- **Checkpoint:** If key/permission absent mark TEST-018 BLOCKED; do not claim OUT-002 PASS. PLAN-007 needs PLAN-006 IR, not its TEST-016/017 FV; keep later FV pending until browser/live evidence.
- **Evidence:** record `PLAN-006-A04` in `evidence/plans/plan-006.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

## Approval and stop conditions

- The complete source-create batch is prepared only after all governing sources and this Plan batch have their exact-revision User approvals. Initial create permission must enumerate every named file and intended content. Additional library-generated files require prior enumeration and approval.
- Ask separately before linked Core test executions. If a test fails, inspect and request fresh permission for any Core edit; don't redefine TEST expectations.
- Stop and request a higher-contract amendment if approved scope, interface, auth/security boundary, classification, or verification seam must change. Record actual evidence separately.
- **This proposal is not permission to execute commands, mutate a repository, or claim any test passed.**

## Current repair execution

The User-approved PLAN-010 supersedes email-registration and retained-volume assumptions in this historical plan. See revised PRD-001/008, Architecture and TEST-001/002/010. Unaffected implementation responsibilities remain valid.
