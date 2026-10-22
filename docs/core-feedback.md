# Core 回饋紀錄

[繁體中文](#zh-tw) · [English](#english)

<a id="zh-tw"></a>

狀態：草稿（2026-10-21）。英文版在文末，與中文版同義；兩者不一致時以中文版為準。

## 用途

`engineering-workflow-core`（以下簡稱 Core）是 codex-dev-skills、grok-build-dev-skills 與 claude-dev-skills 共用的核心流程。本專案的修改如果是 Core 層級的問題，就記在這裡，讓 Core 可以採用，另外兩個專案再自行重新 pin（REQ-019）。

- 流程依 `docs/design-proposal.md` 的 D-001：增量型提案優先，也就是在 Core 新增非權威的伴讀文件，權威原文不動。修改型提案要先讓 codex-dev-skills 與 grok-build-dev-skills 各自 pin 候選版本並跑過 evals。
- 本文件只是紀錄。本專案不修改 Core、codex-dev-skills 或 grok-build-dev-skills。到 Core 開 Issue 需要使用者另外授權。
- 依據的 Core 版本：v0.1.1（commit `7b66978a76597d09be1b55ad199a969b4ee59c0f`）。
- 每個項目的狀態都是「未提出」。

## 項目

### CF-001 Review 收斂：嚴重度門檻、停止規則、紀錄不產生新 head

- 來源決策：D-013（REQ-012）；delta DL-011、DL-012、DL-013。
- 問題：Core 沒有定義嚴重度門檻。Core 把連續兩輪未完成的 review 當成重新評估的時機，不是停止。Core 也沒有規定 PR 建立後 review 紀錄要存在哪裡；紀錄 commit 到 PR 分支會產生新的 head，新的 head 又需要完整審查，形成循環。
- 證據：
  - PR #2 的 Merge Review 1 到 5 一直出現新的 finding；Merge Review 6 與 7 沒有 finding。`merge-review-1.md` 到 `merge-review-4.md` 隨修正一起 commit（c72c64d、c934a29、eb8e08a、2280228），每次都產生新的 head（`.dev/handoff/pr-2-checkpoint.md`）。
  - PR-A（PR #5）第 2 輪後的重新評估移除了沒有需求對應的檢查（`.dev/issue-4-commit-security/reviews/round-2.md`）。
  - PR-B（PR #7）的 Merge Review 連續兩次被擋（MR-B-001 與 MR-B-002，接著是 MR2-B-001）。停止規則因此觸發，使用者用決策卡片 2 決定修正（PR #7 的 comment）。
- 提議的 Core 修改：在 `review-and-security.md#review-findings` 加上嚴重度門檻；在 `workflow.md#wf-verification` 加上停止規則；在 `exact-head-and-evidence.md#exact-transition` 規定 PR 建立後的紀錄不 commit 到 PR 分支。
- 類型：修改型（停止規則與紀錄位置會改變義務）。可以先用增量型伴讀文件試行。
- 對其他專案的影響：codex-dev-skills 與 grok-build-dev-skills 採用後，review 輪數可能減少；兩者都要檢查自己的 gate 與紀錄流程。在它們重新 pin 之前沒有影響。

### CF-002 每次 commit 與 push 前的安全審查，包含 commit 中繼資料

- 來源決策：D-015（REQ-011）；delta DL-010。
- 問題：Core 只在變更碰到信任邊界時要求 Security Diff Scan。在公開 repo 中，每次 commit 與 push 都會公開內容，也會公開作者、committer 與訊息。
- 證據：PR #2 的 SEC-01。分支上 10 個 commit 的作者與 committer 由本機帳號與主機名稱推導出來，push 後已經公開；內容審查沒有檢查中繼資料（`.dev/issue-1-phase1/reviews/security-review-merge.md`）。
- 提議的 Core 修改：在 `review-and-security.md#review-security` 規定公開 repo 的每次 commit、push，以及 PR 與 Issue 文字都要掃描，範圍包含身分、訊息與 trailer。
- 類型：修改型（新增義務）。
- 對其他專案的影響：Codex 與 Grok 的 commit 與 push 步驟要加上這項掃描。

### CF-003 有寫入工具的替代者不能當獨立 reviewer

- 來源決策：PR #2 交接的決定 3（D-008 的 Phase 1 範圍內）；delta DL-009、DL-004。
- 問題：brief 無法拿掉 subagent 的工具。有 Edit 或 Write 工具的替代 agent 不能證明它沒有改動受審內容。為了偵測改動而自製的機制（`tree_fingerprint.py`）一直擴大。
- 證據：PR #2 第 1 輪的 SR-006（`.dev/issue-1-phase1/reviews/round-1.md`）；`tree_fingerprint.py` 在第 2 輪加入後累積了 15 項以上的 finding，之後依使用者決定移除（`.dev/handoff/pr-2-checkpoint.md` 決定 3）。PR #2 的 SEC-02：reviewer 的說明寫「不能編輯檔案」，但它們保留 Bash（`security-review-merge.md`）。
- 提議的 Core 修改：在 `review-and-security.md#review-independent` 寫明：必要的 review 不使用有寫入工具的替代者；找不到唯讀 reviewer 時停在 gate。
- 類型：修改型（收緊）。
- 對其他專案的影響：Codex 版的 reviewer 只靠宣告維持唯讀（`docs/design-proposal.md` 原則 3）；採用後，它要說明在沒有唯讀 reviewer 時怎麼停下。

### CF-004 每個 finding 標明和需求的關係（`requirement_relation`、`REQ-GAP`）

- 來源決策：D-016（REQ-014）；delta DL-011。
- 問題：Core 沒有把 finding 和需求連起來，所以需求範圍內的修正和範圍擴張分不開。
- 證據：PR-A 第 2 輪後的重新評估；需求缺口變成決策卡片 1（`round-2.md`）。PR-B 的 B1-004 先被歸為 `SCOPE-CREEP`，再由使用者用決策卡片 1 加成需求（`.dev/issue-6-review-convergence/reviews/round-1.md`）。D-003 記錄 Codex 曾把專案需求改寫成通用需求。
- 提議的 Core 修改：在 `review-and-security.md#review-findings` 加上 `requirement_relation` 欄位與 `REQ-GAP` 類別；Core 的阻擋項不論關係都照樣阻擋。
- 類型：修改型（finding 格式改變）。
- 對其他專案的影響：Codex 與 Grok 的 review 報告格式要多一個欄位；它們需要有需求來源才能填寫。

### CF-005 決策卡片

- 來源決策：D-014（REQ-013）；delta DL-014。
- 問題：Core 列出提出決策時要寫的內容，但沒有固定格式；交給使用者的決策每次格式都不同。
- 證據：PR-A 的決策卡片 1，使用者用一行回答（「Card1，我選a」；REQ-011 的 sources）。PR-C 的三張卡片也用一行回答（「1a、2b、3a」）。
- 提議的 Core 修改：在 `workflow.md#wf-writing` 與 `authorization-and-stops.md#auth-stops` 附上卡片範本。
- 類型：增量型（範本放在伴讀文件，權威原文不動）。
- 對其他專案的影響：可以不採用；採用時只改輸出格式。

### CF-006 新增機制要對應需求（防止機制擴張）

- 來源決策：D-003、D-013 第 3 項；delta DL-003。
- 問題：Core `wf-assumptions-and-options` 要求說明新增複雜度的獨特作用，但沒有要求對應到需求。
- 證據：`tree_fingerprint.py`（CF-003）；PR-A 的 `--evidence-file` 檢查在第 1、2 輪連續需要修正並產生新問題，重新評估後移除（`round-2.md`）。
- 提議的 Core 修改：在 `workflow.md#wf-assumptions-and-options` 規定新增的機制要對應一條需求，否則列為範圍擴張。
- 類型：修改型（收緊）。
- 對其他專案的影響：Codex 與 Grok 需要有需求來源（例如 REQ wiki）才能檢查。

### CF-007 Context 載入方式：短核心加按需讀取的參考文件（評估）

- 來源：使用者 2026-10-20 對原則 1 的提問；D-011（REQ-016）。
- 問題：原則 1 曾說法條式重複是 Codex 版最大的 context 成本，但沒有量測。
- 事實（2026-10-21 量測檔案大小，不是 token 數）：
  - claude-dev-skills：`skills/dev-core/SKILL.md` 是 35,425 bytes。每個 dev-* 技能都先讀完整份；subagent 的 agent 檔與 brief 不要求讀它。其他 7 個技能的 SKILL.md 是 1.5 到 5.5 KB。
  - Core v0.1.1 的 4 份契約共 42,425 bytes。
  - codex-dev-skills（commit 9935975）：27 個技能的 SKILL.md 是 0.9 到 14 KB（中位數 3.3 KB）；`references/` 共約 199 KB，依操作需要才讀取。
  - grok-build-dev-skills（commit d68b7ad）：目前沒有技能。
- 推論：真正的成本可能是重複載入同一份長文，以及長文造成的注意力分散，而不是單次完整載入。這需要 D-011 的 token 比較來確認。
- 評估（拆分 `dev-core`）：
  - 做法：一份每次都讀的短核心（停止條件、授權、阻擋規則），加上依階段讀取的參考文件（plan、review、gate、交付）。
  - 好處：每次讀取的內容變少；Claude 與 Codex 的載入方式一致。
  - 風險：技能可能漏讀需要的參考文件；規則分散後更容易出現副本不一致（見 CF-008）。拆分會動到所有技能，review 成本高。
  - 結論：等 D-011 的量測結果。要不要實作，由使用者用決策卡片決定（FU-005）。
- 提議的 Core 修改：在 Core 新增一份載入方式的伴讀說明，讓三個接口用同一種載入模型。
- 類型：增量型。
- 對其他專案的影響：Codex 版已經按需讀取；採用後主要是對齊名稱與分段。

### CF-008 每條規則只寫在一個地方（本專案已實作）

- 來源：PR-C 的決策卡片 2，使用者選 (b) 延後（REQ-019 的 sources；FU-006）。
- 問題：同一條規則在多個技能裡重寫，改規則時容易漏改副本。
- 證據：PR-B 連續三輪都出現同一類漏改：C1-001（`round-1.md`）、MR-B-002 與 MR2-B-001（PR #7 的 comment）。後來 PR #13（MR-001）和 PR #15（R2-001、MR15-001、F-001）也出現同一類漏改。
- 提議的 Core 修改：在給接口作者的伴讀說明中，建議每條規則只在摘要中寫一次，其他地方只引用規則 ID。
- 類型：增量型。
- 對其他專案的影響：只影響各接口自己的技能結構。
- 狀態：使用者在 2026-10-21 決定先做，不再等 D-011 量測（「FU-009 合併後 FU-006 優先處理」）。本專案在 Issue #16 實作（REQ-022）：只有三條規則（R-EXH-3 紀錄存放、R-VER-2 停止規則、R-EXH-4 平台結果）的副本換成引用，其他規則文字逐字保留並加上規則 ID。agent 檔保留自己的副本，留給 CF-007（FU-005）處理。Core 的伴讀說明仍是「未提出」。
- 心得（使用者 2026-10-22，card 7a 原話）：「規則文字不改寫、只有單一規則的副本才換成引用、給 subagent 的文件保留全文」。理由（本專案的推論）：subagent 不讀 `dev-core`，例如 review-report.md、task-brief.md 與 agent 檔的讀者。證據：Issue #16 審查三輪都找到改寫造成的阻擋問題（FR1-001、FR1-002、FR1-005、FR2-001、FR3-001 到 FR3-004）：改寫掉了條件、執行者或讀者，或引用了錯的規則。

## 不回饋給 Core 的決策

| 決策 | 理由 |
| --- | --- |
| D-009 Graph engineering 分階段 | graph engineering 不在 Core 契約內；中立層成形後再評估 |
| D-010 不做 agent memory | Core `auth-scope`、`wf-stages` 與 `auth-data` 已涵蓋 |
| D-011 部署與量測 | Claude 端的工作；結果是本文件的證據 |
| D-012 自動交接 | 取決於各接口的 session 能力；Core `wf-stages` 已涵蓋 checkpoint 與接續 |

---

<a id="english"></a>

<details>
<summary>English</summary>

# Core feedback record

Status: draft (2026-10-21). This English version means the same as the
Traditional Chinese version. If the two differ, the Chinese version wins.
Written per ASD-STE100 principles; full conformance not verified.

## Purpose

`engineering-workflow-core` (Core) is the shared workflow of
codex-dev-skills, grok-build-dev-skills and claude-dev-skills. When a change
in this project is a Core-level issue, it is recorded here, so that Core can
adopt it and the other two projects can re-pin it themselves (REQ-019).

- The process is D-001 in `docs/design-proposal.md`. An additive proposal is
  preferred: a non-authoritative companion document in Core, with the
  authoritative text unchanged. A modifying proposal first needs a candidate
  pin and passing evals in codex-dev-skills and grok-build-dev-skills.
- This document is a record only. This project does not change Core,
  codex-dev-skills or grok-build-dev-skills. Opening an Issue in Core needs
  separate approval from the user.
- Core version: v0.1.1 (commit `7b66978a76597d09be1b55ad199a969b4ee59c0f`).
- The status of every item is "not proposed".

## Items

### CF-001 Review convergence: severity thresholds, stop rule, records without a new head

- Decision: D-013 (REQ-012); deltas DL-011, DL-012, DL-013.
- Problem: Core defines no severity thresholds. Core treats two unfinished
  review rounds as a time to re-assess, not to stop. Core does not say where
  review records go once a PR exists. A record committed to the PR branch
  makes a new head, and the new head needs a complete review: a loop.
- Evidence:
  - PR #2 Merge Reviews 1 to 5 kept producing new findings; Merge Reviews 6
    and 7 had none.
    `merge-review-1.md` to `merge-review-4.md` were committed with their
    fixes (c72c64d, c934a29, eb8e08a, 2280228), and each commit made a new
    head (`.dev/handoff/pr-2-checkpoint.md`).
  - The PR-A (PR #5) re-evaluation after round 2 removed checks that no
    requirement covered (`.dev/issue-4-commit-security/reviews/round-2.md`).
  - In PR-B (PR #7), two Merge Reviews in a row were blocked (MR-B-001 and
    MR-B-002, then MR2-B-001). The stop rule fired, and the user decided the
    fix with decision card 2 (PR #7 comments).
- Proposed Core change: severity thresholds in
  `review-and-security.md#review-findings`; the stop rule in
  `workflow.md#wf-verification`; in `exact-head-and-evidence.md#exact-transition`,
  records are never committed to the PR branch once a PR exists.
- Kind: modifying (the stop rule and the record location change
  obligations). An additive companion document can try it first.
- Impact on the other projects: after adoption, codex-dev-skills and
  grok-build-dev-skills may need fewer review rounds; both must check their
  gates and record handling. No effect before they re-pin.

### CF-002 Security review before every commit and push, including commit metadata

- Decision: D-015 (REQ-011); delta DL-010.
- Problem: Core requires a Security Diff Scan only when a change touches a
  trust boundary. In a public repository, every commit and push publishes the
  content and also the author, the committer and the message.
- Evidence: PR #2 SEC-01. The author and committer of all 10 branch commits
  were derived from the local account and the machine hostname, and the push
  published them. No content review checked the metadata
  (`.dev/issue-1-phase1/reviews/security-review-merge.md`).
- Proposed Core change: in `review-and-security.md#review-security`, scan
  every commit, push, and PR and Issue text of a public repository, including identity,
  message and trailers.
- Kind: modifying (a new obligation).
- Impact on the other projects: the commit and push steps of Codex and Grok
  add this scan.

### CF-003 A substitute with write tools is not an independent reviewer

- Decision: PR #2 handoff decision 3 (Phase 1 scope, D-008); deltas DL-009,
  DL-004.
- Problem: a brief cannot remove a subagent's tools. A substitute agent with
  Edit or Write tools cannot prove that it did not change what it reviewed.
  The self-made mechanism to detect such changes (`tree_fingerprint.py`) kept
  growing.
- Evidence: PR #2 round 1 SR-006 (`.dev/issue-1-phase1/reviews/round-1.md`);
  `tree_fingerprint.py` collected 15 or more findings after round 2 added
  it, and was then removed by user decision (`.dev/handoff/pr-2-checkpoint.md`,
  decision 3). PR #2 SEC-02: the reviewer descriptions said "Cannot edit
  files", but the reviewers keep Bash (`security-review-merge.md`).
- Proposed Core change: in `review-and-security.md#review-independent`, a
  required review never uses a substitute with write tools; without a
  read-only reviewer, the work stops at the gate.
- Kind: modifying (a tightening).
- Impact on the other projects: the Codex reviewer is read-only by
  declaration only (`docs/design-proposal.md`, principle 3); after adoption,
  Codex must state how it stops when no read-only reviewer is available.

### CF-004 Every finding states its relation to the requirements (`requirement_relation`, `REQ-GAP`)

- Decision: D-016 (REQ-014); delta DL-011.
- Problem: Core does not relate findings to requirements, so a fix inside
  the requirements cannot be told apart from a scope expansion.
- Evidence: the PR-A re-evaluation after round 2; the requirement gap became
  decision card 1 (`round-2.md`). PR-B finding B1-004 was first rated
  `SCOPE-CREEP`, and the user then added it as a requirement with decision
  card 1 (`.dev/issue-6-review-convergence/reviews/round-1.md`). D-003 records
  that Codex rewrote project requirements into generic ones.
- Proposed Core change: a `requirement_relation` field and a `REQ-GAP`
  category in `review-and-security.md#review-findings`; a Core blocker blocks
  for every relation.
- Kind: modifying (the finding format changes).
- Impact on the other projects: the review reports of Codex and Grok get one
  more field; they need a requirement source to fill it.

### CF-005 Decision card

- Decision: D-014 (REQ-013); delta DL-014.
- Problem: Core lists what a decision request contains, but gives no fixed
  format. The decisions handed to the user had a different format each time.
- Evidence: PR-A decision card 1; the user answered in one line ("Card1，我選a";
  REQ-011 sources). The three PR-C cards were also answered in one line
  ("1a、2b、3a").
- Proposed Core change: a card template for `workflow.md#wf-writing` and
  `authorization-and-stops.md#auth-stops`.
- Kind: additive (the template goes into a companion document; the
  authoritative text does not change).
- Impact on the other projects: optional; adoption changes only the output
  format.

### CF-006 A new mechanism traces to a requirement (against mechanism creep)

- Decision: D-003, D-013 item 3; delta DL-003.
- Problem: Core `wf-assumptions-and-options` requires the unique role of added
  complexity, but not a link to a requirement.
- Evidence: `tree_fingerprint.py` (CF-003); the PR-A `--evidence-file` checks
  needed fixes and produced new problems in rounds 1 and 2, and the
  re-evaluation removed them (`round-2.md`).
- Proposed Core change: in `workflow.md#wf-assumptions-and-options`, a new
  mechanism traces to a requirement, otherwise it is a scope expansion.
- Kind: modifying (a tightening).
- Impact on the other projects: Codex and Grok need a requirement source (for
  example a REQ wiki) to check it.

### CF-007 How context is loaded: a short core plus references read on demand (evaluation)

- Origin: the user's question on principle 1 (2026-10-20); D-011 (REQ-016).
- Problem: principle 1 said that the repeated legal-style text was the
  largest context cost in the Codex version, but nothing measured it.
- Facts (file sizes measured on 2026-10-21; these are not token counts):
  - claude-dev-skills: `skills/dev-core/SKILL.md` is 35,425 bytes. Every
    dev-* skill reads all of it first; the agent files and briefs of the
    subagents do not require it. The SKILL.md files
    of the other 7 skills are 1.5 KB to 5.5 KB.
  - The 4 contracts of Core v0.1.1 are 42,425 bytes in total.
  - codex-dev-skills (commit 9935975): the SKILL.md files of its 27 skills
    are 0.9 KB to 14 KB (median 3.3 KB); its `references/` folders hold about
    199 KB, read only when an operation needs them.
  - grok-build-dev-skills (commit d68b7ad): no skills yet.
- Inference: the real cost may be the repeated loading of the same long text
  and the loss of attention in long text, not one full load. The D-011 token
  comparison must confirm this.
- Evaluation (split `dev-core`):
  - Method: a short core that is always read (stop conditions, authority,
    blocking rules), plus references read per stage (plan, review, gate,
    delivery).
  - Benefit: less text per read; Claude and Codex load in the same way.
  - Risk: a skill can miss a reference it needs; rules spread over more files
    can drift apart (see CF-008). A split touches every skill, so the review
    cost is high.
  - Conclusion: wait for the D-011 measurements. The user decides with a
    decision card whether to implement it (FU-005).
- Proposed Core change: a companion note in Core on how to load the
  contracts, so that the three interfaces use one loading model.
- Kind: additive.
- Impact on the other projects: Codex already reads on demand; adoption
  mainly aligns names and sections.

### CF-008 Each rule in one place (implemented in this project)

- Origin: PR-C decision card 2; the user chose (b) defer (REQ-019 sources;
  FU-006).
- Problem: the same rule is restated in several skills, so a rule change can
  miss a copy.
- Evidence: PR-B had the same kind of missed copy in three rounds in a row:
  C1-001 (`round-1.md`), MR-B-002 and MR2-B-001 (PR #7 comments). Later,
  PR #13 (MR-001) and PR #15 (R2-001, MR15-001, F-001) had the same kind of
  missed copy.
- Proposed Core change: a companion note for interface authors that writes
  each rule once in the digest and cites only its rule ID elsewhere.
- Kind: additive.
- Impact on the other projects: only their own skill structure.
- Status: on 2026-10-21 the user decided to do it now, without waiting for
  the D-011 measurements ("FU-009 合併後 FU-006 優先處理": do FU-006 first
  after FU-009 merges). This project implements it in Issue #16 (REQ-022):
  only the copies of three rules (R-EXH-3 record storage, R-VER-2 stop rule,
  R-EXH-4 platform result) became citations; other rule text stays word for
  word and names its rule IDs. The agent files keep their own copies;
  CF-007 (FU-005) handles them. The Core companion note is still "not
  proposed".
- Lesson (user, 2026-10-22, card 7a): 「規則文字不改寫、只有單一規則的副本才換成引用、給 subagent 的文件保留全文」
  (translation: do not reword rule text; replace only a copy of a single
  rule with a citation; files given to a subagent keep the full text). Reason (this project's inference): a
  subagent does not read `dev-core`, for example the readers of
  review-report.md, task-brief.md and the agent files. Evidence: all
  three review rounds of Issue #16 found blockers caused by rewording
  (FR1-001, FR1-002, FR1-005, FR2-001, FR3-001 to FR3-004): the rewording
  lost a condition, an actor or a reader, or cited the wrong rule.

## Decisions not fed back to Core

| Decision | Reason |
| --- | --- |
| D-009 Graph engineering in stages | Graph engineering is not in the Core contracts; re-evaluate when the runtime-neutral layer takes shape |
| D-010 No agent memory | Core `auth-scope`, `wf-stages` and `auth-data` already cover it |
| D-011 Deploy and measure | Work on the Claude side; the results are evidence for this document |
| D-012 Automatic handoff | Depends on the session capabilities of each interface; Core `wf-stages` already covers the checkpoint and the resume |

</details>
