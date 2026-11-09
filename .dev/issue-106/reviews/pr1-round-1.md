# Issue #106 PR-1 review, round 1

Written per ASD-STE100 principles; full conformance not verified.

Target: the index at HEAD = base `23ed6dd352dba41e76d878655239c22465092f49`,
14 staged files, diff SHA-256 `2b0919c35d3f9b874672b033b45b67573df100972cddcbfb304e2e652af769e9`.
The rules at the base govern these reviews (the plugin loads from `main`).

CB-4 (base text) by the main agent, before and after both reviews: HEAD
`23ed6dd…`, status SHA-256 `9b542bb4…bb85`, diff SHA-256 `2b0919c3…69e9`;
every command exit 0; equal before and after. Both reviewers also reported the
same diff hash at start and end.

| Review | Agent | Requested | Recorded |
| --- | --- | --- | --- |
| P1-deep | `dev-reviewer` | opus/xhigh | `unknown`, case `not read back` |
| P1-sec | `dev-security-reviewer` | opus/xhigh | `unknown`, case `not read back` |

## Findings and triage (R-REV-4)

| ID | Severity | Triage | Disposition |
| --- | --- | --- | --- |
| P1S-01 | MUST-FIX | agent skips the check or the host gives no output: fail-open; Core :25, :31 | Fixed: "does not print `PASS`"; CB-4 "a failed or missing command … the review or scan does not count" (test updated) |
| P1S-02 | SHOULD-FIX | a change of a rule that D-032 covers has no re-acceptance path; Core :31 | Needs Human Decision: card I106-C3 (`cards-2.md`), together with P1D-01 and P1D-02 |
| P1S-03 | NIT | R-EVD-3 (an unverified premise written as a fact) | Fixed by deletion: "The machine is not bound (card I106-C1)." in both languages |
| P1D-01 | MUST-FIX | the exclusion was narrowed after the user's answer, without the user; Core :29 | Needs Human Decision: card I106-C3 |
| P1D-02 | REQ-GAP | no way to land a new acceptance: the change that records it cannot be reviewed | Needs Human Decision: card I106-C3 |
| P1D-03 | NIT | plan and graph did not match the change | Fixed: plan items 5 and 8, graph P1 requirements REQ-007 and REQ-024 |
| P1D-04 | NIT | REQ-024 non-goal and Acceptance read as contradicted | Fixed: the REQ-024 note says they apply to the FU-013 work only |
| P1D-05 | NIT | CHANGELOG entry without the user's quote | Fixed: the quote is in the entry |

Other items fixed (low cost, from residual notes): "an added or moved cite"
(P1S Q3, P1D residual 3); "merge a PR, close an Issue"; "Equal values before
and after do not prove that nothing changed"; the Traditional Chinese D-032
check string is tested too; card C1 (d) notes its correction after the answer.

Kept as is (no recorded agent error reaches them): another GitHub host,
`GH_REPO`, forks with several remotes, a tracked `.claude/settings.json`, the
"read-only" labels that the instruction-only sentence qualifies, a repository
with no commit (CB-4 is `NOT_RUN` and fails closed).

For the PR-1 ready card (P1S Q2): D-032 clauses that the triage added and the
user has not seen on a card: the "Rules covered" scope (qualification rules
only; R-REV-9 is "applies to"), "a later change of R-REV-9, or an added or
moved cite or line number, is no change of these rules", the protected-resource
list, and the "Not covered" list. The user's merge decision covers them only
when the card lists them.

Open: REQ-011 notes change in PR-3 (SEC105B-01), where the scans' dependence on
R-REV-1 is written down.

## Card I106-C3

The user's own message in this session (2026-11-09): 「C3 a」. Applied in
R-REV-1 and both parts of D-032: a change that edits a reviewer agent file,
the pins, D-032 or a rule that D-032 covers has its reviews and scans count
under D-032 only with a new decision of the user for that change, quoted and
recorded in that change; an added or moved cite or line number is no change.
P1S-02, P1D-01 and P1D-02: `Fixed` by this answer. Consequence: PR-3 edits
`agents/dev-security-reviewer.md`, so it needs such a decision before its
first review; PR-2 adds only a cite.

## Round 2 (narrow confirmation, P1-R2)

Dispatch: `dev-security-reviewer`, requested opus/xhigh, recorded `unknown`,
case `not read back`. CB-4 by the main agent: before HEAD `23ed6dd…`, status
`664f93f6…03e0`, diff `d6d8312d…3ccd`; after the same values; exit 0 each.
Result: every round-1 disposition applied; no MUST-FIX.

| ID | Severity | Triage | Disposition |
| --- | --- | --- | --- |
| P1R2-01 | SHOULD-FIX | the card C3 that the user answered says "CB-4"; the record said "the CB-4 detection" (narrower, agent-presumed) | Fixed by deletion: D-032 covers CB-4 (both languages) |
| P1R2-02 | SHOULD-FIX | REQ-GAP P1D-02 answered by the user without a REQ source | Fixed: REQ-024 source and note for 「C3 a」; the `log.md` row of this fix round describes it |
| P1R2-03 | NIT | REQ-024 has one more read-only line (Issue #32) | Fixed: the note says the earlier read-only lines apply to the work that they name |
| P1R2-04 | NIT | wrong record path | Fixed: `reviews/design-round-1.md` |

Open questions for the PR-1 ready card: whether the decision for a change
(C3 (a)) must be the user's own message in the dispatching session or may be
relayed (no rule says; the cards asked for the user's own message); whether
that decision also counts as the re-acceptance after the merge.

## Round 3 (narrow confirmation, P1-R3)

Dispatch: `dev-reviewer`, requested opus/high (role `review-routine`),
recorded `unknown`, case `not read back`. CB-4 by the main agent: before and
after HEAD `23ed6dd…`, status `37bf3ffa…0f1b`, diff `73b2383c…10f6`; exit 0
each; equal. Result: P1R2-01 to P1R2-04 fixed; no new finding.

Observation (no finding, kept as is): the P1S-03 cell reads "Fixed by
deletion: …": the deleted part is the reason clause "it cannot be checked
without a hostname"; the shown sentence is what stays.
