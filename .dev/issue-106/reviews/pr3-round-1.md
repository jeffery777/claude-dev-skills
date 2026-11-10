# Issue #106 PR-3 review, round 1

Written per ASD-STE100 principles; full conformance not verified.

Target: the index on base `1ae24b5a9d3ccd431eb16923cfb3c4abfc4037c4`, SHA-256 of
`git diff HEAD --binary --no-ext-diff --no-textconv` = `b1cfdb08…bb3e`.
Before the reviews: `reviewer_acceptance.py check` printed `PASS` in the same
command as the CB-4 commands; CB-4 before and after: status `0fade8f1…94a8`,
diff `b1cfdb08…bb3e`; equal. Setup change: card I106-C7 (a), the user's own
message in this session (`cards-4.md`).

| Review | Agent | Requested | Recorded |
| --- | --- | --- | --- |
| P3-deep | `dev-reviewer` | opus/xhigh | `unknown`, case `not read back` |
| P3-sec | `dev-security-reviewer` | opus/xhigh | `unknown`, case `not read back` |

The user asked to pause after both reviews (relayed, 2026-11-09), then said
「繼續」 (relayed, 2026-11-10) without answering the two new cards.

| ID | Severity | Triage | Disposition |
| --- | --- | --- | --- |
| P3S-01 | MUST-FIX | "license notices are kept" loosened the base look-for rule (a private real name or email in a LICENSE line); REQ-011, no-regression rule | Fixed: "are not removed for a literal match alone" (SKILL.md, agent, test) |
| P3S-02 | SHOULD-FIX | a rendered PDF or notebook view hides metadata; Core :97, :99 | Fixed: "read whole as raw text; a rendered view does not count"; the attachment name and label are scan input |
| P3S-03, P3D-02 | SHOULD-FIX | `dev-implement` commit step 2 lacked the signing input; REQ-022 | Fixed |
| P3D-03 (b), (c) | SHOULD-FIX | DL-050 lacked Core :99 (reconcile) and :101 (no claim to find every secret) | Fixed: DL-050 items; "A scan never claims that it found every secret" in R-REV-9 and the agent copy |
| P3D-03 (a) | SHOULD-FIX | other PR and Issue metadata (Core :97) | Needs Human Decision: card I106-C9 (`cards-5.md`) |
| P3D-01, P3S-09 | SHOULD-FIX / REQ-GAP | the destination check stops SSH, GitHub Enterprise and GitLab remotes with no allow path; a regression against the base | Needs Human Decision: card I106-C8 (`cards-5.md`) |
| P3S-04 | NIT | `<owner/name>` value rule | Waits for card I106-C8 (the check may be deleted) |
| P3S-07 | NIT | a `pushInsteadOf` test case | Waits for card I106-C8 |
| P3S-05 | NIT | `--repo github.com/<owner/name>` | Kept as is (a single flag, no recorded agent error) |
| P3S-06 | NIT | `user.signingkey` class needs its value in context | Fixed by deletion: set or not set only |
| P3S-08, P3D-06 | NIT | DL-050 merge destination and push-certificates source | Fixed |
| P3D-04 | NIT | FU-007 row still listed release notes | Fixed: release notes covered since PR-3 |
| P3D-05 | NIT | REQ-029 says "private files" does not change | Fixed: "private files, confidential files" keeps the words |
| P3D-07 | NIT | K20 to K26 without per-file rows | Fixed: the search list is run again before the commit with per-file rows |

Kept as is (residual, no recorded agent error): the agent description and the
`dev-review` and `dev-gate` summaries name no Release post; ref names beyond
card I106-C9; the OpenPGP user ID class; the double question for
`commit.gpgsign=true`.

## Cards I106-C8 and I106-C9

The user's own message in this session (2026-11-10): 「C8 d，C9 a」.

