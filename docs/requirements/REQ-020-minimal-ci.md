---
id: REQ-020
title: Minimal CI - validate.sh and a gitleaks scan on GitHub Actions
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-21 (after PR #11 merged), user message agreeing to the CI proposal; relayed by the parent session to the CI session"
    quote: "CI的部份也同意你的建議"
  - type: chat
    locator: "Claude Code session 2026-10-21 (CI PR), user answer to decision cards Q1 to Q4 (Q2 = FU-007 split; Q3 = R1-002 provider profile; Q4 = ES-004 a PR can change its own checks)"
    quote: "Q1 yes；Q2 分開處理：Issue 文字加進 REQ-011（a），commit 時區接受、不處理（c），LFS、push options、release notes 延後（b）；Q3 b；Q4 b"
  - type: chat
    locator: "Claude Code session 2026-10-21 (CI PR), user answer to decision card Q5 (stop rule after round 2: split the provider-profile design out of the CI PR)"
    quote: "Q5 a。FU-009 的設計範圍請一併涵蓋 FU-008（PR 削弱自己的 check），兩者一起設計。"
non_goals:
  - Dependabot, release or deploy workflows
  - Changes to engineering-workflow-core, codex-dev-skills or grok-build-dev-skills
  - Changing repository settings (branch protection, rulesets, required checks); the user does that after the merge
  - Repository secrets of any kind
  - The provider-profile setting and its read-back (FU-009, with FU-008; user decision Q5 (a))
depends_on: [REQ-011]
refines: [REQ-010]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

The repository has CI, so that `scripts/validate.sh` and a secret scan run on
the platform for every pull request and every push to `main`. Then the user can
make the checks required, `platform_enforcement` can later be read back instead
of being `NOT_CONFIGURED` (after FU-009), and Auto-fix has a check result to act on.

The proposal that the user agreed to, as the parent session relayed it: one
GitHub Actions workflow on `pull_request` and on push to `main` that runs the
checks of `validate.sh` (`claude plugin validate` only if the Claude CLI can be
installed in CI without secrets, otherwise skipped in CI with a stated reason);
a gitleaks scan of the commits of the PR and of pushes to `main`; every
third-party action pinned by full commit SHA; `permissions: contents: read`; no
secrets; documentation; after the merge the user sets the checks as required.

## Acceptance

- `.github/workflows/ci.yml` runs on `pull_request` to `main` and on `push` to `main`. It has no `pull_request_target`, no secrets and workflow-level `permissions: contents: read`, and checkout does not keep the token (`persist-credentials: false`).
- Job `validate` runs `scripts/validate.sh` with the Claude CLI installed at an exact npm version, without a login.
- Job `gitleaks` downloads an exact gitleaks release, checks its SHA-256 against a value in the workflow before it runs, and scans every commit reachable from the checked-out commit with redacted output.
- Every action is pinned by a full commit SHA, with the release tag in a comment.
- `dev-gate` reads the checks of a PR back as Core requires (R-EXH-4): one read of the head and the checks, each check listed. The result is `NOT_CONFIGURED`, because no project setting selects a provider profile yet (Q3 (b); the setting is FU-009, Q5 (a)), or `UNVERIFIED` when the read fails or shows another head.
- README, `docs/design-proposal.md` (D-017) and `CHANGELOG.md` `[Unreleased]` describe the CI and the limits of the gitleaks scan, and README gives the steps with which the user makes the checks required.
- CI runs green on the PR that adds it, or its failure is explained.

## Notes

Phase 1 excluded a CI workflow (REQ-010 non-goals, D-008); this is new scope.
The R-REV-9 independent scans stay required: CI adds deterministic checks and
replaces no review. A PR can change its own checks (ES-004); the user deferred
that as FU-008 (Q4 (b)), to be designed together with the provider profile in
FU-009 (Q5 (a)). Related: [[REQ-010]], [[REQ-011]].
