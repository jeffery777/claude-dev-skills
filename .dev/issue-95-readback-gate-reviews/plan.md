# Issue #95 plan: read-back gate for required reviews and scans (Issue #79 slice C2)

- Objective: GitHub Issue #95 (body rev 3), slice C2 of the tracking Issue
  #79: the main agent reads back the recorded model and effort of every
  required review and R-REV-9 scan with the read-back script of Issue #89,
  under the rules of slice C1, and a review or scan whose read-back does not
  pass does not count as the required review or the R-REV-9 scan.
- Rigor `strict`. Reason (R-RIG-1, re-assessed at Discover as R-RIG-2
  says): a change to a security rule (R-DEL-2, R-REV-9) and to pack rule
  text.
- Base: `main` d28a14e, branch `issue-95-readback-gate-reviews` (created
  from Issue #95 on GitHub).
- Spec: design rev 3 of 2026-10-31 (no design review round 3, by card
  I95-R2-C1 (c); the implementation reviews gate it).
- Method (lesson of slices C0 and C1): no word of an existing sentence
  changes; the slice adds sentences, and a deterministic word diff checks
  the pack files and the changed record files.

## Source trace (dev-plan step 2)

Sources: the Issue #95 body rev 3; the Issue #79 body (Change 2); the slice
B dependency table and the Issue #77 limit in REQ-009; FU-021, FU-044,
FU-049 to FU-051, FU-054 and FU-055; and these user answers (Claude Code
session, the user's words in the orchestrator session, relayed):

- 「I79C-C1 a，C2 b，C3 c，C4 a，這些我同意你的建議」 (2026-10-30): slice C2 is
  the reviews and scans; a `light` routine review at `sonnet`/`medium` skips
  the gate until FU-049, its `recorded` value stays `unknown`, residual
  risk.
- 「同意，兩點放進 C2 開頭，開始 C2」 (2026-10-31): the two points of the C1
  smoke test go first. Design round 1 narrowed point 1 to a literal base ID
  only; that the user accepted the narrowing is an inference from the
  relayed sentence "The user did not ask to keep `${B}`", not the user's
  words.
- 「I95-C1 c，C2 a，C3 b，另開模型設定檔 Issue 取代 FU-049」 (2026-10-31):
  I95-C2 (a), the allowlist dead end is a residual risk with its recovery
  path, and Issue #96 replaces the scope of FU-049; I95-C3 (b), a native
  pass in a subagent is read back and is the primary pass only when it
  counts. I95-C1 (c) is replaced by the next answer.
- 「I95-R2-C1 c，R2-C2 c，Merge Review 改由 orchestrator 做」 (2026-10-31):
  every review and scan counts only in the session that dispatched it as a
  subagent and read it back; the session that merges dispatches and reads
  back the Merge Review, the head security review and the merge readiness
  scan; costs in FU-057.

From the design reviews of rounds 1 and 2, not from the user's words: the
other sentences of rev 3 (finding IDs in rev 3).

## Insertion points (checked by hand, lessons D1-07 and D2-04)

The next sentence after each insertion was read for a pronoun or back
reference ("this", "that", "they", "it", "such", "those", "the previous
paragraph") whose reader the insertion changes.

| Point | Anchor | Next sentence | Result |
| --- | --- | --- | --- |
| A1 | R-DEL-2 read-back bullet, after the `git … cat-file blob <full base ID>:… \| python3 -I - subagent …` sentence | "The main agent finds the base itself …" | no back reference; "there" in the sentence after it still means the base |
| A2 | after "When they show more than one agent ID … `unknown`." | "`<DIR>` comes only from …" | no back reference; "they" of the anchor keeps its reader (it comes before A2) |
| A3.1 to A3.7 | end of the bullet, after the FU-054 sentence | next bullet "From a transcript, read only …" | new bullet, no back reference |
| A4 | first R-REV-9 line, after "… never `not applicable`." | sub-bullet "Show content, not encoded data …" | no back reference |
| B1 | first paragraph of the script reference, after "… before Issue #93." | next paragraph "The script is …" | no back reference; "The second and the third sentence of this paragraph" still counts the same sentences |
| B2 | new section before "## What it cannot prove" | first bullet "A recorded value is not …" | no back reference |
| B3 | new last bullet of "## What it cannot prove" | end of file | none |
| B4 | end of "## Allowlist" | heading "## Threat model" | none |
| C1 | new paragraph after the paragraph that ends "… never `dev-reviewer` (R-REV-1)." | "For a commit / push scan, the target is …" | no back reference |
| C2 | step 3, after "Dispatch the reviewer subagent with a brief (R-DEL-1)." | "Give the target, the context paths, …" | no pronoun; the implied object of "Give" stays the brief of the same dispatch |
| C3 | native option, after "… and in which context." | "A native pass that runs in a context with write tools …" | no back reference |
| C4 | step 4, after "Read the report back." | "Check that each finding has …" | no back reference |
| D1 | new template line after `- Reviewer:` | `- Scope:` line | none |
| E1 | commit order step 2, after "… the commit will carry." | step 3 "Pass the `dev-gate` commit gate …" | no back reference |
| E2 | step 4, after "… for the user's decision (R-REV-9)." | step 5 "… push with exactly those arguments" | "those arguments" still means the dry-run arguments of step 4; E2 names no arguments |
| E3 | paragraph after the list, after "… stop before the commit or push (CB-4)." | heading "## Output" | none |
| F1 | step 7, after "… scanned before it is posted (R-REV-9)." | heading "## Output" | none |
| G1 | step 2, after "A previous head's verdict is never reused (Issue #68, E2)." | step 3 | none |
| G2 | step 3, new paragraph after its bullet list, indented three spaces | step 4 "Check the blockers …" | "that review" of G2 means the deep review of the first bullet; the paragraph has the indentation of the step 3 text, after a blank line, so it closes the bullet list and stays in step 3, and step 4 keeps its number |
| G3 | step 4, new bullet after "a missing R-REV-9 scan, …" | bullet "an unresolved substantive security risk …" | no back reference |
| G4 | Output block, after the "Commit / push security scan" line | "Requirement trace:" line | none |
| H1 | Evaluate a handoff step 2, first bullet, after its last sentence "… the floor check of R-DEL-2 applies (`dev-core`)." | second bullet "Once a PR exists, never commit the checkpoint …" | no back reference; "that commit" of H1 means the checkpoint commit of the same bullet |
| H2 | second bullet, after "… without that scan, do not post." | "The checkpoint points to the review and gate records and does not repeat them." | "them" is inside its own sentence; no back reference to H2's place |

Records: the REQ-009 note after the slice B dependency table follows the
existing Issue #93 note; the D-028 sections follow D-027 in each language;
the section 4 note in English follows the Issue #93 note in the paragraph
on starting sessions and subagents (the next sentence "A started session
still …" has no back reference). In Chinese, the paragraph has no
whitespace between its sentences, so a note in the middle would change a
word token; the note goes at the end of the same paragraph, after "下一段是轉述的使用者回答唯一的例外。" and one space, and a new paragraph
there would change the reader of 「前一段」 in the next paragraph.

## Counts and wording

- The count in the script reference (B2) is the state at design rev 3:
  seven background dispatches (the C1 smoke test and six Issue #95
  dispatches at `opus`/`xhigh`). Dispatches after rev 3, T1 included, are
  not in it.
- DL-043 names cards I95-R2-C1 (c) and I95-R2-C2 (c) without the quote
  「I95-R2-C1 c，R2-C2 c，Merge Review 改由 orchestrator 做」, which REQ-009,
  D-028, the log and the CHANGELOG carry: the files under `skills/` keep no
  hit of the word "orchestrator" (0 at the base, 0 after the change).
- The follow-up rows whose status cell is "Open" get the note as
  "Open — Note (Issue #95): …", so that the word "Open" stays one word
  token.
- The front matter of REQ-009 gets the two new quotes of rev 3; the quote
  「同意，兩點放進 C2 開頭，開始 C2」 is in the slice C2 group, D-028, the log
  and the CHANGELOG.

## Dispatches and floor check

| Node or step | Agent | Requested | Recorded | Effective |
| --- | --- | --- | --- | --- |
| C1 smoke test | `dev-explorer` | `opus`/`high` | `opus`/`high` (`PASS`, copy at the bound base; design rev 3 facts) | `unknown` |
| Issue text scans (first body, rev 2) and design rounds 1 and 2 | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `opus`/`xhigh` (`PASS` each, six read-backs; design rev 3 facts) | `unknown` |
| T1 | `dev-implementer` | `opus`/`high` | main agent fills in (R-DEL-2) | `unknown` |

## Word-diff check

Command (bash, `set -o pipefail`, base pinned, run on the working tree
before the commit; the nine pack files, and then the six changed record
files that exist at the base, as separate arguments):

```
git --no-replace-objects diff --no-ext-diff --no-textconv --no-color --text --word-diff=porcelain --word-diff-regex='[^[:space:]]+' d28a14e2df2c1030ee07c64ed206cbd1d6130f30 -- <files> | LC_ALL=C grep -E '^-' | LC_ALL=C grep -Ev '^--- (a/|/dev/null)'; test $? -eq 1 && echo NO-WORD-REMOVED
```

Result on the working tree (T1): `git=0` and `NO-WORD-REMOVED` for the nine
pack files (71 added word lines) and for the six record files; the `-R`
count of each of the fifteen files is above 0. The result at the committed
head goes into a PR comment (R-EXH-3).

## Implementation review round 1

Deep review and Security Diff Scan at `opus`/`xhigh`, read back by R-DEL-2.
The user's words in the orchestrator session, relayed:
「I95-I1-C1 a，C2 a，不認得的 ID 只提醒併入 #96，#96 排在 C2 之後」 and, as
the confirmation of the threat model,
「對，你身為任務編排的責任盡到了、子session的任務盡到了就行，用戶惡搞，那就是用戶自己要負責。」

| Finding | Disposition |
| --- | --- |
| C2R1-D-01 (the re-run of `dev-review` after a trigger on a `light` review) | Fixed by card I95-I1-C1 (a): one added R-DEL-2 sentence |
| C2R1-D-02 (REQ-009 `sources:`) | Fixed: three chat sources; the log line gives five sources |
| C2R1-D-03 (FU-021 and FU-050 notes) | Fixed: "— " before "Note (Issue #95)" |
| C2R1-D-04 (FU-058 line count) | Fixed: 239 lines at `d28a14e` |
| C2R1-D-05 (an `opus` model outside the allowlist) | Deferred to FU-049 (its owner, verification plan and trigger columns; FU-049 stays Open until Issue #96, which takes its scope, is merged). Card I95-I1-C2 (a): a residual risk in D-028 (both languages), the REQ-009 slice C2 section and the CHANGELOG, records only |

Fix revision of the Fixed rows: the diff of round 2 (sha256 `204d5926…f302`); re-reviewed in round 2.

Security Diff Scan: 0 findings.

## Implementation review round 2 (narrow confirmation)

Deep and Security Diff Scan at `opus`/`xhigh`, both read back `PASS`, on the diff with sha256 `204d5926…f302`. Findings: C2R2-D-01 (SHOULD-FIX, `light` exception, headless: the escalation re-run of card I95-I1-C1 (a) is not excluded from the headless sentence of R-DEL-2); C2R2-D-02 = C2R2-S-02 (NIT: record summaries without the card I95-I1-C1 (a) exception); C2R2-S-01 (NIT: "every review and scan does not count" leaves out the `light` exception). The `light` exception needed fixes and produced a new problem in two consecutive rounds, so the R-VER-2 stop held; stop card I95-I2-C1, answer (the user's words in the orchestrator session, relayed): 「I95-I2-C1 a」.

| Finding | Disposition |
| --- | --- |
| C2R2-D-01 | Deferred to FU-056 (its owner, risk, verification and trigger columns). Card I95-I2-C1 (a), residual risk: D-028 residual risk 9 (both languages), REQ-009 slice C2, FU-056 note; no pack text change |
| C2R2-D-02 = C2R2-S-02 | Fixed in the records: CHANGELOG, DL-043, log, D-028 residual risk 6 (both languages), this plan |
| C2R2-S-01 | Fixed in the records: CHANGELOG, D-028 residual risk 8 (both languages), REQ-009 |
| "By the user's decision" wording (both reviewers) | Fixed: "the orchestrator's proposal, agreed by the user in their words" added; the Issue #96 decision points recorded in D-028, REQ-009 and the FU-049 note |

Fix revision of the Fixed rows: the diff of round 3 (sha256 `cdf2d928…c589`); re-reviewed in round 3.

Floor check before the records-only edit (R-DEL-2): trigger: the main session writes records of a node under the floor; values read: `claude-opus-5-5`/`high` (the session's own transcript fields); choice: the main session edits the records itself.

## Implementation review round 3 (records-only narrow confirmation)

Deep and Security Diff Scan at `opus`/`xhigh`, both read back `PASS`, on the diff with sha256 `cdf2d928…c589`. Deep: 0 findings (observations O1 to O7 below the threshold). Security: C2R3-S-03 (SHOULD-FIX: dispositions "Residual risk" and "Card …" are not one of Fixed, Deferred, Rejected or Needs Human Decision), C2R3-S-01 (NIT: present tense of the Issue #96 note in FU-049), C2R3-S-02 = deep O1 (NIT: the A3 summaries of D-028 in both languages and REQ-009 without the card I95-I1-C1 (a) exception). No pack rule text changed in this round. Correction (round 4, C2R4-D-02): the R-VER-2 stop held at this round. The records of the allowlist dead end and the Issue #96 decision (card I95-I1-C2 (a)) needed fixes that made new problems in rounds 2 and 3: C2R2-S-01 and the "By the user's decision" wording came from the round 1 fix, and the FU-049 note of C2R3-S-01 came from the round 2 fix. The round 3 fixes below started without a stop card; stop card I95-I4-C1 records this.

| Finding | Disposition |
| --- | --- |
| C2R3-S-03 | Fixed: C2R1-D-05 Deferred to FU-049 (corrected in round 4, C2R4-D-01); C2R2-D-01 Deferred to FU-056 |
| C2R3-S-01 | Fixed: "will turn" and "is to decide" in the FU-049 note |
| C2R3-S-02 = O1 | Fixed: the exception added to the A3 summaries of D-028 (both languages) and REQ-009 |
| O3 (English D-028 residual risk 6 named both costs) | Fixed: the escalation re-run needs no user question |
| O2, O4 to O7 | Kept as is: below the threshold; the pack sentence of O2 is outside card I95-I2-C1 (a) and goes with Issue #96 |

Fix revision of the Fixed rows: the diff of round 4 (sha256 `f350818d…99de`); re-reviewed in round 4.

Floor check before these record edits (R-DEL-2): trigger: the main session writes records of a node under the floor; values read: `claude-opus-5-5`/`high`; choice: the main session edits the records itself.

## Implementation review round 4 (records-only narrow confirmation)

Deep review at `opus`/`xhigh`, read back `PASS`, on the diff with sha256 `f350818d…99de`; no Security Diff Scan in this round (the R-REV-9 scan before the commit covers the security side). Findings: C2R4-D-01 (SHOULD-FIX: the Deferred row of C2R1-D-05 had no verification plan and no owner that can be checked); C2R4-D-02 (SHOULD-FIX: the round 3 judgement that the R-VER-2 stop did not hold does not match the records). The disposition records (C2R3-S-03, C2R4-D-01) and the Issue #96 decision records also needed fixes that made new problems in consecutive rounds, so the R-VER-2 stop held; stop card I95-I4-C1, answer (the user's words in the orchestrator session, relayed): 「I95-I4-C1 a」. By that option, a new problem of the same mechanism in the round 5 confirmation is not fixed in this session: it goes to the Merge Review as an open item.

| Finding | Disposition |
| --- | --- |
| C2R4-D-01 | Fixed: C2R1-D-05 Deferred to FU-049 (owner, verification plan and trigger columns; Open until Issue #96 is merged) |
| C2R4-D-02 | Fixed: correction of the round 3 judgement above |
| Below the threshold: the residual risk sentence of this plan in the old O3 wording | Fixed: the same wording as D-028 residual risk 6 |
| Below the threshold: "Issue #96 decides" in English D-028 residual risk 8 and REQ-009 | Fixed: "is to decide" |
| Below the threshold: Fixed rows without a fix revision and a re-review round | Fixed: a fix revision line under each table |
| Below the threshold: the O2 note (pack sentence) | Kept as is: recorded in the round 3 table above; it goes with Issue #96 |

Fix revision of the Fixed rows: the diff of round 5; re-reviewed in round 5.

Grep sweep over every changed file after the round 4 fixes (lesson candidate of the round 4 review: check every summary of the same rule and every row of the same table):

- `Deferred` in this plan: C2R1-D-05 (FU-049), C2R2-D-01 (FU-056), and the round 3 row that names both; each target row has the owner, verification plan and trigger columns.
- `Issue #96 decides` or `Issue #96 turns`: no hit.
- Summaries of a review or scan that does not count (`without a re-run`, `不重新派工`, `costs a user question`): D-028 A3 and residual risk 6 (both languages), REQ-009 A3, log, CHANGELOG, DL-043 and this plan carry the card I95-I1-C1 (a) exception; FU-056 is about `unknown` from a host difference, where the exception does not apply; the floor dispatch summaries of slice C1 (section 4, D-027, REQ-009 Gate, DL-042, log of Issue #93) are not about reviews.

Floor check before these record edits (R-DEL-2): trigger: the main session writes records of a node under the floor; values read: `claude-opus-5-5`/`high`; choice: the main session edits the records itself.

## Residual risks

See D-028: headless runs, a read-back after a resume, a dispatch that does
not run in the background and a read-back in a session that merges are not
tested (FU-056); the allowlist dead end (Issue #96 replaces FU-049); the
`light` exception rests on `STOP MODEL_NOT_ALLOWED`, which does not show
what ran; a review or scan of another session never counts (FU-057); the
residual risks of D-027 apply to reviews and scans; every review or scan
that does not count costs a user question and a new dispatch, and the `opus`/`high` re-run of `dev-review` after a trigger found after a `light` review needs no user question (card I95-I1-C1 (a));
`skills/dev-core/SKILL.md` is longer than one default read (FU-058); a model outside the allowlist stops every review and scan apart from the `light` exception (D-028 residual risk 8); in a headless run the escalation re-run of card I95-I1-C1 (a) does not happen, and a re-run whose read-back does not pass stops and asks the user (D-028 residual risk 9).

## Non-goals

`dev-retro` (slice C3), session read-back (slice D), FU-049 or Issue #96,
FU-050, FU-051, FU-053 to FU-055, FU-058, the other FU-052 items, and any
change of the read-back script.
