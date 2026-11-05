# Issue #101 design review round 2 (on d2)

- Target: `.dev/issue-101/plan.md` d2 with the user's answers (SHA-256
  `f75879787b1ea8c272280dabba8e5d70c6ac6951262afacc1ed5536e458d278c`) and
  `.dev/issue-101/cards-2.md` (SHA-256
  `dffb8a8bd472031fc7daa25ccba121bfc62675c52a2c349f20674d3f1d9a1388`, the
  text that the user answered), untracked, at base HEAD
  `c818e4dfd59a92650ba09d3f5d71c6da6a29ee01` with no tracked change.
  Source: `shasum -a 256`, `git rev-parse HEAD`, `git status
  --porcelain=v1 --untracked-files=all`, before the dispatch and after both
  reports; all equal (CB-4).
- Reviews: a deep review (`dev-reviewer`, role `review-deep`) and a security
  review (`dev-security-reviewer`, role `review-security`), both dispatched
  with `opus`/`xhigh`, both read back with the stdin form at the bound base
  and `--floor review-scan`: both `PASS`, `floor=review-scan` (result lines
  with agent IDs go into the PR gate record comment). Both count (R-DEL-2).
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities; dispositions after the stop card)

Every finding is in-scope. Class (R-REV-4): N = necessary fix, H = needs
human decision. Disposition: Needs Human Decision until the user answers
`cards-3.md`; the class says what d3 would do.

| ID | Severity | Finding (own words) | Class |
| --- | --- | --- | --- |
| DR2-01 | MUST-FIX | the "new blocker" definition changes the first stop trigger, which the card said stays | N (remove it; restate R-REV-3: a NIT with a disposition is not a blocker) |
| DR2-02 | MUST-FIX | under C1 (a) as written, PR #100 round 3 still stops (one edit added a sourced fact sentence), so the card's Result line is false | H (card I101-R2-C2) |
| DR2-03 | MUST-FIX | R-EVD-3 "kind and date only, never a URL" contradicts REQ-008 (D-003) and `requirements-wiki.md` locators | N (limit the outside-source form to private sources) |
| DR2-04 | MUST-FIX | E1.1 rates a check that did not run as residual risk (fails open) and a false row below NIT | N (a failed check stops the dependent work, R-AUTH-5; a false row is at least NIT) |
| DR2-05 | MUST-FIX | quotes, record paths, the requirements folder and tree IDs go into commands without a check; a quote with a line break gives a false pass | N or H (card I101-R2-C1) |
| DR2-06 | MUST-FIX | "once per change request (an objective without one counts as one)" widens the card's "once per PR" | N (once per PR; a use before the PR counts for it; no PR, no exception) |
| DR2-07 | SHOULD-FIX | actors, timing and tree binding of E1 do not fit dispatched writers; the rows sit inside the counted tree | N or H (card I101-R2-C1) |
| DR2-08 | SHOULD-FIX | co-change rule 1 can pass wrongly (no exit-code check, ID anywhere in the row, slugless names, rewritten rows) | N |
| DR2-09 | SHOULD-FIX | the plan's own search list misses R-VER-5, DL-035, DL-009, CF-001; C-2 omits `deltas.md` and `log.md` | N |
| DR2-10 | SHOULD-FIX | no source trace from the selected card texts to the rule sentences | N |
| DR2-11 | NIT | card C2 "Unverified" line is false: the P3-T3 trees are recorded in PR #100 and present locally; rule 1 on them fails as predicted | N |
| DR2-12 | NIT | R-EVD-3 says "the writer" fixes; card C4 (a) says the main agent | N |
| DR2-13 | NIT | C-3 names `check_pack.py`; the source-map check is `scripts/check_core_coverage.py` | N |
| DR2-14 | NIT | `requirements-wiki.md:59-60` ("quotes live only in `sources`") contradicts E1.2 rule 2 | N |
| SR2-01 | MUST-FIX | the character rule covers search strings only; IDs in option position (`--output=`, `-O`), quotes, paths unchecked | N or H (card I101-R2-C1) |
| SR2-02 | MUST-FIX | the subagents that run the commands do not get the value check | N or H (card I101-R2-C1) |
| SR2-03 | SHOULD-FIX | E1 false passes: working directory, exit codes, two records in one command, pathspec magic, tree not bound to the index, pipelines, who runs `write-tree` | N or H (card I101-R2-C1) |
| SR2-04 | MUST-FIX | condition (2) does not say which severity counts when two reviews rate one item differently, nor that every required review ran | N (highest severity; every required review and scan ran) |
| SR2-05 | MUST-FIX | the user's answer is not bound to the `cards-2.md` text, and that file is an owned path of T1 | N (record its SHA-256 here and in REQ-012, DL-048, D-030; card files are never edited, only committed as they are) |
| SR2-06 | SHOULD-FIX | the exception's conditions and fix scope are checked only by the side that uses it; PR bound, mechanism renaming, "open concern" | N (the narrow confirmation checks conditions (1) to (4) from the saved reports) |
| SR2-07 | SHOULD-FIX | as DR2-01 (SCOPE-CREEP and REQ-GAP dropped from the first trigger) | N (as DR2-01) |
| SR2-08 | SHOULD-FIX | the R-EVD-3 source rule does not reach writing agents, and it blocks identifiers but not private content | N |
| SR2-09 | SHOULD-FIX | the card C4 (a) management measure has no failure path (Core `workflow.md:88`) | N |

