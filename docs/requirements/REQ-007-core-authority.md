---
id: REQ-007
title: engineering-workflow-core stays the authority
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the Core question)"
    quote: "engineering-workflow-core 原文 vendor 進來並 pin 住 revision 與 digest，它是唯一權威，有衝突時以它為準。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the Core question)"
    quote: "dev-core 是 Claude 執行用的精簡版：只能改寫、壓縮或加嚴，不能放寬或刪除義務；每條規則都要對應到 Core 的錨點。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the Core question)"
    quote: "這次不改 Core、codex-dev-skills 或 grok-build-dev-skills。"
  - type: doc
    locator: "docs/design-proposal.md, section 7, D-001 (2026-10-20)"
    quote: "Core（vendor + pin） | `vendor/engineering-workflow-core/` 放原文，並鎖定 immutable revision 與 digest | **唯一權威**；有衝突時以它為準"
  - type: chat
    locator: "Claude Code session 2026-11-09 (Issue #106 session), user answer to card I106-C1 (one-time acceptance of the reviewer write channel, option a: the account jeffery777 and the repository jeffery777/claude-dev-skills only; D-032)"
    quote: "C1 a，C2 b"
  - type: chat
    locator: "Claude Code session 2026-11-09 (Issue #106 session), user answer to cards I106-C4 (accept the residual risk of the reviewer write channel on the user's own machine, version 1) and I106-C5 (the decision for a setup change is the user's own message in the dispatching session)"
    quote: "C4 a，C5 b"
  - type: doc
    locator: "GitHub Issue #106, section Scope change (2026-11-09): the user's decision relayed by the orchestrator session"
    quote: "同意，照你的建議改走第2條"
non_goals:
  - Modifying engineering-workflow-core, codex-dev-skills or grok-build-dev-skills
depends_on: []
refines: [REQ-001]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Vendor and pin Core; dev-core is a compact execution digest with a source map, a coverage check and recorded deltas.

## Acceptance

- scripts/verify_core.py matches every file and set digest.
- scripts/check_core_coverage.py fails when any Core anchor is unmapped.

## Notes

Related: [[REQ-003]]

Issue #106 PR-1 (D-032, DL-004): Core v0.5.0 `review-required-read-only` is applied by tag before the vendor bump; the reviewer agents count only under the user's one-time acceptance record on the user's own machine (`skills/dev-core/references/reviewer-acceptance.md`). C4 (a) supersedes C1 (a); C5 (b) says where the C3 (a) decision for a setup change is given.
