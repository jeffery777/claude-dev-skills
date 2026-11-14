# Issue #114 決策卡片（設計審查後，第 1 組）

依 ASD-STE100 原則編寫，未完成完整符合性驗證（英文部分）；繁體中文部分採白話寫作，不主張符合 ASD-STE100。

來源：`reviews/design-round-1.md`（設計審查第 1 輪）、`plan.md`。
回答方式：例如「C1 c，C2 a，C3 a，C4 a，C5 a，C6 a」。卡片本身不授權任何動作，只有使用者的回答算數。

回答（轉述）：「全照建議」（使用者，2026-11-14，由 orchestrator session 轉述；orchestrator 問的是「6 張卡片都照建議回答嗎（C1 c、C2 a、C3 a、C4 a、C5 a、C6 a）？」）。所以：C1 (c)，含 C1 的兩件事（答案寫成新需求 REQ-030；這個 PR 不在 Cowork 重測，FU-069 記 release 後的 Check for updates）；C2 (a)；C3 (a)；C4 (a)；C5 (a)；C6 (a)。

名詞：
- manifest：`.claude-plugin/plugin.json` 與 `.claude-plugin/marketplace.json`，告訴 Claude Code／Cowork 這個 plugin 是什麼。
- cache：使用者電腦上已安裝的 plugin 副本。
- tag：GitHub 上指向某個 commit 的名字，例如 `v0.1.0`。

## C1：plugin 的版本字串要怎麼處理？

- **問題：** 第一次 release 時，manifest 的 `version` 要保留、改號，還是拿掉？
- **為什麼要你決定：** 沒有任何需求規定版本策略（DR-D-02，`REQ-GAP`）。Issue #114 的範圍也沒有提 manifest。只有你能新增需求。
- **事實：**
  - 兩個 manifest 都寫 `"version": "0.1.0"`（`plugin.json:4`、`marketplace.json:10`）。
  - 官方文件（code.claude.com/docs/en/plugins/host-marketplace.md，〈Release a new version〉，2026-11-14 以 `curl` 讀回）：
    - 有設 `version` 時，使用者會停在 cache 的副本，直到字串改變。
    - 不設 `version` 時，使用者跟著 commit 走。
    - 不要在兩個 manifest 都設 `version`；兩邊都設時以 `plugin.json` 為準，而且不會警告。
  - 官方文件（.../plugins/loading.md）：不設 `version` 時，同 repo 相對路徑的 plugin，版本就是 commit SHA。
  - 已知的兩份安裝都是 `0.1.0`，內容是 commit `e37a990`（本機 Claude Code 的安裝紀錄；Issue #3 留言的 Cowork 安裝）。`main` 現在是 `7e71ad5`。
  - Cowork 文件（claude.com/docs/cowork/guide/plugins.md）只提到「Check for updates」和「Sync automatically」，沒寫怎麼比較版本。
  - 釘選語法 `owner/repo#ref`（例如 `#v0.1.0`）在 code.claude.com/docs/en/plugins/install.md 有寫。這裡沒有實測。
