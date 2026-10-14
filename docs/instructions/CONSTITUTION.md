# CONSTITUTION — AI Sales Support Hub

> **PROPOSAL R1 — NOT APPROVED.** Upstream authority: approved `OUTCOME.md` SHA-256 `801acfc6e174b781ac1f9293da41154f6decdc9a561c0e21ca0aac015334bbb1`. This draft becomes project law only after User approval of its matching Review HTML revision.

## 1. Authority and amendment law

- **RULE-001 — Contract precedence:** OUTCOME > CONSTITUTION > PRD > ARCHITECTURE (`.md` + `.html` as one semantic pair) > TEST > PLAN > implementation/evidence. Higher authority wins; none may be silently amended by a lower contract.
- **RULE-002 — Approval quorum:** Exactly one User may approve project governance; neither the assistant, code reviewer, CI nor worker may ratify a contract. Approval is revision-specific and must follow the Review HTML containing the complete exact proposal.
- **RULE-003 — Protected artifacts:** `OUTCOME.md`, `CONSTITUTION.md`, `PRD.md`, `ARCHITECTURE.md`, `ARCHITECTURE.html`, `TEST.md` require explicit prior HTML review and User approval for any create/change/rename/delete. The Architecture pair always changes together, with matching semantic revision. `PLAN-###.md` proposals have a single batch review approval for initial creation. Proposal drafts and review HTML live outside governing `docs/instructions/`.
- **RULE-004 — Source traceability:** Maintain stable OUT, RULE/PERM, PRD, US, CORE/MINOR, ADR, RISK, MOD, ARCH-INV, TEST, PLAN identifiers and dependency/source hashes. IDs are not reassigned to unrelated meanings. The PRD alone determines Core/Minor classification.

## 2. Operational permissions

- **PERM-001 — Core mutations:** Core code, test, configuration, dependency or deployment mutations require a prior exact User permission naming impacted IDs, paths and operation. For a new project only, after all approved Plans, one permission can cover one explicitly enumerated initial source-create batch including all test files. Later Core edits require separate approval per mutation.
- **PERM-002 — Core execution:** Builds, runtime starts, migrations, tests and scanners require explicit execution authority when attached to Core work. Approval to edit is not approval to execute; after each Core mutation ask separately before running linked TEST cases. Read-only inspection alone confers no execute authority.
- **PERM-003 — Minor autonomy:** Only PRD-classified `MINOR-*` tasks within approved requirements/architecture/security/TEST and exact authorized scope may mutate and verify autonomously. Crossing an external, data, security, Core or protected-artifact boundary stops execution and escalates.
- **PERM-004 — Terminal read-only allowlist:** Before Core permissions, only effective non-mutating read/search operations (`cat`, `head`, `ls`, `find`, `grep`, equivalents, and stdout-only `echo`) may inspect context. Redirection, scripts, command substitution, package managers and any writing/testing/building are not read-only regardless of executable name. Working in the chat artifact sandbox to produce review proposals does not authorize touching a User repository.
- **PERM-005 — Auth/secrets:** No plaintext passwords, committed keys, token bypass, logged credentials, fabricated product IDs or AI-result claims. Auth and authorization must be checked at FastAPI and not depend on frontend checks alone. Do not put real secrets in screenshots, CI artifacts or commit history.
- **PERM-006 — Architecture change:** User approval is required for every material Architecture revision, including when prompted by a Plan or a failing test. Never repair a design contract through Plan-only edits.

## 3. Test and delivery governance

- **RULE-005 — TEST ownership:** `TEST.md` is the immutable verification specification until explicitly amended. Automated TESTs are run/evaluated by the agent with required permission; Manual TESTs receive the User's decision after review. Results and failures reside in evidence records, not rewritten into TEST.
- **RULE-006 — Verification hierarchy:** Unit/code passing does not mean Docker/system passing, which does not mean OUTCOME accepted. Real OpenRouter evidence cannot be replaced by a mocked call. Scans must be run and findings reported, not just configured.
- **RULE-007 — Test-first plan:** Where an executable behavior seam exists, PLAN schedules test-first small slices; a valid RED is caused by missing approved behavior, then minimal implementation and GREEN. Initial new-project code/test file creation may be one batch, followed by linked Plan test loops.
- **RULE-008 — Safety:** Never commit secrets. Validate product input; fail closed on invalid/expired tokens; treat OpenRouter failure as distinguishable from success. Demo data must remain explicitly fictional.
- **RULE-009 — Docker mandatory:** Do not treat the release as complete without one documented Docker Compose launch path and a genuine clean-instance demonstration. State prerequisite Docker installation and required local environment setup explicitly; no undocumented manual services.

## 4. Amendment propagation and user review matrix

- **RULE-010 — Source-first amendments:** Parse one batch of decisions such as `outcome: approved`, `constitution: ให้แก้`, `architecture: approved`, `plan-007: ให้แก้`. Apply corrections conceptually from highest affected artifact downward. Recalculate traceability, mark changed/stale/unaffected sections, regenerate impacted `.md` and HTML Reviews, then seek exact-revision approval. Never interpret approval of an old revision as approval of regenerated bytes.
- **RULE-011 — Scoped invalidation:** Only dependents affected by changed contract IDs become stale when impact can be determined. If blast radius cannot be bounded, pause for User decision. A Plan amendment cannot change requirements or TEST expectations.
- **RULE-012 — Late-approved upstream:** When a revised upstream artifact is approved after lower drafts have been written, first compare source hashes/semantics, regenerate/review affected lower drafts, and promote only after current approvals. Record `unchanged` with evidence where semantics are genuinely unaffected.

## 5. Walkthrough, commit, review and acceptance gates

- **RULE-013 — Minor walkthrough:** After Minor autonomous code/test work, render `MINOR-WALKTHROUGH.html` with actual paths, evidence and corrections; receive User approval of its exact revision before including it in the full walkthrough.
- **RULE-014 — Full walkthrough and Git:** Render `WALKTHROUGH.html` after approved Automated TEST runs; obtain User approval before local `git add/commit`. Never push, open PR or submit email solely because a local commit was permitted. Git and release mutations have their own approved scope.
- **RULE-015 — Independent review:** After committed code is pinned, obtain independent code review, present `feedback_ai_sales_support_hub.html` and review evidence. User then chooses to revise or continue to Manual TEST. Manual tests and explicit User final acceptance gate the DONE state.
- **RULE-016 — Handoff:** On Plan approval create `HANDOFF.md` with current state, harness, exact revisions, permissions, evidence and next action. If ClickUp is selected, link a verified task; do not create/modify a task from presumed permission.

## 6. Stop conditions and quality bars

- STOP on conflicting higher-level requirements, uncertain Core/Minor classification, missing User gate, unbounded affected scope, altered Architecture/TEST semantics, unsafe missing secrets, or ambiguous writer ownership.
- Status values must be evidence-based: `DRAFT`, `APPROVED`, `STALE`, `BLOCKED`, `FAILED`, `UNVERIFIED` are not interchangeable. Missing executions remain **UNVERIFIED**.
- Zero claims of tested/scanned/deployed/pushed/email-sent until command/provider evidence exists. A report of vulnerability findings is not a claim of zero risk.

## 7. Governance rationale and source map

This Constitution supports `OUT-001`–`OUT-008`; especially OUT-003/007 for auth and security, OUT-004/008 for test/evidence, OUT-005 for Docker/CI/scans and OUT-006 for handover. Sources include the approved Outcome, original product specification and chosen implementation workflow. The User-approved repair plan supersedes earlier email and storage requirements; original governing records are archived privately.
