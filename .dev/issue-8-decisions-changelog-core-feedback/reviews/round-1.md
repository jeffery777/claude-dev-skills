# Review round 1 — issue-8-decisions-changelog-core-feedback (PR-C1)

- Target: working tree at ae312c96fb08a57a36cfe85c76b12c56968b5138 (+ uncommitted, intent-to-add, 17 status entries)
- Diff identity: sha256 of `git diff HEAD --binary` = 83f23bb4e3de088ee22d3694eea8b25d9cff15a2c8b1c142ae16bca91878617c (both reviewers matched it before and after)
- Reviewers: `dev-skills:dev-reviewer` deep (B1-*), `dev-skills:dev-security-reviewer` Security Diff Scan (S1-*); requested model opus; effective: unknown
- Scope: all 17 changed paths. Requirements: REQ-002 (D-009), REQ-015 to REQ-019. DoD: their Acceptance lists and graph nodes T1 to T5
- Thresholds: `dev-core` R-REV-3 (strict)
- Result: 1 MUST-FIX, 2 SHOULD-FIX, 3 NIT, 1 SCOPE-CREEP, 2 REQ-GAP (one rejected)
- Writing: written per ASD-STE100 principles; full conformance not verified

## Findings and dispositions

Each finding was classified before any fix (R-REV-4).

| ID | Relation | Severity | Finding | Class | New mechanism | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| B1-001 | in-scope (REQ-002) | MUST-FIX | Section 5.2 had no done criteria for G3, although D-009 asks for the deliverables and done criteria of each stage; the new bullet postponed them without the user | necessary fix | no | Fixed: provisional G3 done criteria in the 5.2 table (zh, EN), marked to be revised before G3 starts (D-009); the postponing sentence removed |
| B1-002 | gap (REQ-017 vs REQ-012 item 6) | REQ-GAP | Once a PR exists, the automatic checkpoint commit makes a new head that needs a new complete review, the loop that D-013 item 6 removed; no requirement says how D-012 behaves on a PR branch | needs human decision | no | Decided: the user chose (a) and added that the checkpoint's key points are posted as a PR comment after the R-REV-9 scan (REQ-017 sources). Applied in `dev-continue` and D-012 (zh, EN) |
| B1-003 | in-scope (REQ-017) | SHOULD-FIX | Nothing called the handoff evaluation when a work item completes: the `dev-deliver` loop routed to `dev-continue` only for resuming, and its description did not name work-item completion | necessary fix | no | Fixed: `dev-deliver` loop step 6 runs the `dev-continue` handoff evaluation when a node, round or stage completes; the `dev-continue` description names it |
| B1-004 | in-scope (REQ-016, REQ-019) | NIT | CF-007 and FU-005 said every subagent reads all of `dev-core`; no agent file or brief requires it | necessary fix (false documentation) | no | Fixed: "every dev-* skill reads all of it; agent files and briefs do not require it" (zh, EN, FU-005) |
| B1-005 | in-scope (REQ-019) | NIT | CF-001 said PR #2 Merge Reviews 1 to 7 kept producing new findings; MR6 and MR7 had none | necessary fix (false documentation) | no | Fixed in CF-001 (zh, EN). The same pre-existing wording in D-013 and DL-012 is not part of this change; it goes to PR-C2 |
| B1-006 | in-scope (REQ-015) | NIT | D-010 cited Core `auth-data` for the instruction-order rule, which is in `auth-scope` (and "session memory is advisory" is in `wf-stages`) | necessary fix (false documentation) | no | Fixed: D-010 (zh, EN) and the core-feedback table cite `auth-scope`, `wf-stages` and `auth-data` |
| B1-007 | no-requirement | SCOPE-CREEP | "The first tagged release waits for the D-011 measurements" has no user source; the user's question on release was answered by an assistant recommendation | necessary fix (remove) | no | Fixed: removed from CHANGELOG, D-011 (zh, EN), REQ-018 and the FU-004 trigger; FU-001 stays the release blocker (its existing promotion trigger) |
| S1-001 | in-scope (REQ-017, REQ-012 item 6) | SHOULD-FIX | The checkpoint (with "Open findings and dispositions") could put review content on the PR branch | necessary fix | no | Fixed: once a PR exists, the checkpoint points to the review and gate records and never contains them (R-EXH-3), in `dev-continue` and D-012 (zh, EN). The new-head part is B1-002 |
| S1-002 | in-scope (REQ-017) | REQ-GAP raised | When "after the handoff" starts, and what happens on a decline, was unclear | keep as is (requirement covers it) + wording | no | Rejected as REQ-GAP: the user's D-012 words set the moment (「由使用者按下確認；原 session 交接後就停止寫入」); before the confirmation no handoff has happened. Wording clarified: D-012 (zh, EN) and `dev-continue` say the handoff is complete at the confirmation, and before it or on a decline the session continues; only `dev-continue` adds the path without a native handoff and "save the checkpoint again before the next offer" |