- **選項：**
  - **(a) 保留 `version`，這次用 `0.1.0`，之後每次 release 才改號**
    - 做法：manifest 不動。
    - 結果：已裝的兩份 `0.1.0` 拿不到 v0.1.0 的內容（也拿不到 Issue #115 的修正），要手動重裝。之後每個 merge，包括安全修正，都要等下一次改號的 release 才送到使用者。新安裝會拿到 `main` 的最新內容，但標示仍是舊號碼。
    - 風險：同一個 `0.1.0` 對應多份內容。重裝步驟沒有實測，不能寫成給使用者的指示。
    - 成本：C2 必須選 (b)（改 `dev-retro` 規則）。每次修正都要多一次 release。
  - **(b) 保留 `version`，這次改用新號碼（例如 `0.1.1`），之後每次 release 改號**
    - 做法：改兩個 manifest（或只留 `plugin.json`，見 (d)），tag 改成新號碼，Issue 標題、CHANGELOG 標題、REQ-018、`vendor/engineering-workflow-core.lock.json` 的 `consumer.version` 一起改。
    - 結果：已裝的兩份下次更新就會拿到這次 release。之後和 (a) 一樣。
    - 風險：和 (a) 相同的長期問題（每個修正要等 release）。
    - 成本：多一個 manifest 修改節點（strict、Security Diff Scan）；C2 必須選 (b)。
  - **(c) 兩個 manifest 都拿掉 `version`，使用者跟著 commit 走（建議）**
    - 做法：刪除兩處 `version`。`lock.json` 的 `consumer.version` 改成「commit SHA（自 Issue #114 起 manifest 不設 version）」。README 寫一句：沒有釘選的安裝會跟著 `main`；tag `v0.1.0` 是一個審查過的快照，附 release notes。
    - 結果：已裝的兩份下次更新就會換到最新的 `main`。之後每個審查過的 merge，包括安全修正，使用者下次更新就拿得到，不必另外 release。C2 可以選 (a)，`dev-retro` 規則文字不用改。
    - 風險：沒有穩定版通道；想停在 v0.1.0 的人只能在 Claude Code 用 `#v0.1.0` 釘選（沒實測，README 不寫指令）。Cowork 在沒有 `version` 時怎麼顯示、怎麼更新：未驗證。使用者改過的 `model-config.json` 會更常被更新蓋掉（推論）。
    - 成本：一個小的 manifest 修改節點（strict、deep review、Security Diff Scan，改 `lock.json` 後跑 `scripts/verify_core.py`）。
  - **(d) 只拿掉 `marketplace.json` 的 `version`（可以和 (a) 或 (b) 一起選）**
    - 做法：版本只留在 `plugin.json`。
    - 結果：避免文件說的「兩邊都設」。
    - 風險：低。
    - 成本：併入 (a) 或 (b) 的修改。
  - **(e) 延後：manifest 不動，版本策略記成 follow-up**
    - 結果：和 (a) 的結果相同，但沒有記錄成需求。
    - 風險：C2 的 MUST-FIX（DR-D-01）仍然要處理，否則不能 release。
- **建議：** (c)。理由：
  1. 已知的兩份舊安裝下次更新就會拿到 release 的內容。
  2. 每個審查過的修正都能直接送到使用者，不必多一道 release。
  3. `dev-retro` 的「merged to `main` 就算 released」重新成立，這次不必改規則文字（C2 (a)）。
  4. 這是官方文件明列的做法，規則最少。
- **另外兩件事（照建議，你可以改）：**
  - 你的答案會寫成一個新需求（暫定 REQ-030，版本與 release 策略），來源記 DR-D-02、DR-S-06 和你的原話。
  - 有改 manifest 時，Cowork 不在這個 PR 重測。改成在 FU-069 記一項：release 之後，在 Cowork 按 Check for updates，確認載入的 commit。
- **如果你不決定：** manifest、README 的更新說明、C2 都卡住。不相依的工作（FU-001 紀錄、README 的 Cowork 段、CHANGELOG 改名）可以先做。
- **證據：**
  - 事實：上面列的檔案行號、官方文件段落、安裝紀錄（只讀版本與 commit 欄位）、Issue #3 留言。
  - 推論：`model-config.json` 被覆蓋的頻率；(c) 下 Cowork 的行為。
  - 未驗證：其他使用者有幾份安裝；重裝能否換掉舊 cache；Cowork 怎麼比較版本。

## C2：`dev-retro` 的「released」定義要怎麼改？（FU-027）

