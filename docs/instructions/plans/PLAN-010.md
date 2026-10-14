# PLAN-010 — Authentication, disposable state and repository cleanup

R1 — Approved for implementation by the User on 14 October 2026 through the complete repair plan. This scoped plan supersedes earlier email-registration and retained-volume behavior.

The complete implementation grant authorizes the scoped code/document amendments, fresh verification and debugging, private recovery/history rewrite, lease-protected publication, fresh-clone/CI verification and clean-checkout synchronization. Prior per-action gates are superseded for this repair only. Future work retains its original authority rules.

## Authority and interfaces

- OUT-003/005/006/007; PRD-001/002/008/011 and PRD-NFR-002; CORE-001/002/004/005/006/007.
- Register: username, password, confirm_password; normalize usernames before validation; matching confirmation required; no email storage/response; keep password limits and Argon2id.
- Login: username/password; 3600-second signed JWT with a random API-start epoch; old epochs fail even after user-ID reuse.
- Docker: bounded non-root /data tmpfs; zero accounts and ten neutral samples each API container start/restart/recreation. Reload preserves current-run edits; no-op up does not reset a running API.
- Fresh startup: build, force-recreate, wait, then print allocated URLs. Keep existing secrets private and detach old named volumes without blanket deletion.

## Ordered actions

1. PLAN-010-A01: inspect source/remote and retain a private original Git bundle, credentials and raw evidence outside the public repo.
2. PLAN-010-A02: author auth regressions, execute meaningful RED, implement registration/schema/username/session changes, then run backend GREEN.
3. PLAN-010-A03: use disposable Docker storage; verify browser reload, API restart and recreation, username reuse and stale-token rejection with reused IDs.
4. PLAN-010-A04: neutralize first-party app/docs/samples, amend controlling requirements/tests and Architecture pair coherently, and update verification/handoff sources.
5. PLAN-010-A05: execute typecheck/build, isolated real-container Playwright with mocked external provider and four security scans. Preserve exact commands, exits, hashes and findings.
6. PLAN-010-A06: clean history using git-filter-repo in a fresh isolated clone; remove previous excluded reports and targeted contact/branding text, validate current tree and all reachable historical contents/messages/paths.
7. PLAN-010-A07: publish only with an explicit expected-old-tip force-with-lease; reconcile remote changes rather than overwrite them. Verify a fresh remote clone and new CI, then synchronize the original clean checkout while retaining ignored files.

## Acceptance

TEST-001/002/003/004/005/007/010/014/015/019/020/021/022/023 apply to the changed scope. Password/confirmation values never appear in validation errors. All current registration and persistence expectations reflect the revised requirements; test criteria are not weakened to conceal failures.

Original historical execution is retained privately and not represented as a fresh run against rewritten commits. No new live-provider call or external hosting is implied. Current reachable history can be cleaned; remote caches and other people's copies are a separate visibility boundary.
