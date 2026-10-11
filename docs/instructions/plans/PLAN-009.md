# PLAN-009 — README, Presentation, Evidence and Final Review Package

> **PROPOSAL R1 — NOT APPROVED.** Action-only plan. From approved OUTCOME `801acfc6…334bbb1`; conditional Constitution/PRD/Architecture/TEST R1 drafts. Batch approval is a planning gate, not permission to create code, execute tests, git-commit or deploy.

- **Plan ID:** PLAN-009
- **Dependencies:** PLAN-001..008
- **Classifications copied from PRD:** CORE-007
- **Outcomes:** OUT-005, OUT-006, OUT-008
- **Architecture modules:** MOD-010
- **Approved TEST target IDs once verified:** TEST-010, TEST-018, TEST-019, TEST-020, TEST-022, TEST-025, TEST-026
- **Owner:** implementation coordinator; optional isolated worker only after approved contracts and separate permission.
- **Parallelism:** Independent writers possible only when dependencies and file ownership do not overlap; default serialize shared main.py/CI/runtime.

## Exact file operations

| Operation | Exact path | Owner |
|---|---|---|
| CREATE | `README.md` | PLAN-009 |
| CREATE | `docs/presentation/PITCH.md` | PLAN-009 |
| CREATE | `docs/verification/EVIDENCE-MATRIX.md` | PLAN-009 |

## Ordered actions (no source code)

### PLAN-009-A01 — Action 1

- **Do:** Write setup and single-command Docker/Swagger/OpenRouter/reviewer procedures, no secrets.
- **Done when:** README has prerequisites, `.env.example` path, start/stop, test/scan procedures.
- **Verify:** TEST-020/021/023.
- **Checkpoint:** No promise one command without documented env preparation.
- **Evidence:** record `PLAN-009-A01` in `evidence/plans/plan-009.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-009-A02 — Action 2

- **Do:** Prepare 10-minute presentation script: As Is/To Be, Architecture, Features, User Stories, UI Flow.
- **Done when:** All five requested sections plus small demo sequence fit timing.
- **Verify:** TEST-025 Manual.
- **Checkpoint:** Script must describe actual built features and limitations.
- **Evidence:** record `PLAN-009-A02` in `evidence/plans/plan-009.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-009-A03 — Action 3

- **Do:** Populate evidence matrix with final revision, test reports, screenshots, scan findings, real OpenRouter evidence and blockers.
- **Done when:** Each OUT-001..008 is VERIFIED/BLOCKED/UNVERIFIED with links to proof.
- **Verify:** TEST-018/019/022/026.
- **Checkpoint:** Never fill PASS from planned tests; Git URL remains pending until provided.
- **Evidence:** record `PLAN-009-A03` in `evidence/plans/plan-009.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-009-A04 — Action 4

- **Do:** Present Walkthrough to User, then local Git commit, independent code review, post-review User decision, Manual verification and final delivery only at approved gates.
- **Done when:** Proof and approvals follow canonical order; no email sent without authorization.
- **Verify:** TEST-025/026 and Handoff.
- **Checkpoint:** Stop at missing permission/real external key/repository URL.
- **Evidence:** record `PLAN-009-A04` in `evidence/plans/plan-009.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

## Approval and stop conditions

- The complete source-create batch is prepared only after all governing sources and this Plan batch have their exact-revision User approvals. Initial create permission must enumerate every named file and intended content. Additional library-generated files require prior enumeration and approval.
- Ask separately before linked Core test executions. If a test fails, inspect and request fresh permission for any Core edit; don't redefine TEST expectations.
- Stop and request a higher-contract amendment if approved scope, interface, auth/security boundary, classification, or verification seam must change. Record actual evidence separately.
- **This proposal is not permission to execute commands, mutate a repository, or claim any test passed.**
