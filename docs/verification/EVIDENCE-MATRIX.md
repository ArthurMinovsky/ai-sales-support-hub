# Outcome Evidence Matrix — Recorded Verification

**Updated:** 12 October 2026, Asia/Bangkok.

**Source:** main, baseline `c9b5610ddf23bfc04749455512f4d4d891089162` plus uncommitted TEST-019 fixes.
**Executed snapshot digest:** `67ba389c857e95307e0d01c0e67a58219abf11b1019f039f386925e01310cd2f`, before later reporting edits; exact tested code hashes are in the new summary. All 15 protected contract/plan hashes matched HANDOFF.

| Outcome | Evidence state | Actual proof | Limits |
|---|---|---|---|
| OUT-001/002 | Local automated evidence available | Recommendation checks, Swagger readiness and separate real OpenRouter HTTP 200 record in `evidence/openrouter/live-inference-redacted.json`. | No fresh live-provider call in this security run. |
| OUT-003 | Automated behavior executed | Backend 11/11 and container browser 17/17: auth, CRUD, suggestions, origin policy and CSP. | Executed checks do not establish every manual contract subcondition. |
| OUT-004 | Test evidence available | New run's `pytest-regression.xml`, `playwright-final.json`; evaluator 10/10, TypeScript and Web build exit 0. | Browser AI uses an isolated mock provider. |
| OUT-005 | TEST-019 local PASS; baseline CI succeeded | Four actual scans, complete reports/exits/review and cleanup in new `summary.json`. CI baseline run 38157463221: six jobs/image archive. | New workflow has not run remotely; baseline DAST report retention was incomplete. |
| OUT-006 | Materials/source available | Public repository, README, PITCH, WALKTHROUGH, EXAM_APPENDIX. | TEST-025 rehearsal pending. |
| OUT-007 | Bounded security checks executed | Production nonce CSP; SCA/SAST/IaC clear; passive DAST has no high/low alerts. | One medium HTTPS image-source warning reviewed; no zero-risk/authenticated-DAST claim. |
| OUT-008 | Traceable evidence available | Tested code/report hashes, versions, targets, exits and teardown in new run folder. | Independent review and TEST-026 User acceptance pending. |

## TEST-019 checkpoint

- **SCA:** pip-audit 2.10.1, 66 dependency entries/0 vulnerabilities; npm 11.19.0, 0 advisories; exits 0. Editable local package is not auditable through PyPI.
- **SAST:** Semgrep 1.180.0, 23 files with three configured Python rules, 0 findings/errors; exit 0.
- **IaC:** Checkov 3.3.27, 118 Dockerfile + 176 workflow checks passed, 0 failed/parsing errors/skips in this scope; exit 0.
- **DAST:** ZAP 2.17.0, actual exit **2** (warnings), 0 high/0 low/1 medium/3 informational alert types. JSON 15,752 bytes and HTML 49,587 bytes retained. Medium `img-src https:` preserves approved external product images; future image-host restrictions require an approved contract change. Reviewed in `review.json`.
- **Preservation:** fixture containers removed without `-v`; named volume remains. Main API container and SQLite hash unchanged (2 users/10 products/integrity OK). Main Web refreshed to tested image; 2/2 security checks passed.

Evidence: `evidence/security/runs/20261011213538Z/summary.json`, `review.json`, `execution-ledger.json`, `final-scans/`.

Local Web **http://localhost:55016**; API **http://localhost:55011**; Swagger **http://localhost:55011/docs**. Rediscover ports with `./scripts/status.sh`.

[CI baseline 38157463221](https://github.com/ArthurMinovsky/ai-sales-support-hub/actions/runs/38157463221) verifies committed `c9b5610`, not new changes. No external hosting or manual acceptance is claimed. Historical no-key/no-remote, 10/4-test and fixed-port summaries are superseded; raw records are preserved.
