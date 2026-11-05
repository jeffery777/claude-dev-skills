# Issue #101 design review round 1 (on d1)

- Target: `.dev/issue-101/plan.md` d1 (SHA-256
  `f7b30023bdc5d29560d6bb22166592a903379d7df6b9d05c6909bd5c253ae527`) and
  `.dev/issue-101/cards-1.md` (SHA-256
  `8125e1918e8737453b9565cd9d5ba2bb9556d49ffdca4befb3c1004354b4208f`), both
  untracked, at base HEAD `c818e4dfd59a92650ba09d3f5d71c6da6a29ee01` with no
  tracked change. Source: `shasum -a 256`, `git rev-parse HEAD`,
  `git status --porcelain=v1 --untracked-files=all`, run by the main agent
  before the dispatch and after each report; all equal (CB-4).
- Reviews: a deep review (`dev-reviewer`, role `review-deep`) and a security
  review (`dev-security-reviewer`, role `review-security`), both dispatched
  with `opus`/`xhigh`, both read back with the stdin form of the read-back
  script at the bound base and `--floor review-scan`: both `PASS`,
  `floor=review-scan` (the result lines carry agent IDs and go into the PR
  gate record comment, not into this file). Both count (R-DEL-2).
- Scope, DoD and requirements: the briefs (E1 to E4, cards I101-C1 to C4;
  REQ-012, REQ-013, REQ-003, REQ-027, REQ-011).
- Written per ASD-STE100 principles; full conformance not verified.

## Findings and dispositions

Class (R-REV-4): N = necessary fix. Every finding below is in-scope. All
dispositions are `Fixed` in design d2 (the place in d2 is named), to be
confirmed by design review round 2. Severities are the reviewers' own.

