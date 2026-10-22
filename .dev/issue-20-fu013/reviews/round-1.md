# Review round 1 (deep, fresh reviewer), Issue #20

- Target: working tree against HEAD `91f4e8c`, `git diff HEAD --binary` sha256 `2deeae78…`, plus the untracked
  REQ-024 and graph files. Reviewer: `dev-skills:dev-reviewer` (opus, xhigh). CB-4 before and after: HEAD,
  status, diff hash and ignored-file list unchanged; no new file in the session scratchpad.
- Commands (reviewer): `PYTHONDONTWRITEBYTECODE=1 bash scripts/validate.sh` exit 0; `graph.py validate` ok.
  Skipped: GitNexus.
- Result: PASS (no finding above the thresholds). One question for the user (S-1): the existing read-only Bash
  wording forbids the `validate.log` write only by reading, and it did not stop the write in Issue #18 round 3.

## Dispositions

| Item | Relation | Disposition |
| --- | --- | --- |
| REQ-024 Notes attributed the author's reading to card 3d | in-scope | Fixed: stated as the FU-013 session's judgement |
| Deletion-rule copies lacked Core's "explicit" confirmation; `task-brief.md` lacked "a cleanup plan" | in-scope | Fixed: aligned with Core `auth-destructive` |
| S-1: explicit no-write sentence for reviewers | gap | Decision card 9: user chose (b) |
| FU-005 no-regression checklist stops at REQ-023 | gap | Decision card 10: user chose (a) |
| Deletion rule covers delete only, not overwrite or move | gap | Residual risk; existing behavior, not widened (no requirement) |
| `docs/design-proposal.md` D-011 and REQ-016 list two arms | unrelated | Residual risk; FU-004 row governs the runs |
