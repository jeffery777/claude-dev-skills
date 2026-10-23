---
id: REQ-024
title: Reviewer tests write no files; the implementer never deletes untracked or ignored files; official-tools arm in FU-004 (FU-013)
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user answer to the FU-010 decision cards (card 3: reviewer temporary files; option d: keep the rule that reviewers write nothing, no scratchpad allowance, no cleanup mechanism; the test-cache measure is recorded in the FU-013 row)"
    quote: "1a 2a 3d"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user answer to decision cards 5 and 6 (card 6: implementer deletions of untracked or ignored files inside owned paths)"
    quote: "卡片5改走縮小PR-A＋先做按需載入設計，6a"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, after PR #19 merged; relayed to the FU-013 session), user answer to the proposal to add an official-tools-only arm to the FU-004 measurements"
    quote: "同意，FU-004加上只用官方工具這一組"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, relayed to the FU-013 session), user answer to FU-013 decision cards 9 (an explicit no-write sentence in both reviewer agent files: option b) and 10 (REQ-024 and the R-AUTH-3 copies in the FU-005 no-regression checklist: option a); the CF-009 part concerns the orchestrator's upstream Issue draft"
    quote: "9b 10a，CF-009第2點照你的建議改寫"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, relayed to the FU-013 session), user answer to FU-013 decision card 11 (Merge Review security findings SR21-001 and SR21-002 on PR #21: option b, fix both) and to posting the review records as PR comments"
    quote: "11b，同意貼紀錄"
  - type: chat
    locator: "Claude Code session 2026-10-23 (orchestrator session, relayed to the FU-005 PR-3 session, Issue #31), user answer to PR-3 decision card 1 (SR21B-001: option a, add the test commands named in the brief to the dev-security-reviewer Bash allow-list); the change moved to Issue #32"
    quote: "同意你的建議，1a 2c"
  - type: chat
    locator: "Claude Code session 2026-10-23 (Issue #32 session), user approval of the shown allow-list sentence in agents/dev-security-reviewer.md and of the write scope"
    quote: "核准這句修改，也同意你建議的寫入範圍。"
  - type: doc
    locator: ".dev/followups.md, FU-013 row (from FU-010 cards 3d and 6a, Issue #18)"
    quote: "Keep the rule that reviewers write nothing."
non_goals:
  - A scratchpad allowance or a cleanup mechanism for reviewer files (card 3d)
  - Changes to `skills/dev-core/` (CB-5, R-AUTH-3 and `deltas.md` keep their text)
  - Running the FU-004 measurements (deployment steps outside the repository, REQ-016)
  - The `--prune` rule (FU-014), the on-demand loading design (FU-005), FU-011 and FU-012
depends_on: [REQ-016, REQ-023]
refines: [REQ-016, REQ-023]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Reviewers write nothing (card 3d keeps that rule). Their Python test runs
can still leave cache files in the repository, and CB-4 does not see ignored
files; the reviewer agent files therefore tell them to run Python tests
without writing byte code or a pytest cache. The implementer may delete files
inside its owned paths; an untracked or ignored file cannot be restored from
Git, so the implementer reports such a file and the main agent asks the user
(card 6a; Core `auth-destructive`, R-AUTH-3). The FU-004 measurements gain a
third arm next to with and without the pack: official tools only.

## Acceptance

- `agents/dev-reviewer.md` and `agents/dev-security-reviewer.md` tell the
  reviewer, when the brief names Python tests to run (card 11b, SR21-001), to
  run them with `PYTHONDONTWRITEBYTECODE=1` and pytest
  `-p no:cacheprovider` (or the runner's equivalent), so the tests create no
  files in the repository. Both files also state that the reviewer writes no
  file anywhere, including the session scratchpad, and redirects no output
  to files (card 9b). The only exception is a temporary file that a test
  named in the brief creates and removes itself in the system temporary
  directory; files the reviewer writes itself are never covered (card 11b,
  SR21-002). The read-only rules stay as they are.
- The Bash allow-list of `agents/dev-security-reviewer.md` names the test
  commands named in the brief, with the wording of `agents/dev-reviewer.md`
  (SR21B-001, PR-3 card 1 (a), Issue #32). This is the only change to the
  read-only rules.
- `agents/dev-implementer.md` and the Authority line of
  `skills/dev-deliver/references/task-brief.md` state in full that the
  implementer never deletes an untracked or ignored file, even inside its
  owned paths, reports it to the main agent, which asks the user, and that
  the deletion needs the user's explicit confirmation at the time of the action.
- The FU-004 row in `.dev/followups.md` has three arms (with the pack,
  without the pack, official tools only) on the same tasks and the same
  measures.
- The FU-013 row is closed with a link to this change.
- The FU-005 no-regression checklist in `.dev/followups.md` lists REQ-024 and
  the R-AUTH-3 copies in `dev-implementer` and `task-brief.md` (card 10a).
- No project tightening is loosened.

## Notes

The `validate.log` that a reviewer wrote to the session scratchpad in Issue
#18 review round 3 is outside the repository. The existing reviewer rules
already forbid it: Bash only for read-only commands (`dev-reviewer`) or
read-only inspection and the named scanners (`dev-security-reviewer`); a
redirect to a file is a write. That reading was the FU-013 session's
judgement, not part of card 3d, and the same wording did not stop the write
in round 3. The user therefore chose an explicit sentence (card 9b): write no
file anywhere, including the session scratchpad. Card 3d itself keeps the
rule, with no scratchpad allowance and no cleanup mechanism. The repository's
own tests create and remove temporary files with `tempfile`; without a narrow
exception a reviewer running `validate.sh` would break the sentence, so the
user chose card 11b: such self-removed test files are not reviewer writes.
Related: [[REQ-016-deploy-and-measure]], [[REQ-023-core-audit]].
