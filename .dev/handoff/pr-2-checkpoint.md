# Checkpoint：PR #2 交接（2026-10-20）

這份 checkpoint 是交接摘要，不是證據。所有判定以 Git、`.dev/issue-1-phase1/` 下的紀錄，以及實際執行的指令輸出為準（`dev-core` R-STG-5、R-EVD-2）。接手的 session 必須先重新讀取這些來源。

## 1. 識別資訊

| 項目 | 值 |
| --- | --- |
| Repository | jeffery777/claude-dev-skills |
| Issue | #1 "Phase 1 skills, agents, and G0 task graph"（OPEN） |
| PR | #2，OPEN，`Closes #1`，GitHub 狀態 MERGEABLE，無 checks，無 review decision |
| 分支 | `1-phase1-skills`（追蹤 `origin/1-phase1-skills`） |
| base（origin/main） | `5229478aead42cc2d70b7843dd5db3548c08c562` |
| merge-base | `5229478aead42cc2d70b7843dd5db3548c08c562` |
| 最後一個已審查的程式 head | `2280228750c7aafe3e0b7624f166693246357995`（diff sha256 `bc4b2cfbb68a98455523a3b32e29b83e33e981aaf0e0b13ac2657596eb2d21ec`，87 檔） |
| 本 checkpoint commit | 加入本檔案後的新 head（見 `git log -1`），只多出本檔案 |

Commits（由舊到新）：

| Commit | 內容 |
| --- | --- |
| `9f38f06` | Phase 1 初始實作（commit gate PASS，diff `790a1600…`） |
| `c72c64d` | 修正 Merge Review 1 |
| `c934a29` | 修正 Merge Review 2 |
| `eb8e08a` | 修正 Merge Review 3 |
| `2280228` | 修正 Merge Review 4 |
| （新 head） | 本 checkpoint |

## 2. 各輪 Merge Review

完整的 finding 與處置都寫在 `.dev/issue-1-phase1/reviews/merge-review-1.md` 到 `merge-review-4.md`。每一輪都由全新的獨立 subagent 執行，涵蓋完整的 base-to-head 範圍。

| 輪次 | 審查的 head | 結果 | Findings | 處置摘要 | 修正 commit |
| --- | --- | --- | --- | --- | --- |
| MR1 | `9f38f06` | content BLOCKED／platform NOT_CONFIGURED | MR-01..MR-21（1 MUST-FIX、5 SHOULD-FIX、15 NIT） | Fixed：其餘全部。Rejected：MR-15、MR-19、MR-21。Deferred：MR-18 → FU-002 | `c72c64d`。另有三項在 `c934a29` 補完或被取代：MR-03 補完（見 MR2-01）、MR-04 被 MR2-02 取代、MR-05 被 MR2-06 收窄 |
| MR2 | `c72c64d` | BLOCKED／NOT_CONFIGURED | MR2-01..MR2-17（0 MUST-FIX、3 SHOULD-FIX、14 NIT） | Fixed：其餘全部。Rejected：MR2-09、MR2-16 | `c934a29`；MR2-17 在 `eb8e08a` 補完（MR3-02） |
| MR3 | `c934a29` | BLOCKED／NOT_CONFIGURED | MR3-01（SHOULD-FIX）、MR3-02（NIT） | 兩項 Fixed | `eb8e08a`；MR3-02 的測試在 `2280228` 補強（MR4-04） |
| MR4 | `eb8e08a` | BLOCKED／NOT_CONFIGURED | MR4-01..MR4-03（SHOULD-FIX）、MR4-04（NIT） | 四項 Fixed | `2280228` |
| MR5 | `2280228` | **未完成**：本 session 依使用者指示中途停止，沒有結果 | — | — | — |

每一輪 BLOCKED 的原因都相同：新 finding 在審查當下還沒有處置。MR1 之後沒有再出現 MUST-FIX。

Commit 之前另外做過 5 輪 review（round 1 到 5）與 commit gate，紀錄在 `.dev/issue-1-phase1/reviews/round-1.md` 到 `round-4.md` 及 `gate-commit.md`。

### 目前仍未解的事項

