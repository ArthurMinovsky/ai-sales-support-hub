# Outcome Evidence Matrix — Current Implementation Verification

**Recorded:** 2026-10-11T13:59:12Z  
**Source revision:** branch main, no commit or remote configured; implementation/test-inputs SHA-256 30ec1aa74c28dd316c4c7605c101c3ee77db390f2b113ad2984d78d97071814a (excludes README, walkthrough/evidence outputs, generated build/test files and caches).  
**Approved contracts:** hashes remain equal to the values in docs/instructions/HANDOFF.md.

| Outcome | Status | Evidence | Limits / blockers |
|---|---|---|---|
| OUT-001 | BLOCKED | Mocked known-catalog suggestion tests passed: TEST-011 and TEST-016; Playwright report at evidence/frontend/playwright-report/. | TEST-018 requires one real OpenRouter inference. No API key was provided; mocked output is not live-provider proof. |
| OUT-002 | BLOCKED | Swagger /docs and /openapi.json returned HTTP 200 (TEST-021); endpoint authorization schema was inspected. | Real OpenRouter inference evidence for TEST-018 is missing. |
| OUT-003 | VERIFIED | Pytest auth/JWT/protected-route/CRUD/persistence cases and Playwright registration, login, logout and catalog journeys passed. TEST-006 Origin control returned 403 for the disallowed origin and 201 for the configured origin. | Local test fixtures remain in the SQLite volume. |
| OUT-004 | VERIFIED | evidence/backend/pytest-results-final.xml: 10 passed. web/test-results/.last-run.json: passed, no failed tests; Playwright HTML report contains 4 passed browser tests. | Browser tests used the isolated mock OpenRouter service for deterministic AI journeys. |
| OUT-005 | BLOCKED | TEST-020 local Compose build/start/readiness passed; API and Web containers are healthy. TEST-019 ran SCA, SAST, DAST and IaC scans; see evidence/security/triage-summary.json and scanner reports. | TEST-022 GitHub Actions run is blocked: there is no Git remote or commit. DAST reported security-header warnings; see evidence/security/scan-review.json. |
| OUT-006 | BLOCKED | README and 10-minute pitch draft are present. | No Git repository URL; TEST-025 walkthrough has not been rehearsed or approved. |
| OUT-007 | VERIFIED | Invalid/expired token, product validation, provider failure, allowlist and secrets cases passed in Pytest/E2E. Runtime OpenRouter key is empty, and the plain local deployment has no mock-provider container. | DAST header warnings remain reported; no claim of zero security risk. |
| OUT-008 | BLOCKED | This matrix and raw test/scan reports are tied to the working-tree fingerprint above. | TEST-026 user acceptance remains pending the required walkthrough, local commit, independent review and post-review user decision. |

## Executed test summary

- **PASS:** Pytest 10/10; Playwright 4/4; local Compose API /health, Web /login, Swagger /docs, and /openapi.json all returned HTTP 200.
- **PASS:** SQLite named-volume persistence across docker compose down without -v and up --build -d; volume saleshub-implementation-check_app_data remained mounted at /data, and product ID 4 remained present.
- **EXECUTED WITH REPORTED FINDINGS:** SCA, SAST, DAST and IaC. All final scanner command exit codes are 0; ZAP warnings and the one Checkov false-positive skip are recorded, not described as vulnerability clearance.
- **BLOCKED:** TEST-018 live OpenRouter, TEST-022 remote CI, TEST-025 manual rehearsal and TEST-026 manual acceptance.

The Web port is http://localhost:3001 because an unrelated service already occupies host port 3000. API: http://localhost:8000; Swagger: http://localhost:8000/docs. Do not commit secrets or infer external deployment from this local Compose run.
