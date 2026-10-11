# HANDOFF — AI Sales Support Hub
> Lifecycle state: `AUTO_START_URL_REPORTING_VERIFIED` — automatic one-command Docker launch verified; TEST-019 retains its separately recorded local PASS with findings. Changes uncommitted; independent/manual acceptance pending.
> Last reviewed: 2026-10-12, Asia/Bangkok, by Codex on the User's Mac. Main Web refreshed to tested image at http://localhost:55016; API remains http://localhost:55011; SQLite data unchanged.

## 1. Objective / source of authority
Build Sales Support Hub AI Sales Support Hub under OUT-001..008: FastAPI + Swagger + OpenRouter; Next.js + TypeScript registration/login, 3600s JWT and protected product CRUD/search; Pytest/Playwright; Git/CI, Compose one-command and SCA/SAST/DAST/IaC with evidence; reviewer documentation and 10-minute pitch. Employer project is the three-page `ข้อสอบ.pdf`; governing meanings are the approved contract files listed below.

## 2. Harness, destination and ownership
- **Harness:** opencode on the User's Mac (Codex desktop session 01a12aec-97b1-7141-8900-6788f191c912 performed the earlier verification work; opencode continued it).
- **User-local project path:** `/Users/aminovsky/Desktop/Personal/Code_project/Engineering/Developer/ai-sales-support-hub-contracts-review-r1/ai-sales-support-hub-implementation-pretest-r1/ai-sales-support-hub`.
- **Git state:** main, baseline `c9b5610ddf23bfc04749455512f4d4d891089162`; TEST-019 changes and the new `start` launcher/reporting updates remain uncommitted. No new commit/push.
- **Remote:** `https://github.com/ArthurMinovsky/ai-sales-support-hub` (public). Baseline CI 38157463221 on `c9b5610`: six successful jobs; DAST JSON/HTML absent. Modified workflow has not run remotely.
- **Lifecycle directory within project:** `docs/instructions/`.
- **ClickUp tracking:** still `NOT_LINKED` (searched 2026-10-11; no matching task; no card created).
- **Runtime resources:** securely provided OpenRouter/JWT settings remain in ignored local `.env`; values were not read/printed/changed in this security fix. GitHub baseline proof exists. ClickUp tracking, independent review and manual acceptance remain separate.

## 3. Approval record / immutable contracts
- On 2026-10-11 User explicitly approved `PLAN-001..004 R2`, `PLAN-006..008 R2` and directed transition to HANDOFF and *separate* Initial Source Create Batch approval.
- Prior User decisions approved `OUTCOME R1`, `CONSTITUTION R1`, `PRD R1`, Architecture R1 `.md`+`.html`, `TEST R1`, and `PLAN-005/009 R1`.
- The original header `PROPOSAL` in some R1 bytes is historical and remains untouched to preserve exact approved SHA. Approval authority is the User decision record and matching SHA, not the unchanged draft-status phrase.

| Approved artifact | Revision | Path | SHA-256 |
|---|---|---|---|
| OUTCOME | R1 | `docs/instructions/OUTCOME.md` | `801acfc6e174b781ac1f9293da41154f6decdc9a561c0e21ca0aac015334bbb1` |
| ARCHITECTURE | R1 | `docs/instructions/ARCHITECTURE.md` | `8b9e321b7ad0b6192a951d875e59f1b09c19e0db82354c6a3089658142e65135` |
| CONSTITUTION | R1 | `docs/instructions/CONSTITUTION.md` | `63a2e73661c090b557d317e356e219a1e2f20dac470cd338c55a12f2c273d449` |
| PLAN-001 | R2 | `docs/instructions/plans/PLAN-001.md` | `0f1dee98242def147523b60df7be699df71bb91cc91350da1e006ce177f41b44` |
| PLAN-002 | R2 | `docs/instructions/plans/PLAN-002.md` | `30b265690fb81f4f2b1980369126ee67327108e7c8190358ed7382fadd469b9b` |
| PLAN-003 | R2 | `docs/instructions/plans/PLAN-003.md` | `444c8ef3d6eb9f542e1a9e22d3e8c3315ceef46f59b3441ca01b42c928b2e446` |
| PLAN-004 | R2 | `docs/instructions/plans/PLAN-004.md` | `c255b0157a52e2b0ec1c4b09bacd4de9e1f36e0ba8e5ae2438ba9042c507896d` |
| PLAN-005 | R1 | `docs/instructions/plans/PLAN-005.md` | `7b51fc2c85843e6f4fd4eef758a71bf34848b85bd999193f207e6e7c3e9e0b57` |
| PLAN-006 | R2 | `docs/instructions/plans/PLAN-006.md` | `e51341e3b98f5bc7463461050adbb5b63fd8dc3b10e14c1b7df8426f3dbb3c0c` |
| PLAN-007 | R2 | `docs/instructions/plans/PLAN-007.md` | `e24ffb054100ffada9acb9d244f2351eb63805d49df41b80a9a5059e7d9008c2` |
| PLAN-008 | R2 | `docs/instructions/plans/PLAN-008.md` | `17e617ef7e68657818283bbca926bb78144fd8cd53b26100eb37311fcb611261` |
| PLAN-009 | R1 | `docs/instructions/plans/PLAN-009.md` | `b0c7ec9b6b72c59aa8219fa8c9638afef634b0c085f11b045382896c78daeb8c` |
| PRD | R1 | `docs/instructions/PRD.md` | `093a085d7236a7c7ec7492113e65d867eb42d2d34820c0bc1c84c7fd1c70af6a` |
| TEST | R1 | `docs/instructions/TEST.md` | `6791137e683c015c97d2f4e3c32ba25b191a4d5ff99426fd38469c24173a63fc` |

