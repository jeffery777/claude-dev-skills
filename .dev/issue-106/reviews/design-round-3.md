# Issue #106 PR-1 redesign, design review round 3 (design v1)

Written per ASD-STE100 principles; full conformance not verified.

Target: `.dev/issue-106/plan.md` section "PR-1 redesign" (design v1) and
`cards-3.md` (draft), on PR #107 head `e71b2eb793b9c0d2a4f5d00df7dd2637457aa04c`.
CB-4 (base text) by the main agent before and after both reviews: HEAD
`e71b2eb…`, status SHA-256 `54506b5c…504c`, diff SHA-256 `1e0b1548…0dca`;
exit 0; equal. The target files did not change during the reviews.

| Review | Agent | Requested | Recorded |
| --- | --- | --- | --- |
| DR3-deep | `dev-reviewer` | opus/xhigh | `unknown`, case `not read back` |
| DR3-sec | `dev-security-reviewer` | opus/xhigh | `unknown`, case `not read back` |

## Findings and triage (R-REV-4)

| ID | Severity | Triage | Disposition (design v2 item) |
| --- | --- | --- | --- |
| DR3-S-01, DR3-D-03 | MUST-FIX | a pack update changes rules, detection or `disallowedTools` and the acceptance stays; Core :31 | Fixed by deletion: free-text fields gone; one reference file; a digest of it, CB-4, CB-5 and both tool lines pinned to `ACCEPTANCE_VERSION` (items 1, 3) |
| DR3-S-02, DR3-D-04 | MUST-FIX | the resource and isolation limits and "agent never edits a record" were lost; Core :29, :31 | Fixed: kept in R-REV-1 in general words (item 4) |
| DR3-S-03 | MUST-FIX | wrong base or loose parse lets a change qualify itself | Fixed: base contract of the read-back script, parse contract of `platform_profile.py`, fixed key set (item 2) |
| DR3-D-01, DR3-S-05 | MUST-FIX / SHOULD-FIX | re-acceptance dead end | Fixed: a record-only change replaces the record codes with the user's decision; `validate` on the head before merge (items 2, 5) |
| DR3-D-02, DR3-S-07 | MUST-FIX | a new `.dev/config.json` key makes `platform_profile` `BLOCKED` | Fixed by a separate file (item 1) |
| DR3-S-04 | SHOULD-FIX | stderr and tracebacks leak paths | Fixed: one stdout line, empty stderr, all failures as codes (item 2) |
| DR3-S-06 | SHOULD-FIX | the first-record path rides on unrelated work | Fixed: only a change that touches that file alone; the decision names its change (item 5) |
| DR3-S-08 | SHOULD-FIX | the login and words become public history | Fixed: card fact; `decision` without paths or IDs; template with placeholders (items 1, 7) |
| DR3-D-05 | SHOULD-FIX | names left in DL-004, CB-5, REQ notes; no search list | Fixed (items 8, 9, 11) |
| DR3-D-06 | SHOULD-FIX | dev-retro names the Core repository already at base | Reading written in item 10; the orchestrator confirms it |
| DR3-S-09, DR3-D-07 | REQ-GAP / NHD | GitHub, `gh` and network needed | Needs Human Decision: card I106-C6 |
| DR3-D-08 | REQ-GAP | one account per repository | Needs Human Decision: card I106-C6 |
| DR3-D-09 | MUST-FIX (unclear) | card C4 (b) relaxed Core :31; C1 (a) already chose the binding | Fixed: the binding question is deleted; C4 asks only for this repository's acceptance |
| DR3-D-10 | NIT | card C5 fact without source; missing relay facts | Fixed in the card |
| DR3-S-10 | NIT | a narrowing on main reaches a branch after rebase | Fixed: README sentence (item 7) |

Kept as is (no recorded agent error): `GH_REPO` and several remotes for
`gh repo view` (false `STOP` only), the host reloading agent files mid
session (listed in the reference under what it misses), an `IN_REPO` self
check in the script (the base-copy rule covers the pack repository).
Residual: a full commit ID of the change passed as the base still lets a
change qualify itself; only the base rule (`git merge-base`, the literal in
the command text) stops it.

## Round 4 (narrow confirmation of design v2, DR4)

Dispatch: `dev-security-reviewer`, requested opus/xhigh, recorded `unknown`,
case `not read back`. CB-4 by the main agent before and after: HEAD
`e71b2eb…`, status `ba16c8aa…4f7b`, diff `972ebe63…9e74`; exit 0; equal.

