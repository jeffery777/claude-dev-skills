---
name: dev-implement
description: Implement one clear, bounded code change or bug fix, verify it, and inspect the diff. Use for implementation requests whose target behavior is clear; use dev-plan first when it is not, and dev-review for review-only requests.
---

# dev-implement

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first, then the Core files that its stage map lists for `dev-implement`.

## Workflow

1. Read the project instructions, the relevant files and tests, and the Git
   state (R-STG-2). If a task graph node drives this work, read the node and
   move it to `in_progress` with `graph.py transition` (see `dev-plan`); a
   `planned` node moves to `ready` first. The
   transition re-checks the requirement files; a `REQUIREMENT_CONFLICT` means
   the user must decide first.
2. Name the requirement this change serves (R-RIG-3), the affected files, the
   risk and the verification you will run. When GitNexus is available, run
   `gitnexus impact` on the symbols you will change.
3. Make the smallest change that meets the DoD. Follow existing patterns. Do
   not refactor unrelated code, add speculative options or overwrite other
   people's changes.
4. Run the smallest relevant verification, then widen the check to what the
   change can affect (R-STG-4). Record every command and its result.
5. Read the full diff (`git diff`, including untracked files). Remove anything
   that no requirement covers.
6. Hand off. For `standard` and `strict` work, request `dev-review`. For
   `light` work, request `dev-review` and the `dev-gate` commit gate before any
   commit, push or PR. A light change you leave uncommitted reports "not
   independently reviewed" as residual risk (R-RIG-2).

Do not commit, push or open a PR unless the user asked for it (R-AUTH-2).
When the user asked for it, use this order (R-REV-9):

1. Stage only the intended files and check the staged list.
2. `dev-security-reviewer` scans the staged diff and the author, committer
   (`git var GIT_AUTHOR_IDENT`, `git var GIT_COMMITTER_IDENT`), message and
   trailers the commit will carry.
3. Pass the `dev-gate` commit gate, then commit without overriding the
   identity. Read back `git log -1 --format=fuller`.
4. Before the push, confirm that the recorded identity and message match what
   was scanned. Run `git ls-remote --heads --tags <remote>` (no `git fetch`), then
   `git push --dry-run --porcelain` with the exact arguments
   of the real push, and have `dev-security-reviewer` scan everything it
   lists: every commit the remote does not have yet and any annotated tag.
5. Pass the `dev-gate` push gate, then push with exactly those arguments.

Any change after a scan needs a new scan. Scan and gate records go into a
later commit or into a PR comment that the user has authorized, never into
the commit they cover (R-REV-9). Once a PR exists, they never go into a commit on the
PR branch (R-EXH-3). Without `dev-security-reviewer`, stop before the commit
or push (CB-4).

## Output

- Requirement IDs served
- Changed files and behavior change
- Verification run (commands and results) and verification skipped
- Residual risk, including "not independently reviewed" when that applies
