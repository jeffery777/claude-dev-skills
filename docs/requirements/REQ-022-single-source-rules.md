---
id: REQ-022
title: Each rule in one place - skills cite dev-core rule IDs (FU-006)
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-21 (PR-C, Issue #8), user answer to the dev-plan decision cards (card 1 split PR-C into C1 and C2: (a) split; card 2 keep each rule in one place: (b) defer; card 3 open the Issue: (a) yes)"
    quote: "1a、2b、3a"
  - type: chat
    locator: "Claude Code session 2026-10-21 (orchestrator session), user decision on the order of work after FU-009"
    quote: "FU-009 合併後 FU-006 優先處理"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-006 session, Issue #16), user answer to inventory decision cards 1 to 5 and the REQ-022 acceptance"
    quote: "1a、2a、3a、4b（通用測試也要檢查 CB-1 到 CB-5）、5a。REQ-022 的驗收條件同意。"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-006 session, Issue #16), user answer to decision card 6 (method after the R-VER-2 stop rule in review round 2)"
    quote: "6a，FU-006 合併後 FU-010 列為下一項並做完整盤點"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-006 session, Issue #16), user answer to decision card 7 (scope after review round 3)"
    quote: "7a。第 4 輪請加一項檢查：這三條規則的引用只能出現在主 session 技能讀取的檔案，不可出現在交給 reviewer subagent 的參考文件（如 review-report.md、task-brief.md）。另外把「規則文字不改寫、只有單一規則的副本才換成引用、給 subagent 的文件保留全文」這個心得記入 CF-008。"
non_goals:
  - Splitting dev-core into a short core and per-stage references (FU-005, waits for FU-004)
  - Adding, relaxing, removing or rewording any rule in meaning
  - Removing the rule copies in the agent files (card 1a; they do not load dev-core)
  - README and docs wording
  - Changes to engineering-workflow-core, codex-dev-skills or grok-build-dev-skills
depends_on: []
refines: [REQ-019]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

A rule restated in several skills is easy to miss when the rule changes. This
caused findings in PR #7 (C1-001, MR-B-002, MR2-B-001), PR #13 (MR-001) and
PR #15 (R2-001, MR15-001, F-001). Each rule is written once in `dev-core`; the
other skills and their references cite the stable rule ID, never a file path,
line or section number, so that a later split of `dev-core` (FU-005) keeps
every citation valid. Operational steps (commands, order) stay in the skills.
After three review rounds found blockers caused by rewording, the user
narrowed the change (card 7a): only the copies of the three rules that were
actually missed become citations; other rule text is not reworded and names
its rule IDs, and files given to a subagent keep the full text.

## Acceptance

- The restated copies of R-EXH-3 (record storage), R-VER-2 (stop rule) and
  R-EXH-4 (platform result) in the main-session skills are replaced by
  citations of the rule ID (card 7a). Every other restated rule text stays
  word for word as on main and names its rule IDs; no rule changes in
  meaning.
- Citations of these three rules appear only in files that main-session
  skills read, never in references given to a reviewer subagent (for
  example `review-report.md`, `task-brief.md`) or in the agent files
  (card 7a).
- The masking rule for review and gate records is in `dev-core` R-REV-8 and
  recorded in `deltas.md` (card 2a); `dev-review` and its references keep
  their text and cite R-REV-8.
- The `dev-core` section 8 bindings carry the IDs CB-1 to CB-5, and no file
  cites `dev-core` by section number (card 3a).
- The agent files keep their copies (card 1a); FU-005 records them.
- Tests (card 4b): the GateRuleText sentences exist once, in `dev-core`
  R-EXH-4, and `dev-gate` and `platform-profile.md` cite R-EXH-4; a general
  test fails when a rule ID (`R-…` or `CB-…`) cited in `skills/` or `agents/`
  does not exist in `dev-core`, and when a file cites `dev-core` by section
  number.
- The FU-006 row and CF-008 cite the user's decision to do FU-006 now; CF-008
  records the lesson of card 7a.

## Notes

Related: [[REQ-016]] (FU-004 measurements), [[REQ-019]] (CF-008).