| ID | Severity | Triage | Disposition (design v3) |
| --- | --- | --- | --- |
| DR4-01 | MUST-FIX | the list was narrower than card C3 (a): a record edit or an R-REV-1 apply-sentence edit needed no decision; Core :29 | Fixed: one list as C3 (a) |
| DR4-02 | SHOULD-FIX | a digest-only update could keep a changed rule accepted | Fixed: version rule; apply sentences in the reference |
| DR4-03 | SHOULD-FIX | `--name-only` without `--no-renames` and without untracked files | Fixed: three fixed commands |
| DR4-04 | SHOULD-FIX | where the decision of a record-only change is kept | Fixed: the `decision` field; no other file; content-bound |
| DR4-05 | SHOULD-FIX | an agent-accepted residual (head passed as base) | Needs Human Decision: card I106-C4 fact; FU-063 scope |
| DR4-06 | SHOULD-FIX | card C6 lacked the main consequence (no commit at all off GitHub) | Fixed in the card |
| DR4-07 | SHOULD-FIX | card C5 overstated the relay rule and the merge-gate card | Fixed in the card |
| DR4-08 | SHOULD-FIX | false fact on dev-retro lines | Fixed; reading reworded; the orchestrator confirms |
| DR4-09 | NIT | digest ranges undefined | Fixed |
| DR4-10 | NIT | README hardening notes; source mark | Fixed |
| DR4-11 | NIT | when the check runs; exit 0 | Fixed |

Over-design: 1 (`validate`) deleted; 2 (README repeating CB-4) deleted; 3
(optional hardening) kept short at the user's request for reasons; 4 (two
lists) merged.

Re-evaluation (R-VER-2): rounds 3 and 4 each reported a new `MUST-FIX`, so
the main agent re-evaluated the approach. Result: the approach stands; both
`MUST-FIX` came from the design text drifting from the user's card answers
(C3 (a)), not from a wrong mechanism. Method change: the amendments quote the
card scope. No requirement change and no loosening; the work does not stop
for the user on this re-evaluation. The design-v3 amendments have no
separate confirmation round; the implementation review covers them.

## Round 5 (narrow review of design v4, DR5)

Dispatch: `dev-security-reviewer`, requested opus/xhigh, recorded `unknown`,
case `not read back`. CB-4 by the main agent before and after: HEAD
`e71b2eb…`, status `ba16c8aa…4f7b`, diff `e63f1f79…8a93`; exit 0; equal.

| ID | Severity | Triage | Disposition (design v4.1) |
| --- | --- | --- | --- |
| DR5-01 | MUST-FIX | the CB-4 exit-status rule lives in dev-retro, outside the pins; Core :31 | Fixed: the dev-retro Read-back section is pinned |
| DR5-02 | MUST-FIX | item 6 dropped D-032, "quoted" and "recorded" of card C3 (a); Core :29 | Fixed: C3 (a) words restored |
| DR5-03 | SHOULD-FIX | any typed text became a record | Fixed: exact `yes`, else no write |
| DR5-04 | SHOULD-FIX | the terminal gate was overstated; `/dev/tty` can reach the user's terminal | Fixed: stdin and stdout tty check; honest card and reference text |
| DR5-05 | SHOULD-FIX | a re-clone at the same path reused the record | Fixed: `st_dev` and `st_ino` in the key |
| DR5-06 | SHOULD-FIX | needs a terminal and a lasting home folder | Needs Human Decision: card I106-C4 fact |
| DR5-07 | SHOULD-FIX | card C4 omissions; an inference listed as fact | Fixed in the card |
| DR5-08 | SHOULD-FIX | an unpinned summary in the script | Fixed: `accept` prints the pinned reference section |
| DR5-09 | SHOULD-FIX | Issue body still says "in their own project" | To the orchestrator |
| DR5-10 | NIT | wrong directory | Fixed: `check` in the same command as CB-4 |
| DR5-11 | NIT | guessable file-name hash | Fixed: never in records; `accept` prints no path |
| DR5-12 | NIT | parse contract | Fixed |
| DR5-13 | NIT | reading of "路徑" | Fixed: one mapping sentence |
| DR5-14 | NIT | unsourced "loads from main" | Fixed |

Re-evaluation (R-VER-2): rounds 4 and 5 each had a new `MUST-FIX`. Both
again came from the design text dropping parts of an earlier user answer or
of an earlier pin, not from a wrong mechanism. Method change for the
implementation: before each design or rule edit, the main agent compares the
edited list with the card text it implements, word for word. No requirement
change and no loosening.
