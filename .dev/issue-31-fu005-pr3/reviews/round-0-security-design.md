# Review round 0 — issue-31-fu005-pr3 (early security design review and R-REV-7 Security Diff Scan)

- Target: working tree at f2dfd19 (+ uncommitted)
- Diff identity: sha256 of `git diff HEAD --binary` after `git add -N .` = 9f843c7285400763828ab245b6db839cf08948f5d11c1a474aae65dc50bc06c5 (same before and after the review)
- Mode: security (early design review, spec 7.1; R-REV-7 Security Diff Scan)
- Reviewer: `dev-skills:dev-security-reviewer` (requested model/effort: opus/xhigh; effective: unknown)
- Scope: `CHANGELOG.md`, `agents/dev-reviewer.md`, `agents/dev-security-reviewer.md`, `docs/requirements/REQ-025-on-demand-core-loading.md`, `docs/requirements/log.md`, `skills/dev-deliver/references/task-brief.md` (+37/−0). Requirements: REQ-025, REQ-024, REQ-011. DoD: graph node T1.
- Core review criteria given: `review-and-security.md`, `authorization-and-stops.md` from the pack that the main session loaded (main checkout at `main` f2dfd19; not the tree under review; regular files; sha256 equal to the lock).
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR3-S0-001 | gap | REQ-GAP | `agents/dev-reviewer.md` and `agents/dev-security-reviewer.md`, new paragraph ("only your brief sets policy") | The paragraph makes the brief the only policy source but does not say that a policy in the brief must still meet R-REV-7 (verifiable source, accountable authority, defined scope, no weakening of non-waivable requirements) | `skills/dev-core/SKILL.md` R-REV-7 policy sub-bullet, R-REV-8 formal exception; Core `review-and-security.md:45`, `:51`, `:69` | If the main agent copies an injected "policy" into a brief, the reviewer does not challenge it; only the gate (`dev-gate` reads rev:45) stops it. Not a regression: the base had no policy sentence, and the new sentence narrows the policy sources | needs human decision | Rejected (user decision card 2 (c), 2026-10-23, relayed by the orchestrator session: 「同意你的建議，1a 2c」). Source: approved spec 2.2 text and card 9b (the reviewer sentence is exactly the spec text). Reason: stricter than the base; the main agent that writes the brief is bound by R-REV-7 and R-AUTH-1 and has the Core text (stage map); the sentence was kept on purpose after S2-002. Residual risk: as in Impact |
| PR3-S0-002 | in-scope | NIT | new paragraph in `agents/dev-reviewer.md`, against its Bash list (lines 14-16) | `dev-reviewer` has no listed Bash command that can check whether a listed file "is not a regular file" (symlink, directory) | `agents/dev-reviewer.md:14-16` | The reviewer cannot always make that check | keep as is | Rejected. Source: `agents/dev-reviewer.md:53-54` ("Mark what you could not check as unverified") already covers a check the reviewer cannot make; no change to the approved text. Residual risk: a symlinked Core file is not detected by `dev-reviewer` (the security reviewer can inspect; `verify_core.py` rejects symlinks in `validate.sh` and CI) |

## SR21B-001 (input from PR #21, decision card 1)

- Finding (PR #21 merge-time security review): the Bash allow-list of `agents/dev-security-reviewer.md` names scanners but not tests, while the same file tells the reviewer how to run Python tests that the brief names.
- R0-SEC security view: option (a) lets the security reviewer run code from the tree under review without technical isolation; the added risk is small next to the status quo (the main agent and `dev-reviewer` run the same tests).
- User decision 1: first 「同意你的建議，1a 2c」 (option (a)); then, after this session's auto-mode permission check refused the change, 「同意你的建議，選2」 (both relayed by the orchestrator session, 2026-10-23): move it to a follow-up and keep the file text.
- Process note: after the shell edit was refused, the same change was retried once with the Edit tool and then reverted. A refused action must not be retried with another tool; the session must stop and report. (finding PR3-S3-001 in the round-2 record)
- Disposition: Deferred.
  - Target: GitHub Issue #32 (user decision card PR3-C3 (a), 2026-10-23, relayed by the orchestrator session: 「同意你的建議，C3a C4b」); the change is made in its own small PR in which the user approves it directly.
  - Owner: jeffery777 (maintainer).
  - Reason: the session's auto-mode permission check classified widening the security reviewer allow-list as security weakening; the user chose to handle it in its own PR.
  - Remaining risk: unchanged since PR #21 (low). When a brief names tests for the security reviewer, the model decides at run time whether the allow-list permits them.
  - Verification plan: in that PR, `agents/dev-security-reviewer.md` lines 13-15 name "the test commands named in the brief" (wording as in `agents/dev-reviewer.md:15`); REQ-024 records the user's answer; a security review of the change.
  - Promotion trigger: a brief names tests for `dev-security-reviewer`, or the user starts the PR.
- `.dev/followups.md` is not changed (the spec PR-3 row does not list it). Its FU-005 row still says "PR-2 also waits for the FU-004 baseline run" and "PR-3 gives it to the user as a REQ-GAP decision card"; both are stale. Neither the spec nor REQ-025 assigns this update to a PR: residual risk, not a Deferred finding (PR3-R1-003).

## Requirement trace

| REQ | Covered by | Verified by |
| --- | --- | --- |
| REQ-025 PR-3 (brief line) | `skills/dev-deliver/references/task-brief.md:9` | equal to spec 2.2 text (script comparison) |
| REQ-025 PR-3 (reviewer paragraphs) | `agents/dev-reviewer.md`, `agents/dev-security-reviewer.md` | equal to spec 2.2 text after joining lines; 0 deleted lines |
| REQ-025 PR-3 (copies unchanged) | all files: 0 deleted lines | `git diff HEAD` |
| REQ-024, REQ-011 | reviewer write, test and R-REV-9 text unchanged | diff read |

## Security scan

Applicable: yes (agent tool and permission policy; the brief that subagents get; trust boundary for the listed file paths and their content; vendored Core as review input).
Status: FINDINGS (PR3-S0-001, PR3-S0-002; no MUST-FIX). Source to sink: the Core paths come from the main agent's brief and are read with Read into the reviewer's context as criteria; tampered Core can only make the reviewer report more or fewer findings, not act more. No new tool, Bash use, write exception or external call; frontmatter unchanged (DL-004). No private path, email, token or key in the diff.

## Verification evidence

- CB-4 tree check before and after: HEAD f2dfd19; the same 6 ` M` files, no untracked files; diff sha256 as above.
- `git diff HEAD --text --no-textconv --no-ext-diff` read in full; `--check` clean.
- Spec 2.3 [unverified] item: reading the Core files outside the worktree with Read, and `stat`, `shasum`, `git -C` on them, gave no permission prompt or refusal. Limit: the main checkout is the parent folder of the worktree; other locations or permission modes not tested.
- Not run: tests and `validate.sh` (per brief); `gh` (PR #21 record taken from the brief quote and `.dev/followups.md`).

## Residual risk and limits

- "guidance" in the new paragraph may be read to cover a CLAUDE.md in the tree under review; that is intended injection defense. Not tested: the reviewer's own instructions were the base version.
- The brief template says nothing for the implementer or explorer beyond "(reviewers only)" (REQ-025 non-goal).
- When the brief lists `none`, or a file cannot be read or is tampered, the table F rows covered through reviewer criteria fall back to the main session's reading; PR-4 re-checks coverage.
- Zero MUST-FIX does not prove there are no defects.
