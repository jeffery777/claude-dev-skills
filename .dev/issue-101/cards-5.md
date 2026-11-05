# Issue #101 決策卡 第 5 組：U1 實作審查第 1 輪的停止卡（2026-11-04）

依據：`reviews/impl-u1-round-1.md`。

- 設計審查第 3 輪報了新的 MUST-FIX，U1 實作審查第 1 輪又報了新的 SHOULD-FIX。兩輪都出在 E1 的「tree 綁定」。
- R-VER-2 的停止規則因此第三次成立。
- 卡 I101-R3-C1 (a) 也寫明：遇到這種情形要再停一次。
- 你回答之前，我不會開始修正。

名詞說明：
- **節點 tree**：主代理在每個寫入節點之後，用 `git write-tree` 記下的內容快照編號。
- **staged diff**：已經放進 Git 暫存區、準備 commit 的變更。

### 決策卡 I101-IR1-C1：E1 的「每個節點檢查一次」要怎麼綁住內容

- **問題：** E1 要求每個寫入節點都檢查一次 co-change 規則，例如「改了 REQ 檔，同一節點要加一列 `log.md`」。目前用節點 tree 綁住內容，接連出問題。要改成什麼做法？
- **為什麼要你決定：**
  - R-VER-2 停下時，做法的重新評估要交給你決定。
  - 選項 (a) 會增加 commit 和掃描的次數，也就是增加成本。
  - 選項 (c) 會改變 Issue #101 的完成條件。
- **選項：**
  - **(a) 每個寫入節點（包括修正輪）審查通過後就 commit，檢查改綁 commit（建議）**
    - 做法：
      - 刪掉節點 tree、`git write-tree`、讀 `git status` 判斷 owned path，以及 tree 綁定指令。
      - 審查前：
        - HEAD 就是上一個節點的 commit。
        - co-change 規則 1 改用 `git diff --cached --name-only`（比較 HEAD 和暫存區）和 `git diff --cached -U0 -- <log>`。
        - 搜尋清單改用 `git grep --cached`。
        - 這些指令都不需要任何 tree ID。
      - commit 前照舊做 R-REV-9 掃描。
      - Merge Review 用 base..head 裡每個 commit 的 ID 重跑。commit ID 已經 push，任何 clone 都能重跑。
    - 結果：
      - 值規則只剩搜尋字串和資料夾；commit ID 由 Git 輸出取得，再用正規式核對。
      - IR1-D-01、IR1-D-02、IR1-S-01 的成因都被刪掉。
    - 風險：PR 會多出幾個 commit，例如每個修正輪一個。
    - 成本：每多一個 commit，就多一次 R-REV-9 掃描（opus/xhigh）。
  - **(b) 保留節點 tree，照修三個 finding**
    - 做法：
      - 另外定義審查用的「完整 staged tree」。
      - owned path 的檢查改成和上一個節點的 tree 比較。
      - 綁定指令補上 `--no-ext-diff --no-textconv --ignore-submodules=none`。
      - 做一輪範圍限定的審查。
    - 結果：不必增加 commit 次數。
    - 風險：同一機制已經修了四輪；這一輪的新問題，正是上一輪的修法引出來的。
    - 成本：一輪修正加一輪審查，可能還會再停。
  - **(c) 把 E1 拆到另一個 Issue**
    - 做法：
      - 這個 PR 只做 E2 和 E3。
      - 撤回已 stage 的 U1。新檔 `REQ-029`、`tests/test_review_loop_rules.py` 的刪除，屬於破壞性操作，會另外問你（R-AUTH-3）。
      - E1 開新 Issue。
      - Issue #101 的完成條件改成只有缺陷 2、3。
    - 結果：這個 PR 的範圍最小。
    - 風險：E1 完成之前，缺陷 1（漏改紀錄）還會發生；U1 已經做完的審查會白費。
    - 成本：多一個 Issue 和 PR。
- **建議：** (a)——它把會出問題的元件（節點 tree 和綁定）整個拿掉，而不是再修一次；代價是可以預估的掃描次數。
- **如果你不決定：** U1 不能 commit，U2、U3 也不能開始。
- **證據：**
  - 事實：
    - IR1-D-01：deep reviewer 實測，`diff --cached --quiet` 對 T1 的節點 tree 回 exit 1，對完整的 staged tree 回 exit 0（`reviews/impl-u1-round-1.md`）。
    - 同一機制先前出問題的 finding：SR1-06、SR2-03、DR2-07、DR3-04、DR3-05。
    - PR #100 的那次漏失：P3-T3 是單獨一個修正節點，它改了 REQ-009，卻沒有加 `log.md` 列（`.dev/issue-96-pr3/plan.md:303-305`）。
  - 推論：
    - 照 (a) 的寫法，P3-T3 會是單獨一個 commit，`git diff --cached` 的檢查會在 commit 前失敗。這一點沒有實測，因為 P3-T3 當時沒有單獨 commit。
  - 未驗證：(a) 實際會多出幾個 commit。

### 決策卡 I101-IR1-C2：請在本 session 確認 R3-C1 (a)

- **問題：** 你對卡 I101-R3-C1 的回答「同意你建議a」是 orchestrator 轉述給我的。要在本 session 確認它嗎？
- **為什麼要你決定：**
  - 我在 plan 寫了「依卡 C5 (a)，轉述就算數」，但這句不準確。C5 (a) 的選項只涵蓋 C1；提到 C2–C4 的，是它的建議句。
  - R-AUTH-1 說，從另一個 session 轉來的文字只是資料。
- **選項：**
  - **(a) 在本 session 確認（建議）**
    - 做法：你在這裡回一句，例如「R3-C1 a 確認」。
    - 結果：之後的紀錄可以寫成「你在本 session 的訊息」。
    - 風險：沒有。
    - 成本：一則訊息。
  - **(b) 維持轉述**
    - 做法：紀錄寫成「由 orchestrator 轉述」，依據是先前 Issue #96 的作法，而不是 C5 (a)。
    - 結果：plan 那一句照這個依據改寫。
    - 風險：依據只是先前的作法。
    - 成本：沒有。
- **建議：** (a)。
- **如果你不決定：** 紀錄先寫「轉述，未在本 session 確認」。
- **證據：**
  - 事實：`cards-2.md` 卡 I101-C5 的選項 (a) 與建議句；`.dev/issue-101/plan.md` Decisions 表 `cards-4.md` 那一列。
