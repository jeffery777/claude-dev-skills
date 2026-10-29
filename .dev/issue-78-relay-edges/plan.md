# Issue #78 plan: one rule for relayed model and effort answers with a reference value for each node; README explains Discover

- Objective: GitHub Issue #78, Change 1 to 4. Item 1 explains Discover in
  the README rigor line (finding MR1-001 of the PR #76 Merge Review). Items
  2 to 4 replace the relay sentence of R-DEL-2 (Issue #75, D-023) with one
  "Relayed answers" bullet: values that cannot be compared, `max` and
  "adds no authority" (MR2-001); a relayed answer that takes back an
  escalation or relays a lower-row judgment (Issue #75 review round 4
  residual risks R4 and S4); rows with more than one value. The basis is
  the user decision 「I75-M1 選 a，同意合併 PR #76」 (Issue #78 Goal).
- Rigor `strict`. Reason (R-RIG-1, re-assessed at Discover as R-RIG-2
  says): the change edits the rule text that the pack publishes (public
  contract), and the new bullet is an exception to the R-AUTH-1 data
  sentence, so it is also a change to a security rule. The design got four
  rounds of independent deep and security review before implementation
  (see Design reviews).
- Base: `main` 7a76ae0, branch `78-relay-edges`.

## Requirement trace

- REQ-009 (subagent model and effort; R-DEL-2, DL-034): T1, the rule and
  its copies (section 4, D-023 notes, D-025, DL-034, REQ-009, CHANGELOG,
  FU-039 to FU-044).
- REQ-003 (proportionate rigor; R-RIG-2): T2, the README line; T1 writes
  the REQ-003 source, the acceptance item and the log row.
- REQ-005 (language): zh and en of section 4, D-025 and the README agree.
- REQ-022 (each rule in one place): the bullet is in `dev-core` once; the
  other files restate it with the same meaning.
- REQ-008 (requirements wiki): `docs/requirements/log.md` gets new rows
  only.

## Source trace (dev-plan step 2)

Sources: the GitHub Issue #78 body (Goal and Change 1 to 4), with the user
decision 「I75-M1 選 a，同意合併 PR #76」; and three user answers, Claude
Code session 2026-10-29, orchestrator relay:

- the design cards I78-D1 to I78-D7:
  「D1–D7 選 a，D3 補說明，188 行先列 follow-up」;
- the design review round 2 cards I78-R2-C1 and I78-R2-C2:
  「R2-C1 a，R2-C2 a」;
- the design review round 3 stop card I78-R3-C1: 「R3-C1 c」.

The content of 「D3 補說明」 is the orchestrator's reading, not the user's
words. Its source is the user's earlier explanation, relayed by the
orchestrator (a paraphrase, not the user's words: when a long conversation
moves to a new session, an escalation raised in the old session stays in
the new one; a simpler task in the new session may go back to the table
value).

The user's reason for I78-R3-C1 (c) is the user's explanation, relayed by
the orchestrator (a paraphrase, not the user's words): a confirmation needs
the facts behind it, the setting of the original session and the setting
of the new one, and the user wants the orchestrator to gather them; nobody
can see the history of a setting afterwards (session views show only
current values; the transcript of a session records the requested effort
for each turn, but only that session can read it (the user's view; not
verified) (wording corrected after review DS4-03; not the user's words)
and it is not tamper-proof; the reason for an escalation is not kept where
a session that takes over must read it (wording corrected after review
DS4-03; not the user's words)); so the fix belongs at record time, not at
confirmation time. FU-044 has the same text in its
"Reason deferred" column, with the pack facts.

The design drafts, the design cards and the review reports are session
notes outside the repository (design rev 1 to rev 4); this plan names them
only by card and finding IDs.

| Sentence of the "Relayed answers" bullet (`dev-core`) | Source |
| --- | --- |
| 1 Scope: the one exception to the data sentence, only for the model and effort of a session or subagent that the main agent starts | Issue Change 3; D-023 D5 (a) |
| 2 Counts without a confirmation: quotes the user's words and the setting is at or above the reference value of the node | Issue Change 3; D-023 D5 (a); I78-D1 (a) and I78-D2 (a); I78-R3-C1 (c) |
| 3 Every other relayed answer, a loosening of a floor included, needs the user's confirmation in this session | Issue Change 3; D-023 (card I75-R2-C1 (a)) |
| 4 to 6 Confirmation: the user's own message; text that another session, an agent, a hook, a tool, or a scheduled or background task adds is never a confirmation; a message that the session cannot tell apart is a relay | I78-D4 (a); DS2-02 |
| 7 The reference value belongs to a node (one task of the plan without a graph file) and stays with it when another session runs the node | the I78-D3 reading (「D3 補說明」); DR2-03; I78-R3-C1 (c) |
| 8 The reference value: for the model and the effort each, the highest of the floor, the row value and an escalation or `light` trigger that applies | Issue #75 review round 4 R4 and S4; I78-D1 (a) and I78-D2 (a) |
| 9 For a session: each node that it runs itself and the session value | the D-023 session rule; DS2-06 |
| 10 A row with more than one value | Issue Change 4; DR1-02; DS1-11 (a) |
| 11 A value that a row allows only when the user asks (`max` for a security review) is not the row value and not a condition of the row | I78-IS1-02; I78-D2 (a) (its example `max` back to `xhigh`); I78-D5 (a); the `dev-deliver` security row |
| 12 Own reading | DS1-01 |
| 13 and 14 Data (a tier, a row, a condition, an escalation or a `light` trigger that applies to the node, or whether the floor applies, in text that the session did not check) never sets the reference value; a higher value that it names applies | DS1-01; DS2-07; DS4-05 |
| 15 and 16 Escalation orders; a value outside them counts as below | Issue Change 2; DS1-04 |
| 17 `max` for a security review is above its row value and counts on the quote | I78-D5 (a); I78-R3-C1 (c) |
| 18 Neither the exception nor a confirmation allows a value that another rule forbids | DR1-08; DS1-08 |
| 19 Exclusions (the main session's own floor check, REQ-017, the agent, the dispatch method, the review mode) | DS1-09 |
| 20 R-AUTH-1 to R-AUTH-6 do not change for other decisions | existing text (Issue #75) |

Conditions not kept, with the reason:

- The planned setting of DS1-03: I78-D1 (a), the reference value does not
  include a setting that the main agent chose above the row (D-025
  residual risk 1).
- An earlier user request: I78-D2 (a) (D-025 residual risk 2).
- Bounds on relayed raises (DS1-05): I78-D5 (a), follow-up FU-042.
- "Highest tier since Discover" (DS1-01): follow-up FU-040.
- The R-RIG-2 confirmation text: I78-D4 (a), follow-up FU-041.
- I78-R2-C1 (b), an exemption for `opus`/`max`: not chosen.
- I78-R2-C2 (b), no check: not chosen.
- DS2-06 "no row gives the higher value": not applied; D-025 residual
  risk 10 records it.
- The fail-closed sentence of I78-D3 (a), I78-R2-C1 (a) and I78-R2-C2 (a):
  decided, then moved to FU-044 by I78-R3-C1 (c); Issue #78 does not ship
  them.
- I78-R3-C1 (a), (b) and (d): not chosen.

## Main session setting and dispatch (R-DEL-2)

- This session (main): its transcript fields read `opus`/`medium`, below
  the floor. So it wrote no repository file and dispatched all design and
  implementation work.
- The T1 dispatch record is in this plan. The T2 dispatch record and the
  T2 review record are in `.dev/issue-78-relay-edges/t2/` (DR2-07).
- Dispatch record (requested; recorded). A `recorded` value comes only
  from the model and effort fields that the runtime writes in the
  subagent's transcript (`skills/dev-deliver/references/task-brief.md`).
  - Design drafts rev 1, rev 2, rev 3 and rev 4 (`dev-explorer`, one
    dispatch each): requested `opus`/`high`; recorded `opus`/`high` each.
  - Design review rounds 1 to 4 (`dev-reviewer`, deep, and
    `dev-security-reviewer`, one dispatch each per round): requested
    `opus`/`xhigh`; recorded `opus`/`xhigh` each.
  - T1 implementation (`dev-implementer`, the same dispatch as T2):
    requested `opus`/`high`; recorded `opus`/`high` (the main session
    read the transcript fields); effective `unknown`.
  - Implementation review round 1 (see "Implementation review"): deep
    review of T1 (`dev-reviewer`) and Security Diff Scan of T1 and T2
    (`dev-security-reviewer`), requested `opus`/`xhigh`, recorded
    `opus`/`xhigh` each. The routine review of T2 is recorded in
    `t2/review-1.md`.
  - Fix dispatch 1, the round 1 fixes of T1 and T2 (T1-F1 and T2-F1,
    `dev-implementer`, one dispatch): requested `opus`/`high`; recorded
    `opus`/`high` (the main session read the transcript fields).
  - Implementation review round 2 (see "Implementation review"): deep
    review (`dev-reviewer`) and Security Diff Scan
    (`dev-security-reviewer`), requested `opus`/`xhigh`, recorded
    `opus`/`xhigh` each.
  - Fix dispatch 2, the round 2 NIT fixes and these records (T1-F2 and
    T2-F2, `dev-implementer`, one dispatch): requested `opus`/`high`;
    recorded `unknown` (this line is written in the same dispatch, before
    the main agent can read the transcript field; the PR description gives
    the value).

## Design reviews (before implementation)

| Round | Target | Review | Agent | Requested / recorded | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | rev 1 | deep | `dev-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | REVISE, 0 MUST-FIX / 4 SHOULD-FIX / 1 SCOPE-CREEP / 3 NIT |
| 1 | rev 1 | security | `dev-security-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | PASS, 0 MUST-FIX / 6 SHOULD-FIX / 5 NIT |
| 2 | rev 2 | deep | `dev-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | REVISE, 0 MUST-FIX / 2 SHOULD-FIX / 6 NIT |
| 2 | rev 2 | security | `dev-security-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | PASS, 0 MUST-FIX / 3 SHOULD-FIX / 7 NIT |
| 3 | rev 3 | deep | `dev-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | 0 MUST-FIX / 1 SHOULD-FIX (DR3-01) / 3 NIT; R-VER-2 stop |
| 3 | rev 3 | security | `dev-security-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | PASS, 0 MUST-FIX / 1 SHOULD-FIX (DS3-01) / 4 NIT; R-VER-2 stop; card I78-R3-C1 (c) |
| 4 | rev 4 | deep | `dev-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | ready for implementation, 0 MUST-FIX / 0 SHOULD-FIX / 3 NIT (wording) |
| 4 | rev 4 | security | `dev-security-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | PASS, 0 MUST-FIX / 1 SHOULD-FIX (DS4-01, wording) / 5 NIT (wording) |

- Round 3: both reviews found that the R-VER-2 stop rule applied (the same
  fail-closed mechanism had a new design problem in round 2, DR2-01, DR2-02
  and DS2-01, and in round 3, DR3-01 = DS3-01). The user chose I78-R3-C1
  (c).
- Round 4: no new mechanism problem; no further design round. The
  implementation applied the wording fixes: DS4-01 (FU-042 Remaining
  risk), DS4-02 = DR4-01 (FU-044 item (1)), DS4-03 and DR4-02 (FU-044
  Reason deferred: "is not kept where a session that takes over must read
  it", "(the user's view; not verified)", the pack facts, "adds no record
  duty"), DS4-04 (D-025 residual risk 4 and FU-044: any session that
  cannot read them, for example after its context was summarized), DS4-05
  (the data list adds an escalation or a `light` trigger that applies to
  the node, in every copy), DS4-06 (the round 4 result in D-025 and this
  table), DR4-03 (D-025 item 3: the reference value is decided for each
  node) and the deep residual (D-025 origin 4 also cites DR2-01, DR2-02
  and DS2-01).

## Implementation review

Round 1 (diff identity `12ff0da00d7386a7`). The routine review of T2 is
recorded in `t2/review-1.md`.

| Review | Target | Agent | Requested / recorded | Result |
| --- | --- | --- | --- | --- |
| deep | T1 | `dev-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | 0 MUST-FIX / 0 SHOULD-FIX; NIT I78-IR1-01; note I78-IR1-02 |
| Security Diff Scan | T1 and T2 | `dev-security-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | PASS; 4 NIT (I78-IS1-01 to I78-IS1-04); gitleaks 8.30.1 on the full diff: no leaks |

- I78-IR1-01 (NIT; the same finding as I78-IT1-01, SHOULD-FIX, of the T2
  review): the T1 and T2 dispatch
  records said "recorded: see receipt". Fixed: they give the recorded
  value `opus`/`high` that the main session read from the transcript
  fields; the effective value stays `unknown`.
- I78-IR1-02: the reviewer could not verify the recorded values of design
  review round 4 and of design rev 4. The main session read them from the
  transcript fields (`opus`/`high` for rev 4, `opus`/`xhigh` for the round
  4 deep review and security review). No change.
- I78-IS1-01 (NIT): the FU-044 paraphrase of the user's reason changed
  after design review round 4 without saying so. Fixed: in FU-044 "Reason
  deferred" and in the Source trace of this plan, the reworded clause and
  the added note carry "(wording corrected after review DS4-03; not the
  user's words)".
- I78-IS1-02 (NIT): "`max` only when the user asks" against the rule for a
  row with more than one value. Fixed: R-DEL-2 "Relayed answers" says that
  a value that a row allows only when the user asks, such as `max` for a
  security review, is not the row value and not a condition of the row;
  section 4 and the D-025 rule summary (both languages), the REQ-009 Issue
  #78 group and the CHANGELOG entry say the same.
- I78-IS1-03 (NIT): the FU-042 "Remaining risk" did not name D-025
  residual risks 1 and 2. Fixed.
- I78-IS1-04 (NIT): D-025 "Difference from Core" and residual risk 2 (both
  languages) now say that in the case of residual risk 2 the relayed
  answer counts because of the user's decisions D-023 D5 (a) and I78-D2
  (a), not because Core lets the main agent choose; Core `auth-scope` puts
  user instructions above skill defaults (inference). To be named on the
  merge card (main agent).

Round 2 (narrow, diff identity `526a923d610aa6e6`). Round 2 had no T2
finding (`t2/review-2.md`).

| Review | Target | Agent | Requested / recorded | Result |
| --- | --- | --- | --- | --- |
| deep | T1 | `dev-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | 0 MUST-FIX / 0 SHOULD-FIX; NIT I78-IR2-01, I78-IR2-02 |
| Security Diff Scan | T1 and T2 | `dev-security-reviewer` | `opus`/`xhigh` / `opus`/`xhigh` | PASS; NIT I78-IS2-01; gitleaks 8.30.1 on the full diff: no leaks |

- I78-IR2-01 (NIT): the Source trace table had no row for the sentence
  that I78-IS1-02 added. Fixed: row 11 is added and the old rows 11 to 19
  are now 12 to 20.
- I78-IR2-02 and I78-IS2-01 (NIT): in D-025 "Difference from Core" (both
  languages), the general sentence did not exclude the case of residual
  risk 2. Fixed: it starts with "Outside the case of residual risk 2"; a
  new sentence after the I78-IS1-04 sentence says that whether this case
  relaxes Core `auth-scope` depends on whether the user's decisions D-023
  D5 (a) and I78-D2 (a) count as a valid user instruction, and that the
  user decides this at merge (inference). I78-IS2-01 is also on the merge
  card (main agent).
- The round 2 text fixes are covered by the commit scan and the
  exact-head Merge Review (no separate review round).

## User answers (cards I78-D1 to I78-D7)

「D1–D7 選 a，D3 補說明，188 行先列 follow-up」

1. I78-D1 (a): the reference value does not include a setting that the
   main agent chose above the row.
2. I78-D2 (a): the reference value does not include an earlier user
   request.
3. I78-D3 (a): the per-node reading (the orchestrator's reading of
   「D3 補說明」, see Source trace), and a fail-closed sentence that card
   I78-R3-C1 (c) later moved to FU-044.
4. I78-D4 (a): a confirmation is the user's own message in the session;
   follow-up FU-041.
5. I78-D5 (a): a relayed raise counts on the quote; follow-up FU-042.
6. I78-D6 (a): a new decision D-025, with notes at D-023.
7. I78-D7 (a): follow-ups in `.dev/followups.md`; by 「188 行先列 follow-up」
   (line 188 of `skills/dev-core/SKILL.md` at commit 7a76ae0, the
   escalation rule) the rule stays and FU-039 records the missing user
   exception.

## User answers (design review round 2 cards I78-R2-C1 and I78-R2-C2)

「R2-C1 a，R2-C2 a」

1. I78-R2-C1 (a): when the session cannot read the earlier rounds of a
   node, every relayed answer about it needs a confirmation, raises
   included. Moved to FU-044 by I78-R3-C1 (c); not shipped.
2. I78-R2-C2 (a): that a node has no earlier rounds comes only from the
   session's own reading. Moved to FU-044 by I78-R3-C1 (c); not shipped.

## User answer (design review round 3 stop card I78-R3-C1)

「R3-C1 c」

1. I78-R3-C1 (c): the fail-closed mechanism for a node whose earlier rounds
   the session cannot read moves out of Issue #78; the per-node reference
   value stays; D-025 residual risk 4 records the handover gap; FU-044
   first records escalations and triggers where a session that takes over
   a node can read them, then re-evaluates the fail-closed question.

## Items and files

1. R-DEL-2 in `skills/dev-core/SKILL.md`: the two relay sentences of the
   start bullet are removed; the pointer sentence and the new "Relayed
   answers" bullet are added (T1).
2. `docs/design-proposal.md`: section 4 (zh and en), the D-023 notes
   (Rules 1, residual risk 6, Difference from Core; zh and en) and the new
   D-025 (zh and en) (T1).
3. `skills/dev-core/deltas.md` DL-034: Difference, Reason and Evidence
   columns (T1).
4. `docs/requirements/REQ-009-subagent-model-effort.md`: four new sources,
   a note on the Issue #75 relay sentence, a new Issue #78 group (T1).
5. `docs/requirements/REQ-003-proportionate-rigor.md`: one new source and
   one acceptance item (T1).
6. `docs/requirements/log.md`: two new rows (T1).
7. `CHANGELOG.md`: a new entry and a note in the Issue #75 entry (T1).
8. `.dev/followups.md`: FU-039 to FU-044 (T1).
9. `README.md`: the Discover line, zh `:60` and en `:178` (T2).

## FU-005 comparison (agent files and `task-brief.md`)

The relay sentence has no copy in `agents/*.md` or
`skills/dev-deliver/references/task-brief.md` (a grep for "relay" finds
none), and no skill outside `dev-core` has relay text. No change there.

## Task graph

`graph.json` has two write nodes and no edge:

- `T1` (`risk` `high`, review `deep`): items 1 to 8. It owns the rule
  files, the copies, `plan.md` and `reviews/`. The deep review and the
  Security Diff Scan check it.
- `T2` (`risk` `low`, review `routine` at `opus`/`high` under `strict`):
  item 9. It owns `README.md` and `t2/`; its dispatch record and its
  review record go into `t2/`, never into this plan.

`graph.json` and `events.jsonl` belong to no node; only `graph.py
transition` writes `events.jsonl`, and re-planning goes through `dev-plan`.

## DoD

- The "Relayed answers" bullet and the pointer sentence are in
  `skills/dev-core/SKILL.md` once with the design rev 4 text and the
  round 4 wording fixes; the two replaced sentences are gone.
- Section 4, the D-023 notes, D-025, DL-034, REQ-009, the REQ-003 trace,
  the log rows, the CHANGELOG and FU-039 to FU-044 agree with it in
  meaning; zh and en agree.
- No committed text says that the fail-closed rule of I78-D3 (a),
  I78-R2-C1 (a) or I78-R2-C2 (a) ships.
- `docs/requirements/log.md` only gets new rows.
- No notes path, session ID or private value.
- A read of the whole of `skills/dev-core/SKILL.md` after the change, in
  parts where the read tool limits it, reaches the last rule (CB-7).
  Size after the change: 68,933 bytes after the round 1 fixes (68,792
  bytes before them; 65,530 bytes at 7a76ae0).
- `bash scripts/validate.sh` passes; `python3
  ${CLAUDE_SKILL_DIR}/../dev-plan/scripts/graph.py validate
  .dev/issue-78-relay-edges/graph.json` passes.
- The independent deep review and the Security Diff Scan of T1, and the
  routine review of T2, find no open MUST-FIX or SHOULD-FIX.

Residual risks: D-025 "Residual risks and limits" (items 1 to 11).
Follow-ups: FU-039 to FU-044.

## Implementer

`dev-implementer`, requested `opus`/`high` (implement and docs row at the
`strict` tier; R-DEL-2 floor: public pack rule text and an exception to a
security rule). Recorded: see "Main session setting and dispatch".

## Lesson candidates

- When a protection is removed, the plan DoD greps every copy of the
  change for "can" and "cannot" capability statements and checks each one
  against the removal.
  - Suggested level: L1 (this project).
  - Trigger: the same kind of finding came back in two rounds of this work.
  - Source: this plan, "Design reviews" (round 4, DS4-01) and
    "Implementation review" (round 1, I78-IS1-03).
  - Observation (fact, read back in this plan and in FU-042): the FU-042
    "Remaining risk" needed two fixes for missing capability statements
    (DS4-01, then I78-IS1-03).
  - Lesson (inference): after a protection moves out of scope (here the
    fail-closed rule, and the reference value without the main agent's
    choice or an earlier user request), the statements of what a relay
    can and cannot do drift in the copies that restate it.
  - Independent events: 2.
  - Already covered by: REQ-022 (one place for each rule) and the plan DoD
    "agree in meaning"; neither names capability statements (inference).
  - Judgment: worth improving.
  - Smallest fix: a DoD item in the plan of such a change, not a new check.
  - Abstraction checklist: project names, customer names, internal system
    names, hosts, accounts, real names, email addresses, versions,
    vulnerability details: not present.