- **處置欄位已填，但尚未經獨立確認**：MR4-01..MR4-04 已在 `2280228` 修正，不過 MR5 沒有完成，所以這些修正還沒有獨立 reviewer 確認。
- **沒有任何 finding 缺處置。**
- **Deferred（追蹤於 `.dev/followups.md`）**：
  - DR-022b → FU-001：Cowork 實測。
  - MR-18 → FU-002：大型 ignored 目錄的指紋效能。
- **PR 尚未通過 exact-head Merge Review。** 目前沒有任何一個 head 拿到 `content_review: PASSED`。

## 3. 為什麼 4 輪都還有新 finding

依證據判斷，主因有兩個：一是驗收標準沒有寫清楚，二是修正引入新問題。review 範圍太廣是放大因素。另外，紀錄存在同一分支的結構，讓這個循環無法自然結束。

1. **驗收標準不明確（主因）**
   - MR1 到 MR4 的 brief 都要求以 recall 為主的 `/code-review high --max-findings all`，卻沒有設定「什麼程度的問題才算阻擋」。每輪都把邊界情況當成 finding 回報。
   - 兩個自製機制沒有寫明規格：一是 YAML 子集 parser（`graph.frontmatter`、`check_pack.sources`），二是 `tree_fingerprint.py` 的威脅模型。結果邊界情況沒有上限，例如引號跳脫、註解行、rename 紀錄、cache 目錄、submodule。MR2 到 MR4 有超過一半的 finding 集中在這兩處。
   - MR5 的 brief 已經加上門檻，但沒有跑完。
2. **修正引入或遺漏問題（主因）**：
   - MR-10 的修正造成 MR2-04 回歸。
   - MR-04 的修正讓程式違反 REQ-008（MR2-02）。
   - MR-03、MR-13、MR2-17、R2C-02 都只修了一部分（MR2-01、MR2-05、MR3-02、MR4-01）。
   - MR3-02 的測試寫得太弱，連舊程式也會通過（MR4-04）。
   - 共同原因：修正後直接 push，push 前沒有做窄範圍的獨立確認；部分測試的斷言沒有驗到實際行為。
3. **範圍太廣（放大因素）**：每輪都要完整重審約 8,300 行。Core 要求每個新 head 都做完整 base-to-head review，這是必要的；但 recall 模式套在大範圍上，必然會產出新的 NIT。
4. **結構性循環**：處置寫在同一分支的 `.dev/` 紀錄裡。每寫一筆處置就產生新 head，新 head 又需要完整 Merge Review（Core `exact-transition`）。只有某一輪 review 回報零 finding、而且不需要再寫紀錄，循環才會結束。
5. **可能的 SCOPE-CREEP**：
   - `tree_fingerprint.py` 是 round 2 為了修 SR-006 而新增的機制，之後累積了 15 項以上的 finding。
   - 依 R-RIG-3 與 R-RIG-4，它的存在理由應該重新評估。備案：拿不到 plugin agent 時，必要的 review 一律不用 general-purpose 替代，直接停在 gate。

### 下一輪的調整建議

1. **沿用 MR5 的嚴格門檻**：
   - MUST-FIX 只限 Core 的真正阻擋項。
   - SHOULD-FIX 必須有重現的失敗，而且影響需求、DoD 或文件寫明的行為。
   - NIT 只限 delta 引入的回歸，或不實的文件陳述。
   - 其他都列為 residual risk，不列為 finding。
2. **先寫規格，再審查**：
   - 在 `graph.py` 的 docstring 或 graph-schema.md 寫明支援的 YAML 子集；子集以外的寫法只回報為格式限制。
   - 為 `tree_fingerprint.py` 寫明威脅模型：只偵測本機狀態，失敗時偏安全，不是隔離機制。
3. **修正後、push 前**，先由獨立 subagent 做窄範圍確認：確認修正確實有效、沒有回歸，而且測試換成舊程式時會失敗。
4. **完整 Merge Review 可以重用證據**：未變更的部分，在寫明理由與覆蓋範圍的前提下，重用前一輪的證據（MR3、MR4 已這樣做）。重點放在 delta 與相依路徑。
5. **解決結構性循環**：最後一次 PASSED 的結果放在哪裡，需要使用者決定（見第 5 節）。