- **問題：** 「一個安全修正 merge 到 `main` 就算 released」這句要保留，還是改？
- **為什麼要你決定：** 這是安全規則，也是公開的規則文字（strict）。它決定「還沒修好的安全問題」的教訓什麼時候可以發布。FU-027 的觸發條件「第一次 tagged release」已經成立。
- **事實：**
  - 規則原文（`skills/dev-retro/SKILL.md`，〈### L4 lines〉前一條）："For this pack, a fix counts as released when it is merged to `main`"。REQ-026 Acceptance 有同一句。
  - FU-027 原本的前提是「第一次 tagged release 之前這句都成立」。設計審查推翻了這個前提（DR-D-01，MUST-FIX）：manifest 設了 `version`，merge 不會送到已安裝的副本（C1 的官方文件）。所以這句今天就不準。
  - 沒有任何選項能保證使用者「已經安裝」修正，只能保證「下次更新拿得到」。
- **選項：**
  - **(a) 保留原文**
    - 只有 C1 選 (c) 時成立：merge 之後，使用者下次更新就拿得到。
    - 做法：規則文字不改；FU-027 列記下這個前提與 C1 的答案。
    - 成本：無規則修改。
  - **(b) 改成「修正包含在一個改過號、打過 tag 的版本裡，使用者更新就會拿到」**
    - C1 選 (a)、(b)、(e) 時需要。
    - 做法：改 `dev-retro/SKILL.md` 和 REQ-026 那一句，加 `log.md` 一列。
    - 結果：安全教訓要等改號的 release 之後才能發布。
    - 成本：一個規則修改節點（strict、work floor、deep review、Security Diff Scan），release 會晚一些。
  - **(c) 延後**
    - 結果：錯的安全規則跟著 v0.1.0 發布。DR-D-01 是 MUST-FIX，不解決就不能 release。
- **建議：** 跟著 C1。C1 選 (c) 就選 (a)；C1 選其他就選 (b)。
- **如果你不決定：** DR-D-01 維持開啟，release 擋住。
- **證據：**
  - 事實：規則原文位置、FU-027 列（`.dev/followups.md`）、C1 的官方文件。
  - 推論：沒有選項能保證「已安裝」。

## C3：Deferred 的 finding 算不算「你在卡片裡接受的殘餘風險」？（FU-027 第二題）

- **問題：** `dev-retro` 說「你在卡片裡接受的殘餘風險，不算還沒修好的安全問題」。一個只標成 Deferred 的 finding 適用嗎？
- **為什麼要你決定：** FU-027 要求你決定這一點。這會影響安全教訓能不能提早發布。
- **事實：**
  - 規則原文：「a residual risk that the user accepted in a card is not a security problem that is not fixed」。
  - Core `review-and-security.md` 的 Deferred 必填欄位裡沒有「接受」（設計審查 DR-D 回答 3）。
- **選項：**
  - **(a) 不算，規則文字不改（建議）**
    - 做法：只有你在卡片裡點名接受的那一項才算。Deferred 本身不算接受。FU-027 列記下這個讀法。
    - 成本：無規則修改。
  - **(b) 不算，並在規則裡加一句寫明**
    - 成本：一個規則修改節點（strict、Security Diff Scan）。
  - **(c) 所有 Deferred 都算**
    - 風險：一個只是延後的安全問題，教訓可能在修好前就發布。不建議。
- **建議：** (a)。理由：現有文字已經要求「在卡片裡接受」，Deferred 不是接受；不加新句子。
- **如果你不決定：** FU-027 維持開啟。release 不受影響。

## C4：R-DEL-2 的 floor 要不要涵蓋 release 和 packaging 工作？（FU-036）

- **問題：** 工作 floor（tier 3、effort `high` 以上）目前只列安全、資料、migration、對外契約。要不要加上 release 和 packaging？
- **為什麼要你決定：** 這會改 R-DEL-2 的規則文字；不改也是一個要記錄的決定。
- **事實：**
  - R-RIG-1 把 release 和 packaging 列為 `strict`，但 R-DEL-2 的 floor 清單沒有它們（`skills/dev-core/SKILL.md`）。
  - `strict` 的 implement 角色已經是 `opus`、`high` 以上（`model-config.json` 的 `implement`）。審查和掃描都是 `opus`/`xhigh`。
  - 剩下的缺口：explore 節點可以用 `haiku`/`low`；主 session 自己實作低於 `high` 時，只要在計畫裡寫一句（FU-036 列）。
  - 這個 repo 以前沒有任何 tag（`git tag -l` 為空），所以沒有過去的 release 節點可以算成本。
