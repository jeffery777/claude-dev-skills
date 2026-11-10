# Issue #106 PR-1 redesign, implementation review round 1

Written per ASD-STE100 principles; full conformance not verified.

Target: the index on PR #107 head `e71b2eb793b9c0d2a4f5d00df7dd2637457aa04c`,
16 staged files, SHA-256 of `git diff HEAD --binary --no-ext-diff --no-textconv`
= `850d7f7b…282c`. The rules at the base govern these reviews.
CB-4 by the main agent before and after both reviews: status `a6eb6ed8…a150`,
diff `850d7f7b…282c`; exit 0; equal.

| Review | Agent | Requested | Recorded |
| --- | --- | --- | --- |
| P1R-deep | `dev-reviewer` | opus/xhigh | `unknown`, case `not read back` |
| P1R-sec | `dev-security-reviewer` | opus/xhigh | `unknown`, case `not read back` |

| ID | Severity | Triage | Disposition |
| --- | --- | --- | --- |
| P1RD-01 | MUST-FIX | card C4 told the user that `accept` shows the date and words of a record; it did not (Core :29 decision on true facts) | Fixed: `accept` first shows the current record's date and words, or that it is missing or unreadable; tested |
| P1RD-02, P1RS-05 | SHOULD-FIX / NIT | card C5 (b) says "with its date"; the reference and D-032 did not | Fixed |
| P1RD-03 | NIT | REQ-007 said C3 (a) was superseded | Fixed: C4 (a) supersedes C1 (a); C5 (b) says where the C3 (a) decision is given |
| P1RD-04 | SCOPE-CREEP | README hardening bullet had no requirement source (the user asked for the reasons) and implied an unverified subagent effect | Fixed by deletion (both languages) |
| P1RS-01 | SHOULD-FIX | R-REV-1 kept apply sentences outside the digest (DR4-02) | Fixed by deletion: R-REV-1 keeps one sentence and the pointer; the reference holds the rest; the test asserts them in the reference |
| P1RS-02 | NIT | the stop for "record does not apply" was not stated | Fixed in the reference |
| P1RS-03 | NIT | a relative `HOME` could find a file in the worktree | Fixed: a relative or root home gives `STOP NO_RECORD` (checked in-process by P1R-R2; the unit test does not tell the guard apart, P1RR-02) |
| P1RS-04 | NIT | `GIT_DIR` redirects the key | Kept as is (no recorded agent error; CB-4 follows the same variables) |
| P1RS-06 | NIT | inode reuse on other file systems | Fixed: the reference sentence is hedged |

Residual items fixed: the reference lists the output codes (except `STOP NO_RECORD` of `accept` under a relative or root home, P1RR-01); README says the
main agent gives the full command with the pack root in the chat; a test
writes a record and checks `PASS`; R-REV-1 wording "the check that … gives";
"the user's record" in the agent rule. Kept as is: the README word "ignore"
(the page: "These fields are ignored when loading agents from a plugin",
verbatim per the fetch agent); `__pycache__` files (ignored, not staged).
K14 note: the plan row said exit 1; after the plan text was added it hits only
`.dev/issue-106/plan.md`, which gets no row.

## Round 2 (narrow confirmation, P1R-R2)

Dispatch: `dev-security-reviewer`, requested opus/xhigh, recorded `unknown`,
case `not read back`. CB-4 by the main agent before and after: status
`dc377a89…442d`, diff `96707bad…e60f`; exit 0; equal. Result: every round-1
disposition applied.

| ID | Severity | Triage | Disposition |
| --- | --- | --- | --- |
| P1RR-01 | NIT | under a relative or root home, `accept` asks first and then stops with `STOP NO_RECORD`, which the reference does not list for `accept`; fails closed, no write; no requirement | Kept as is (record wording corrected above) |
| P1RR-02 | NIT | the relative-home test passes with or without the guard; the guard works (in-process check) | Kept as is (record wording corrected above) |

Observations kept as is: D-032 item 6 wording ("the D-032 scope of C3 (a)");
`accept` prints the current-record line before the accepted text (order only).

## Correction of P1RD-04 (after the push of `39d332d`)

The user's own words, relayed by the orchestrator (2026-11-09): 「關於README 的
P1RD-04，原本的建議是"沒有有效紀錄時檢查會停下，README 會說明怎麼建立紀錄。"，這我
同意。我的想法是希望README裡也要寫上原因，否則其它人可能也會和我一樣有相同的擔憂。
畢竟這是因為原生功能的一種妥協，不是你和我不願意做。我的原意不是只要求寫原因」.
The triage of P1RD-04 ("the user asked for the reasons"), read as "only the reasons", is wrong. The
README gets back one line on the optional session sandbox, with only the
verbatim fact of the official page (sandboxing.md, "Scope": "Bash commands
inside a subagent are sandboxed when sandboxing is enabled in the parent
session.", read by a fetch agent, 2026-11-09). `permissions.deny` is not on
that page verbatim, so it is not written. The line says that it does not
make the reviewers read-only and does not replace the record. A third
commit carries it.

## Merge Review fixes (head 92492bf)

The orchestrator's Merge Review, head security review and merge readiness
scan of head `92492bf` (relayed, 2026-11-09; read-back PASS, opus/xhigh, in
the orchestrator session). The user's words to the orchestrator: 「現在修，連
NIT 一起」.

| ID | Severity | Disposition |
| --- | --- | --- |
| MR107B-01 | MUST-FIX | Fixed: the setup-change rule (reference) and D-032 item 5 (both languages) say "with its date and the change it was given for", as card C5 (b); plan C5 (b) summary corrected. The version is raised to 2, as the Version rule of the reference says for a change of meaning (first written as "stays 1"; P1DR-01 below; renamed from P1D-01, which `pr1-round-1.md` already uses, MR107C-01); the Accepted text is unchanged |
| MR107B-02 | NIT | Fixed: the REQ-024 C1 (a) source and note say that C4 (a) supersedes C1 (a); plan K11 row corrected; `log.md` row |
| MR107B-03 | NIT | Fixed: D-032 origin says which words are in the Issue body and which came only in the orchestrator's message |
| SEC107B-01 | NIT | Fixed: README (both languages) keeps the re-clone sentence with the inode hedge of the reference |
| SEC107B-02 | NIT | Fixed: the test's Git calls use a clean environment (no `GIT_*`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `commit.gpgsign=false`), as `tests/test_push_precheck.py` |

Narrow review of these fixes (P1D-REV, `dev-reviewer`, requested opus/high,
recorded `unknown`, case `not read back`; CB-4 before and after equal: status
`c634bf38…71e1`, diff `ec826009…3357`): all five applied. New finding:

| ID | Severity | Triage | Disposition |
| --- | --- | --- | --- |
| P1DR-01 | NIT | "version stays 1" was outside the Version rule of the reference (a change of meaning raises the version) | Fixed: `ACCEPTANCE_VERSION` 2, the Accepted text heading, the version table (1 never in a merged pack; 2 adds "the change it was given for"), `PINNED` keeps 1 and adds 2; D-032 item 5 notes the version |
