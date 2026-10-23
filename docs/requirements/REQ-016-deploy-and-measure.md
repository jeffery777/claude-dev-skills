---
id: REQ-016
title: Deploy the pack and measure it on real tasks
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), opening line"
    quote: "請先重讀 docs/design-proposal.md，再新增以下決策："
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), D-011"
    quote: "D-011 部署與量測：Phase 1 合併後，先以 user scope 安裝到 Claude Code，只在個人專案使用；Cowork 等 FU-001 驗證後再說。挑 3 到 5 個真實任務，在有裝技能包與沒裝技能包的情況下各跑一次，記錄漏掉的錯誤、不在需求內的改動、token 用量與耗時，依結果決定加強或刪減。在 ~/.claude/CLAUDE.md 加一段簡短指引：開發任務先用 dev-deliver 判斷等級。"
  - type: chat
    locator: "Claude Code side session 2026-10-20 (question on the context cost of Core), user message at 08:41 UTC"
    quote: '主對話說"Core 全文的 context 成本很高"是什麼意思？全文載入的context成本很高嗎？但codex說是要設計成按需載入，需要時再讀取'
  - type: chat
    locator: "Claude Code side session 2026-10-20 (question on the context cost of Core), user message at 08:44 UTC (approval to record the unverified context-cost claim, the token comparison and the dev-core split evaluation; the proposal itself was the assistant's)"
    quote: "可以"
  - type: chat
    locator: "Claude Code side session 2026-10-20 (question on the context cost of Core), user message at 08:54 UTC"
    quote: "我懂了，因為工具特性不同。同樣一份core，codex按需載入。但在claude這邊的做法可能不同，但仍有機會可以達成類似的效果。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:37 UTC (the user let the assistant choose between fixing the other risks now or recording them as follow-ups; at 07:49 UTC the assistant scheduled the runtime check of plugin agent tools with the D-011 deployment; it is item 4 of the D-011 measurement plan; the choice was the assistant's)"
    quote: "其它的風險，你可以選擇現在修？或記入follow up後續再安排修、一併測。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
  - type: chat
    locator: "Claude Code session 2026-10-21 (PR-C, Issue #8), user answer to the dev-plan decision cards (card 1 split PR-C into C1 and C2: (a) split; card 2 keep each rule in one place: (b) defer; card 3 open the Issue: (a) yes)"
    quote: "1a、2b、3a"
  - type: chat
    locator: "Claude Code session 2026-10-23 (orchestrator session, relayed to the FU-004 records session, Issue #27), user answer to decision card R1-004 (REQ-GAP from review round 1 of Issue #27: a replay of the baseline tasks after FU-005 PR-4 does not restore the GitHub and remote state; option a, one factual sentence in the Limits of `.dev/issue-27-fu004-baseline/report.md`, no rule; how to rerun is decided later by a separate card)"
    quote: "同意你的建議，選a"
non_goals:
  - Installing the pack, editing `~/.claude/CLAUDE.md` or running the measurements inside this repository change (they are deployment steps outside the repository)
  - Cowork use before FU-001 (GitHub Issue #3) is verified
  - Implementing a split of `dev-core` without a user decision
depends_on: []
refines: [REQ-001]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

After Phase 1, the user installs the pack at user scope in Claude Code for personal
projects only. Cowork waits for FU-001. Three to five real tasks run once with
and once without the pack. Each run records missed errors, changes outside the
requirements, token use and time; the results decide what to strengthen or
trim. A short note in `~/.claude/CLAUDE.md` says that development tasks start
with `dev-deliver` to choose the tier. The design text must not claim a context
cost that nothing measured; the measurement compares the token use of the same
task in claude-dev-skills and codex-dev-skills.

## Acceptance

- `docs/design-proposal.md` records D-011 in zh and EN with a Core-feedback note and a measurement plan: the tasks, the with/without runs, the four measures, and a token comparison of the same task in claude-dev-skills and codex-dev-skills that counts the reads of `dev-core`.
- Design principle 1 (zh and EN) no longer states the unmeasured context-cost claim as a fact.
- The install, the `~/.claude/CLAUDE.md` note and the runs are documented as deployment steps with an owner in `.dev/followups.md`; they are not performed in the repository change.
- An evaluation of splitting `dev-core` into a short always-read core plus on-demand per-stage references is recorded in `docs/core-feedback.md`; it changes no skill.

## Notes

The context-cost claim and the split evaluation come from the 08:41 question and
the assistant's answer, which the user approved for recording (08:44). Related:
[[REQ-001]], [[REQ-003]], [[REQ-019]].
