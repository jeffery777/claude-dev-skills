---
id: REQ-005
title: Language - English skills and agents, bilingual human docs
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the language question)"
    quote: "skill.md、agent用英文。README.md和設計文件原則上希望雙語（由於技能的設計主要是希望由agent視需求自行調用，但又保留了人可以自行視需求調用計）所以才需要雙語，方便中、英語系的人閱讀。"
non_goals: []
depends_on: []
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Agent-facing files are English; README and design documents are bilingual (Traditional Chinese and English).

## Acceptance

- Every SKILL.md and agent file is English.
- README.md and the design document have zh-TW and English versions with the same obligations.
