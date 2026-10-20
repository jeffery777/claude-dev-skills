---
id: REQ-004
title: Code impact graph plus requirement lookup, usable by Claude, Codex and Grok Build
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the graph-engineering question)"
    quote: "以後無論是你、codex甚至grok build在開發時除了從gitnexus上可查到程式碼修改的影響範圍之外，也可以在graphify同步查閱原始的需求，避免codex過度工程化的問題。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the graph-engineering question)"
    quote: "如果你認為LLM Wiki更可行且單純，那也可以。只是要考量後續也要能讓codex和grok build調用"
non_goals:
  - Installing or reconfiguring GitNexus from this pack
  - Making Graphify mandatory
depends_on: []
refines: [REQ-002]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Use the installed GitNexus for code impact, and keep the original requirements in a form all three agents can read.

## Acceptance

- Skills query GitNexus read-only and label its results advisory.
- Requirements are plain Markdown in Git, readable without extra tools.

## Notes

Related: [[REQ-002]], [[REQ-008]]
