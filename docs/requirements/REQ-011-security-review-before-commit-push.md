---
id: REQ-011
title: Security review before every commit and push
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message after the SEC-01 author-email finding"
    quote: "commit、push之前一定要做security review，因為要確保金鑰、密碼、及其它不該被公開的文件被上傳到gitlab或github。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 2 (correction of the first quote)"
    quote: '我也要承認我剛說錯一句話"要確保金鑰、密碼、及其它不該被公開的文件被上傳到gitlab或github" 這句話應該修正為 "要確保金鑰、密碼、及其它不該被公開的文件不會被上傳到gitlab或github"'
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), same user message, on the other review findings"
    quote: "其它的風險，你可以選擇現在修？或記入follow up後續再安排修、一併測。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), answer to the --evidence-file question (selected option)"
    quote: "Project-only + hash (Recommended)"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 2, answer to decision card 1 (scan PR text before posting)"
    quote: "Card1，我選a"
non_goals:
  - Installing gitleaks or Git hooks without the user's approval
  - Review convergence, decision cards and REQ-GAP (PR-B, D-013, D-014, D-016)
depends_on: []
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Nothing secret or private reaches a public repository. Before every commit and
every push, an independent security reviewer checks exactly what will be
published: the staged diff and the commit identity and message. The
repositories are public, so anything pushed is published.

A tool of this pack must not copy private file content into a file that is
committed by default.

## Acceptance

- `dev-core` requires a `dev-security-reviewer` scan of what will be
  published: the staged diff and the commit author, committer, message and
  trailers before every commit; everything a push sends (commits and
  annotated tags) before every push; PR text before it is posted; and every
  commit in the range plus the merge or squash commit at merge.
- R-REV-1 says that a required security review uses `dev-security-reviewer`,
  never `dev-reviewer`.
- `dev-review`, `dev-gate`, `dev-implement` and `dev-deliver` apply the rule at
  their commit and push steps.
- `graph.py transition --evidence-file` accepts only a regular, non-symlink
  file inside the project root and records its relative path and SHA-256,
  never its content. Tests cover each refusal and the recorded form.

## Notes

The first quote has a slip; the user's correction (second source) gives the
intended meaning: such files must **not** be uploaded. Decision card 1 (a):
PR or MR titles, bodies and comments are scanned before posting, because they
are published too.

Origin: PR #2 SEC-01 (a hostname-derived author email was pushed). Design
record: D-015 in `docs/design-proposal.md`. Related: [[REQ-003]], [[REQ-007]].
