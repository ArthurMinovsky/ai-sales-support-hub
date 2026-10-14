# HANDOFF — AI Sales Support Hub

## Current authority and scope

The User approved the complete repair implementation plan on 14 October 2026: remove email registration, add password confirmation, reset all accounts/product edits on API container start/restart, invalidate earlier sessions, neutralize first-party branding/docs, and clean published Git history.

Current executable plan: plans/PLAN-010.md. It supersedes the email and persistent-volume requirements of the earlier source. Revised governing contracts retain stable OUT/PRD/CORE/TEST IDs. The original bundle, governing bytes, ignored credentials and raw historical reports are privately archived outside this repository.

## Implementation

- Registration DTO: username, password, confirm_password. Username normalization precedes validation. No email DB column or public DTO field.
- Passwords remain Argon2id hashes. Confirmation is validated but never stored. Login remains username/password.
- JWT TTL remains 3600 seconds. A random epoch is generated on each API lifespan; previous-start JWTs fail even if IDs repeat.
- Docker /data uses a 64 MiB tmpfs with UID/GID 10001 and mode 0700. Start/restart/recreation resets accounts and edits; ten neutral samples reload. No-op up does not reset an API that stays running.
- Fresh launch uses --force-recreate and existing dynamic-port/status reporting.
- No real credential is stored in the repo. The private .env must remain ignored.

## Verification and release state

The scoped repair is verified and published. Actual results belong in ../verification/REPAIR-REPORT.md and its referenced evidence. This state applies to the approved repair scope, not new live inference or a fresh manual acceptance decision.

Backend RED/GREEN logs are retained privately. Current local verification passes 18 backend tests, 18 browser checks, 10 scanner-evaluator cases, typecheck/build, real-container readiness, tmpfs ownership/bounds and separate restart/recreation reset checks. Four scans pass under their documented scope; DAST retains one reviewed medium warning and four informational alert types. Exact source/report hashes are in repair-evidence.json. Rewritten-history CI is a separate publication check.

No new live inference, independent review or external hosting is claimed by this repair. Earlier manual decisions and execution reports describe their original revision, not automatic acceptance of these changed behaviors.

## Git safety

Before rewriting, main and origin/main were e9d3ec05c8365d2476163b595f31914de81dad7a. Recheck the remote immediately before lease-protected publication. Stop and reconcile concurrent changes.

Use a fresh isolated clone for git-filter-repo. Retain the original recovery bundle and commit mapping privately. Remove earlier excluded report paths and target branding/contact text throughout reachable history. Do not publish private originals, real .env values or claim edited historical evidence as a fresh execution.

## Publication verification

Implementation commit 9aa6ffcadfed38d58c7bd6a1f8da15d9fdb12062 was published with the recorded expected-old-tip lease. A fresh GitHub clone passed the reachable-history audit (17 commits, 182 blobs, no targeted findings), all 66 execution-relevant source hash checks, 18 backend tests, clean npm installation, typecheck and build.

GitHub Actions run 38505764658 passed all six jobs: backend, frontend, integration (including API restart/recreation and stale-token rejection), static security, passive DAST and release images. Test/scan artifacts and the Docker image archive were downloaded privately. See https://github.com/ArthurMinovsky/ai-sales-support-hub/actions/runs/38505764658 for the exact implementation revision.

The original clean checkout was synchronized after CI success. Its ignored credentials and local historical reports were preserved byte-for-byte; original named volumes remain detached rather than deleted. The documented local launcher built, force-recreated, waited for health and printed dynamically allocated URLs successfully. Rediscover current URLs using scripts/status.sh.

Final updates change reporting and clarify the verification recipe's isolated project name so it matches the reset helper's safety guard. Application, test and configuration code remains identical to the verified implementation. Inspect the exact latest commit's CI separately; earlier results are never silently relabeled as a new execution.
