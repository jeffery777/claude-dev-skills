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
