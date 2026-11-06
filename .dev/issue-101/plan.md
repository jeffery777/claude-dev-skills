# Issue #101 plan: completeness checks and an evidence rule (`Closes #101`)

Design revision: d10 (2026-11-05): E3 is withdrawn from this PR and moved to
Issue #102 (card I101-U3R1-C1 (b), 「U3R1-C1 b」); the review unit U3b takes the
place of U3 and holds the closing records. d9 (2026-11-05), after U2 review
round 3: E2.3 is one narrow clause with no exclusion (card I101-U2R3-C1 (a)). d8:
the text that `reviews/impl-u2-round-3.md` reviewed (plan SHA-256
`7fcea85e44494af006a4f5953d981c30c40d6dc2e6b7172e474bcb6e987c325e`, source: that
report; inference: the revision after U2 review round 2, card
I101-U2R2-C1 (a)). d7 (card
I101-IR3-C1 (a)): d6 with the limit of the reading check in the rule. d6
(card I101-IR2-C1 (a)): at node level a rule and a reading check; commands
only before a commit and in the Merge Review. No design review round 4 (card
I101-R3-C1 (a)); the U1 to U3 implementation reviews read the same text.
Earlier revisions: d5 (the unstaged text of U1 review round 2; plan SHA-256
`fab0190ffb39db5568e8be808c87bbcc98139ce883378c2f28d66134999fd3df`), d4 (the
staged text of U1 review round 1), d3 (SHA-256
`e64abb32a3452cc735587bf4a0a8630f52b657413dc45fe2e03bed7a3a55c5c9`), d1 (SHA-256
`f7b30023bdc5d29560d6bb22166592a903379d7df6b9d05c6909bd5c253ae527`), d2
(SHA-256 `f75879787b1ea8c272280dabba8e5d70c6ac6951262afacc1ed5536e458d278c`).
Review records: `reviews/design-round-1.md`, `reviews/design-round-2.md`,
`reviews/design-round-3.md`.

## Decisions

The card files are never edited; the SHA-256 below binds each answer to
the text that the user read (SR2-05). `cards-2.md` to `cards-15.md` are
committed as they are. `cards-1.md` is never committed: it paraphrases a
private instruction file (SR3-02); its SHA-256 here is its only record.

