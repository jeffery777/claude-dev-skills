# Issue #106 卡片（PR-1 review 之後）

請在本 session 直接打字回答，例如「C3 a」。轉述的答案不算：這題是 D-032 接受範圍的一部分（Core `review-and-security.md:29`）。

回答（使用者在本 session 的訊息，2026-11-09）：「C3 a」。

## I106-C3：變更改到 reviewer 設定或 D-032 本身時，那次變更的 review 怎麼算？

- 問題：當一個變更改到 reviewer 的 agent 檔、`check_pack.py` 的釘選、D-032，或 D-032 涵蓋的規則（R-REV-1 套用它的句子、CB-4、CB-5），這次變更的 review 要怎麼計入？
- 為什麼要你決定：
  - 卡片 C1 給你看的事實寫：「改到 reviewer 的 agent 檔、釘選或 D-032，這次變更的 review 不適用 D-032，要你重新接受」。
  - 你回答之後，我把它縮小成「只看 agent 檔的 `tools` 和 `disallowedTools` 行」，沒有再問你。這等於我推定你接受縮小後的範圍，Core 不允許（P1D-01）。
  - 規則也沒寫「重新接受」怎麼落地。照現在的寫法，記錄新接受的那次變更，它自己的 review 永遠不能算數，會卡死（P1D-02、P1S-02）。
- 事實：
  - PR-3 會改 `agents/dev-security-reviewer.md` 的內文（掃描清單），PR-2 會在 R-REV-1 新增一個 cite（`.dev/issue-106/plan.md`）。
  - pack 沒有不帶寫入通道的 reviewer（CB-5）。
  - PR-1 自己的 review 照 base 的規則跑，不受這題影響。
- 選項：
  - **(a) 回到卡片的範圍，並寫明重新接受怎麼落地。**（建議）
    - 內容：變更改到 reviewer 的 agent 檔（整個檔）、釘選、D-032 或 D-032 涵蓋的規則時，這次變更的 review 只有在你為這次變更新給、有引述的決定之下才算數。決定記在這次變更裡。新增或移動 cite 與行號不算改到規則。
    - 結果：PR-3 開始前，我會請你對 PR-3 給一個決定。PR-2 只新增 cite，不需要。往後要把別的 repo 加進 D-032，也走同一條路。
  - **(b) 維持縮小後的範圍（只看 `tools` 和 `disallowedTools` 行），也加上落地方式。**
    - 內容：同 (a) 的落地方式，但只改 agent 檔內文的變更（例如 PR-3）照常適用 D-032，不用問你。
    - 代價：agent 檔內文的 Bash 使用說明改了，你不會被問到。
  - **(c) 不加落地方式，只回到卡片的範圍。**
    - 結果：改到這些檔案的變更一律停在必要 review，包括 PR-3。之後要另開 Issue 處理。