- P3D-01, P3S-09: `Fixed` by C8 (d). Push step 2 is the base test again (the
  push URL equals the fetch URL, from `get-url` after rewrites); the URL-form
  check is deleted. When step 2 prints `STOP`, push step 5 lets the user decide
  in the session that dispatches the push scan; the URL goes into the chat only.
- P3S-04: no longer applies (the `<owner/name>` value of the deleted check).
- P3S-07: `Fixed`: a test sets `pushInsteadOf` and expects `STOP` from step 2.
- P3D-03 (a): `Fixed` by C9 (a): the scans read the labels, milestone and
  assignees that a post sets, and the ref names that a push sends.

## Round 2 (narrow confirmation, P3-R2)

Dispatch: `dev-security-reviewer`, requested opus/xhigh, recorded `unknown`,
case `not read back`. Before it: `reviewer_acceptance.py check` printed `PASS`
in the same command as CB-4; CB-4 before and after: status `bf951729…30f8`,
diff `cbb432ca…c728`; equal. Result: the round-1 fixes are applied (P3S-01
gives no loosening against the base); the fix round is not confirmed.

| ID | Severity | Triage | Disposition |
| --- | --- | --- | --- |
| P3R2-01 | MUST-FIX | the step-5 allow path for a step-2 difference lets commits that the fetch side has, and the push destination does not, pass unscanned (the FU-015 (1) case; Core :95) | Needs Human Decision: card I106-C11 (`cards-7.md`) |
| P3R2-02 | SHOULD-FIX | "the user decides" lacked "own message" of the card | Waits for card I106-C11 (gone under its option (a)) |
| P3R2-03 | SHOULD-FIX | showing the push URL can put a credential into the context | Waits for card I106-C11 (gone under its option (a)) |
| P3R2-04 | NIT | ref names read in the push scan, not the text scan | Kept as is (the same reviewer reads them; no recorded agent error) |
| P3R2-05 | NIT | summaries shorter than the rule text | Kept as is (the rule text is complete) |

## Card I106-C10

The user's own message in this session (2026-11-10): 「C10 a」 (`cards-6.md`).
Applied: the record key is the SHA-256 of the real path and `st_ino` (no
`st_dev`); `ACCEPTANCE_VERSION` 3; the reference record paragraph and version
table; `PINNED` keeps 1 and 2 and adds 3; a test checks the key; CHANGELOG.

## Card I106-C11

The user's own message in this session (2026-11-10): 「C11 a」 (`cards-7.md`).
Applied: push step 5 and the `dev-implement` push check are the base text
again; `skills/dev-core/references/push-scan.md` has no change in PR-3. P3R2-01
`Fixed` by deletion; P3R2-02 and P3R2-03 no longer apply (the allow path and
the URL display are gone). DL-050, REQ-011 note, `log.md` row and CHANGELOG
say that a push-URL difference still stops the push.

## Round 3 (narrow confirmation, P3-R3)

Dispatch: `dev-security-reviewer`, requested opus/xhigh, recorded `unknown`,
case `not read back`. CB-4 before and after: status `f14afcaa…a7dd`, diff
`17233520…cd1c`; equal; `check` printed `PASS` before it. Result: C10 (a) and
C11 (a) applied word for word; P3R2-01 fixed; P3R2-02 and P3R2-03 no longer
apply; no `MUST-FIX` or `SHOULD-FIX`.

| ID | Severity | Triage | Disposition |
| --- | --- | --- | --- |
| P3R3-01 | NIT | the README said the check prints `STOP VERSION` at a version raise; for this raise the key changes too, so it prints `STOP NO_RECORD` | Fixed by deletion: the README parentheses are gone; the pinned reference sentence stays (it holds for a raise without a key change) |
| P3R3-02 | NIT | the plan section "PR-3 implementation" did not name the later cards | Fixed: one note in that section |

Residual (no finding): a container rebuilt from an image with a kept home
folder, or a block-level copy, can keep the same path and inode number and so
reuse the record; this is the residual of card I106-C10 that the user
accepted.
