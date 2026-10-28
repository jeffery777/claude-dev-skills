---
id: REQ-003
title: Proportionate rigor; no over-engineering
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the graph-engineering question)"
    quote: "我發現Codex在開發時，有時會過度工程化，忽略了原始的專案需求，變成了通用需求"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the graph-engineering question)"
    quote: "我不是說嚴謹不好，而是要適度地嚴謹。"
  - type: issue
    locator: "GitHub Issue #75 body, Change 5 (rigor at Discover; Issue #73 was planned as standard although R-RIG-1 makes public-contract work strict)"
    quote: "Add a check where the orchestrating agent writes an Issue's process line: work that changes a security rule, a public contract, packaging or a release is `strict`, and its design is reviewed independently before implementation."
  - type: chat
    locator: "Claude Code session 2026-10-28 (orchestrator relay), user answer to the Issue #75 design cards I75-D1 to I75-D6 (D2 (a): R-RIG-1 strict adds packaging, and every change to the rule text of a skill pack in a public repository is public-contract work; D4 (b): the pack re-assesses the tier at Discover (R-RIG-2), and the line in the user's own instructions is outside this repository)"
    quote: "D1 a，D2 a，D3 a，D4 b（全域那一行由你加），D5 a，D6 b"
  - type: chat
    locator: "Claude Code session 2026-10-28 (orchestrator relay), user answer to the Issue #75 review round-1 cards I75-R1-C1 to I75-R1-C3 (R1-C3 (b): R-RIG-2 adds that a relayed decision to lower a tier written before Discover counts only after the user confirms it in this session)"
    quote: "R1-C1 a，R1-C2 b，R1-C3 b"
non_goals:
  - Weakening Core obligations to reduce ceremony
depends_on: []
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Rigor scales with risk, and every change traces back to the user's original requirement so the work does not drift into generic requirements.

## Acceptance

- Work is classified into light, standard and strict tiers with a recorded reason.
- Additions without a requirement are reported as SCOPE-CREEP findings.
- Issue #75 item 5 (D-023, DL-039; cards I75-D2 (a) and I75-D4 (b)): R-RIG-1 `strict` names security work (a change to a security rule included), data, migration, public contract, packaging or release; every change to the rule text of a skill pack in a public repository is public-contract work; `strict` asks for an early deep and security review of the design before implementation and an early deep code review as soon as code exists. R-RIG-2: a tier written before Discover, for example in an Issue or a brief, is a proposal; Discover re-assesses it with R-RIG-1 and the plan records the result; the re-assessment may raise the tier, and it lowers such a tier only with the user's decision, with the reason in the plan; a relayed decision to lower it counts only after the user confirms it in this session (card I75-R1-C3 (b)). `dev-plan` step 3 cites R-RIG-2; README and D-004 (both languages) agree.

## Notes

Related: [[REQ-007]], [[REQ-008]]
