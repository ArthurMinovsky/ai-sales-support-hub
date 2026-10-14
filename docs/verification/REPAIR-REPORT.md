# Authentication and disposable-state repair

Fresh verification: 14 October 2026. Authority: the User-approved repair plan, recorded in PLAN-010. The existing implementation was repaired; original source, ignored credentials and raw reports are archived privately outside the public repository.

## Root cause and changes

Login already used username/password. Registration collected email and rejected duplicate email addresses, while the named SQLite volume retained accounts across rebuilds. The exact original login failure was not reproduced. The approved repair removes email collection/storage/uniqueness checks, requires matching confirmation, normalizes usernames and makes Docker data disposable.

Every API container start/restart/recreation now initializes zero accounts and ten neutral sample products using a 64 MiB non-root tmpfs. Current-run page reloads preserve product edits. Earlier tokens fail after restart, including after numeric user IDs repeat. Password hashing, HttpOnly cookies, Origin protection and the one-hour token lifetime remain enforced.

## Executed results

| Check | Result | Actual evidence |
|---|---|---|
| Backend authentication, protected routes, CRUD, suggestions | PASS | 18 Pytest cases; no failures/errors |
| Dependency installation, TypeScript, production build | PASS | npm ci, typecheck and build exit 0; Docker images built |
| Real-container browser flows with isolated mock provider | PASS | 18 checks, zero skipped/flaky/unexpected; includes confirmation, normalized login and edited-product reload |
| Restart and recreation, account reuse, stale JWTs | PASS | Both operations restore ten original products; old login/token 401, new session 200 with reused ID 1 |
| tmpfs owner and bound | PASS | UID/GID 10001, mode 0700, size 64 MiB; no named /data volume |
| Readiness and Swagger | PASS | API /health, /docs, /openapi.json and Web /login return 200 |
| Security report evaluator | PASS | 10 regression cases |
| SCA | PASS | 67 Python dependency entries, zero vulnerabilities; npm zero advisories. Editable local package has no PyPI advisory record |
| SAST | PASS | Semgrep 1.180.0: 23 files, three configured Python rules, zero findings/errors |
| IaC | PASS | Checkov 3.3.29: 118 Dockerfile and 180 workflow checks, zero failures/skips/parsing errors |
| DAST | PASS with reviewed warnings | ZAP 2.17.0 exit 2: zero high/low, one medium and four informational alert types |
| Architecture pair | PASS | Chromium render has visible SVG topology and matching Markdown SHA-256 |

[repair-evidence.json](repair-evidence.json) contains source file hashes, raw-report hashes, command exits and scanner/reset observations. Full logs, JUnit, browser reports, screenshots and ZAP JSON/HTML remain in the private recovery archive. CI uploads runnable test and scan artifacts for each newly published revision; inspect the exact commit on [GitHub Actions](https://github.com/ArthurMinovsky/ai-sales-support-hub/actions).

## Failures investigated

The initial browser environment lacked the matching Chromium binary; it was installed. Subsequent browser evidence exposed an accessible password label containing its hint; the input now has an exact label and separate description. The new mismatch assertion also needed to target the form's alert rather than Next.js's separate route announcement. Assertions retain their required outcomes.

Semgrep initially failed to open its log under sandbox permissions; the authorized rerun completed successfully. One Docker recreation produced no published Web port despite internal health; recreating that isolated Web container restored allocation. Failed runs and exits are retained privately. The final runtime checks use rediscovered ports.

## DAST review and limits

The medium CSP warning concerns img-src https:, which permits external HTTPS product images. It remains broader than an image-host allowlist. Script/style nonce restrictions remain covered by browser checks. Informational findings concern the empty root redirect's missing Content-Type, JavaScript application detection, deliberate no-store documents and cacheable versioned public JavaScript assets. No sensitive account payload was identified in those passive findings.

The scan is unauthenticated and passive. Its result does not establish complete authenticated security or zero risk. No new live OpenRouter call is claimed: current recommendation tests use the isolated mock, and earlier redacted live evidence remains historical.

## Repository cleanup and release procedure

Remove targeted contact/branding/framing text from current first-party files and all reachable historical blobs/messages/paths. Exclude earlier private report paths and their validation records throughout history. Keep replacement rules, the original bundle and commit maps privately. Publication uses an explicit expected-old-tip force-with-lease; concurrent remote changes must be reconciled.

Verify the published commit through a fresh clone and its own CI run before closing the repair. Historical results and manual acceptance are not automatically transferred to the changed implementation. Removing reachable history cannot guarantee removal from hosting caches, pull-request references or other people's clones.
