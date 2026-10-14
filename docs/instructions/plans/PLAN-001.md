# PLAN-001 — Foundation, Docker and Database Wiring

> **PROPOSAL R2 — NOT APPROVED.** Action-only amendment of approved upstream OUTCOME/CONSTITUTION/PRD/ARCHITECTURE/TEST R1. The proposal corrects Plan readiness/verification sequencing and shared-file ownership only; no API, Architecture or TEST contract change. Batch review is planning approval only, never permission to create source, execute tests, commit or deploy.

- **Plan ID:** PLAN-001
- **Dependencies:** none
- **Classifications copied from PRD:** CORE-004; CORE-002
- **Outcomes:** OUT-002, OUT-003, OUT-005
- **Architecture modules:** MOD-001, MOD-009
- **Linked TEST obligations:** TEST-020 (foundation readiness after full initial create batch); TEST-021 full OpenAPI coverage deferred to PLAN-006 route integration and PLAN-007 verification.
- **Owner:** implementation coordinator; optional isolated worker only after approved contracts and separate permission.
- **Parallelism:** no parallel edits to owned shared files; dependent source integration begins only after PLAN-001 IR and the initial-create authorization gate.

## Dependency checkpoints — initial-batch exception

- **Implementation Ready (IR)** = the named interface, source composition and prerequisite behavior are ready for a dependent Plan to integrate. This is **not** TEST PASS, project acceptance, or permission for source mutation/test execution. For a new project, the initial approved create batch contains all source/test files before any test runs; IR is the logical integration/readiness order after that batch exists.
- **Fully Verified (FV)** = every linked mandatory TEST obligation assigned to this Plan has current PASS evidence on the integrated build; `UNVERIFIED`, `BLOCKED`, RED and `FAILED` never count as PASS. Cases requiring later modules/harnesses are explicitly deferred to their named owner and retain pending status until execution.
- **Dependency edges below refer to IR, not FV**, unless an explicit FV prerequisite is named. A later Plan may finish the earlier Plan's deferred verification; no circular edge is introduced. New Core edits and individual Core TEST runs still require their own User permissions.

## Exact file operations

| Operation | Exact path | Owner |
|---|---|---|
| CREATE | `compose.yaml` | PLAN-001 |
| CREATE | `.env.example` | PLAN-001 |
| CREATE | `.gitignore` | PLAN-001 |
| CREATE | `backend/pyproject.toml` | PLAN-001 |
| CREATE | `backend/Dockerfile` | PLAN-001 |
| CREATE | `backend/app/__init__.py` | PLAN-001 |
| CREATE | `backend/app/main.py` | PLAN-001 final integrator (PLAN-002/003/006 contribute routes) |
| CREATE | `backend/app/core/__init__.py` | PLAN-001 |
| CREATE | `backend/app/core/config.py` | PLAN-001 |
| CREATE | `backend/app/db/__init__.py` | PLAN-001 |
| CREATE | `backend/app/db/session.py` | PLAN-001 |
| CREATE | `backend/app/api/__init__.py` | PLAN-001 |
| CREATE | `backend/app/api/routes/__init__.py` | PLAN-001 |
| CREATE | `backend/app/schemas/__init__.py` | PLAN-001 |
| CREATE | `backend/app/services/__init__.py` | PLAN-001 |
| CREATE | `web/package.json` | PLAN-001 final integrator (PLAN-007 contributes Playwright dependencies) |
| CREATE | `web/package-lock.json` | PLAN-001 final integrator (PLAN-007 contributes matching lock resolution) |
| CREATE | `web/tsconfig.json` | PLAN-001 |
| CREATE | `web/next.config.ts` | PLAN-001 |
| CREATE | `web/Dockerfile` | PLAN-001 |
| CREATE | `web/src/app/layout.tsx` | PLAN-001 |
| CREATE | `web/src/app/page.tsx` | PLAN-001 |
| CREATE | `web/src/app/globals.css` | PLAN-001 |

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

### PLAN-001-A01 — Action 1

- **Do:** Confirm blank-new-project tree and public runtime port map; enumerate every package bootstrap file and pinned dependencies.
- **Done when:** Explicit list of source files, env preconditions and all five shared-file ownership/contributions matches this Plan and the integrated initial source batch.
- **Verify:** diff agreed path list against current workspace tree and approved PRD/Architecture.
- **Checkpoint:** No code creation without complete batch approval + separate initial code-create permission.
- **Evidence:** record `PLAN-001-A01` in `evidence/plans/plan-001.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-001-A02 — Action 2

- **Do:** Maintain the Next/FastAPI/Compose scaffold and health endpoint; use bounded disposable `/data` tmpfs owned by UID/GID 10001.
- **Done when:** Both Docker images build after the *complete* initially approved code/create batch, required services expose declared ports and no secrets are committed.
- **Verify:** TEST-020 after User approves its Core test invocation; only `/docs` route accessibility may be inspected here. TEST-021 complete endpoint/schema assertion belongs to PLAN-007 after PLAN-006 IR.
- **Checkpoint:** STOP on undocumented additional files/missing JWT secret/health failure.
- **Evidence:** record `PLAN-001-A02` in `evidence/plans/plan-001.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-001-A03 — Action 3

- **Do:** Exercise clean Compose boot and teardown without `-v`; record configs and status.
- **Done when:** Web / and API /health respond on correct ports.
- **Verify:** TEST-020 with real launch and `/health`; `/docs` HTTP availability is *partial observation*, not TEST-021 PASS until all route modules exist.
- **Checkpoint:** Report any launch failure as UNVERIFIED and repair with new Core permission.
- **Evidence:** record `PLAN-001-A03` in `evidence/plans/plan-001.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

### PLAN-001-A04 — Action 4

- **Do:** Record durable foundation evidence and runtime limits for next Plans.
- **Done when:** Foundation module and source hash appear in Handoff/evidence after authorization.
- **Verify:** record TEST-020 evidence; mark TEST-021 `DEFERRED TO PLAN-007` (requires PLAN-002/003/006 IR).
- **Checkpoint:** PLAN-001 IR permits catalog/auth/AI source integration; PLAN-001 FV must wait for full TEST-021 schema evidence collected under PLAN-007. Never wait for FV to start PLAN-002.
- **Evidence:** record `PLAN-001-A04` in `evidence/plans/plan-001.json` with executed revision, observed vs expected and next permission; NOT produced during drafting.

## Approval and stop conditions

- The complete source-create batch is prepared only after all governing sources and this Plan batch have their exact-revision User approvals. Initial create permission must enumerate every named file and intended content. Additional library-generated files require prior enumeration and approval.
- Ask separately before linked Core test executions. If a test fails, inspect and request fresh permission for any Core edit; don't redefine TEST expectations.
- Stop and request a higher-contract amendment if approved scope, interface, auth/security boundary, classification, or verification seam must change. Record actual evidence separately.
- **This proposal is not permission to execute commands, mutate a repository, or claim any test passed.**

## Current repair execution

The User-approved PLAN-010 supersedes email-registration and retained-volume assumptions in this historical plan. See revised PRD-001/008, Architecture and TEST-001/002/010. Unaffected implementation responsibilities remain valid.