| Card file | SHA-256 | User's answer (2026-11-04) |
| --- | --- | --- |
| `cards-1.md` | `8125e1918e8737453b9565cd9d5ba2bb9556d49ffdca4befb3c1004354b4208f` | none (replaced by `cards-2.md` before an answer) |
| `cards-2.md` | `dffb8a8bd472031fc7daa25ccba121bfc62675c52a2c349f20674d3f1d9a1388` | 「C1 a，C2 a，C3 a，C4 a，C5 a」 (the user's own message in this session) |
| `cards-3.md` | `fa0cf1d863f4607e31da384302bc4e02cd734c3531e3527a098125775d967502` | 「R2-C1 a，R2-C2 a」 (the user's own message in this session) |
| `cards-4.md` | `4ef1eddec71e9bce2ef3eacd85f7c89f7ecd8b98fb5ddb4acee899803d69c265` | 「同意你建議a」, relayed by the orchestrator session, 2026-11-04: I101-R3-C1 (a); confirmed by the user's own message in this session: 「R3-C1 a 確認」 (card I101-IR1-C2 (a)). The earlier sentence "by card I101-C5 (a) a relay counts" was not exact: C5 (a) covers C1 only |
| `cards-5.md` | `cc16819dc7f0295dfa62a699995b9c58c12043f39a13f883afff16357f612966` | 「IR1-C1 a，IR1-C2 a，R3-C1 a 確認」 (the user's own message in this session); I101-IR1-C1 (a) is replaced by I101-IR2-C1 (a) |
| `cards-6.md` | `2341b62699c4b70267bac6fb8b253b1f1e69e600582cdf12ba65c724b2e292d6` | 「都選 a」 (the user's own message in this session, 2026-11-05), the answer to "I101-IR2-C1 和 IR2-C2 都照建議選 (a) 嗎？". `cards-7.md` corrects three of its sentences |
| `cards-7.md` | `10bb13554ad11bf4398661dd70f3a1c49df0b8059d087ecbc80f35904a9f1a5b` | 「IR3-C1 選 a」 (the user's own message in this session, 2026-11-05) |
| `cards-8.md` | `b0b759288fca6736a08b2a4213ba8b6e8b5229de5eec59a18a515c31cf20c8c3` | 「NC1-C1 選 a」 (the user's own message in this session, 2026-11-05) |
| `cards-9.md` | `a20a6a3e612a07725b48e40b2e330dbf48b51e48d14782013e210bac6912d37a` | 「NC2-C1 選 a」 (the user's own message in this session, 2026-11-05) |
| `cards-10.md` | `12d474ffd6cd450765c8ea907423b8fe0155a2ea87aa8de17b13d0808b5bb538` | 「NC3-C1 a」, relayed by the orchestrator session, 2026-11-05: I101-NC3-C1 (a). Basis for taking the relay: the practice of Issue #96 for cards that loosen no rule; this card follows R-REV-3 as it stands |
| `cards-11.md` | `aa88afc3baf18b41d2faf2024366fbde7b3b933dfe04b0d50577ba8df4fb597a` | 「U2S-C1 a」, relayed by the orchestrator session, 2026-11-05: I101-U2S-C1 (a). Basis for taking the relay: the practice of Issue #96 for cards that loosen no rule; this card tightens R-AUTH-7 |
| `cards-12.md` | `36fd37d53e48ce9d2b26e5f111e8288cf6826635d5685222046a7970e39bd9da` | 「U2R2-C1 a，C2 a」, relayed by the orchestrator session, 2026-11-05: I101-U2R2-C1 (a) and I101-U2R2-C2 (a). Basis for taking the relay: the practice of Issue #96 for cards that loosen no rule; C1 replaces the wording of a tightening, and C2 adds a requirement |
| `cards-13.md` | `05ad099a3f4481c458661e36cc462eff629f74273c7d1dfd143d3ae0d334ab00` | 「U2R3-C1 a」, relayed by the orchestrator session, 2026-11-05: I101-U2R3-C1 (a). Basis for taking the relay: the practice of Issue #96 for cards that loosen no rule; against `main` this still tightens R-AUTH-7 |
| `cards-14.md` | `fa99dfd7d05bd521a3e6476cedfd12b02669107d4c69643e5862f0a67458e2b7` | 「U3R1-C1 b」 (the user's own message in this session, 2026-11-05): I101-U3R1-C1 (b). 「可以撤回」 (the user's own message in this session, 2026-11-05), the answer to the next question, the withdrawal of the staged U3 content. I101-U3R1-C2: no answer |
| `cards-15.md` | `fd717b67e65535052a5e8774c78ddc47aef36fbb6d1c88b864059c5df0dc2922` | 「U3B-C1 a」, relayed by the orchestrator session, 2026-11-05: I101-U3B-C1 (a). Basis for taking the relay: the practice of Issue #96 for cards that loosen no rule |

- I101-C1 (a): the bounded NIT-repeat exception of R-VER-2, as changed by
  I101-R2-C2 (a).
- I101-C2 (a): rule-text commands, no script.
- I101-C3 (a): three review units in one PR, one after the other.
- I101-C4 (a): a true fact sentence without a source is residual risk that
  the main agent fixes before the commit; a false one is at least a NIT.
- I101-C5 (a): the answer to C1 counts only from this session (the card covers
  C1, `cards-2.md`); the answer to R2-C2 was asked for in the same way
  (`cards-3.md:61`); both were given here.
- I101-R2-C1 (a): E1 keeps only two command forms whose values are checked
  tree IDs, fixed paths and checked strings; quotes are checked by reading;
  a scoped design review round 3 on d3.
- I101-R2-C2 (a): the exception allows a new fact sentence that a NIT asks
  for when it gives its source (R-EVD-3); the narrow confirmation checks it
  and conditions (1) to (4); once per PR, and a use before the PR exists
  counts for that PR.
- I101-R3-C1 (a): fix the round-3 findings by deletion (the private-source
  sentence; plan values in E1.0 commands), fixed places for the record of
  exception uses, `cards-1.md` not committed; then U1 directly.
- I101-IR1-C1 (a): replaced by I101-IR2-C1 (a). The main agent's correction
  of this card (d5: a fix round checked as the working tree against the
  index) went beyond the option and was never a decision (IR2-D-04,
  IR2-S-03); it is dropped.
- I101-IR1-C2 (a): the user confirmed I101-R3-C1 (a) in this session.
- I101-IR2-C1 (a): at node level, a rule that a reviewer checks by reading;
  commands (the `--cached` forms) only before a commit, and the per-commit
  and head forms in the Merge Review. No rule requires a commit for each
  node. The card states a limit: a second change of one REQ without a row
  is caught by reading only, not by a command (I101-IR3-C1 (a) narrows the
  reading part).
- I101-IR3-C1 (a): the limit of the reading check goes into the rule, with
  no new mechanism: reading works only on a target that shows that change
  alone; on a cumulative diff the report says so, and this item does not
  count as passed. The main agent gives the fix diff when it can. Then a narrow confirmation (R-REV-4) and the U1
  commit. The card's limit corrects I101-IR2-C1 (a), whose "reading catches
  it" was too wide (`cards-7.md`).
- I101-NC1-C1 (a): after the fix and a narrow confirmation, when only NITs
  remain, the NIT exception of I101-C1 (a) and I101-R2-C2 (a) is used once
  early for U1, with all its conditions and its own narrow confirmation.
  This uses the once-per-PR allowance of this PR. A new `MUST-FIX` or
  `SHOULD-FIX`, or a finding of the same mechanism in that confirmation,
  stops the work by R-VER-2.
- I101-NC2-C1 (a): condition (2) of the exception does not hold on the
  cumulative target of NC2, so the exception is not used; this is an ordinary
  stop with one bounded fix of the NITs of NC2 (NC2-02 stays as it is: that
  file is the record of its round). A new finding of any severity in the
  next narrow confirmation stops the work.
- I101-NC3-C1 (a): NC3-01 is `Deferred` (below); U1 is committed now; T2
  fixes it.
- I101-U2S-C1 (a): R-AUTH-7 gets a class for private file content (E2.3),
  copied into the agent files. The Issue's Scope was updated first (R-REV-9
  scan read back `PASS`; the posted body read back equal to the scanned text,
  but for a final line break that `gh` adds).
- I101-U2R2-C1 (a): the class of R-AUTH-7 is drawn by where the content comes
  from; the exception sentence and "chosen to publish" are deleted. This
  replaces the wording of I101-U2S-C1 (a).
- I101-U2R2-C2 (a): the two reviewer agent files get the class too, and REQ-029
  gets an item for it (REQ-GAP U2R2-D-03).
- I101-U2R3-C1 (a): R-AUTH-7 gets one narrow clause with no exclusion; this
  replaces the wording of I101-U2R2-C1 (a). Ceiling of the card: a new
  `MUST-FIX` or `SHOULD-FIX` on this sentence in the next round moves it to
  option (b), a separate Issue, with no further fix round.
- I101-IR2-C2 (a): the user confirmed the resume in this session. The pause
  of 2026-11-04 ended on 「請繼續」, relayed by the orchestrator session,
  2026-11-05.
- I101-U3R1-C1 (b): 「U3R1-C1 b」 moves defect 3 and every change of R-VER-2 to
  Issue #102. This PR holds E1 and E2 only, and R-VER-2 does not change (source:
  `cards-14.md`, option (b); Issue #101, Scope update of 2026-11-05). For this
  PR this item replaces the U3 of I101-C3 (a).
- Withdrawal: 「可以撤回」 answers the question that `cards-14.md`, option (b),
  announces. The main agent withdrew T3's staged U3 content with
  `git restore --source=HEAD --staged --worktree`; HEAD is the U2 commit
  `da87694bba7ebd9b3c74b9b1e474cc5ea79371d1` (source: `git status` and
  `git rev-parse HEAD`, run by the main agent). A copy of the diff stays outside
  the repository; its SHA-256
  `7ddb4d93b7e9a20570d63e3ddd7a6c928e9738cc1f9a81211d16736b1b4319e9` is the one
  of the staged diff that `reviews/impl-u3-round-1.md` reviewed (source:
  `shasum -a 256`, and `git apply --check` exit 0, run by the main agent).
- I101-U3R1-C2: no answer; it moved to Issue #102 (source: `cards-14.md`,
  「選 C1 (b) 時，這張卡移到新 Issue」).
- I101-U3B-C1 (a): one bounded fix of the dispositions and the words of the U3b
  review, a narrow confirmation, then the U3b commit, the push and the PR. When
  the confirmation reports only NITs, they get dispositions with no fix round;
  a new `MUST-FIX` or `SHOULD-FIX` stops the work and goes to the user. This
  answer is the source of the U3b commit (source: `cards-15.md`).
- I101-C1 (a) and I101-R2-C2 (a) stay above as records of what the user decided.
  Whether they hold for a new design is an open point of Issue #102 (source:
  Issue #102, State at the move, Earlier decisions).

## Deferred findings

NC3-01 (NIT; `reviews/impl-u1-nc3.md`), `Deferred` by card I101-NC3-C1 (a);
T2 made the fix, and the U2 review checks it:

- Target: T2 (U2). Owner: the main agent.
- Reason: U2 changes the same records and gets a full implementation
  review; each fix of a copy needed a new confirmation, and each confirmation
  found another copy (NC1, NC2, NC3; `cards-10.md`).
- Remaining risk: the local U1 commit keeps sentences in DL-047, the REQ-029
  source locator and D-030 that say the NIT exception was used; it was not.
  The U1 commit is not pushed alone.
- Verification plan: T2 gives those sentences the conditions of card
  I101-NC1-C1 (a) and says that the exception was not used; the T2 brief and
  the U2 implementation review name NC3-01, and the main agent searches the
  records for `I101-NC1-C1`.
- Trigger that makes it blocking: NC3-01 not resolved in the U2 review stops
  the push.

U2R4-D-01, U2R4-D-02 and U2R4-D-03 (NIT; `reviews/impl-u2-round-4.md`), `Deferred`
(R-REV-3), the same way as NC3-01; T4 made the fixes, and the review of T4 checks
them:

- Target: T4 (U3b), in place of T3, whose result was withdrawn. Owner: the main
  agent.
- Reason: T4 changes D-030 and this plan anyway, and it gets a review; no fix
  round starts for three NITs in record text.
- Remaining risk: until T4, D-030's date range leaves out item 12, this plan's
  revision chain skips d8, and the Files table says "sentences".
- Verification plan: the T4 brief and the review of T4 name these three.
- Trigger that makes them blocking: not resolved in the review of T4 stops the
  push.

U3R1-S-01 to U3R1-S-05, U3R1-D-01, U3R1-D-02, U3R1-D-05 and U3R1-D-06
(`reviews/impl-u3-round-1.md`), `Deferred` (R-REV-3) to Issue #102 by card
I101-U3R1-C1 (b):

- Target: Issue #102. Owner: the session of that Issue.
- Reason: the text is withdrawn, so no rule of this PR holds it.
- Remaining risk: none for this PR: R-VER-2 does not change. For Issue #102 the
  list stands.
- Verification plan: the design review of Issue #102.
- Trigger that makes them blocking: a new text of the exception.

U3R1-D-03 (NIT; same report): `Rejected`. Source: U3R1-D-03 names rows of the
completeness table of T3, and that table was withdrawn with the staged U3
content (source: `cards-14.md`, option (b); the table of this PR is in section
"U3b before its commit", and U3B-D review item 5 found no false reason in it).

U3R1-D-04 (NIT; same report): `Fixed` by T4. The item on I101-C5 (a) in Decisions
now agrees with the row of `cards-4.md`; the card covers C1, and `cards-3.md:61`
asked for the answer to R2-C2 in the same way. At HEAD
`da87694bba7ebd9b3c74b9b1e474cc5ea79371d1` no other record of this objective makes
the claim (source: `git grep -n -i -F -e 'C5 (a)'`, cards and reviews excluded);
inference: the three new records of the finding were in T3's withdrawn content.
Fix revision: the U3b staged content; verification: that `git grep`; re-review:
the U3b review round 1 (`reviews/impl-u3b-round-1.md`, deep review).

The open question of the Security Diff Scan in the same report (may the exception
apply to the remaining rounds of this PR?) has its answer in section "R-VER-2
exception uses".

PS3 and PS4, the R-REV-9 post scans of the new texts of Issue #101 and Issue #102:
both read back `PASS`, `floor=review-scan` (source: the read-back results of this
session; the result lines go into the PR gate record comment). The private data
result of both scans is no hit (source: their reports: 「私人資料掃描 PASS」 and
「私人資料掃描：PASSED，兩份文字都沒有命中」).

- PS3-01, PS3-02 and PS3-03 (NIT): `Fixed`. Fix: the text before the post
  (the list of earlier decisions, the old scope words, the path of `log.md`).
  Verification and re-review: PS4 reports the three as resolved.
- PS4-01 and PS4-02 (NIT; class: keep as is): `Rejected`. Source: the PS4 report: neither is of a
  class that R-REV-9 lists; PS4-01 is a sentence on repository paths and holds no
  private path, and PS4-02 is one direction line of Issue #101. Reason: the Scope
  update of Issue #101 covers the line, and a repository path that needs its
  folder is found by a reader of Issue #102 in the same list.

U3b review round 1 (`reviews/impl-u3b-round-1.md`):

- U3B-D-01 and U3B-S-01 (SHOULD-FIX, one subject): `Fixed` by the dispositions
  above. Fix revision: the fix round of card I101-U3B-C1 (a); verification and
  re-review: the narrow confirmation (`reviews/impl-u3b-nc.md`).
- U3B-S-02 (NIT): `Fixed`: D-030 no longer names the copy of the diff under what
  the user decided, and "superseded" has the mark "inference". Same verification.
- U3B-D-02 (NIT): `Deferred`. Target: Issue #102. Owner: the session of that
  Issue. Reason: the fixes of the exception text (items 1 to 6 of `cards-14.md`,
  option (a)) were not made, so the main sense of the Issue stands, and a change
  of the Issue needs a new scan. Remaining risk: a reader of Issue #102 takes
  items 7 (U3R1-D-04) and 9 of that list as open; the plan says that they are
  done. Verification plan: the design review of Issue #102 reads this item.
  Trigger: the start of the design of Issue #102.

U3b narrow confirmation (`reviews/impl-u3b-nc.md`), under the ceiling of card
I101-U3B-C1 (a) (only NITs: dispositions, no fix round):

- U3B-NC-01 and U3B-NC-02 (NIT; class: worth improving): `Deferred`. Target: the
  PR of Issue #102, which changes D-030 or adds a decision record. Owner: the
  session of that Issue. Reason: the card allows no fix round for NITs. Remaining
  risk: the "What ships (U3b)" list of D-030 leaves out `cards-15.md`,
  `reviews/impl-u3b-round-1.md` and `reviews/impl-u3b-nc.md` (the Files table
  names them), and the row of `cards-15.md` holds a clause that does not apply to
  that card; the basis of the relay does not rest on it. Verification plan: the
  review of that PR reads this item. Trigger: the first change of D-030 after
  this PR.
- U3B-NC-03 (NIT; class: necessary fix): `Fixed`. The section "U3b before its
  commit" is written after the run on the index that it describes; this is the
  record that the commit needs, not a fix round. Verification: the commands of
  that section; re-review: the R-REV-9 commit scan reads it, and the Merge Review
  runs the checks again.
- U3B-NC-04 (NIT; class: worth improving): `Fixed`: the class is back in the PS4 item
  above, with the disposition. Same verification.

## Objective and scope

- Objective: GitHub Issue #101 (body; no comments at d3, source:
  `gh issue view 101`). Two defects of the review loop that Issue #96
  PR-3 (PR #100) showed each get a rule or a deterministic check: (1)
  records that must change together were missed; (2) unverified statements
  were copied forward as facts. Defect (3), R-VER-2 stopped on repeats whose
  last round had only NIT findings, moved to Issue #102 (card
  I101-U3R1-C1 (b); source: Issue #101, Scope update of 2026-11-05 and Done
  when, read with `gh issue view 101`). This PR does not change R-VER-2.
- Requirements: new REQ-029 (E1, E2; refines REQ-012, REQ-013, REQ-027;
  related REQ-008, whose locator rule R-EVD-3 keeps); REQ-003 (R-RIG-3 trace
  of every new mechanism). REQ-012 does not change here: its change for E3
  moved to Issue #102.
- Rigor `strict`. Reason (R-RIG-1): rule text of a skill pack in a public
  repository (public contract); up to d9 also a stop rule, which moved to
  Issue #102. The Issue's Process line
  proposes `strict` (a proposal by R-RIG-2; this Discover keeps it). The
  R-DEL-2 floor applies to every node.
- Base: `main` `c818e4dfd59a92650ba09d3f5d71c6da6a29ee01` (`c818e4d`, the
  merge of PR #100; source: `git ls-remote origin refs/heads/main` and
  `git merge-base HEAD origin/main`, 2026-11-04). Branch
  `claude/issue-101-review-loop-c94cb8`, created at that commit; the Issue
  ID is in the branch name, as for PR #100 (source:
  `gh pr view 100 --json headRefName`).
- Floor check of the main session (R-DEL-2): source kind "the model and
  effort fields of this session's transcript", read 2026-11-04 before each
  write. It records `claude-opus-5-5`, an ID that the configuration file at
  the base lists under `opus`, tier 3 (source:
  `git --no-replace-objects cat-file blob c818e4d…:skills/dev-core/model-config.json`),
  with effort `high` for the turns that wrote these records. Earlier turns
  recorded `medium`; they ran Discover reads only and wrote nothing in the
  repository (the main agent's statement; not checkable by a reviewer). On
  2026-11-05 the same fields, read before each write, record the same model
  and effort `high`.

## Source trace (dev-plan step 2)

Issue words (the user's words are quoted in the Issue's Process line:
「開 Issue，先做它」, 2026-11-04):

| Item | Issue words | Where it goes | Conditions kept or dropped |
| --- | --- | --- | --- |
| E1.1 | "a search list (for example `git grep -F` strings) in the plan, where every hit is changed, noted or marked historical, and checked one to one" | `dev-plan` step 6 | kept: fixed strings, the three dispositions, one to one (as a count per string and file on the index; rows with line numbers drift, DR1-05). Dropped: hits in the objective's own record folder get no row, because that folder holds the list and its rows (DR3-07) |
| E1.2 | "co-change rules: a change to a requirement adds a log row, and a user decision quote goes into the CHANGELOG quote list" | `dev-plan` step 6 | kept; rule 1 at node level by reading, by command before a commit and in the Merge Review (card I101-IR2-C1 (a)); rule 2 by reading (card I101-R2-C1 (a)). No skill asks a project for a CHANGELOG (source: `git grep -n CHANGELOG skills/`, no rule hit), so the pack rule says "every record of the project that lists the decisions of a change", and this plan names `CHANGELOG.md` |
| E2 | "every new fact sentence in records, cards and briefs gives its test or source, or says it is an inference. Briefs pass facts with their source, not as bare text." | R-EVD-3, R-DEL-1, `decision-card.md`, `task-brief.md`, agent files | kept; added the mark "unverified" (R-VER-5 uses it) and the masking sentence (R-REV-8) with the R-AUTH-7 clause; the private-source sentence of d2 and d3 was removed (DR3-01, card I101-R3-C1 (a)) |
| E3 | "when a repeated mechanism has only NIT findings left, the main agent fixes them with a recorded diff, and the Merge Review covers them; MUST-FIX and SHOULD-FIX repeats still stop. This loosens a stop rule, so the user decides it." | moved to Issue #102 (card I101-U3R1-C1 (b)); up to d9, R-VER-2 | record of d9: the user decided (cards I101-C1 (a), I101-R2-C2 (a)). Kept: NIT only, a recorded diff, the Merge Review covers it, MUST-FIX and SHOULD-FIX still stop. Added: the narrow confirmation of R-REV-4 still runs (dropping it would also loosen `dev-gate` and may loosen Core, SR1-04); the bound; "the main agent" widened to "the fixing side" (R-DEL-2 escalation, DR1-13) |
| E4 | "first choice, fixed in the rule text (no configuration, no extra check)" | E3 rule text, moved to Issue #102; E1 and E2 add no configuration (REQ-029, non-goals) | kept |
| — | "Defects 1 and 2 above have a rule or a deterministic check, each with a test or a recorded example." (Issue #101, Done when, read with `gh issue view 101`; before the Scope update of 2026-11-05 the item began "The three defects above") | Acceptance | kept |
| — | "Defect 3 is recorded as moved to Issue #102." (the same Done when) | Acceptance, Decisions, REQ-029, D-030, CHANGELOG | kept |
| — | "Any loosening of R-VER-2 has the user's recorded decision." (now in the Done when of Issue #102) | moved to Issue #102; this PR loosens nothing | record of d9 |
| — | "Out: the review roles, floors and efforts; adversarial review stays as it is." | Non-goals | kept |

Card texts to rule sentences (DR2-10). The rows that name E3 are a record of d9;
E3 moved to Issue #102:

| Card sentence (zh, short) | Rule sentence of d9 | Kept or changed, with reason |
| --- | --- | --- |
| C1 (a) 1: 只有「同一機制」觸發條件成立；另一個觸發條件是「連續兩輪有新的 MUST-FIX 或 SHOULD-FIX」，它照舊會停 | E3 condition (1); "a NIT that a review reports is not a new blocker of this rule; it still gets a disposition (R-REV-3)" | kept: the card names MUST-FIX and SHOULD-FIX as the other trigger, and every other finding kind (SCOPE-CREEP, REQ-GAP, Needs Human Decision) still counts for it as before; d2's definition removed (DR2-01, SR2-07); d3's disposition wording replaced (DR3-02) |
| R2-C1 (a): 指令只留搜尋清單與規則 1；值只有 tree ID、固定資料夾、檢查過的字串；加引號、頂層、`--literal-pathspecs`、不接管線、檢查 exit code；沒跑成就停；引文用閱讀核對；主代理執行並產生 tree ID，reviewer 照 brief 重跑（`cards-3.md:29`；tree ID 由 IR2-C1 (a) 取代）；值的檢查句逐字寫進 agent 檔與 brief | value rule, E1.0 to E1.4 | kept; E1.0 puts no plan value into a command (DR3-03, SR3-01) |
| IR2-C1 (a): 節點層級改成規則加閱讀；指令保留三種形式，commit 前跑 `--cached`，Merge Review 跑每個 commit 與 head；刪掉每節點 commit、修正輪 unstaged 順序、不加 `--cached` 的形式；風險：同一 REQ 第二次改動沒加列只靠閱讀 | E1.0, E1.1, E1.2, E1.4 | kept; the limit is in the rule text |
| IR3-C1 (a): 規則改回「修正 diff」；閱讀只在 target 顯示那次修正時有效；累積的 diff 分不出輪次，報告寫明，不算通過這一項（`cards-7.md:49`）；主代理能給修正 diff 就給，不是硬性順序；不加機制 | E1.2, E1.4 | kept; "does not count as passed" is no check that did not run, so it does not stop the work (the reviewer's warning in NC1-01) |
| NC1-C1 (a): 修完後若只剩 NIT，提早用一次例外，窄範圍確認照舊 | section "R-VER-2 exception uses" | kept; no rule text changes for it in U1 |
| C1 (a) 2: 每個審查與掃描都算數；照獨立 reviewer 的嚴重度都是 NIT；沒有未解疑慮、未驗證安全問題、查不到的部分、`NOT_RUN` | E3 condition (2) | kept; tightened: every required review ran, and the highest severity counts (SR2-04); "open" means reported as open by a reviewer (SR2-06). Note (d10): U3R1-S-04 found 「最新一輪」 of the card not kept: the rule says "the round" (`reviews/impl-u3-round-1.md`) |
| C1 (a) 3: 品質問題，不是規格、驗收或設計 | E3 condition (3) | kept. Note (d10): U3R1-S-01 found it not kept: the card says that the failure is a quality failure, and the rule says that the main agent classified it (`reviews/impl-u3-round-1.md`) |
| C1 (a) 4 and R2-C2 (a): 同一個 PR 裡還沒用過；PR 開之前用過也算在這個 PR | E3 condition (4) | kept as the card says; work that never gets a PR cannot use it (DR2-06) |
| C1 (a) 修法: floor check、升級、R-REV-4 分類、可「維持現狀」 | E3 "The fixing side works at the R-DEL-2 setting …" | kept |
| C1 (a): 只動 NIT 指到的文字，不新增事實句; R2-C2 (a): 附來源的新事實句可以加 | E3 "changes only the text that each NIT names, and adds a new fact sentence only when …" | changed by R2-C2 (a) |
| C1 (a): 記錄輪次、機制、修正 diff；下一次回覆告訴你 | E3 record and reply sentences | kept; the record also names the reports (SR2-06) |
| C1 (a): 窄範圍確認、R-REV-9、Merge Review 照舊；R2-C2 (a): 窄範圍確認核對新事實句與四個條件 | E3 confirmation sentence | kept |
| C1 (a): 修正超出 NIT 文字或同一機制又要修就停 | E3 last condition sentence | kept; "by any name" added (SR2-06 (ii)) |
| C4 (a): residual risk；主代理在 commit 前補上；內容錯的至少 NIT | R-EVD-3 severity sentence | kept; the actor is the main agent (DR2-12); a failure path added (SR2-09) |

Corrections of the Issue text, in the records only: the gate record title
is "Gate record: read-backs of PR-3's own dispatches (writer session)"
(source: the first PR #100 comment); R-EVD-2 says "A summary is not
original evidence" (source: `skills/dev-core/SKILL.md:223`).

## Slices and review units (card I101-C3 (a))

| Slice | Content | Unit |
| --- | --- | --- |
| S1 | E1 completeness checks | U1 |
| S2 | E2 evidence rule R-EVD-3 | U2 |
| S3 | E3 R-VER-2 exception: moved to Issue #102 (card I101-U3R1-C1 (b)); T3's U3 result was reviewed and withdrawn | none |
| — | closing records after the move, and the fixes of U2R4-D-01 to U2R4-D-03 | U3b |

## Design d10

### Value rule (shared by E1; card I101-R2-C1 (a))

One sentence in `dev-plan` step 6, copied word for word into
`agents/dev-reviewer.md`, `agents/dev-security-reviewer.md`,
`agents/dev-implementer.md` and the "Completeness checks" field of
`task-brief.md` (subagents do not load `dev-core`, source:
`docs/requirements/REQ-024-agent-write-and-delete.md:67`; inference: nor
`dev-plan`, because their `tools:` lines have no Skill tool):

> Before a value from a plan or a brief goes into a completeness-check
> command, check it in the text, never with a command that contains it: the
> whole of a commit ID matches `[0-9a-f]{40}` or `[0-9a-f]{64}`; a search
> string is not empty and holds only printable characters, with no `'`,
> `\`, line break or Unicode format character; the whole of a folder
> matches `[A-Za-z0-9._][A-Za-z0-9._/-]*`, and it is the requirements folder
> of the project. A value that fails is never put into a command: report
> it, and that check did not run.

### E1 Completeness checks (S1; REQ-029)

New bullet group at the end of `dev-plan` step 6 (no step number changes).

E1.0 When the commands run (card I101-IR2-C1 (a)). At `standard` and
`strict`, the main agent runs E1.1 and co-change rule 1 before a commit,
after it has staged the content of that commit and before the R-REV-9
commit scan. This rule requires no commit: when the user authorized none,
the main agent runs no command, and the rule and the reading check of E1.2
still apply.
Commands run alone (no pipeline) from the top of the worktree
(`git rev-parse --show-prefix` prints an empty line).

E1.1 Search list (`standard` and `strict` slices that change, rename,
move or remove a rule, a term, a value, a path or a recorded fact that
other files state; at `light` the plan may skip it with a reason).

- The plan lists fixed strings with IDs (`K1`, …): the IDs of the changed
  rules, deltas, decisions and findings first, then each changed wording
  and each translation.
- Command on the index:
  `git --no-replace-objects --literal-pathspecs -c core.quotePath=false grep --cached -c -F -i -e '<string>' --`.
  Exit 0: hits; exit 1: no hit; any other exit code: the check did not run.
- A hit is one matching line. The plan records, for each string, one row
  per file with hits: the path, the count, the disposition and a reason in
  the writer's own words; no line numbers and no hit text. Files under the
  objective's own record folder (`.dev/<objective-id>/`) get no rows: they
  hold the list itself. Dispositions: `changed` (the change edits that
  place), `noted` (the old text stays true, and the reason says why, or a
  note at that place qualifies it), `historical` (it records an earlier
  decision, and a record of this change has a sentence that supersedes it).
- Limit: the search finds only the listed strings; a line break inside a
  phrase, another wording or another translation is found only by reading.

E1.2 Co-change rules (`standard` and `strict`).

1. Each write node and each fix round that changes a requirement file adds
   its own `log.md` row, in that same change, whose REQ column names its
   ID; `log.md` is append-only. The reviewer of a node checks this by
   reading the node's diff, and the reviewer of a fix round by reading the
   fix diff, which the main agent gives when it can. Reading shows this only
   on a target that holds that change alone: on a cumulative diff it cannot
   tell the rounds apart, the report says so, and this item does not count
   as passed. That is no check that did not run, so it does not stop the
   work. Before a commit, the
   main agent also runs these commands, each with exit 0 required (any
   other exit code: the check did not run):
   - `git --no-replace-objects --literal-pathspecs -c core.quotePath=false diff --cached --no-relative --no-ext-diff --no-textconv --no-renames --no-color --ignore-submodules=none --name-only -- '<requirements folder>'`
   - `git --no-replace-objects --literal-pathspecs -c core.quotePath=false diff --cached --no-relative --no-ext-diff --no-textconv --no-renames --no-color --ignore-submodules=none -U0 -- '<requirements folder>/log.md'`

   Each listed name directly in the folder that matches
   `REQ-<digits>.md` or `REQ-<digits>-<slug>.md` must have its ID in the
   REQ column (the second cell) of a line of the second output that starts
   with `+|`. A line that starts with `-|` is a finding. Limit: the commands
   see one row for the whole commit, so a second change of one requirement
   file in one commit without its own row is found only by reading.
2. Each user decision that a write node records is quoted, in the same
   node, in every record of the project that lists the decisions of the
   change. The plan names those records. The reviewer checks this by
   reading, not by a command. A confidential quote follows
   `references/requirements-wiki.md`.

E1.3 Results and severity.

- A check that did not run (a value that fails the value rule, a wrong
  working directory, an exit code other than the ones above)
  is a required verification that did not run: the dependent work stops
  (R-AUTH-5).
- A row whose count or file is wrong, a file with hits but no row, a
  missing co-change row or quote, or a `-|` log line is a finding: at
  least `NIT` (a false record), and `SHOULD-FIX` when it leaves a place
  that the change made false without a disposition (R-REV-3).

E1.4 Who runs it.

- `dev-deliver` step 7 (Gate; a commit), at `standard` and `strict`: the
  main agent runs E1.1 and co-change rule 1 as E1.0 says and records the
  outputs (counts and exit codes) in the plan.
- `dev-review` step 2 and `task-brief.md`: the brief of an implementation
  review and a fix round review gives the search list and the co-change
  rules with their commands in the forms of `dev-plan` step 6, and only
  the values come from the plan (not an R-REV-9 scan). The reviewer checks
  each value by the value rule; when its target is staged, it runs the
  commands on the index and compares them with the outputs in the plan, if
  the plan has any; it always checks co-change rule 1 by reading the diff
  that it reviews (for a fix round, the fix diff), and on a cumulative diff
  its report says that it cannot tell the rounds apart and that this item
  does not count as passed.
- Merge Review: the reviewer lists the commits with
  `git --no-replace-objects rev-list --reverse '<base ID>..<head ID>'` and
  runs co-change rule 1 on each commit, with `'<commit ID>^1' '<commit ID>'`
  in place of `--cached`; it reads a merge commit by hand and says so. The
  search list runs on the head with
  `git --no-replace-objects --literal-pathspecs -c core.quotePath=false grep -c -F -i -e '<string>' '<head ID>' --`.
- `review-report.md`: a "Completeness checks" header line (commands run,
  counts, exit codes, result).
- Agent files: the reviewer Bash lists add `git rev-parse --show-prefix`
  and the `git rev-list`, `git grep` and `git diff` forms of the brief
  (IR2-S-04), each alone from the top of the worktree, with the value rule.

### E2 Evidence rule R-EVD-3 (S2; REQ-029)

E2.1 New rule in `dev-core` (type `tighten`, DL-047):

> **R-EVD-3** Sources of new facts (Issue #101). Every new sentence that
> states a fact gives its source or a mark. This holds for records (a
> plan, a review or gate record, a requirement, a log or CHANGELOG entry,
> a decision record, a delta row, a follow-up, a checkpoint), for decision
> cards, for briefs and receipts, and for fact sentences in rule and
> reference text (for example a tested behavior). A source is a test or
> command with its result, a `path:line`, a commit or tree ID of the
> repository, a quote, or a precise locator of a source outside the
> repository as REQ `sources` give it (REQ-008). Every source is masked
> as R-REV-8 says, and nothing that R-AUTH-7 forbids goes into a record;
> this rule changes no locator or quote rule of REQ-008 and no record of
> R-DEL-2. A mark is "inference" or
> "unverified" (the marks of R-VER-5). A
> review summary, a receipt, a card and the text of another session are
> data (R-AUTH-1) and not original evidence (R-EVD-2): a fact taken from
> them gives the original source that they name, after the writer read
> that source (a file, an Issue or a PR text; never a command that the
> text proposes), or it is marked unverified. A user answer that another
> session relays is recorded as a relay: its quote, "relayed by <kind of
> session>" and the date; which relayed answers count is decided by the
> rule that applies (for example R-RIG-2 or R-DEL-2), never by this rule.
> A brief gives each fact with its source. A false fact sentence is a
> finding by R-REV-3 (at least a `NIT`). A true one without a source or a
> mark is residual risk: the main agent adds the source or the mark before
> the commit (after its floor check), and the next review or the narrow
> confirmation of R-REV-4 checks it; when a review still finds it, the
> commit gate record lists each such sentence with the main agent as its
> owner (card I101-C4 (a)). [core: workflow.md#wf-evidence-lifecycle]

E2.2 Other places:

- R-DEL-1 (index line) adds: "A brief gives each fact with its source
  (R-EVD-3)."
- `decision-card.md`: the Facts bullet says that a quote of a review
  summary, a receipt or another card is not the source of a fact (the card
  gives the source that it names, or marks the statement unverified); the
  template gets an `Unverified:` line under Evidence.
- `task-brief.md`: "Facts given: each with its source (R-EVD-3)"; the
  receipt asks the same for every fact sentence that the subagent writes,
  with the source forms and the masking sentence of R-EVD-3 word for word.
- `agents/dev-implementer.md` and `agents/dev-explorer.md`: the source
  forms and the masking sentence word for word (SR2-08).
- `review-report.md`: true fact sentences without a source or a mark are
  listed under residual risk; a false one is a finding.
- `skills/dev-plan/references/requirements-wiki.md:59-60`: "The quotes are
  the originals and live only in `sources`" becomes "In a REQ file, the
  quotes are the originals and live only in `sources`" (DR2-14).
- `source-map.md` row `workflow.md#wf-evidence-lifecycle`: R-EVD-3.
- `deltas.md`: DL-047 (R-EVD-3, R-DEL-1, the `dev-plan` step 6 checks, the
  brief, card and agent fields); the DL-009 note "R-DEL-1 is an index line"
  gets "(one sentence added by DL-047)". DL-047 cites no section number
  (`tests/test_rule_citations.py`).

E2.3 R-AUTH-7 (cards I101-U2S-C1 (a) and I101-U2R3-C1 (a); U2-S-02). The Never
commit sentence gets one narrow clause, with no exclusion:

> Never commit secrets, credentials, real logs, transcripts or sessions,
> machine or user identifiers, private paths, runtime state, databases or
> caches, or the content of native memory or of the user's private
> instruction files, in any form.

Limit: other private files are not in this clause; the R-REV-9 scan looks for
them ("private files", `skills/dev-core/SKILL.md:156`, unchanged).

Agent files. Card I101-U2S-C1 (a) says that the same sentence is copied. The
files get a sentence with the same clause, with the word "write", because
subagents do not commit (source: `agents/dev-implementer.md`, the "Never commit"
bullet; `agents/dev-explorer.md`, read-only). Both reviewers of U2 round 2 found
this inside the option, because it is stricter (`reviews/impl-u2-round-2.md`).
`agents/dev-implementer.md`, `agents/dev-explorer.md` and the receipt template of
`task-brief.md` get the private-data sentence below; `agents/dev-reviewer.md` and
`agents/dev-security-reviewer.md` (card I101-U2R2-C2 (a)) get its last sentence,
because they already hold the masking text.

> In what you write, give a secret or private identifier by its kind,
> location and length or class only; for an email, say only whether it is a
> noreply address and its provider; replace the account or host part of a
> path or hostname with a placeholder. Never paste raw command output that
> holds such a value. Never write the content of native memory or of the
> user's private instruction files, in any form.

### E3 R-VER-2 exception for NIT repeats (S3; REQ-012)

Note (d10): this section is withdrawn from this PR and moved to Issue #102 (card
I101-U3R1-C1 (b), 「U3R1-C1 b」). The text below is the one that
`reviews/impl-u3-round-1.md` reviewed; it is in no rule, and it stays word for
word as the record that Issue #102 points to. `review-report.md:86` in its record
list is now `review-report.md:90` (source: `grep -n`).

Fact: the stop rule of R-VER-2 is stricter than Core: Core
`workflow.md:72` says two unfinished rounds trigger a re-assessment,
「並非自動停工」; the project rule stops the fix loop (DL-012; REQ-012
D-013 item 5 and PR-B card 1 (a)). A change that stops less is a
loosening of a project tightening, which only the user decides
(`skills/dev-core/deltas.md:4-17`); the user decided it (cards I101-C1 (a)
and I101-R2-C2 (a)).

Appended to R-VER-2:

> A `NIT` that a review reports is not a new blocker of this rule; it
> still gets a disposition (R-REV-3). Exception
> for NIT repeats (Issue #101, cards I101-C1 (a) and I101-R2-C2 (a)): the
> fix loop does not stop when all of these hold: (1) only the second
> trigger holds; (2) every review and scan that the round requires ran and
> counts by R-DEL-2, and every finding in them is a `NIT` by the highest
> severity that any of them gave it, whatever its disposition, with no
> concern or question that a reviewer reports as open, no unverified
> security question, no part that a reviewer could not check, and no
> `NOT_RUN`; (3) the main agent classified the failure as a quality failure
> (R-DEL-2), not one that the spec, the acceptance criteria or the design
> caused; (4) the exception was not used before for this PR (a use before
> the PR exists counts for that PR; work that never gets a PR cannot use
> it). The re-assessment of this rule is still recorded. The fixing side
> works at the R-DEL-2 setting (the floor check, and the escalation for a
> quality failure), classifies each NIT first (R-REV-4; "keep as is" is
> allowed), changes only the text that each NIT names, and adds a new fact
> sentence only when the NIT asks for it and the sentence gives its source
> (R-EVD-3). Each use of the exception is recorded in two fixed places:
> the section "R-VER-2 exception uses" of the plan, and, once the PR
> exists, the PR gate record comment (R-EXH-3); the record gives the
> round, the mechanism, the reports and the fix diff (the files, the tree
> IDs before and after, which the main agent reads with `git write-tree`,
> and the diff hash). The narrow confirmation of
> R-REV-4 (for a design review, the next review round) gets both places
> and checks conditions (1) to (4), that the diff stays inside the text
> that the NITs name, and each new fact sentence; a reviewer that cannot
> read both places reports the check as failed, and when one of these
> checks fails, the stop rule applies. The main agent tells the user of each use in its next
> reply (in a headless run, in the final output). The R-REV-9 scans and the
> Merge Review still run. When the fix needs more than that, or a later
> round again needs fixes of that mechanism under any name, the stop rule
> applies whatever the severity. The first trigger, a Core blocker, every
> other stop of R-AUTH-5 and Core `workflow.md:72` and `:82` do not change.

Records: DL-012 note and DL-048 (source: cards I101-C1 (a) and
I101-R2-C2 (a) with the SHA-256 of their card files; quote: the two
answers; authority: the user's own messages in this session; reason: the
cards' recommendation reasons (inference: the user chose the recommended options and gave no reason of their own);
scope: R-VER-2 only); REQ-012 sources and acceptance; D-030 in
`docs/design-proposal.md` (zh and EN, with a Core-feedback note);
`docs/core-feedback.md` CF-001 item 4 gets a note; `source-map.md` row
`workflow.md#wf-verification`. R-VER-5 and `review-report.md:86` do not
change (d2's Lesson trigger sentence is dropped; it was an addition that
no source asked for).

## Files (d10)

| Status | Path | Unit |
| --- | --- | --- |
| M | `skills/dev-plan/SKILL.md` (step 6) | U1 |
| M | `skills/dev-deliver/SKILL.md` (step 7) | U1 |
| M | `skills/dev-review/SKILL.md` (step 2) | U1 |
| M | `skills/dev-review/references/review-report.md` | U1, U2 |
| M | `skills/dev-deliver/references/task-brief.md` | U1, U2 |
| M | `agents/dev-reviewer.md`, `agents/dev-security-reviewer.md` | U1 |
| M | `agents/dev-implementer.md` | U1, U2 |
| M | `agents/dev-explorer.md`, `agents/dev-reviewer.md`, `agents/dev-security-reviewer.md` | U2 |
| M | `skills/dev-review/references/decision-card.md` | U2 |
| M | `skills/dev-plan/references/requirements-wiki.md` (line 59) | U2 |
| M | `skills/dev-core/SKILL.md` (R-EVD-3, R-DEL-1, R-AUTH-7) | U2 |
| M | `skills/dev-core/source-map.md` | U2 |
| M | `skills/dev-core/deltas.md` (DL-047) | U1, U2, U3b |
| A | `docs/requirements/REQ-029-review-loop-checks.md` | U1, U2, U3b |
| M | `docs/requirements/index.md` | U1 |
| M | `docs/requirements/log.md` | U1, U2, U3b |
| M | `docs/design-proposal.md` (D-030 zh and EN) | U1, U2, U3b |
| M | `CHANGELOG.md` | U1, U2, U3b |
| A | `tests/test_review_loop_rules.py` (pins the word-for-word copies of the value rule, the source sentence and the private-data sentence, the R-AUTH-7 sentence and the command forms) | U1, U2 |
| A | `.dev/issue-101/plan.md`, `reviews/*.md` | records, owned by each T node |
| A | `.dev/issue-101/cards-2.md` to `cards-10.md` | committed as they are in U1 (source: `git log --name-status`); owned by no node; `cards-1.md` is never committed (SR3-02) |
| A | `.dev/issue-101/cards-11.md` to `cards-13.md` | committed as they are in U2 (source: `git log --name-status`); owned by no node |
| A | `.dev/issue-101/cards-14.md`, `.dev/issue-101/cards-15.md`, `.dev/issue-101/reviews/impl-u3-round-1.md`, `.dev/issue-101/reviews/impl-u3b-round-1.md`, `.dev/issue-101/reviews/impl-u3b-nc.md` | committed as they are in U3b; owned by no node |

`README.md`: no change (it names no review-loop rule; source:
`git grep -n -i -e 'stop rule' -e 'R-VER-2' -e 'R-EVD' README.md`, no hit).

## Completeness checks of this change

Search list (each string passes the value rule):

```
K1  R-VER-2
K2  R-EVD-2
K3  R-EVD-3
K4  R-DEL-1
K5  DL-012
K6  D-013
K7  DL-035
K8  DL-009
K9  CF-001
K10 stop rule
K11 停止規則
K12 same mechanism
K13 同一個機制
K14 停止修正
K15 decision-card.md
K16 live only in
K17 R-VER-5
K18 no command runs
K19 reports differences
K20 the diff that it reviews
K21 commands again
K22 指令不跑
K23 回報差異
K24 Mark everything else
K25 used once early
K26 quotes are the originals
K27 R-AUTH-7
K28 native memory
K29 chosen to publish
K30 private instruction files
K31 Issue #102
```

Co-change rules:

- C-1 (rule 1): every write node that changes REQ-029 adds a `log.md` row
  naming it.
- C-2 (rule 2, by reading): each user answer of the Decisions table that a
  node records in REQ-029 is also in the `CHANGELOG.md` entry, in D-030 and
  in `log.md`.
- C-3: R-EVD-3 is defined once in `skills/dev-core/SKILL.md` and covered in
  `skills/dev-core/source-map.md` (`tests/test_rule_citations.py` and
  `scripts/check_core_coverage.py`, both run by `scripts/validate.sh`).

The main agent records the outputs (counts and exit codes) here before each commit (DR3-06).

## Task graph

| Task | Agent | Paths | Requested | Recorded | Effective |
| --- | --- | --- | --- | --- | --- |
| T1 (U1) | `dev-implementer` | U1 rows | role `implement` (`opus`/`high`) | `opus`/`high`, read back `PASS`, `floor=work` | `unknown` |
| T1-fix (U1) | `dev-implementer` | U1 rows | role `implement` (`opus`/`high`) | `opus`/`high`, read back `PASS`, `floor=work` | `unknown` |
| T1-fix2 (U1) | `dev-implementer` | U1 rows | role `implement` (`opus`/`high`) | `opus`/`high`, read back `PASS`, `floor=work` | `unknown` |
| T1-fix3 (U1) | main session, after its floor check | the sentences of card I101-IR3-C1 (a), this plan, the records | the session's `opus`/`high` | transcript fields, see Objective and scope | `unknown` |
| T1-fix4 (U1) | main session, after its floor check | NC1-01 to NC1-03, this plan, the records | the session's `opus`/`high` | transcript fields, see Objective and scope | `unknown` |
| T2 (U2) | `dev-implementer` | U2 rows | role `implement` (`opus`/`high`) | `opus`/`high`, read back `PASS`, `floor=work` | `unknown` |
| T2-fix (U2) | `dev-implementer` | U2 rows | role `implement` (`opus`/`high`) | `opus`/`high`, read back `PASS`, `floor=work` | `unknown` |
| T2-fix2 (U2) | `dev-implementer` | U2 rows | role `implement` (`opus`/`high`) | `opus`/`high`, read back `PASS`, `floor=work` | `unknown` |
| T2-fix3 (U2) | `dev-implementer` | U2 rows | role `implement` (`opus`/`high`) | `opus`/`high`, read back `PASS`, `floor=work` | `unknown` |
| T3 (U3) | `dev-implementer` | U3 rows, this plan, `reviews/` | role `implement` (`opus`/`high`) | `opus`/`high`, read back `PASS`, `floor=work` | `unknown` |
| T4 (U3b) | `dev-implementer` | U3b rows, this plan | role `implement` (`opus`/`high`) | `opus`/`high`, read back `PASS`, `floor=work` | `unknown` |
| T4-fix (U3b) | main session, after its floor check | the items of card I101-U3B-C1 (a) | the session's `opus`/`high` | transcript fields, see Objective and scope | `unknown` |

T3's result was reviewed (`reviews/impl-u3-round-1.md`) and withdrawn (card
I101-U3R1-C1 (b), 「U3R1-C1 b」; 「可以撤回」). The review unit of T4 is U3b.

Why role `implement`: the implement row at the `strict` tier; the R-DEL-2
floor applies. Read-backs: `--floor work`, stdin form at the bound base.
Each unit: implementation review (role `review-deep` and role
`review-security`, both `opus`/`xhigh`, `--floor review-scan`) on its
staged diff; then the E1 commands, the commit scan and the commit, as
card I101-C3 (a) says (`cards-2.md`, 「每個單位的實作審查（deep＋Security Diff
Scan）通過、commit 之後，才開始下一個」; answer 「C1 a，C2 a，C3 a，C4 a，C5 a」).
That answer covers unit commits only; the U3b commit rests on card I101-U3B-C1 (a) (`cards-15.md`). The next unit starts after that commit. Verification after each task:
`scripts/validate.sh`, `python3 -I -m unittest discover -s tests`,
`python3 -I -B scripts/check_pack.py`; the main agent runs the checks above before each commit.

## Design review

- Round 1 on d1: `reviews/design-round-1.md`.
- Round 2 on d2: `reviews/design-round-2.md`; the R-VER-2 stop rule fired;
  stop cards `cards-3.md`, answered 「R2-C1 a，R2-C2 a」.
- Round 3 on d3 (card I101-R2-C1 (a); plan SHA-256
  `e64abb32a3452cc735587bf4a0a8630f52b657413dc45fe2e03bed7a3a55c5c9`): a
  deep review and a security review, both `opus`/`xhigh`, both read back
  `PASS` with `floor=review-scan`; `reviews/design-round-3.md`. The
  R-VER-2 stop rule fired again (new MUST-FIX in rounds 2 and 3; R-VER-2
  applies as written, not only to the E1 and E3 mechanisms, SR3-04). Stop
  card: `cards-4.md` (I101-R3-C1). `cards-1.md` is not committed (SR3-02);
  its SHA-256 stays in the Decisions table.

## Completeness check outputs

### U1 commit

U1 is commit `2c68faedf14a5f7692f3f296a9b7f88322d78ab6` (tree
`46361e9c60b1a36580da5688f97bd8499c954e89`; source: `git rev-parse`). Its R-REV-9
commit scan read back `PASS`, `floor=review-scan` (source: the read-back result
of this session, 2026-11-05; the result line goes into the PR gate record
comment), with no finding (source: the scan's report). Its outputs are in
that commit's copy of this file.

### U2 commit

U2 is commit `da87694bba7ebd9b3c74b9b1e474cc5ea79371d1` (tree
`d2715fa1be6a3b69b17030af93b1a7896a0f26f3`; source: `git rev-parse`). Its R-REV-9
commit scan read back `PASS`, `floor=review-scan` (source: the read-back result
of this session, 2026-11-05; the result line goes into the PR gate record
comment), with no finding (source: the scan's report). Its outputs are in
that commit's copy of this file.

### U3b before its commit

- Run by the main agent from the top of the worktree
  (`git rev-parse --show-prefix` printed an empty line), on the index,
  2026-11-05.
- Co-change rule 1, `--cached` forms: the name list (exit 0) gave
  `docs/requirements/REQ-029-review-loop-checks.md` and `log.md`; the `-U0` log
  command (exit 0) shows two `+|` lines whose REQ column is `REQ-029` (T4 and its fix round) and no
  `-|` line. Pass.
- Search list: the same arguments as the `--cached` grep form with `-n` in place of `-c`, through Python `subprocess` with
  an argument list (no shell), once per string, on the index and on HEAD (the
  U2 commit); the rows count matching lines; every exit code was 0 or 1. A row
  is `changed` when the set of its matching lines differs from HEAD. The reasons
  of the `noted` rows are the main agent's reading.

| ID | String | Exit (HEAD / index) | Files with hits (outside `.dev/issue-101/`) | `changed` | `noted` or `historical` |
| --- | --- | --- | --- | --- | --- |
| K1 | `R-VER-2` | 0 / 0 | 56 | 4 | 52 |
| K2 | `R-EVD-2` | 0 / 0 | 16 | 0 | 16 |
| K3 | `R-EVD-3` | 0 / 0 | 11 | 2 | 9 |
| K4 | `R-DEL-1` | 0 / 0 | 22 | 2 | 20 |
| K5 | `DL-012` | 0 / 0 | 7 | 1 | 6 |
| K6 | `D-013` | 0 / 0 | 27 | 0 | 27 |
| K7 | `DL-035` | 0 / 0 | 8 | 0 | 8 |
| K8 | `DL-009` | 0 / 0 | 20 | 1 | 19 |
| K9 | `CF-001` | 0 / 0 | 6 | 0 | 6 |
| K10 | `stop rule` | 0 / 0 | 44 | 2 | 42 |
| K11 | `停止規則` | 0 / 0 | 4 | 1 | 3 |
| K12 | `same mechanism` | 0 / 0 | 19 | 0 | 19 |
| K13 | `同一個機制` | 0 / 0 | 2 | 0 | 2 |
| K14 | `停止修正` | 0 / 0 | 2 | 0 | 2 |
| K15 | `decision-card.md` | 0 / 0 | 23 | 2 | 21 |
| K16 | `live only in` | 0 / 0 | 6 | 1 | 5 |
| K17 | `R-VER-5` | 0 / 0 | 13 | 0 | 13 |
| K18 | `no command runs` | 0 / 0 | 0 | 0 | 0 |
| K19 | `reports differences` | 0 / 0 | 0 | 0 | 0 |
| K20 | `the diff that it reviews` | 0 / 0 | 1 | 0 | 1 |
| K21 | `commands again` | 0 / 0 | 0 | 0 | 0 |
| K22 | `指令不跑` | 0 / 0 | 0 | 0 | 0 |
| K23 | `回報差異` | 0 / 0 | 0 | 0 | 0 |
| K24 | `Mark everything else` | 0 / 0 | 1 | 0 | 1 |
| K25 | `used once early` | 0 / 0 | 2 | 1 | 1 |
| K26 | `quotes are the originals` | 0 / 0 | 2 | 0 | 2 |
| K27 | `R-AUTH-7` | 0 / 0 | 32 | 2 | 30 |
| K28 | `native memory` | 0 / 0 | 16 | 1 | 15 |
| K29 | `chosen to publish` | 0 / 0 | 4 | 0 | 4 |
| K30 | `private instruction files` | 0 / 0 | 8 | 1 | 7 |
| K31 | `Issue #102` | 1 / 0 | 5 | 5 | 0 |

| ID | Path | Count | Disposition | Reason |
| --- | --- | --- | --- | --- |
| K1 | `.dev/followups.md` | 14 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-1-phase1/reviews/round-1.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-1-phase1/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-12-minimal-ci/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-14-platform-profile/reviews/round-1.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-16-single-source-rules/graph.json` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-16-single-source-rules/inventory.md` | 4 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-16-single-source-rules/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-16-single-source-rules/reviews/round-3.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-16-single-source-rules/reviews/round-4.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-16-single-source-rules/reviews/round-5.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-16-single-source-rules/reviews/round-6.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-18-core-audit/audit.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-18-core-audit/reviews/round-1.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-18-core-audit/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-18-core-audit/reviews/round-3.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-22-fu005-records/fu005-checklist.md` | 3 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-22-fu005-records/fu005-spec.md` | 4 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-24-fu014/reviews/round-1.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-31-fu005-pr3/reviews/round-1-deep.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-31-fu005-pr3/reviews/round-2-narrow-and-scan.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-6-review-convergence/reviews/round-1.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-64-fu025-skill-paths/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-66-user-level-install/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-69-readonly-tools-check/plan.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-73-model-routing/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-73-model-routing/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-73-model-routing/reviews/round-3.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-77-effort-readback/plan.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-78-relay-edges/plan.md` | 3 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-85-retest-values/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-89-readback-script/plan.md` | 3 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-91-floor-check-writes/plan.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-93-readback-gate-dispatch/plan.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-95-readback-gate-reviews/plan.md` | 3 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-96-model-config/plan.md` | 3 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-96-pr2/plan.md` | 8 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `.dev/issue-96-pr3/plan.md` | 6 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `CHANGELOG.md` | 6 | `changed` | U3b edits lines with this string here |
| K1 | `docs/core-feedback.md` | 7 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `docs/design-proposal.md` | 40 | `changed` | U3b edits lines with this string here |
| K1 | `docs/requirements/REQ-009-subagent-model-effort.md` | 8 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `docs/requirements/REQ-011-security-review-before-commit-push.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `docs/requirements/REQ-022-single-source-rules.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `docs/requirements/REQ-023-core-audit.md` | 4 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `docs/requirements/REQ-026-lessons-skill.md` | 5 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `docs/requirements/REQ-027-plan-trace-and-slicing-cost.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `docs/requirements/REQ-028-user-level-read-grant.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `docs/requirements/REQ-029-review-loop-checks.md` | 2 | `changed` | U3b edits lines with this string here |
| K1 | `docs/requirements/log.md` | 8 | `changed` | U3b edits lines with this string here |
| K1 | `skills/dev-core/SKILL.md` | 4 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `skills/dev-core/deltas.md` | 5 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `skills/dev-core/source-map.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `skills/dev-deliver/SKILL.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `skills/dev-plan/references/graph-schema.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K1 | `skills/dev-review/SKILL.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K2 | `.dev/followups.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `.dev/handoff/pr-2-checkpoint.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `.dev/issue-18-core-audit/audit.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `.dev/issue-18-core-audit/reviews/round-2.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `.dev/issue-18-core-audit/reviews/round-3.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `.dev/issue-22-fu005-records/fu005-checklist.md` | 3 | `noted` | U3b does not change this rule or wording |
| K2 | `.dev/issue-22-fu005-records/fu005-spec.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `.dev/issue-22-fu005-records/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `docs/requirements/REQ-026-lessons-skill.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `skills/dev-continue/SKILL.md` | 2 | `noted` | U3b does not change this rule or wording |
| K2 | `skills/dev-core/SKILL.md` | 3 | `noted` | U3b does not change this rule or wording |
| K2 | `skills/dev-core/deltas.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `skills/dev-core/source-map.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `skills/dev-plan/references/requirements-wiki.md` | 1 | `noted` | U3b does not change this rule or wording |
| K2 | `skills/dev-plan/templates/index.md` | 1 | `noted` | U3b does not change this rule or wording |
| K3 | `CHANGELOG.md` | 2 | `noted` | U3b does not change this rule or wording |
| K3 | `docs/design-proposal.md` | 11 | `changed` | U3b edits lines with this string here |
| K3 | `docs/requirements/REQ-029-review-loop-checks.md` | 5 | `noted` | U3b does not change this rule or wording |
| K3 | `docs/requirements/log.md` | 2 | `noted` | U3b does not change this rule or wording |
| K3 | `skills/dev-core/SKILL.md` | 2 | `noted` | U3b does not change this rule or wording |
| K3 | `skills/dev-core/deltas.md` | 1 | `changed` | U3b edits lines with this string here |
| K3 | `skills/dev-core/source-map.md` | 1 | `noted` | U3b does not change this rule or wording |
| K3 | `skills/dev-deliver/references/task-brief.md` | 2 | `noted` | U3b does not change this rule or wording |
| K3 | `skills/dev-review/references/decision-card.md` | 1 | `noted` | U3b does not change this rule or wording |
| K3 | `skills/dev-review/references/review-report.md` | 1 | `noted` | U3b does not change this rule or wording |
| K3 | `tests/test_review_loop_rules.py` | 2 | `noted` | U3b does not change this rule or wording |
| K4 | `.dev/followups.md` | 2 | `noted` | U3b does not change this rule or wording |
| K4 | `.dev/issue-16-single-source-rules/inventory.md` | 2 | `noted` | U3b does not change this rule or wording |
| K4 | `.dev/issue-16-single-source-rules/reviews/round-5.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `.dev/issue-18-core-audit/audit.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `.dev/issue-22-fu005-records/fu005-checklist.md` | 3 | `historical` | it records what R-DEL-1 held then; DL-047 and the DL-009 note supersede it |
| K4 | `.dev/issue-22-fu005-records/fu005-spec.md` | 2 | `historical` | it records what R-DEL-1 held then; DL-047 and the DL-009 note supersede it |
| K4 | `.dev/issue-35-fu005-pr4/table-d-f.md` | 1 | `historical` | it records what R-DEL-1 held then; DL-047 and the DL-009 note supersede it |
| K4 | `.dev/issue-95-readback-gate-reviews/plan.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `.dev/issue-96-pr3/plan.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `CHANGELOG.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `docs/design-proposal.md` | 4 | `changed` | U3b edits lines with this string here |
| K4 | `docs/requirements/REQ-025-on-demand-core-loading.md` | 1 | `historical` | it records the index-line form of FU-005 PR-4; DL-047 and the DL-009 note supersede it |
| K4 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `docs/requirements/log.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `skills/dev-core/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `skills/dev-core/deltas.md` | 4 | `changed` | U3b edits lines with this string here |
| K4 | `skills/dev-core/source-map.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `skills/dev-deliver/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `skills/dev-deliver/references/task-brief.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `skills/dev-retro/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `skills/dev-review/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K4 | `tests/test_rule_citations.py` | 1 | `noted` | U3b does not change this rule or wording |
| K5 | `.dev/issue-22-fu005-records/fu005-checklist.md` | 1 | `noted` | U3b does not change this rule or wording |
| K5 | `.dev/issue-6-review-convergence/reviews/round-1.md` | 2 | `noted` | U3b does not change this rule or wording |
| K5 | `.dev/issue-8-decisions-changelog-core-feedback/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K5 | `docs/core-feedback.md` | 2 | `noted` | U3b does not change this rule or wording |
| K5 | `docs/design-proposal.md` | 4 | `changed` | U3b edits lines with this string here |
| K5 | `skills/dev-core/deltas.md` | 1 | `noted` | U3b does not change this rule or wording |
| K5 | `skills/dev-core/source-map.md` | 2 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/followups.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-10-cleanups/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-18-core-audit/audit.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-22-fu005-records/fu005-checklist.md` | 8 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-22-fu005-records/fu005-spec.md` | 2 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-27-fu004-baseline/report.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-31-fu005-pr3/reviews/round-1-deep.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-4-commit-security/reviews/round-2.md` | 2 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-6-review-convergence/events.jsonl` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-6-review-convergence/graph.json` | 2 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-6-review-convergence/reviews/round-1.md` | 5 | `noted` | U3b does not change this rule or wording |
| K6 | `.dev/issue-8-decisions-changelog-core-feedback/reviews/round-1.md` | 5 | `noted` | U3b does not change this rule or wording |
| K6 | `CHANGELOG.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/core-feedback.md` | 4 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/design-proposal.md` | 10 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-011-security-review-before-commit-push.md` | 2 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-012-review-convergence.md` | 10 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-013-decision-card.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-014-requirement-relation.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-015-no-agent-memory.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-016-deploy-and-measure.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-017-automatic-handoff.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-018-changelog.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-019-core-feedback.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/REQ-025-on-demand-core-loading.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `docs/requirements/log.md` | 1 | `noted` | U3b does not change this rule or wording |
| K6 | `skills/dev-core/deltas.md` | 3 | `noted` | U3b does not change this rule or wording |
| K7 | `.dev/issue-57-d019-pr3/graph.json` | 2 | `noted` | U3b does not change this rule or wording |
| K7 | `CHANGELOG.md` | 3 | `noted` | U3b does not change this rule or wording |
| K7 | `docs/design-proposal.md` | 4 | `noted` | U3b does not change this rule or wording |
| K7 | `docs/requirements/REQ-026-lessons-skill.md` | 1 | `noted` | U3b does not change this rule or wording |
| K7 | `docs/requirements/log.md` | 2 | `noted` | U3b does not change this rule or wording |
| K7 | `skills/dev-core/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K7 | `skills/dev-core/deltas.md` | 1 | `noted` | U3b does not change this rule or wording |
| K7 | `skills/dev-core/source-map.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-1-phase1/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-16-single-source-rules/inventory.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-16-single-source-rules/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-18-core-audit/audit.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-22-fu005-records/README.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-22-fu005-records/fu005-checklist.md` | 2 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-22-fu005-records/fu005-spec.md` | 4 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-35-fu005-pr4/graph.json` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-69-readonly-tools-check/plan.md` | 2 | `noted` | U3b does not change this rule or wording |
| K8 | `.dev/issue-8-decisions-changelog-core-feedback/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `CHANGELOG.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `docs/core-feedback.md` | 2 | `noted` | U3b does not change this rule or wording |
| K8 | `docs/design-proposal.md` | 2 | `changed` | U3b edits lines with this string here |
| K8 | `docs/requirements/REQ-025-on-demand-core-loading.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `docs/requirements/log.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `scripts/check_pack.py` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `skills/dev-core/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K8 | `skills/dev-core/deltas.md` | 3 | `noted` | U3b does not change this rule or wording |
| K8 | `tests/test_rule_citations.py` | 1 | `noted` | U3b does not change this rule or wording |
| K9 | `.dev/followups.md` | 1 | `noted` | U3b does not change this rule or wording |
| K9 | `.dev/issue-22-fu005-records/fu005-spec.md` | 1 | `noted` | U3b does not change this rule or wording |
| K9 | `.dev/issue-8-decisions-changelog-core-feedback/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K9 | `CHANGELOG.md` | 2 | `noted` | U3b does not change this rule or wording |
| K9 | `docs/core-feedback.md` | 8 | `noted` | U3b does not change this rule or wording |
| K9 | `docs/requirements/REQ-025-on-demand-core-loading.md` | 1 | `noted` | U3b does not change this rule or wording |
| K10 | `.dev/followups.md` | 8 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-12-minimal-ci/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-14-platform-profile/reviews/round-1.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-16-single-source-rules/inventory.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-16-single-source-rules/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-16-single-source-rules/reviews/round-3.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-16-single-source-rules/reviews/round-4.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-16-single-source-rules/reviews/round-5.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-16-single-source-rules/reviews/round-6.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-18-core-audit/audit.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-18-core-audit/reviews/round-2.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-24-fu014/reviews/round-1.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-31-fu005-pr3/reviews/round-1-deep.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-31-fu005-pr3/reviews/round-2-narrow-and-scan.md` | 3 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-4-commit-security/reviews/round-2.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-6-review-convergence/graph.json` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-64-fu025-skill-paths/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-66-user-level-install/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-69-readonly-tools-check/plan.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-73-model-routing/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-73-model-routing/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-73-model-routing/reviews/round-3.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-77-effort-readback/plan.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `.dev/issue-78-relay-edges/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `CHANGELOG.md` | 3 | `changed` | U3b edits lines with this string here |
| K10 | `docs/core-feedback.md` | 13 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/design-proposal.md` | 18 | `changed` | U3b edits lines with this string here |
| K10 | `docs/requirements/REQ-009-subagent-model-effort.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/REQ-012-review-convergence.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/REQ-020-minimal-ci.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/REQ-021-platform-profile.md` | 3 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/REQ-022-single-source-rules.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/REQ-023-core-audit.md` | 6 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/REQ-025-on-demand-core-loading.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/REQ-026-lessons-skill.md` | 5 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/REQ-027-plan-trace-and-slicing-cost.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/REQ-028-user-level-read-grant.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `docs/requirements/log.md` | 8 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `skills/dev-core/SKILL.md` | 3 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `skills/dev-core/deltas.md` | 4 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `skills/dev-core/source-map.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `skills/dev-deliver/SKILL.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `skills/dev-review/SKILL.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K10 | `skills/dev-review/references/review-report.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K11 | `.dev/issue-22-fu005-records/fu005-checklist.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K11 | `.dev/issue-22-fu005-records/fu005-spec.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K11 | `docs/core-feedback.md` | 10 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K11 | `docs/design-proposal.md` | 16 | `changed` | U3b edits lines with this string here |
| K12 | `.dev/followups.md` | 3 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-12-minimal-ci/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-16-single-source-rules/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-16-single-source-rules/reviews/round-3.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-18-core-audit/reviews/round-2.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-18-core-audit/reviews/round-3.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-31-fu005-pr3/reviews/round-2-narrow-and-scan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-6-review-convergence/reviews/round-1.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-66-user-level-install/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-89-readback-script/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-93-readback-gate-dispatch/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-95-readback-gate-reviews/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `.dev/issue-96-pr2/plan.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `docs/core-feedback.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `docs/design-proposal.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `docs/requirements/REQ-012-review-convergence.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `skills/dev-core/SKILL.md` | 2 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `skills/dev-core/deltas.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K12 | `skills/dev-review/references/review-report.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K13 | `docs/core-feedback.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K13 | `docs/design-proposal.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K14 | `docs/core-feedback.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K14 | `docs/design-proposal.md` | 1 | `noted` | this place cites the rule or records an earlier use of it; R-VER-2 does not change in this PR, so the place stays true |
| K15 | `.dev/followups.md` | 2 | `noted` | U3b does not change this rule or wording |
| K15 | `.dev/issue-10-cleanups/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `.dev/issue-16-single-source-rules/reviews/round-4.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `.dev/issue-18-core-audit/audit.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `.dev/issue-18-core-audit/reviews/round-3.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `.dev/issue-22-fu005-records/fu005-checklist.md` | 3 | `noted` | U3b does not change this rule or wording |
| K15 | `.dev/issue-22-fu005-records/fu005-spec.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `.dev/issue-6-review-convergence/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `.dev/issue-64-fu025-skill-paths/plan.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `.dev/issue-73-model-routing/plan.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `CHANGELOG.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `docs/design-proposal.md` | 6 | `changed` | U3b edits lines with this string here |
| K15 | `docs/requirements/REQ-026-lessons-skill.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `docs/requirements/REQ-029-review-loop-checks.md` | 2 | `noted` | U3b does not change this rule or wording |
| K15 | `docs/requirements/log.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `skills/dev-core/SKILL.md` | 2 | `noted` | U3b does not change this rule or wording |
| K15 | `skills/dev-core/deltas.md` | 2 | `changed` | U3b edits lines with this string here |
| K15 | `skills/dev-deliver/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `skills/dev-gate/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `skills/dev-retro/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `skills/dev-review/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K15 | `skills/dev-review/references/review-report.md` | 2 | `noted` | U3b does not change this rule or wording |
| K15 | `tests/test_review_loop_rules.py` | 1 | `noted` | U3b does not change this rule or wording |
| K16 | `CHANGELOG.md` | 1 | `noted` | U3b does not change this rule or wording |
| K16 | `docs/design-proposal.md` | 1 | `noted` | U3b does not change this rule or wording |
| K16 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `noted` | U3b does not change this rule or wording |
| K16 | `skills/dev-core/deltas.md` | 1 | `changed` | U3b edits lines with this string here |
| K16 | `skills/dev-plan/references/requirements-wiki.md` | 1 | `noted` | U3b does not change this rule or wording |
| K16 | `tests/test_platform_profile.py` | 1 | `noted` | U3b does not change this rule or wording |
| K17 | `.dev/issue-57-d019-pr2/graph.json` | 1 | `noted` | U3b does not change this rule or wording |
| K17 | `.dev/issue-57-d019-pr3/graph.json` | 3 | `noted` | U3b does not change this rule or wording |
| K17 | `CHANGELOG.md` | 5 | `noted` | U3b does not change this rule or wording |
| K17 | `docs/design-proposal.md` | 5 | `noted` | U3b does not change this rule or wording |
| K17 | `docs/requirements/REQ-026-lessons-skill.md` | 9 | `noted` | U3b does not change this rule or wording |
| K17 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `noted` | U3b does not change this rule or wording |
| K17 | `docs/requirements/log.md` | 2 | `noted` | U3b does not change this rule or wording |
| K17 | `skills/dev-core/SKILL.md` | 2 | `noted` | U3b does not change this rule or wording |
| K17 | `skills/dev-core/deltas.md` | 1 | `noted` | U3b does not change this rule or wording |
| K17 | `skills/dev-core/source-map.md` | 1 | `noted` | U3b does not change this rule or wording |
| K17 | `skills/dev-deliver/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K17 | `skills/dev-retro/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K17 | `skills/dev-review/references/review-report.md` | 3 | `noted` | U3b does not change this rule or wording |
| K20 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `noted` | U3b does not change this rule or wording |
| K24 | `skills/dev-review/references/decision-card.md` | 1 | `noted` | U3b does not change this rule or wording |
| K25 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `noted` | U3b does not change this rule or wording |
| K25 | `skills/dev-core/deltas.md` | 1 | `changed` | U3b edits lines with this string here |
| K26 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `noted` | U3b does not change this rule or wording |
| K26 | `skills/dev-plan/references/requirements-wiki.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/followups.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-1-phase1/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-16-single-source-rules/inventory.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-16-single-source-rules/reviews/round-4.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-16-single-source-rules/reviews/round-7.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-18-core-audit/audit.md` | 2 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-18-core-audit/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-18-core-audit/reviews/round-2.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-18-core-audit/reviews/round-3.md` | 3 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-18-core-audit/reviews/round-4.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-22-fu005-records/fu005-checklist.md` | 4 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-22-fu005-records/fu005-spec.md` | 2 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-22-fu005-records/reviews/round-1.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-27-fu004-baseline/report.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-38-fu004-after-pr4/report.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `.dev/issue-77-effort-readback/plan.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `CHANGELOG.md` | 4 | `noted` | U3b does not change this rule or wording |
| K27 | `agents/dev-explorer.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `agents/dev-implementer.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `docs/design-proposal.md` | 21 | `changed` | U3b edits lines with this string here |
| K27 | `docs/requirements/REQ-015-no-agent-memory.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `docs/requirements/REQ-029-review-loop-checks.md` | 13 | `noted` | U3b does not change this rule or wording |
| K27 | `docs/requirements/log.md` | 3 | `noted` | U3b does not change this rule or wording |
| K27 | `skills/dev-core/SKILL.md` | 3 | `noted` | U3b does not change this rule or wording |
| K27 | `skills/dev-core/deltas.md` | 3 | `changed` | U3b edits lines with this string here |
| K27 | `skills/dev-core/source-map.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `skills/dev-deliver/references/task-brief.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `skills/dev-docs/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `skills/dev-plan/scripts/graph.py` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `skills/dev-retro/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K27 | `tests/test_core_checks.py` | 2 | `noted` | U3b does not change this rule or wording |
| K27 | `tests/test_review_loop_rules.py` | 4 | `noted` | U3b does not change this rule or wording |
| K28 | `CHANGELOG.md` | 2 | `noted` | U3b does not change this rule or wording |
| K28 | `agents/dev-explorer.md` | 1 | `noted` | U3b does not change this rule or wording |
| K28 | `agents/dev-implementer.md` | 1 | `noted` | U3b does not change this rule or wording |
| K28 | `agents/dev-reviewer.md` | 1 | `noted` | U3b does not change this rule or wording |
| K28 | `agents/dev-security-reviewer.md` | 1 | `noted` | U3b does not change this rule or wording |
| K28 | `docs/design-proposal.md` | 5 | `noted` | U3b does not change this rule or wording |
| K28 | `docs/requirements/REQ-015-no-agent-memory.md` | 1 | `noted` | U3b does not change this rule or wording |
| K28 | `docs/requirements/REQ-026-lessons-skill.md` | 4 | `noted` | U3b does not change this rule or wording |
| K28 | `docs/requirements/REQ-029-review-loop-checks.md` | 2 | `noted` | U3b does not change this rule or wording |
| K28 | `docs/requirements/log.md` | 1 | `noted` | U3b does not change this rule or wording |
| K28 | `skills/dev-core/SKILL.md` | 2 | `noted` | U3b does not change this rule or wording |
| K28 | `skills/dev-core/deltas.md` | 2 | `changed` | U3b edits lines with this string here |
| K28 | `skills/dev-deliver/references/task-brief.md` | 1 | `noted` | U3b does not change this rule or wording |
| K28 | `skills/dev-retro/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K28 | `skills/dev-review/references/review-report.md` | 1 | `noted` | U3b does not change this rule or wording |
| K28 | `tests/test_review_loop_rules.py` | 3 | `noted` | U3b does not change this rule or wording |
| K29 | `agents/dev-security-reviewer.md` | 1 | `noted` | U3b does not change this rule or wording |
| K29 | `docs/design-proposal.md` | 1 | `noted` | U3b does not change this rule or wording |
| K29 | `skills/dev-core/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K29 | `tests/test_review_loop_rules.py` | 2 | `noted` | U3b does not change this rule or wording |
| K30 | `CHANGELOG.md` | 1 | `noted` | U3b does not change this rule or wording |
| K30 | `agents/dev-explorer.md` | 1 | `noted` | U3b does not change this rule or wording |
| K30 | `agents/dev-implementer.md` | 1 | `noted` | U3b does not change this rule or wording |
| K30 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `noted` | U3b does not change this rule or wording |
| K30 | `skills/dev-core/SKILL.md` | 1 | `noted` | U3b does not change this rule or wording |
| K30 | `skills/dev-core/deltas.md` | 1 | `changed` | U3b edits lines with this string here |
| K30 | `skills/dev-deliver/references/task-brief.md` | 1 | `noted` | U3b does not change this rule or wording |
| K30 | `tests/test_review_loop_rules.py` | 1 | `noted` | U3b does not change this rule or wording |
| K31 | `CHANGELOG.md` | 1 | `changed` | U3b edits lines with this string here |
| K31 | `docs/design-proposal.md` | 4 | `changed` | U3b edits lines with this string here |
| K31 | `docs/requirements/REQ-029-review-loop-checks.md` | 1 | `changed` | U3b edits lines with this string here |
| K31 | `docs/requirements/log.md` | 1 | `changed` | U3b edits lines with this string here |
| K31 | `skills/dev-core/deltas.md` | 1 | `changed` | U3b edits lines with this string here |

## R-VER-2 exception uses

None. The early use that card I101-NC1-C1 (a) allowed for U1 did not happen:
condition (2) did not hold on the cumulative target of NC2, and card
I101-NC2-C1 (a) made that round an ordinary stop. The exception of E3 is in no
rule, and it moved to Issue #102 (card I101-U3R1-C1 (b)), so the base R-VER-2
applies to this PR to its end.

## Acceptance

- Defect 1: E1 in `dev-plan`, `dev-deliver`, `dev-review`, the brief, the
  report and the agent files; recorded example: PR #100 P3-T3 changed
  REQ-009 without a `log.md` row of its own, a reviewer found it by reading
  (IR2-P3-D-01; source: `.dev/issue-96-pr3/plan.md:303-305`), and on the
  whole PR range the command form passes (source: `reviews/design-round-2.md`,
  read-only test with the tree form), so this case stays a reading check, and
  only on a target that shows the fix alone (card I101-IR3-C1 (a)); this
  plan's own check outputs.
- Defect 2: R-EVD-3 and the other E2 places; recorded example: the PR #100
  `GIT_WORK_TREE` condition copied from a review summary (source:
  `.dev/issue-96-pr3/plan.md:316-321`).
- Defect 3: moved to Issue #102 (card I101-U3R1-C1 (b), 「U3R1-C1 b」; Issue
  #101, Done when: "Defect 3 is recorded as moved to Issue #102."). This PR does
  not change R-VER-2. Its example stays as a record for that Issue: PR #100
  implementation review round 3 (NIT
  only; one fix added a sourced fact sentence; stopped; source: the first
  PR #100 comment, lines 26-33). Counterfactual (inference): with the
  d4 row format (no line numbers) that round's line-number edits are not
  needed, because the per-file counts of G1 to G16 are equal on the round-3
  tree and the final tree (source: the round-3 deep review's read-only
  test); then the exception would not have stopped it, provided its
  reports had no open concern (unverified: those reports are not
  available).
- `tests/test_review_loop_rules.py` pins the value rule copies and the
  command forms that REQ-029 lists.

## Non-goals

The review roles, floors and efforts; adversarial review; a new script or
configuration; Issue #79 slices C3 and D; open follow-ups; R-VER-2 and defect 3
(moved to Issue #102, card I101-U3R1-C1 (b)).
