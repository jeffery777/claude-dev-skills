---
id: REQ-021
title: Provider profile setting and platform read-back in dev-gate (FU-009, FU-008, MR-001)
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-21 (CI PR), user answer to decision cards Q1 to Q4 (Q3 = R1-002 provider profile; Q4 = ES-004 a PR can change its own checks)"
    quote: "Q1 yes；Q2 分開處理：Issue 文字加進 REQ-011（a），commit 時區接受、不處理（c），LFS、push options、release notes 延後（b）；Q3 b；Q4 b"
  - type: chat
    locator: "Claude Code session 2026-10-21 (CI PR), user answer to decision card Q5 (stop rule after round 2: split the provider-profile design out of the CI PR)"
    quote: "Q5 a。FU-009 的設計範圍請一併涵蓋 FU-008（PR 削弱自己的 check），兩者一起設計。"
  - type: chat
    locator: "Claude Code session 2026-10-21 (FU-009 session, Issue #14), user answer to decision cards Q1 (approve spec v2 with a checker script) and Q2 (FU-008 report: always-on note plus a fixed path list)"
    quote: "Q1 a。但 script 只實作規格列出的性質；review 若找到規格以外的新邊界情況，一律做成需求缺口卡片交給我決定，不可直接加程式。Q2 a。"
  - type: chat
    locator: "Claude Code session 2026-10-21 (FU-009 session, Issue #14), user answer to decision cards Q4 (stop rule after design review and implementation review round 1: one bounded fix round), Q5 (R1-006/ES1-002: without a profile, compare the PR's base with the bound base) and Q6 (R1-005/ES1-004: a checker failure or a missing result line is UNVERIFIED)"
    quote: "Q4 a；Q5 a；Q6 a"
  - type: chat
    locator: "Claude Code session 2026-10-21 (FU-009 session, Issue #14), user answer to decision cards Q7 (stop rule after the round-2 confirmation: fix the dev-core text and continue) and Q8 (ES2-003: pin the GitHub host in the no-profile read)"
    quote: "Q7 a；Q8 a"
  - type: doc
    locator: ".dev/followups.md rows FU-008 and FU-009 (main 97406d7)"
    quote: "the setting is read from the bound base commit, never from the PR head or the working tree; a change to it in base..head is a provider-policy change for the user (R-AUTH-2); every `gh` call uses the bound repository; \"passed\" means only `SUCCESS`; BLOCKED, then UNVERIFIED, then VERIFIED; the union of the profile's and the platform's required checks; an unreadable or invalid setting fails closed; and how a PR that changes its own checks is reported (FU-008)"
non_goals:
  - Changing repository settings (rulesets, branch protection, required checks); the maintainer owns them
  - Providers other than GitHub
  - A rule that blocks a PR because it changes its own checks (FU-008 blocking rule stays deferred, Q4 (b))
  - Reading or verifying ruleset rules other than required status checks (PR required, merge method, approvals, deletion)
  - Any checker behaviour that the approved spec does not list; a new edge case is a REQ-GAP card for the user
  - Changes to engineering-workflow-core, codex-dev-skills or grok-build-dev-skills
depends_on: [REQ-020]
refines: [REQ-020]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

A project can select a GitHub provider profile with `platform_profile` in
`.dev/config.json`. At the merge gate, `dev-gate` then reads the platform state
back and reports `platform_enforcement` as `VERIFIED`, `UNVERIFIED` or
`BLOCKED` instead of `NOT_CONFIGURED`. The design (spec v2) was reviewed in
design round 1 and approved by the user (Q1 (a)) on the condition that the
checker script implements only the listed properties. A PR that changes its own
checks is reported, not blocked (Q2 (a)). The `dev-core` R-EXH-4 wording for
`NOT_CONFIGURED` matches `dev-gate` (MR-001, PR #13 comment).

## Acceptance

- `skills/dev-gate/references/platform-profile.md` defines the format, where it
  is read, the fail-closed cases, the GitHub read-back, the policy-change and
  FU-008 report, and what it does not protect.
- The setting is read only at the bound base commit (`git cat-file`,
  `git ls-tree`); a missing base commit is `UNVERIFIED`; the PR head and the
  working tree are never read for it.
- Invalid JSON, a duplicate key, an unknown key, a missing key, a wrong type, a
  duplicate check name, empty checks, a provider other than `github`, or a
  repository that is not the bound repository → `BLOCKED` with a message.
- Every `gh` call is `gh api --hostname github.com repos/<bound repo>/...`.
- Only `success` passes; a pending or missing run is `UNVERIFIED`; any other
  conclusion is `BLOCKED`; result precedence `BLOCKED` > `UNVERIFIED` > `VERIFIED`.
- Required checks = profile ∪ platform (rulesets, all pages, and classic
  protection); a profile-only check or an app id mismatch is `BLOCKED`; an
  unpinned platform-only check is `UNVERIFIED`.
- Check runs are read with `filter=all` over all pages, filtered by head, name
  and app id, grouped by check suite; the newest run of every suite must be
  `success`. The PR head is read again after the runs.
- A change of `.dev/config.json` in base..head gives the user a decision card
  (R-AUTH-2), bound to the head blob.
- With a profile, `VERIFIED` reads `VERIFIED (checks ran this PR's own
  definitions)`, and the gate lists changed files under the fixed FU-008 paths
  (`--no-renames`).
- Without a profile, the one `gh pr view --repo github.com/<owner/name>` read
  (Q8 (a)) also returns `baseRefOid`; a base that is not the bound base is
  `UNVERIFIED` (Q5 (a)).
- A checker failure or a missing `platform_enforcement:` line is `UNVERIFIED`
  at the gate, never `NOT_CONFIGURED` (Q6 (a)).
- `tests/test_platform_profile.py` has a negative case for each item above and
  runs in `scripts/validate.sh`.
- `dev-core` R-EXH-4 states when the result is `NOT_CONFIGURED` and when it is
  `UNVERIFIED` (MR-001).
- This repository's `.dev/config.json` selects a profile with `validate` and
  `gitleaks` from GitHub Actions (app 15368) on `main`, matching the active
  ruleset read back on 2026-10-21.

## Notes

Design records: Issue #14 and its PR. Design review round 1 (DR-001 to DR-008,
ES0-001 to ES0-008) was run on the spec before any rule text. Related:
[[REQ-020-minimal-ci]], [[REQ-011-security-review-before-commit-push]].