## Decision card 1

### Decision card 1: 有 PR 時的 checkpoint commit

- **問題：** PR 建立後，D-012 的自動 checkpoint commit 要不要 commit 到 PR 分支？
- **為什麼需要你決定：** 你的兩個決定在這裡衝突。D-012 說「自動寫好 checkpoint 並 commit」。D-013 第 6 項說審查紀錄的保存方式不能產生新的 head。checkpoint 不是審查紀錄，但 commit 到 PR 分支一樣會產生新的 head，新的 head 需要一次新的完整 Merge Review。需求沒有寫這種情況，agent 不能自己選（REQ-GAP）。
- **選項：**
  - **(a) PR 建立後，checkpoint 不 commit**
    - 做什麼：PR 建立後，checkpoint 只存在工作目錄，並放進交接說明；PR 建立前照常自動 commit。
    - 結果：交接不會產生新的 head，不會觸發新的完整審查。
    - 風險：新 session 必須在同一個資料夾，或靠交接說明取得 checkpoint；換到另一個 clone 時看不到檔案。
    - 成本：`dev-continue` 和 D-012 各加一句；REQ-017 記錄你的回答。
  - **(b) 照常 commit，接受新的 head**
    - 做什麼：維持現在的文字。
    - 結果：每次在 PR 上交接，都要再跑一次完整 Merge Review。
    - 風險：可能回到 D-013 想消除的循環。
    - 成本：每次交接多一輪完整審查。
  - **(c) 延後**
    - 做什麼：記成 follow-up，之後再決定。
    - 結果：現在的文字（b）暫時有效。
    - 風險：同 (b)。
    - 成本：低。
- **建議：** (a)。理由：它保留 D-012 在 PR 前的自動 commit，也守住 D-013 第 6 項「不產生新的 head」的目的。
- **不決定的後果：** PR-C1 的 commit gate 會擋住（開放中的 Needs Human Decision）。其他修正與準備可以繼續。
- **證據：**
  - 事實：`skills/dev-continue/SKILL.md` 的「Evaluate a handoff」第 2 項；REQ-012 第 6 項的原話「審查紀錄的保存方式不能產生新的 head」；REQ-017 的 D-012 原話；B1-002 與 S1-001（本檔）。
  - 推論：交接多半發生在一輪 review 結束時，也就是 PR 已經存在的時候，所以 (b) 的成本會經常出現。

## Requirement trace

| REQ | Covered by | Verified by |
| --- | --- | --- |
| REQ-002 | Section 5.2 D-009 rules and the provisional G3 criteria (zh, EN); D-009 | Deep review round 1; B1-001 fix pending confirmation |
| REQ-015 | D-010 (zh, EN); section 6 | Deep review round 1; B1-006 fix pending confirmation |
| REQ-016 | Principle 1; D-011 plan; FU-004, FU-005; CF-007 | Deep review round 1; B1-004, B1-007 fixes pending confirmation |
| REQ-017 | `dev-continue` "Evaluate a handoff"; `dev-deliver` loop step 6; D-012 (zh, EN) | Deep review and security scan round 1; B1-002 open (card 1) |
| REQ-018 | `CHANGELOG.md` | Deep review round 1 (pin matches the vendor lock) |
| REQ-019 | Core-feedback notes D-009 to D-016; `docs/core-feedback.md`; deltas Evidence | Deep review round 1; B1-005 fix pending confirmation |

