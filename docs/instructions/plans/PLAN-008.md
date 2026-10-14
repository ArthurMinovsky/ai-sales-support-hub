# PLAN-008 — GitHub CI/CD and Four Security Scans

> **PROPOSAL R2 — NOT APPROVED.** Action-only amendment of approved upstream OUTCOME/CONSTITUTION/PRD/ARCHITECTURE/TEST R1. The proposal corrects Plan readiness/verification sequencing and shared-file ownership only; no API, Architecture or TEST contract change. Batch review is planning approval only, never permission to create source, execute tests, commit or deploy.

- **Plan ID:** PLAN-008
- **Dependencies:** PLAN-007 IR with runnable Web/API/Compose/Playwright harness; security scan FV requires a real readiness-verified target, not a YAML-only configuration.
- **Classifications copied from PRD:** CORE-006
- **Outcomes:** OUT-005, OUT-007, OUT-008
- **Architecture modules:** MOD-009
- **Approved TEST target IDs once verified:** TEST-019, TEST-022, TEST-023
- **Owner:** implementation coordinator; optional isolated worker only after approved contracts and separate permission.
- **Parallelism:** Independent writers possible only when dependencies and file ownership do not overlap; default serialize shared main.py/CI/runtime.

## Dependency checkpoints — initial-batch exception

- **Implementation Ready (IR)** = the named interface, source composition and prerequisite behavior are ready for a dependent Plan to integrate. This is **not** TEST PASS, project acceptance, or permission for source mutation/test execution. For a new project, the initial approved create batch contains all source/test files before any test runs; IR is the logical integration/readiness order after that batch exists.
- **Fully Verified (FV)** = every linked mandatory TEST obligation assigned to this Plan has current PASS evidence on the integrated build; `UNVERIFIED`, `BLOCKED`, RED and `FAILED` never count as PASS. Cases requiring later modules/harnesses are explicitly deferred to their named owner and retain pending status until execution.
- **Dependency edges below refer to IR, not FV**, unless an explicit FV prerequisite is named. A later Plan may finish the earlier Plan's deferred verification; no circular edge is introduced. New Core edits and individual Core TEST runs still require their own User permissions.

## Exact file operations

| Operation | Exact path | Owner |
|---|---|---|
| CREATE | `.github/workflows/ci.yml` | PLAN-008 |
| CREATE | `.semgrep.yml` | PLAN-008 |
| CREATE | `scripts/security/run-scans.sh` | PLAN-008 |
| CREATE | `scripts/security/triage.py` | PLAN-008 |

## Ordered actions (no source code)

### PLAN-008-A01 — Action 1

- **Do:** Define CI jobs and versions for pytest, Playwright/Compose, Docker image build and four scan categories.
- **Done when:** All job steps use pinned executable/config or documented version resolution.
- **Verify:** TEST-019/022 static coverage review.
- **Checkpoint:** Do not mark security tools run from workflow files alone.
- **Evidence:** record `PLAN-008-A01` in `evidence/plans/plan-008.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-008-A02 — Action 2

- **Do:** Add SCA pip-audit/npm audit, SAST Semgrep, IaC Checkov, DAST ZAP baseline; retention of outputs and triage.
- **Done when:** SCA/SAST/IaC outputs and a DAST launch/readiness/scan/teardown procedure have exact report destinations and exit policies; configuration alone is not actual scan execution.
- **Verify:** TEST-019/023.
- **Checkpoint:** ZAP baseline is passive/unauthenticated by default and only probes the reachable test target; report limitations. It MUST run after Web/API readiness; do not claim authenticated coverage.
- **Evidence:** record `PLAN-008-A02` in `evidence/plans/plan-008.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-008-A03 — Action 3

- **Do:** Build tagged Docker images and upload image archive/build artifact from CI.
- **Done when:** Release-build proof can be retrieved from actual GitHub run.
- **Verify:** TEST-022.
- **Checkpoint:** GitHub remote/connect and workflow execution may require separate User authorization.
- **Evidence:** record `PLAN-008-A03` in `evidence/plans/plan-008.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-008-A04 — Action 4

- **Do:** Execute explicit DAST sequence in isolated target project: (1) start `compose.yaml` test stack (2) poll `/health` and Web `/` and fail closed on timeout (3) run OWASP ZAP baseline against reachable app, retaining stdout/stderr/JSON/HTML even on findings (4) capture versions, target URI, revision, return status and scope (5) teardown test-owned containers without `down -v`; preserve reports. Also execute SCA/SAST/IaC, triage severity and record actual CI job result when authorized.
- **Done when:** Report directories `evidence/security/{sca,sast,dast,iac}/` contain real outputs and tool statuses, DAST includes readiness/target/scope/teardown record, and all reports survive cleanup; execution without live target is FAILED/BLOCKED, never PASS.
- **Verify:** TEST-019/022/023.
- **Checkpoint:** Never swallow scanner failure; distinguish findings from tool failure/readiness failure, record remote CI blockers. No deletion of non-test resources or Docker volumes without separate authority.
- **Evidence:** record `PLAN-008-A04` in `evidence/plans/plan-008.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

## Approval and stop conditions

- The complete source-create batch is prepared only after all governing sources and this Plan batch have their exact-revision User approvals. Initial create permission must enumerate every named file and intended content. Additional library-generated files require prior enumeration and approval.
- Ask separately before linked Core test executions. If a test fails, inspect and request fresh permission for any Core edit; don't redefine TEST expectations.
- Stop and request a higher-contract amendment if approved scope, interface, auth/security boundary, classification, or verification seam must change. Record actual evidence separately.
- **This proposal is not permission to execute commands, mutate a repository, or claim any test passed.**

## Current repair execution

The User-approved PLAN-010 supersedes email-registration and retained-volume assumptions in this historical plan. See revised PRD-001/008, Architecture and TEST-001/002/010. Unaffected implementation responsibilities remain valid.
