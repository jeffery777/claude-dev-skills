---
id: REQ-008
title: Per-project requirements wiki with precise sources, templates and ingest
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 4 (Phase 1 supplement)"
    quote: "需求 wiki 是各目標專案自己的 docs/requirements/，不另建專案。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 4 (Phase 1 supplement)"
    quote: "dev-plan 要做 ingest：把使用者原話寫成 REQ 檔（source 欄位保留原話），task 的 requirements 必須指向實際存在的 REQ。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 4 (Phase 1 supplement)"
    quote: "lint 腳本仍留到 Phase 2。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 5 (D-003 supplement)"
    quote: "REQ frontmatter 的 sources 是一個清單，每筆包含 type（doc/chat/issue/commit）、locator（檔名加頁碼或章節錨點、日期、URL、SHA）、quote（逐字原文）。模型整理的敘述與原文分開存放。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 5 (D-003 supplement)"
    quote: "來源互相矛盾時保留雙方說法並附出處，status 設為 conflict，由使用者決定；不得自行挑選或覆寫。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 5 (D-003 supplement)"
    quote: "被取代的結論不刪除：status 改為 superseded 並寫 superseded_by 與理由；每次變更記入 log.md。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 5 (D-003 supplement)"
    quote: "若專案已有正式需求系統（Jira、Confluence、PRD），wiki 只做索引並連回原處；第一次建立前先徵求同意，路徑可設定；機密原文不得離開該專案。"
non_goals:
  - A separate requirements project
  - A lint script in Phase 1
depends_on: []
refines: [REQ-003, REQ-004]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Each target project keeps its own requirements wiki. dev-plan ingests the originals verbatim with precise locators, keeps conflicts side by side for the user to decide, never deletes superseded requirements, and links to formal systems instead of copying confidential text.

## Acceptance

- skills/dev-plan/templates/ has REQ, index and log templates; the REQ template has sources[type, locator, quote].
- graph.py validate fails when a cited REQ has no matching file, or when an open write task cites a REQ in conflict.
- dev-plan asks before creating the wiki and honors requirements_dir in .dev/config.json.

## Notes

Related: [[REQ-003]], [[REQ-004]]