- `ARCHITECTURE.html` pair hash: `ece451e0ef9aa0954a36d8e6dbef3f3d16ec5ce8c51dd30334f8d8c9a90253f8` (must remain semantically equivalent to `ARCHITECTURE.md`).

## 4. Current Plan set and checklists
- [x] Verify R1 contracts and Architecture pair file hashes.
- [x] Verify R2 plan hashes and User approval statement.
- [x] Copy nine plans into the canonical approved plan directory exactly once.
- [x] Enumerate 68 distinct proposed `CREATE` paths from all nine plans; resolve five multi-plan shared files to one final owner.
- [x] Prepare complete exact **source AND executable test file contents** and per-file SHA-256 (delivered in `ai-sales-support-hub-source-manifest-r1.json`).
- [x] Review the resulting full initial source/test bundle and its exact 68-path change-action map with the User.
- [x] User permission granted (Fast Mode authorization, 2026-10-11) for the scoped local edits, builds, tests and debug loop.
- [x] Create the exact approved initial source files in the authorized project root.
- [x] Resolve the full npm lockfile; Docker/CI use `npm ci` (reproducibility gap closed).
- [x] Fresh TEST-019 regressions: Pytest 11/11, Playwright 17/17 on actual isolated containers, evaluator 10/10, TypeScript and production Web build passed. Earlier persistence/Compose proof remains separately recorded.
- [x] TEST-019 local PASS: four complete reports; SCA/SAST/IaC clear in scope; ZAP 0 high/0 low/1 medium/3 informational alert types. Raw ZAP exit 2; broad image-source warning reviewed in `evidence/security/runs/20261011213538Z/review.json`.
- [x] TEST-018 live OpenRouter inference PASS with redacted evidence (model `nvidia/nemotron-3-super-120b-a12b:free`).
- [x] Realism upgrade executed per approved `saleshub-realism_plan.md` (10-product Sales Support Hub-style catalog, professional self-contained UI, realistic test data).
- [x] Local Git commits of the verified state (see §2 chain).
- [x] Public baseline and successful CI available (38157463221). New security fixes remain uncommitted, with remote CI NOT_RUN; publication requires its own review/decision.
- [ ] Independent review and post-review User decision; then Manual TEST-025/026 acceptance.

## 5. Dependency/execution graph and shared writers
- First integrated create: all paths in `review/INITIAL_SOURCE_CREATE_BATCH_manifest.json`, one write each, after explicit batch approval. Contents must combine all approved Plan contributions.
- Checkpoints: `PLAN-001 IR → PLAN-002 IR → PLAN-003 IR`; `PLAN-004 IR` is needed for authenticated UI; PLAN-005 and PLAN-006 can progress when their relevant interfaces are integrated; `PLAN-007 IR` supplies browser harness; `PLAN-008 IR` supplies scans; `PLAN-009` is final handover.
- `IR` means **Implementation Ready**, not TEST PASS. `FV` means **Fully Verified** and requires real evidence from the eventual integration runs; all 26 TEST cases retain their original criteria.
- Product/API auth/scanning deferrals remain as approved R2; do not mark deferred tests pass.
- Shared path owners: PLAN-001 `backend/app/main.py`, `web/package.json`, `web/package-lock.json`; PLAN-002 `backend/app/api/routes/products.py`, `backend/tests/conftest.py`.