## 4. 剩餘 DoD、驗證指令與最後結果

D-008 與 Issue #1 的狀態：

| 項目 | 狀態 |
| --- | --- |
| D-008 各列（Core vendor、8 技能、source map／覆蓋檢查、4 agents、G0 graph、wiki 範本與 ingest、本專案 REQ、打包） | MR4 判定全部達成（at `eb8e08a`）；`2280228` 未經獨立確認 |
| REQ-001「skills 能在 Cowork 載入」 | 未驗證（FU-001，Deferred） |
| REQ-002..REQ-010 | MR4 判定已達成 |
| Issue #1：`validate.sh` 通過 | 達成（見下方） |
| Issue #1：每個 finding 都有 ID 與處置，沒有未解的 MUST-FIX | 紀錄上達成；`2280228` 的修正未經獨立確認 |
| Issue #1：通過 exact-head Merge Review | **未達成** |

驗證指令（在 repo 根目錄執行）：

```bash
./scripts/validate.sh
```

```bash
python3 scripts/verify_core.py --upstream <engineering-workflow-core 的 clone>
```

```bash
python3 -W error::ResourceWarning -m unittest discover -s tests -q
```

最後一次結果（2026-10-20，本機，head `2280228`）：

- `validate.sh`：all checks passed
  - core vendor OK（v0.1.1 `7b66978a7659`，14 檔）
  - core coverage OK（21 anchors、40 rules）
  - pack structure OK
  - 83 tests OK
  - `claude plugin validate` 對 marketplace 與 plugin.json 兩份 manifest 都通過
- `verify_core.py --upstream`：MR4 在 `eb8e08a` 用全新 upstream clone 驗證過，tag object、commit 與 14 個檔案都吻合。vendor 檔案自此沒有變更。

尚未執行（NOT_RUN）：

- Cowork runtime（FU-001）
- 安裝後 plugin agent 的 `tools` 與 `effort` 實際是否生效
- SAST／SCA 靜態掃描（未設定）
- CI（Phase 1 不在範圍內）

`platform_enforcement` 一直是 NOT_CONFIGURED：沒有選定 provider profile，main 沒有 branch protection 或 ruleset。

## 5. 待使用者決定的事項

1. **是否繼續 Merge Review**：由新 session 對新 head 做完整 Merge Review，並採用第 3 節的嚴格門檻。
2. **最後 PASSED 結果的保存位置**：要解決第 3 節第 4 點的循環，選項如下：
   - (a) 授權把結果寫成 PR comment，head 不變；
   - (b) 合併後再另開 commit 補紀錄；
   - (c) 接受在紀錄 commit 之後，再做一次只檢查紀錄的完整 review。
3. **是否保留 `tree_fingerprint.py`**：或改成「拿不到 plugin agent 就不用替代 reviewer」，以縮小範圍（R-RIG-4）。
4. **是否合併 PR #2**：合併授權只屬於使用者。目前不能合併，因為沒有任何 head 拿到 `content_review: PASSED`。
5. **是否為 FU-001、FU-002 開 GitHub Issue**：這需要另外授權。本 session 只獲授權開 Issue #1。
6. **確認幾個實作中的預設**：
   - plugin 名稱 `dev-skills`：`claude-` 開頭的名稱被保留，所以 plugin 與 repo 名稱不同。
   - `.dev/` 預設隨工作一起 commit。
   - `light` 等級若要 commit 或開 PR，必須先通過獨立 review 與 commit gate（R-RIG-2）。
7. **Cowork 實測**：需要在使用者的 Cowork 環境進行（FU-001）。

## 6. 接手步驟

1. 讀取 `CLAUDE.md`（目前沒有）、`docs/design-proposal.md` 第 7 節、`docs/requirements/index.md`、`.dev/issue-1-phase1/` 全部紀錄、`.dev/followups.md` 與本檔案。
2. 執行 `git fetch`，確認 `origin/1-phase1-skills` 的 head 等於本 checkpoint commit，`origin/main` 仍是 `5229478`。若有漂移，以實際狀態為準。
3. 先取得第 5 節第 1、2 項的使用者決定，再開始下一輪。
4. 本 session 交接後，不再寫入這個分支。
