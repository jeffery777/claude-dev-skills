# Issue #104 卡片（設計審查後）

請在本 session 直接打字回答，例如「C1 a，C2 a」。轉述的答案不算，因為這兩題涉及放寬。

## I104-C1：Q2 之後，還算符合 Core 的「核對 effort」嗎？

- 問題：Core `workflow.md:56` 寫「由各接口核對實際生效的 model/effort」。Q2 之後，只有 Merge Review、merge 前的 security review 和 merge readiness scan 會做 read-back，其他 dispatch 都不做。
- 事實：
  - `deltas.md:5` 寫 Relaxing Core 一律是缺陷，使用者的同意也不能放寬 Core。
  - Core `workflow.md:64` 寫模型與 effort 的控制「皆由接口承擔」。
  - read-back 只讀 transcript 記的值，實際生效值一直是 `unknown`（R-DEL-2）。
  - deep reviewer 無法判定這算不算 Core blocker，依 R-REV-3 列為 MUST-FIX（`reviews/design-round-1.md` DR-D-01）。
- 推論：`workflow.md:56` 是接口層的義務，不是每次 dispatch 都要核對。留下的核對是：dispatch 傳兩個值、`check_pack` 釘住 agent file、REQ-009 的 tested-host record、主 session 的 floor check、merge 前三項 read-back。
- 未驗證：Core 作者是否這樣讀；Core v0.4.1 的文字我沒有讀。
- 選項：
  - (a) 接受這個讀法，寫進 DL-049 和 D-031，標為推論。Core 更新時再對照一次。（建議）
  - (b) 不接受，Q2 退回，read-back 維持現狀。這個 PR 只做其他項目。
- 建議 (a)。理由：本來的 read-back 也沒有核對到實際生效值，而且 Issue #104 記錄的取樣裡沒有抓到錯誤值。

## I104-C2：確認這些放寬嗎？

- 問題：這幾項是放寬，只有使用者能決定。我只在 Issue #104 讀到，沒有看到你的原話。
- 內容：
  1. Q1：R-VER-2 回到 Core 層級，只有 MUST-FIX、需求改變或放寬才停給使用者。
  2. Q2：read-back 只留 merge 前三項。
  3. Q3：Issue 和 PR 文字的掃描只看私人資料，不看事實精度。agent 和 effort 不變，因為 Issue 把 effort 列在範圍外。
  4. Issue Scope（不在「同意」那段）：GitHub 在 merge 或 squash commit 上的簽章只記錄，不問你。
  5. Issue Scope：你接受過的殘餘風險，同一件工作的後續 PR 不再提。
  6. Issue Scope：R-REV-4 先判斷威脅範圍和需求，才修。
- 影響：紀錄寫進 DL-049，來源是你在這裡的回答。
- 選項：
  - (a) 全部確認。（建議）
  - (b) 確認其中幾項，請列編號，其餘說明要怎麼改。
- 未驗證：第 3 項的「lighter」你是否也想降 effort。若要降，要改 role 和 floor，屬於另一個 Issue。
