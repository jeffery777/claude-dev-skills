# Issue #106 卡片（設計 v4：接受紀錄放在你自己的電腦上）

請在本 session 直接打字回答，例如「C4 a，C5 b」。轉述的答案不算：C4 是你本人的接受（Core `review-and-security.md:29`）。

回答（使用者在本 session 的訊息，2026-11-09）：「C4 a，C5 b」。

上一版的 C6（只支援 GitHub、一個 repo 一個帳號）已刪除：新設計不比對帳號和 repo，也不需要 `gh` 和網路。

## I106-C4：接受 reviewer 寫入通道的殘餘風險嗎？PR-1 merge 之後，由你自己建立紀錄。

- 問題：你要不要接受 reviewer 保留 Bash 的殘餘風險？如果接受，PR-1 merge 之後你要在自己的終端機跑一次 `accept`，為這個 clone 建立紀錄。
- 為什麼要你決定：Core 規定接受要由你本人決定，agent 不能推定（`review-and-security.md:29`）。
- 事實：
  - 這張卡取代你在 C1 (a) 選的「綁帳號加 repo」。新做法不再檢查 `gh` 帳號或 remote：同一台電腦上換了 `gh` 帳號或 token，或 clone 換了 remote，檢查都不會停下（推論，依設計 v4 第 3 點）。
  - 紀錄存在你電腦的 `~/.claude/dev-skills/reviewer-acceptance/`，不放進 repo，也不經過 git。每個 clone 一個檔案，檔名是 clone 的 `.git` 資料夾（路徑和 inode）的 hash。內容只有版本、你的原話和日期，沒有帳號、repo 名稱或路徑。
  - 建立紀錄的 `accept` 會先逐字印出 reference 裡你要接受的那一段，再請你打原話，最後要你打 `yes` 確認；打別的、空白或中斷，都不會寫入。
  - `accept` 只在 stdin 和 stdout 都是終端機時才執行。本 session 實測過：agent 的 Bash 沒有終端機（`isatty` 是 `False`）。所以 agent 直接跑 `accept` 會被擋下。擋不住的情況：agent 用 pseudo-terminal 跑，或用別的工具直接寫檔，或某些主機模式下 agent 的 shell 有終端機（未驗證）。規則禁止這些做法。README 會請你在另一個終端機視窗跑，不要透過 Claude Code 跑。
  - 你接受的是版本 1 的 pack 文字（`skills/dev-core/references/reviewer-acceptance.md`），內容和 PR #107 的 D-032 相同，只是不寫任何名稱。以下是摘要，完整內容是 `accept` 印出的全文：
    - 寫入通道：兩個 reviewer 的 Bash，可以寫 worktree、`.git`、repo 外和網路（例如用你的 `gh` token）。
    - 偵測：CB-4。
    - 偵測不到：worktree 和 index 以外的一切，以及改了又改回的修改。
    - 寫入通道還包括：主機在 agent 檔之外給 subagent 的任何工具（執行時是否限制工具，未驗證，FU-004）。
    - 偵測不到的還有：未追蹤檔案內的修改、ignored 檔案、其他 worktree、plugin 載入的 checkout、review 以外的時間、主機權限設定的改變。
    - 任務指明其他受保護資源，或要求技術隔離時，紀錄不適用。
    - 不免除：獨立審查、必要掃描、exact-head、資料保護、操作授權。
  - pack 改變這份文字、CB-4、CB-5、`dev-retro` 的 read-back 那一節的意思，或改了 reviewer 的工具行，版本號就會提高。你的紀錄會停下，要再跑一次 `accept`。
  - 搬移或重新 clone 這個 repo、還原家目錄、換電腦時，也要再跑一次 `accept`。
  - 限制：`accept` 需要你自己電腦上的終端機，以及會保留下來的家目錄。雲端或網頁 session、CI、每次重建的容器沒有這些，那裡的必要 review 會一直停下（推論，未驗證）。原生 Windows 能不能用，也未驗證。
  - 每次必要 review 前的檢查只讀本機檔案、印一行結果，不需要網路。GitLab、沒有 remote 的 repo、離線環境都能用。
  - 殘餘風險：agent 如果出錯，用別的工具直接寫出這個檔案，script 擋不住。規則禁止 agent 這樣做；你下次跑 `accept` 或打開檔案時，看得到日期和原話。
- 推論：Core 沒有規定紀錄要放在 repo 裡或在 PR 上看得到（`review-and-security.md:29-35`），所以這個做法不必回報上游。
- 選項：
  - **(a) 接受。**（建議）PR-1 merge 之後，你在這個 clone 的頂層跑一次 `accept`。
  - **(b) 不接受。** PR-1 merge 之後，每個必要 review 和掃描都會停下，直到有唯讀的 reviewer 可用，或你改變決定。

## I106-C5：改到 reviewer 設定的變更，你為它給的決定一定要在派 review 的 session 裡親自打字嗎？

- 問題：變更如果改到 reviewer agent 檔、`check_pack.py` 的釘選、檢查 script、reference、釘住的 digest、D-032，或紀錄涵蓋的規則，它的 review 除了檢查要 `PASS`，還要有你為這次變更給的、有引述並記在變更裡的決定（C3 (a)）；這個決定也要寫明版本號要不要提高。這個決定一定要在派 review 的 session 裡由你親自打字嗎？
- 為什麼要你決定：規則沒寫；之前的卡片都要求你在本 session 回答。
- 事實：
  - merge 前的 Merge Review、security review 和 merge readiness scan 由 orchestrator session 派，merge 也在你同意之後由它執行（orchestrator 給本 session 的任務說明，2026-11-09）。
  - pack 現有的轉述規則（R-DEL-2 的 Relayed answers）只管 model 和 effort，不管其他決定（`skills/dev-core/SKILL.md:177`）。其他轉述算不算，由各自適用的規則決定（R-EVD-3）。
  - merge gate 的「設定變更」卡片只看 `.dev/config.json`（`skills/dev-gate/SKILL.md:112-114`），不會自動列出這類變更。
- 選項：
  - **(a) 可以來自同一件工作的其他 session。** 原話、日期和它是為哪個變更給的，都記在變更裡。
    - 風險：agent 轉述錯誤或捏造原話時，只能靠你在 merge 卡片上讀到才擋得住。
  - **(b) 一定要在派 review 的那個 session 裡親自打字。**原話、日期和它是為哪個變更給的，同樣記在變更裡。（建議：你說過要用工作流程把出錯的可能降到最低）
    - 代價：寫變更的 session 和 orchestrator 都要你各回答一次。