## 6. Quality / safety gates and blockers
- `TEST-010`: **PASS** — named-volume restart without `docker compose down -v`, re-proven twice (latest after the realism rebuild). Evidence: `evidence/docker/persistence.json`.
- `TEST-018`: **PASS** — at least one real OpenRouter HTTPS inference executed (twice: pre- and post-realism) with redacted evidence. Evidence: `evidence/openrouter/live-inference-redacted.json`.
- `TEST-019`: **PASS locally with reviewed findings** — four actual reports, versions/targets/exits, report/code hashes, lower-severity review and teardown in `evidence/security/runs/20261011213538Z/summary.json`. Report retention directly verified; tool errors fail closed.
- `TEST-020`: **PASS** — Docker build, Web/API readiness from one command (`docker compose -p saleshub-implementation-check up --build -d`), dynamic host ports. Evidence: `evidence/docker/smoke.json`.
- `TEST-022`: **Historical baseline PASS** — CI 38157463221 at `c9b5610`, six successful jobs/image archive. Its DAST retention gap was diagnosed and repaired locally; modified workflow is **NOT_RUN remotely**.
- `TEST-025/026`: **PENDING** — Manual Outcome acceptance by User after code review and the walkthrough gate.
- Remaining: review/publication of new fixes, independent review, walkthrough/manual acceptance and real ClickUp linkage. Remote Git and historical live-AI proof are available.

## 7. Current state → evidence → next gate → blockers
`TEST019_LOCAL_PASS_WITH_REVIEWED_FINDINGS` → new run's summary/review/raw reports, 11/17/10 regressions and preserved-volume teardown → review/publication decision and authorized remote CI of modified workflow; independent review/manual TEST-025/026 → no external hosting/final acceptance claimed.

## 8. Receiving harness instructions
Before any further mutation, read the approved files in `docs/instructions/` (hashes unchanged in the table above), inspect `git log`/`git status` for the current commit chain, and verify the local stack with `./scripts/status.sh`. `.env` is gitignored and holds the only secrets (JWT_SECRET, User-provided OPENROUTER_API_KEY) — never commit, print or log them. The E2E fixture stack (`compose.yaml` + `compose.e2e.yaml`, project `saleshub-e2e`) is separate from the hosting stack; tear it down after test runs. Docker volumes were reset during the realism upgrade; the 10-product catalog seeds automatically on first start.


## 9. Source creation update — historical record (superseded)
> This section is retained as the historical record of the ChatGPT authoring stage; it no longer describes the current state. See §10 for what has since been executed and verified.

- On 2026-10-11 User requested implementation until immediately before the TEST stage. All approved 68 planned source paths were authored in the ChatGPT artifact workspace and exported with the approved documentation.
- No unit/e2e tests, builds, container starts, CI jobs, security scans, real OpenRouter calls, Git commits or pushes were executed **during that stage**.
- Source/content SHA-256 map and file ownership are recorded in `ai-sales-support-hub-source-manifest-r1.json` (delivered with the archive, not inside protected contracts).
- The lockfile gap and all "not verified" statements in this section were resolved later — see §10.

## 10. Local verification execution record (2026-10-11, evening)
Executed under the User's Fast Mode authorization and subsequent explicit approvals, on the User's Mac, in the project directory listed in §2:

- **Dependency repair:** `web/package-lock.json` fully resolved (1,109 lines); Dockerfile, CI and verification recipe switched to `npm ci`; scoped PostCSS 8.5.23 override over Next.js 15.5.27 (npm audit zero advisories).
- **Tests:** backend Pytest **11/11** (final: `evidence/backend/pytest-results-post-origin-fix.xml`, realism rerun `pytest-results-realism.xml`); Playwright browser suite **15/15** on the rebuilt fixture stack (4 journeys + full origin-policy/BFF suite; `evidence/frontend/playwright-execution.json`); TypeScript typecheck and Next production build pass.
- **Docker:** one-command `docker compose -p saleshub-implementation-check up --build -d` starts both services healthy; dynamic host ports (`API_PORT=0`/`WEB_PORT=0`) with an origin check that validates the actual request Host/port (red→green evidence in `evidence/dynamic-ports/`); `scripts/status.sh` prints live URLs; TEST-010 persistence re-proven twice, including after the realism rebuild.
- **Security:** SCA (pip-audit 66 deps/0 vulns; npm audit 0), SAST (Semgrep 0 findings), IaC (Checkov 294 passed/0 failed — workflow-level `permissions: contents: read` added for CKV_GHA_7; CKV_SECRET_6 false-positive skips documented on both runtime-generated CI JWT lines), DAST (ZAP baseline exit 0). Reports and review: `evidence/security/`.
- **TEST-018:** live OpenRouter HTTPS inference PASS, twice (pre- and post-realism): model `nvidia/nemotron-3-super-120b-a12b:free`, HTTP 200, catalog-grounded suggestions; redacted record at `evidence/openrouter/live-inference-redacted.json`.
- **Realism upgrade (approved `saleshub-realism_plan.md`):** 10 realistic fictional Sales Support Hub-style products (Demo Sensors/Demo Automation families), professional UI with inline SVG icons and self-contained system fonts (Google Fonts CDN dependency removed), realistic test data; schema/API/selectors unchanged; volumes intentionally reset; demo user `nattapong.s` registered.
- **Fixes verified along the way (root causes in `WALKTHROUGH.html`):** lockfile metadata gap, Next standalone binding, suggestion validator boundary, test-domain email fixtures, selector races, stale scanner markers, hard-coded CI demo JWTs (now runtime-generated), dynamic-port origin rejection, missing workflow permissions.
- **Git:** local commit chain in §2; working tree clean; `.env` and runtime evidence folders gitignored; `evidence/dynamic-ports/` and `evidence/openrouter/` intentionally tracked.
- **Remote + CI:** pushed to `https://github.com/ArthurMinovsky/ai-sales-support-hub`; GitHub Actions run 38157082971 success (all 6 jobs) with retained image artifact — TEST-022 satisfied.
- **Still pending:** User walkthrough approval, independent review, Manual TEST-025/026, 10-minute pitch rehearsal.
## 11. TEST-019 repair checkpoint — 12 October 2026

