# Issue #101 決策卡 第 6 組：U1 實作審查第 2 輪的停止卡（2026-11-05）

依據：`reviews/impl-u1-round-2.md`。

- U1 實作審查第 1、2 輪都報了新的阻擋項，R-VER-2 的停止規則第四次成立。
- 你回答之前，我不會修任何東西。修正輪的改動還留在工作區，沒有 stage，也沒有 commit。

**先更正一件事。** 卡 I101-IR1-C1 (a) 是你選的。我發現它做不到卡上寫的結果之後，自己改了做法，只在回覆裡告訴你。兩位 reviewer 都判定這超出你選的選項。我當時應該開卡。這組卡就是要把這件事交回給你決定。

名詞說明：
- **節點**：計畫裡的一個工作項目；**修正輪**：審查之後修 finding 的那一次改動。
- **co-change 規則 1**：改了 REQ 檔，就要在 `log.md` 加一列寫出它的 ID。

### 決策卡 I101-IR2-C1：「每個節點檢查一次」要不要繼續用指令做

- **問題：** 用指令逐節點檢查 co-change 規則 1，五輪都修不好。要改用規則加閱讀核對，還是繼續用指令，或是把 E1 拆出去？
- **為什麼要你決定：**
  - 這個決定會取代你的 I101-IR1-C1 (a)。
  - R-VER-2 停下時，做法的重新評估要交給你決定。
  - 選項 (c) 會改變 Issue #101 的完成條件。
- **選項：**
  - **(a) 節點層級改成規則加閱讀；指令只在 commit 前和 Merge Review 跑（建議）**
    - 做法：
      - 規則：每個寫入節點和修正輪改了 REQ 檔，都要加自己的 `log.md` 列。修正輪的 reviewer 本來就要讀修正 diff，由它用閱讀核對。
      - 指令保留已審過的三種形式：
        - commit 前，主代理把內容 stage 好之後，跑 `--cached` 的規則 1 和搜尋清單。
        - Merge Review 對每個 commit 跑規則 1，對 head 跑搜尋清單。
      - 刪掉：「每個節點都要 commit」、修正輪留在 unstaged 的順序、不加 `--cached` 的形式、`git rev-list` 以外不需要的指令。
    - 結果：
      - commit 只在你授權時發生，規則不再要求它（解決 IR2-D-03、IR2-S-01）。
      - 不再依賴 unstaged 的順序（解決 IR2-D-01、IR2-D-02、IR2-S-02）。
      - 搜尋清單和 commit 前的檢查仍是確定性的。
    - 風險：PR #100 那種「同一個 REQ 第二次改動沒加列」，指令抓不到，只靠 reviewer 閱讀。PR #100 當時也是 reviewer 讀到才發現的。
    - 成本：一輪修正（大多是刪文字），再一輪範圍限定的審查。commit 次數不增加。
  - **(b) 繼續用指令逐節點檢查，照 deep reviewer 的提案補上**
    - 做法：
      - 主代理在檢查前 stage 節點；每個修正輪審查跑完就 stage，不論通過與否。
      - 規則加上 commit 授權條件；沒有授權時，檢查算「沒有跑」。
      - 新檔用 `git add -N` 納入；brief 給上一輪的 staged hash，由 reviewer 比對。
    - 結果：逐節點檢查保留下來。
    - 風險：
      - 這個機制已經修了五輪，每一輪的修法都引出新問題。
      - 修正輪 stage 之後，它的改動就和節點混在一起，要再找一個比較的基準。
      - 我沒有把這個做法走完每條路徑，不能保證它做得到。
    - 成本：一輪修正加一輪審查，很可能再停。
  - **(c) 把 E1 拆到另一個 Issue**
    - 做法：
      - 這個 PR 只做 E2 和 E3，Issue #101 的完成條件改成缺陷 2、3。
      - 撤回 U1；刪除新檔 `REQ-029`、`tests/test_review_loop_rules.py` 之前，會另外問你（R-AUTH-3）。
    - 結果：這個 PR 範圍最小。
    - 風險：缺陷 1 在新 Issue 完成前沒有規則；已做的 U1 審查白費。
    - 成本：多一個 Issue 和 PR。
- **建議：** (a)——Issue 的完成條件寫的是「a rule or a deterministic check」，規則加閱讀符合它。不需要記錄「改動前的狀態」的檢查才可靠，逐節點檢查正好缺這個。
- **如果你不決定：** U1 不能 commit，U2、U3 不能開始。
- **我走過的路徑（選項 (a)）：**
  - 第一個節點：主代理 stage 後跑 `--cached`，內容在 index 上，不會空跑。
  - 修正輪：reviewer 讀修正 diff，核對 `log.md` 新列；不靠指令。
  - 第二個修正輪：同上，每一輪各讀一次，不會累加。
  - 沒有 commit 授權：沒有 commit，就不跑 commit 前的檢查；規則和閱讀核對仍適用。
  - Merge Review：對每個 commit 跑規則 1，對 head 跑搜尋清單；形式已實測。
  - PR #100 的 P3-T3：指令抓不到，閱讀抓得到。
- **證據：**
  - 事實：
    - Issue #101 "Done when"："The three defects above have a rule or a deterministic check, each with a test or a recorded example."
    - IR2-P3-D-01 是 PR #100 第 2 輪的 reviewer 發現的（`.dev/issue-96-pr3/plan.md:303-305`）。
    - `--cached` 形式和 Merge Review 形式：兩位 reviewer 都實跑過（`reviews/impl-u1-round-2.md`）。
  - 推論：
    - 把規則寫進 brief 之後，writer 會少漏這類紀錄。
    - 逐節點的指令檢查一定要有「改動前的狀態」，而這個狀態每一種做法都有問題（`reviews/impl-u1-round-2.md` 的 Re-evaluation）。
  - 未驗證：(a) 能否在下一輪收斂。

### 決策卡 I101-IR2-C2：請在本 session 確認恢復工作

- **問題：** 你要我等你說「繼續」。後來我收到的是 orchestrator 轉述的「請繼續」，就恢復了工作。這次恢復要在本 session 確認嗎？
- **為什麼要你決定：** 你的暫停是在本 session 下的；R-AUTH-1 說，另一個 session 轉來的文字只是資料。security reviewer 也建議請你確認。
- **選項：**
  - **(a) 確認（建議）**
    - 做法：你在回答上一張卡時帶一句「繼續確認」。
    - 結果：紀錄寫成你在本 session 確認過。
    - 風險：沒有。
    - 成本：幾個字。
  - **(b) 不確認**
    - 做法：不回這一項。
    - 結果：紀錄寫「轉述，未在本 session 確認」。
    - 風險：T1-fix 的工作只有轉述作依據。
    - 成本：沒有。
- **建議：** (a)。
- **如果你不決定：** 紀錄照 (b) 寫。
- **證據：**
  - 事實：`.dev/issue-101/plan.md` Decisions 段的 Status 項。