| ID | Severity | Finding (own words) | Class | Disposition (d2) |
| --- | --- | --- | --- | --- |
| DR1-01 | MUST-FIX | C-1 checks the whole base diff, so it does not catch the PR #100 log miss (a REQ-009 row already existed when round 1 changed REQ-009 again); C-2 and C-3 have no command; card C3's inference fails | N | Fixed: E1 co-change check per write node with two tree IDs (d2 E1.2); C3 corrected |
| DR1-02 | MUST-FIX | option (a)'s bound and conditions undefined: node restarts per fix task, no record of use, "blocker" undefined, concerns ignored, severities mixed with a disposition | N | Fixed: d2 E3 (once per change request, use recorded, blocker defined, concerns and unchecked parts exclude it) |
| DR1-03 | SHOULD-FIX | `git grep --untracked` cannot search a commit or the index; one row per line vs per occurrence; wrapped text and case missed; `historical` undefined; `'` breaks quoting | N | Fixed: d2 E1.1 (search the reviewed tree ID, a hit is a matching line, `-i`, limits stated, dispositions defined, character rule) |
| DR1-04 | SHOULD-FIX | plan's own record list misses places (zh D-013 item 5, core-feedback CF-001, agent files, dev-deliver step 4, README reason, DL-009 and source-map notes, owned paths of the plan) | N | Fixed: d2 Files table and search list |
| DR1-05 | SHOULD-FIX | one row per hit with line numbers is large and drifts | N | Fixed: d2 E1.1 rows per string and file with a count, no line numbers |
| DR1-06 | SHOULD-FIX | subagents do not load `dev-core`; reviewer Bash lists lack `git grep`; E2 reaches subagents only for facts passed in | N | Fixed: d2 E1.3, E2.3 (brief fields, agent file lists) |
| DR1-07 | SHOULD-FIX | new "finding" kinds have no severity and conflict with R-REV-3 | N | Fixed: d2 E1.1 and card I101-C4 (severity of an unsourced true sentence) |
| DR1-08 | SHOULD-FIX | closed source forms of R-EVD-3 conflict with masking and transcript rules; no Unverified line in the card template | N | Fixed: d2 E2.1 (source kind and date for outside sources; masking), E2.2 |
| DR1-09 | SHOULD-FIX | R-EVD-3 makes relayed user answers unverified; the authority path of the C1 answer is open | N | Fixed: d2 E2.1 (relay records) and card I101-C5 |
| DR1-10 | SHOULD-FIX | R-EVD-3 scope leaves out delta rows, decision records and fact sentences of reference text | N | Fixed: d2 E2.1 scope |
| DR1-11 | SHOULD-FIX | U1 joins E1 and E2 in a strict objective; no option with separate units | N | Fixed: d2 slices and card I101-C3 |
| DR1-12 | SHOULD-FIX | no REQ named for E1 and E2; REQ-013, REQ-027 not cited | N | Fixed: d2 REQ-029 (new) for E1, E2; REQ-012 for E3 |
| DR1-13 | SHOULD-FIX | option (a) leaves out the R-DEL-2 classification and escalation of the fixing side | N | Fixed: d2 E3 |
| DR1-14 | SHOULD-FIX | cards incomplete: C1 bundles bounds and misnames (b); C2 (b) leaves warn-or-stop open; C4 fact without a source and a paraphrase of a private instruction file; terms not explained | N | Fixed: cards-2 (C2 of d1 dropped, E4 follows the Issue's first choice; no private file quoted) |
| SR1-01 | MUST-FIX | plan strings go into a shell command unchecked (quote breaks, injection); R-EVD-3 read-back may run commands that a summary proposes | N | Fixed: d2 E1.1 character rule checked in the text first; closed command forms; E2.1 read-back by read-only reads only |
| SR1-02 | MUST-FIX | R-EVD-3 source forms push transcript paths, session IDs or private instruction text into committed records | N | Fixed: d2 E2.1 (outside sources by kind and date; R-REV-8, R-AUTH-7) |
| SR1-03 | MUST-FIX | "all NIT" not bound to the independent reviewers' severities or to every review of the round | N | Fixed: d2 E3 condition 2 |
| SR1-04 | MUST-FIX | card C1 (b) also loosens `dev-gate` and REQ-012 and may loosen the Core re-review duty of `Fixed`; "nobody reviews" is not exact | N | Fixed: the no-confirmation variant is no option in cards-2 (it can loosen Core, `deltas.md:4-5`); the reason is on card I101-C1 |
| SR1-05 | SHOULD-FIX | option (a) imprecise: mechanism can be renamed, node undefined, re-assessment, spec failures, escalation, R-REV-9, keep-as-is, scope of the fix, telling the user | N | Fixed: d2 E3 |
| SR1-06 | SHOULD-FIX | E1 commands not bound to the reviewed revision, exit codes not checked, `git diff` not hardened, pathspec magic, reviewer lists lack `git grep` | N | Fixed: d2 E1.1, E1.2 |
| SR1-07 | SHOULD-FIX | hit rows can carry paths of unrelated untracked files and hit text; decision quotes copied without the confidentiality rule | N | Fixed: d2 E1.1 (tree ID only; rows hold path, count, disposition, own-words reason), E1.2 |
| SR1-08 | SHOULD-FIX | "without a source is a finding" bypasses the R-REV-3 thresholds (user decision D-013 item 1) without a card | N | Fixed: card I101-C4 |
| SR1-09 | SHOULD-FIX | card C2 (b) does not say where the setting is read | N | Fixed: C2 of d1 dropped; E4 fixed in rule text |
| SR1-10 | SHOULD-FIX | as DR1-11 | N | Fixed: as DR1-11 |

Overlaps: DR1-11 = SR1-10; DR1-07 and SR1-08; DR1-08 and SR1-02; DR1-02,
DR1-13, SR1-03 and SR1-05; DR1-14 and SR1-04, SR1-09.

## Residual risks named by the reviewers (kept)

- Core `workflow.md:72` re-assessment and `workflow.md:82` still apply under
  E3 (d2 E3 says so).
- R-VER-5's trigger "the stop rule fired" still holds by its definition;
  d2 E3 says that a use of the exception is a Lesson candidate trigger too.
- E2 may raise the number of record-precision findings, so the exception may
  be used more often (inference of both reviewers).
- The main session's floor-check record rests on its transcript; the
  reviewers cannot read it (R-DEL-2). The earlier `medium` turns ran
  Discover reads only and wrote nothing in the repository; this is the main
  agent's statement, not checked by a reviewer.
- `docs/requirements/REQ-012` non_goals name CHANGELOG and core-feedback for
  PR-C of 2026-10-20; E1 and E2 go to the new REQ-029, so this does not
  conflict.

## R-VER-2

Round 1 of the design review. No stop trigger yet (one round). Mechanisms
to watch in round 2: the precision of E3's conditions, and the E1 command
forms.

## Lesson candidates

The reviewers' candidates are kept as proposals in their reports: the
trace of a condition into card options can hide an open choice (L1,
observation); a one-wording search list misses paraphrases and wrapped
lines (L2, worth improving, folded into d2 E1.1 limits); a value from a
plan put into a shell command needs a text check first (L2, folded into
d2 E1.1). No R-VER-5 minimum trigger fired.
