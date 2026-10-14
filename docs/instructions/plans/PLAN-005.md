# PLAN-005 — Product Management UI

> **PROPOSAL R1 — NOT APPROVED.** Action-only plan. From approved OUTCOME `801acfc6…334bbb1`; conditional Constitution/PRD/Architecture/TEST R1 drafts. Batch approval is a planning gate, not permission to create code, execute tests, git-commit or deploy.

- **Plan ID:** PLAN-005
- **Dependencies:** PLAN-002, PLAN-004
- **Classifications copied from PRD:** CORE-002
- **Outcomes:** OUT-003
- **Architecture modules:** MOD-007
- **Approved TEST target IDs once verified:** TEST-015, TEST-008, TEST-009
- **Owner:** implementation coordinator; optional isolated worker only after approved contracts and separate permission.
- **Parallelism:** Independent writers possible only when dependencies and file ownership do not overlap; default serialize shared main.py/CI/runtime.

## Exact file operations

| Operation | Exact path | Owner |
|---|---|---|
| CREATE | `web/src/lib/api.ts` | PLAN-005 |
| CREATE | `web/src/app/(app)/products/page.tsx` | PLAN-005 |
| CREATE | `web/src/components/ProductForm.tsx` | PLAN-005 |
| CREATE | `web/src/components/ProductTable.tsx` | PLAN-005 |
| CREATE | `web/tests/e2e/catalog.spec.ts` | PLAN-005 |

## Ordered actions (no source code)

### PLAN-005-A01 — Action 1

- **Do:** Specify Playwright CRUD and validation user flows through real browser and BFF.
- **Done when:** Tests assert visible fields/state, not implementation internals.
- **Verify:** TEST-015 expected RED when appropriate.
- **Checkpoint:** No Core execution without separate approval.
- **Evidence:** record `PLAN-005-A01` in `evidence/plans/plan-005.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-005-A02 — Action 2

- **Do:** Implement typed product client and page with list/add/edit/delete confirmation and validation.
- **Done when:** Form matches required product fields; unauthorized access blocked.
- **Verify:** TEST-015; paired API TEST-008/009.
- **Checkpoint:** No image server-side fetching.
- **Evidence:** record `PLAN-005-A02` in `evidence/plans/plan-005.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-005-A03 — Action 3

- **Do:** Verify persistence through browser refresh and REST view.
- **Done when:** Changes visible without state divergence.
- **Verify:** TEST-015, API TEST-008.
- **Checkpoint:** Shared catalog is explicitly all-authenticated, not per-user.
- **Evidence:** record `PLAN-005-A03` in `evidence/plans/plan-005.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-005-A04 — Action 4

- **Do:** Record screenshot/evidence and correct UI only under applicable Core/Minor scopes.
- **Done when:** CRUD happy/error path verified against current API.
- **Verify:** TEST-015 and test reports.
- **Checkpoint:** Pure visual polish only may be MINOR-001 after PRD approval.
- **Evidence:** record `PLAN-005-A04` in `evidence/plans/plan-005.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

## Approval and stop conditions

- The complete source-create batch is prepared only after all governing sources and this Plan batch have their exact-revision User approvals. Initial create permission must enumerate every named file and intended content. Additional library-generated files require prior enumeration and approval.
- Ask separately before linked Core test executions. If a test fails, inspect and request fresh permission for any Core edit; don't redefine TEST expectations.
- Stop and request a higher-contract amendment if approved scope, interface, auth/security boundary, classification, or verification seam must change. Record actual evidence separately.
- **This proposal is not permission to execute commands, mutate a repository, or claim any test passed.**

## Current repair execution

The User-approved PLAN-010 supersedes email-registration and retained-volume assumptions in this historical plan. See revised PRD-001/008, Architecture and TEST-001/002/010. Unaffected implementation responsibilities remain valid.