## Security scan

Applicable: yes (agent authority wording in `dev-continue`, persistent state files, the Core pin in the changelog). Status: findings S1-001 and S1-002 (above). No secrets, private paths, hostnames, private emails or real names in the 17 paths. This is not the R-REV-9 pre-commit scan.

## Verification evidence

`bash scripts/validate.sh`: all checks passed before and after the fixes (core vendor, coverage 21 anchors and 41 rules, pack structure, 78 tests, plugin manifests). `graph.py validate` passed after the owned paths of T2 (README) and T3 (`dev-deliver`) were re-planned for the fixes.

## Residual risk and limits

- The `dev-continue` list of commit rules names R-REV-9 and `commit_state`, not the `dev-gate` commit gate; "Every commit rule still applies" covers it.
- `dev-continue` does not say which state files the checkpoint commit stages; the R-REV-9 "nothing unintended is staged" check covers it.
- D-012 does not record its tension with Core "prefer the original session" (`wf-stages`); the user's confirmation resolves it.
- CF-003 cites `pr-2-checkpoint.md` decision 3, which is the question; the user's answer is recorded in DL-009.
- D-011 item 4 (runtime check of agent tools) rests on the follow-up list agreed on 2026-10-20 in project notes; the reviewer could not verify the user's agreement.
- The per-stage layer mapping in 5.2 and the provisional G3 criteria are the agent's elaboration, labelled as revisable before each stage.
- `CHANGELOG.md` uses a "### Upstream" heading that Keep a Changelog does not define.
- REQ-016 and REQ-019 quote user questions and a remark, with UTC times; this follows the verbatim-source convention.
- The reviewers could not read the session transcripts; the main agent extracted all quotes by script.
- GitHub visibility of codex-dev-skills and grok-build-dev-skills was not checked over the network; both are already linked from the public README.

## Narrow confirmation C1 (before the commit)

- Candidate: `git diff HEAD --binary` sha256 20ded0e2bfcb33644289a06d197231f0538380c2ea316f5674f316804dca8350 (19 status entries; both reviewers matched it before and after)
- Reviewers: `dev-skills:dev-reviewer` narrow confirmation (C1-*), `dev-skills:dev-security-reviewer` confirmation of S1-001, S1-002 and the decision card 1 change (C1S-*)
- B1-001 to B1-007, S1-001, S1-002 and the card 1 answer: CONFIRMED. `bash scripts/validate.sh`: all checks passed. No secrets or private identifiers in the diff.

| ID | Relation | Severity | Finding | Class | New mechanism | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| C1S-001 | in-scope (REQ-017) | NIT | D-012 item 4 did not say that the PR comment authority covers only this comment, or that no scan means no post; `dev-continue` says both | necessary fix (parity caused by this change) | no | Fixed: D-012 item 4 (zh, EN) states both |
| C1S-002 | in-scope (REQ-017) | NIT | The S1-002 disposition said D-012 also got the "save again" clause; only `dev-continue` has it | necessary fix (false record) | no | Fixed: the S1-002 disposition now says which text is in which file |

Residual risk (below the thresholds): each declined offer on a PR branch can post another scanned comment, with no limit on their number; after a PR exists, another clone sees only what the PR comments contain; an uncommitted post-PR checkpoint can be staged into a later work commit when `commit_state` is `true`; the checkpoint template line "Open findings and dispositions" holds pointers only on a PR branch, by instruction; whether the pre-PR checkpoint commit passes the `dev-gate` commit gate is covered only by "every commit rule still applies"; the MR6 and MR7 results were not re-read by the C1 reviewer.

The C1S fixes make a new candidate. Its R-REV-9 pre-commit scan (which also confirms C1S-001 and C1S-002) is recorded outside this commit (R-REV-9).
