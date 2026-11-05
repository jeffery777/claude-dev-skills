# Issue #101 決策卡 第 13 組：U2 第 3 輪審查（2026-11-05）

依據：`reviews/impl-u2-round-3.md`。

- 第 3 輪：Security Diff Scan 2 個 MUST-FIX，deep 1 個 SHOULD-FIX、2 個 NIT。R-VER-2 的停止規則成立。
- 你回答之前，我不會修任何東西。

**我上一張卡的問題。** U2R2-C1 (a) 的句子是我擬的。我在卡上走了十條路徑，說都符合預期。三條走讀是錯的：
- 「pack 檔不算私人檔案」：在這個 repo 裡，它只能排除沒追蹤的檔案，那正是要保護的東西。`cards-1.md` 就是這種檔案。它也動到了 R-REV-9 的「private files」，所以它其實是放寬。
- 「訊息裡的話不是檔案」：你把私人指示檔貼進訊息時，同一段文字既算又不算。
- 「floor check 的值不是檔案內容」：它們就是從 transcript 檔複製的。

三輪的共同原因（推論）：類別寫得太廣，所以要靠例外收回來，而每條例外都有漏洞。

### 決策卡 I101-U2R3-C1：R-AUTH-7 這一類怎麼收尾

- **問題：** 要改成一個很窄、沒有例外的句子，還是把這一類拆出這個 PR？
- **為什麼要你決定：** 這會改掉你選的 U2R2-C1 (a) 的文字；新的隱私風險由使用者決定（Core `authorization-and-stops.md:34`）。
- **選項：**
  - **(a) 改成很窄的一句，沒有例外（建議）**
    - 做法：
      - Never commit 清單最後一項改成：
        > or the content of native memory or of the user's private instruction files, in any form.
      - 刪掉 "Files of this pack ..."、"When it is unclear ..." 兩句，以及紀錄裡「訊息不是檔案」的說法。
      - agent 檔的類別句改成同樣的字，動詞用 write。
      - 這一輪審查若再有新的 MUST-FIX 或 SHOULD-FIX，就直接改走 (b)，不再開修正輪。
    - 結果：
      - 只禁兩種東西，沒有例外要解釋。
      - 其他私人檔案不在這一類，照舊靠 R-REV-9 的「private files」（這個字不再被動到）。
    - 風險：
      - 範圍比前兩版窄：私人指示檔和原生記憶以外的私人檔案，只有 R-REV-9 掃描一層。
      - 這一輪若再找到問題，R-AUTH-7 這部分就拆出去。
    - 成本：一輪小修正和一輪範圍限定的審查。
  - **(b) 現在就拆到另一個 Issue**
    - 做法：撤回 R-AUTH-7 的改動和 agent 檔裡的類別句，遮蔽句保留。紀錄寫明這類內容只靠 R-REV-9，並開新 Issue。Issue #101 的 Scope 要再更新一次。
    - 結果：U2 只剩 R-EVD-3，這條線不再拖住 U2、U3。
    - 風險：新 Issue 完成前，保護只有一層；repo 是公開的，外洩無法收回。這個 Issue 裡已經發生兩次，都是審查擋下的。
    - 成本：多一個 Issue 和 PR。
  - **(c) 保留現在的句子，繼續補**
    - 做法：限定 pack 句的範圍、定義貼上的文字、補回 R-DEL-2 的例外。
    - 結果：範圍最廣。
    - 風險：同一機制已經修三輪，每條新例外都引出新問題。
    - 成本：可能再多幾輪。
- **建議：** (a)——一句話，沒有例外，也設了上限：再出問題就拆出去。
- **如果你不決定：** U2 不能 commit，U3 不能開始。
- **我走過的路徑（選項 (a)），每條附上依據：**
  - 私人指示檔的逐字引用、轉述、貼進訊息的片段：都是該檔內容，"in any form" 涵蓋，擋下。
  - 原生記憶的內容：擋下。
  - `cards-1.md`：是私人指示檔內容的轉述，擋下，和現在不 commit 的處理相同。
  - repo 追蹤的 `CLAUDE.md`、`AGENTS.md`、agent 檔：不是私人的，不算。
  - pack 檔：沒有提到，所以不必排除；R-AUTH-6 的引用不受影響（`skills/dev-core/SKILL.md:99`）。
  - 你的卡片回答、轉述的回答：不是這兩種內容，不算；你另外貼進來的私人指示檔片段仍算。
  - floor check 的 model 和 effort：不是這兩種內容；它和 transcript 的既有關係是 R-DEL-2 的事，和 main 上相同，這次不改（`skills/dev-core/SKILL.md:100`、`:184`、`:191`）。
  - R-REV-9 的 "private files"：沒有動（`skills/dev-core/SKILL.md:156`）。
  - 這個 pack 自己的 repo：沒有 pack 句，所以沒有那道門。
- **證據：**
  - 事實：`reviews/impl-u2-round-3.md`（U2R3-S-01、U2R3-S-02、U2R3-D-01）。
  - 推論：類別窄到不需要例外時，例外的漏洞就不存在。
  - 未驗證：新文字還沒有審查；"private instruction files" 仍要靠判斷。

## 修正輪一併處理、不需你決定的項目

- U2R3-D-02：K28 那一列的理由。
- U2R3-D-03：plan 的標題改成目前的版本。
- plan 那句 "subagents do not commit" 補上來源。