Overlaps: DR2-01 = SR2-07; DR2-05 = SR2-01; DR2-07 and SR2-03; DR2-06 and
SR2-06 (i).

Recorded test (deep review, read-only, on trees that the first PR #100
comment records): co-change rule 1 on the P3-T3 trees
`b96c42986ea54bab35c43e804e1c714ce8e4b235` →
`539a2f056e9774f1f6ee392d7d17077314d802f9` lists REQ-009 and finds no `+|`
log row, so it fails (it catches IR2-P3-D-01); on the whole PR range
`c78d53c7…` → `539a2f05…` it passes (a per-PR check misses it). The main
agent did not re-run this test.

## R-VER-2: the stop rule fired

- Fact: round 1 reported new MUST-FIX and SHOULD-FIX findings
  (`design-round-1.md`), and round 2 reported new MUST-FIX and SHOULD-FIX
  findings (this record). Two consecutive review rounds with new blockers
  stop the fix loop (`skills/dev-core/SKILL.md:195`). The second trigger
  holds too: the two mechanisms named to watch after round 1 (E1 command
  forms; precision of E3's conditions) both needed fixes again.
- Classification (R-VER-2, R-DEL-2): not an environment, auth, data,
  permission or context failure. Inference: mostly a design failure of E1
  (rule text that tells agents to build shell commands from free text) and
  a spec-precision failure of E3, so no escalation of the writing side;
  the re-evaluation goes to the user on `cards-3.md`.
- No d3 fix round starts before the user's answers.

## Re-evaluation (R-RIG-4)

- Premise that failed: "deterministic checks as rule-text commands are
  cheap" (card I101-C2 (a)). Two rounds showed that every free value in
  such a command needs its own check in several agent files (SR1-01,
  SR2-01, SR2-02, DR2-05).
- Options: narrow E1 to commands whose values are only hex IDs and fixed
  paths; move E1 to a script that takes no free text on its command line;
  or split E1 off. See card I101-R2-C1.
- E2 and E3: the findings are precision fixes inside the decided options,
  except DR2-02 (card I101-R2-C2).

## Lesson candidates

- Trigger: the R-VER-2 stop rule fired (rounds 1 and 2). Level L2;
  observation (fact): a fix for one value class or one list was applied
  only to that class (SR1-01 → SR2-01, DR1-04 → DR2-09); lesson
  (inference): a fix covers every value of the same commands and every item
  of the same kind; number of independent events: 1; existing coverage:
  R-REV-4 (widen the scope), R-REV-9 step 7; judgment: worth improving;
  smallest fix: the fix brief lists each placeholder with its check;
  abstraction checklist: project names, customer names, internal system
  names, hosts, accounts, real names, email addresses, versions not
  present; vulnerability details turned into a category.
- Trigger: a card's Result line was not checked against its own example
  (DR2-02). Level L2; observation (fact): the Result of card I101-C1 (a)
  was written without applying its conditions to the recorded PR #100
  round-3 diff; lesson (inference): check a card's Result against its named
  example before the card goes to the user; events: 1; coverage:
  `decision-card.md:20-22`, R-AUTH-6; judgment: worth improving; smallest
  fix: the card's Evidence states that check as a fact with its source;
  abstraction checklist: every item not present.