- User directed immediate completion under existing Fast Mode local edit/build/test/debug authorization. All 15 protected contracts/plans unchanged.
- Root causes: nonroot ZAP could not write runner-owned bind output; prior successful exits concealed missing reports; Web lacked CSP/browser headers; root redirect had a large body. Review retains RED evidence and fixes.
- Fixes: container-owned report collection, fail-closed triage/CI security dependencies, fresh response nonce CSP/browser headers, small public root redirect and CSS replacement of inline styling; 2 browser/10 evaluator regressions added.
- Results: pip/npm 0 advisories; Semgrep 23 files/0 findings; Checkov 294/0; ZAP 0 high/0 low/1 medium/3 informational alert types. ZAP exit **2**, copy/collection/cleanup exits **0**. JSON 15,752 bytes, HTML 49,587 bytes retained.
- Medium HTTPS image-source warning is real and retained for PRD ADR-006 external image URLs. Scripts/styles require nonces. A future host allowlist needs approved contract scope; unauthenticated passive DAST remains bounded.
- Base `c9b5610` plus uncommitted fixes. Executed snapshot `67ba389c857e95307e0d01c0e67a58219abf11b1019f039f386925e01310cd2f` precedes later reporting edits; summary has exact tested code hashes.
- Main Web only refreshed; API unchanged. SQLite before/after `818c627881399d2ccb31855b899b007fb2cb70c1910fe4e0c98984cae4503715`, 2 users/10 products/integrity OK. Old image retained; fixture named volume preserved after container teardown.
- Evidence `evidence/security/runs/20261011213538Z/`: summary/review/execution ledger, raw reports/hashes/logs/exits, readiness/teardown/refresh. Backend 11/11, browser 17/17, evaluator 10/10, main security 2/2.
- No fresh provider call, commit/push, remote modified-workflow run or independent/manual acceptance claim.
## 12. Automatic startup URL reporting — 12 October 2026

- User requested allocated ports be printed automatically after build/start, before any push. Existing Fast Mode local implementation/build/test authorization covers this bounded continuation.
- Added executable POSIX-shell `start`; reviewed exact implementation creates one Compose launch with build/detach/wait, then queries actual mappings and prints Web/API/Swagger URLs. No new service, Docker socket mount, runtime dependency, fixed host port or protected-contract change.
- Files: `start` CREATE; README/WALKTHROUGH/EXAM_APPENDIX/HANDOFF operational reporting edits. Trace: CORE-004/007, OUT-005/006/008, PLAN-001-A03/A04 + PLAN-009-A01, scoped TEST-020/021/010 verification.
- Success: two isolated plain-stack `./start` invocations, exits 0. Web/API ports changed from 55018/55017 to 55020/55019; all printed login/health/Swagger endpoints HTTP 200. Startup failures print no misleading ready banner; six control checks passed.
- Data: test SQLite hash unchanged across restart; 10 seed products, integrity OK. Main Web/API container IDs unchanged. Only owned test containers removed without `-v`; fixture volume remains.
- Evidence: `evidence/docker/automatic-start/20261011T221254Z/summary.json`, `control-tests.json`, build/start/query/readiness/database/cleanup logs and exits. Executed `start` SHA-256 `04409bf7e7174fc4b4cfe1ce4cee806b67d9762cca1a50a5f1eea54b90428328`.
- Limits: tested on local Docker Compose 5.5.1/macOS; launcher uses host POSIX shell/standard tools. No clean-checkout/full TEST-020, new live AI, remote CI or final acceptance claim. App code/Compose/Dockerfile bytes from TEST-019 unchanged; scanner results stay tied to that earlier snapshot.
- Next: review/publish the combined local changes when authorized; independent review/manual decisions remain separate.
