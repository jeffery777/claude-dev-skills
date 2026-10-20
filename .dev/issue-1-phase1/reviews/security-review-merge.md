# Merge-time security review — PR #2 (closes #1)

- Identity:
  - base and merge-base: `5229478aead42cc2d70b7843dd5db3548c08c562`
  - head: `8dc678744040046a50371aa106a17c9bfc17eda7` (10 commits)
- Reviewer: a fresh `dev-skills:dev-security-reviewer` subagent. It ran a sensitive-data scan of every commit in the range (added and removed lines, commit messages, author and committer metadata) and a Security Diff Scan of the full range.
- Tree check: HEAD, `git status --porcelain=v1 --untracked-files=all` and the SHA-256 of `git diff HEAD --binary` were the same before and after the review.
- Content scan: no keys, passwords, tokens, private keys, credential files, private absolute paths or binary blobs. No secret scanner (gitleaks, trufflehog) was available; a manual pattern scan was used instead.
- Result: `security_review: BLOCKED`. 2 findings had no disposition.

| ID | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| SEC-01 | MUST-FIX | Git had no `user.name` or `user.email`, so the author and committer of all 10 commits were derived from the local account and the machine hostname (`yang…@medm…`, `yang…@yang….local`). The branch is public, so these identifiers are already published | Fixed going forward and contained at merge (user decision, 2026-10-20, option B): the global Git identity is now `jeffery777` with the GitHub noreply address. PR #2 is merged with a squash merge whose author is that identity; the merge message must not keep `Co-authored-by:` lines with the old addresses. The old commits stay visible on PR #2; removing them needs GitHub Support and is the maintainer's choice |
| SEC-02 | NIT | The `dev-reviewer` and `dev-security-reviewer` descriptions said "Cannot edit files", but both keep Bash | Fixed: the descriptions now say the agents have no Edit or Write tools and that read-only Bash use is enforced by instructions only |

The repositories named in the pack (`engineering-workflow-core`, `codex-dev-skills`, `grok-build-dev-skills`) are public (user confirmation, 2026-10-20).
