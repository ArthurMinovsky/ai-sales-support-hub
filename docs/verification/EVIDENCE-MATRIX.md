# Outcome Evidence Matrix — Current Repair

Updated 14 October 2026. Current authority: PLAN-010 and the User-approved repair plan.

| Outcome | Current evidence | Limit |
|---|---|---|
| OUT-001/002 | Mock recommendation tests and actual Swagger readiness pass | Earlier live-provider evidence is historical; no fresh live call |
| OUT-003 | 18 backend and 18 browser checks pass; normalized username/confirmation, CRUD reload and one-hour sessions | Shared demo catalog, no tenant isolation |
| OUT-004 | Pytest, Playwright, typecheck and production build executed successfully | Exact tested source hashes in repair-evidence.json |
| OUT-005 | Compose builds/startup and four local scans pass under recorded scope | Verify the exact newly published commit through its own CI artifacts |
| OUT-006 | Generic README, API documentation, Architecture pair and verification recipes | Original private reports are excluded from publication |
| OUT-007 | Missing/wrong/expired/previous-start tokens rejected; secret-safe validation | Passive DAST retains one reviewed medium warning and four informational types |
| OUT-008 | Per-file hashes, report hashes, exits and observations retained | Historical manual decisions do not establish acceptance of changed behavior |

TEST-010 explicitly proves reset on API restart and force-recreation, restored ten samples, reusable username/ID, and old-token 401 after ID reuse. Product edits survive browser reload while the same API runs.

See [REPAIR-REPORT.md](REPAIR-REPORT.md) and [repair-evidence.json](repair-evidence.json). Full originals are retained privately; prior results are not presented as fresh proof.
