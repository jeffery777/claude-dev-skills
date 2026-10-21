---
id: REQ-002
title: Graph engineering, delivered in phases
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 1 (initial request)"
    quote: "讓你參考的技能最終我希望能做到graph engineering（可以分階段實施）"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), opening line"
    quote: "請先重讀 docs/design-proposal.md，再新增以下決策："
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), D-009"
    quote: "D-009 Graph engineering 分階段完成：G1、G2、G3 各自是一輪獨立交付（Issue → 分支 → review/scan → PR → Merge Review），前一階段合併後才開始下一階段。每階段開工前，先依前一階段的實際使用結果修正設計。第 5.2 節補上各階段的交付物與完成判準。graph／REQ 的 schema、graph.py、fixtures 列為 runtime 中立層，不得依賴 Claude 專用工具；Agent／Workflow 執行方式列為 Claude 專用層，供日後 Codex／Grok 參考或提回 Core。"
non_goals:
  - A self-written graph execution engine or graph database in Phase 1
depends_on: []
refines: [REQ-001]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

The pack grows toward graph engineering (execution, knowledge and governance graphs) in phases; Phase 1 delivers the task graph (G0).

## Acceptance

- The design document defines the phases and their acceptance.
- Phase 1 ships a validated task graph tool.
- `docs/design-proposal.md` records D-009 in zh and EN with a Core-feedback note: G1, G2 and G3 are
  each one independent delivery (Issue, branch, review and scan, PR, Merge Review); the next stage
  starts only after the previous one merges, and its design is revised first from real use of the
  previous stage; section 5.2 gives each stage its deliverables and done criteria; the graph and REQ
  schema, `graph.py` and the fixtures are a runtime-neutral layer, and Agent and Workflow execution is a
  Claude-specific layer.

## Notes

D-009 added the stage rules (PR-C1, Issue #8). Related: [[REQ-004]], [[REQ-010]], [[REQ-019]].