- **選項：**
  - **(a) 不改，關閉 FU-036（建議）**
    - 結果：release／packaging 中不屬於其他 floor 類別的部分，explore 仍可用較低設定。
    - 重新開啟的條件：出現一次 release 或 packaging 工作低於 floor 而出錯的實例。
    - 成本：無。這不算放寬（規則不變）。
  - **(b) 依類別加入：release 和 packaging 進 floor 清單**
    - 做法：改 R-DEL-2 一句，以及它的副本（REQ-009、DL-034、設計文件 section 4）。
    - 成本：一個規則修改節點（strict、deep review、Security Diff Scan），release 會晚一些。之後這類 explore 節點的費用變高。
  - **(c) 依 tier 加入：所有 `strict` 工作都套 floor**
    - 和 (b) 的差別：也涵蓋因其他原因被定為 strict 的工作，並且把「a `strict` tier」放回 R-DEL-2 的 session 那句（卡 I75-D3 (b)）。
    - 成本：比 (b) 多，影響面也較大。
- **建議：** (a)。理由：release 的高代價步驟（tag、Release、merge）都有人工關卡和掃描；審查與實作角色已在 floor 以上。缺口只剩 explore 節點，出錯代價低（推論）。
- **如果你不決定：** FU-036 維持開啟。release 不受影響。

## C5：engineering-workflow-core#40 還沒回答，要等嗎？

- **問題：** 現在就發布 v0.1.0，還是等 Core 回答 #40？
- **為什麼要你決定：** #40 如果回答 Reading A，已發布的 v0.1.0 在 read-back 範圍上會比 Core 寬鬆，只能靠下一版修正。
- **事實：**
  - DL-049 (2) 只在 merge 前讀回三項 dispatch，其他記為 `unknown`。它對 Core `workflow.md:57` 的讀法自己標成推論（`skills/dev-core/deltas.md` DL-049）。
  - #40 是 open，沒有留言（`gh issue view 40 --repo jeffery777/engineering-workflow-core`，2026-11-14）。
  - FU-067 的觸發條件包含「#40 回答 Reading A」。
- **推論（兩位設計 reviewer）：** 不擋。同一條規則今天已經在 `main` 上；打 tag 不改變使用者實際跑的內容；floor、dispatch 值和主 session 的 floor check 都還在。沒有安全上要擋的理由。#38、#39 也不擋。
- **選項：**
  - **(a) 現在發布，在 `[0.1.0]` 的限制段寫明 DL-049 的讀法是推論，並連到 #40（建議）**
  - **(b) 等 #40 回答再發布**
    - 成本：release 時間未定。
- **建議：** (a)。
- **如果你不決定：** 打 tag 前要再問一次。PR 可以先做。

## C6：PR 要寫 `Closes #114` 嗎？

- **問題：** PR 寫 `Closes #114`（orchestrator 的 brief 這樣要求），還是改成 `Part of #114`？
- **為什麼要你決定：** 這和 brief 的指示不同（DR-D-03）。
- **事實：**
  - Issue #114 的 Done when 第 2 項是 tag 和 Release 存在並已讀回。
  - `Closes #114` 會在 merge 時就關閉 Issue，那時 tag 和 Release 都還沒有（GitHub 的關鍵字行為，這次沒有重測）。
- **選項：**
  - **(a) `Part of #114`，保留 `Closes #3`；orchestrator 讀回 Release 後再關 #114（建議）**
  - **(b) 照 brief：`Closes #114` 和 `Closes #3`**
    - 風險：Release 失敗時，追蹤用的 Issue 已經關了，要重開。
- **建議：** (a)。
- **如果你不決定：** 照 brief 用 (b)。
