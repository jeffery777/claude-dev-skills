# Issue #106 卡片（PR-3 開始前）

請在本 session 直接打字回答，例如「C7 a」。

回答（使用者在本 session 的訊息，2026-11-09，為 PR-3 這次變更，即 branch `issue-106-pr3-publication-data` 的變更）：「C7 a」。轉述的答案不算：依卡片 I106-C5 (b)，改到 reviewer 設定的變更，你的決定要在派 review 的那個 session 由你親自打字。

## I106-C7：PR-3 要改 `agents/dev-security-reviewer.md` 的掃描清單，你同意這次變更，並維持接受版本 2 嗎？

- 問題：PR-3 會改 `agents/dev-security-reviewer.md` 的本文，也就是 reviewer 照著掃描的清單。這屬於 setup change。依規則，PR-3 的 review 和掃描除了檢查要 `PASS`，還要有你為這次變更給的決定，並寫明版本號要不要提高。
- 為什麼要你決定：`skills/dev-core/references/reviewer-acceptance.md` 的 Setup change 一節（卡片 I106-C3 (a)、I106-C5 (b)）。
- 事實：
  - PR-3 只改這個 agent 檔的本文，讓它跟上 R-REV-9 的新內容：Release 的標題、說明和 tag、附件、貼文的目的地 repo、貼出去的必須是掃描過的那個檔、要找的私人資料多了憑證、帳號和不必要的執行紀錄，以及 commit 前要回報 Git 會不會簽章。`tools:` 和 `disallowedTools:` 這兩行不改（`agents/dev-security-reviewer.md:6-7`）。
  - 版本號綁住的是 reference、CB-4、CB-5、`dev-retro` 的 read-back，以及兩個 reviewer 的工具行（`tests/test_reviewer_acceptance.py` 的 `pinned_digest`）。agent 檔本文不在裡面，所以 PR-3 改了也不會讓測試失敗。
  - R-REV-9 本身不是接受紀錄涵蓋的規則（reference 的 Setup change 一節）。
  - 這個決定只對 PR-3 有效。之後在 merge 前，orchestrator 也會派 review，所以你也要在 orchestrator 的 session 親自回答一次。
  - 在你跑 `accept` 之前，本 session 的檢查會印 `STOP NO_RECORD`，必要 review 和掃描都不算數。
- 推論：版本維持 2 不需要改任何被釘住的文字。
- 選項：
  - **(a) 同意 PR-3 改 `agents/dev-security-reviewer.md` 的本文，版本維持 2。**（建議）
  - **(b) 同意，但提高到版本 3。** 你和其他使用者都要重新跑一次 `accept`。要先把版本規則的範圍擴大到 agent 檔本文，才有理由提高版本。
  - **(c) 不同意。** PR-3 不改這個 agent 檔。agent 檔裡的掃描清單會和 R-REV-9 不一致，違反 REQ-022（單一來源）的要求，PR-3 會停下等你另做決定。
