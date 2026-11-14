# Issue #114 implementation review of U1, round 1

Written per ASD-STE100 principles; full conformance not verified.

## Binding

- Target: U1 paths, uncommitted, at HEAD = base
  `7e71ad5061b345d6f8c921adca65bf494876855c`: `git diff HEAD` of
  `.dev/followups.md`, `CHANGELOG.md`, `README.md`, REQ-018, REQ-020,
  REQ-026, `docs/requirements/index.md`, `docs/requirements/log.md`; the new
  file REQ-030 (SHA-256 `299650549eacd611b7e6eb20eb8918c2e81db0766f5e7263fc96edf042484261`);
  the records under `.dev/issue-114/`. Diff hash of the whole tree before
  and after the reviews (CB-4): `67a1f18fcd54e78a7d5773cef3b3331d4d6ed36a5f64ce212698935f3c7f0fd2`
  (it also holds the U2 paths, which were not a target).
- Reviews, dispatched in parallel: deep (`dev-skills:dev-reviewer`, role
  `review-deep`) and Security Diff Scan (`dev-skills:dev-security-reviewer`,
  role `review-security`), each with `opus`/`xhigh` passed. Recorded:
  `unknown`, case `not read back`. Effective: `unknown`.
- `reviewer_acceptance.py check` printed `PASS` (exit 0) in the same Bash
  command as the CB-4 values before the dispatch; after both reviews the
  CB-4 values and the file hashes were the same (exit 0).
- Reported commands: read-only `git diff`, `git grep`, `git status`,
  `gh issue view`, `gh api` (GET), `gh release create --help`, `curl` of
  official docs (deep), `cmp`, `shasum`, `awk`, `perl`; the deep reviewer
  ran `python3 -I -B -m unittest discover -s tests -q` -> 424 tests, OK
  (3 skipped), status unchanged. No reviewer reports a write.
- Security Diff Scan verdict: PASSED (bounded; no claim that every secret
  was found). The `awk` check printed lines only in unchanged rule text
  (`-----BEGIN ` as a literal).

## Findings and dispositions

| ID | Relation | Severity | Summary | Class | Disposition |
| --- | --- | --- | --- | --- | --- |
| IR1-D-01 | in-scope | SHOULD-FIX | CHANGELOG "entries are in the order of the changes" is false: the section is grouped by kind | necessary fix | Fixed: "grouped by kind, not by date; the entry of the later merged change supersedes" |
| IR1-D-02 | in-scope | SHOULD-FIX | FU-027 and REQ-026: "reaches a user at the next update" without host scope; "no option makes sure" without a mark | necessary fix | Fixed: scoped to Claude Code (official docs), pinned installs excluded, Cowork not verified (FU-069 item 5); marked inference |
| IR1-S-01 | in-scope | SHOULD-FIX | Same root as IR1-D-02 in the CHANGELOG limits; FU-069 item 5 does not link back to FU-027 | necessary fix | Fixed: limit item 1 scoped to Claude Code; FU-069 item 5 reopens FU-027 when the update does not arrive; Remaining risk says the definition is verified for Claude Code only while item 5 is open. No change of the card C2 answer: card C1 (c) named the Cowork gap |
| IR1-D-03 | in-scope | SHOULD-FIX | Release limits miss two Cowork items that FU-069 says they name | necessary fix | Fixed: limit item 3 names pack-read prompts and updates without `version` |
| IR1-D-04 | in-scope | SHOULD-FIX | Graph node G and the plan DoD say `Closes #114`, against card C6 (a); stale requirement lists | necessary fix | Fixed: `Part of #114` and `Closes #3`; requirement lists include REQ-020, REQ-030, REQ-009 |
| IR1-D-05 | in-scope | NIT | CHANGELOG entry says REQ-026 follows the rename; REQ list incomplete | necessary fix | Fixed |
| IR1-D-06 | in-scope | NIT | "only three dispatches" | necessary fix | Fixed: "three kinds of dispatch", listed; same as IR1-S-03 |
| IR1-S-03 | in-scope | NIT | Same as IR1-D-06 | necessary fix | Fixed with IR1-D-06 |
| IR1-S-02 | in-scope | NIT | Reviewer read-only "rests on instructions" only under Cowork | necessary fix | Fixed: a separate limit item for Claude Code and Cowork, with FU-004 |
| IR1-D-07 | in-scope | NIT | FU-001 "four plugin agents passed" says more than the comment; REQ-001 scope sentence missing | necessary fix | Fixed: "were available, and a dispatched `dev-explorer` worked"; REQ-001 sentence marked inference |
| IR1-D-08 | in-scope | NIT | Card numbers in the design record are off by one; NHD answers not mapped | necessary fix | Fixed in `plan.md` (section "Implementation review U1, round 1"), not in the hashed design record |
| IR1-S-04 | in-scope | NIT | Handover has no check before the create that `v0.1.0` does not exist | necessary fix | Fixed in plan D6 handover: fetch, tag ref must answer 404, squash assumption |

Also changed from residual notes of the deep review: README says that
`e37a990` is earlier than the release commit, and explains "ref"; the
CHANGELOG explains "Reading A"; REQ-030 non-goals cite card C1 (c).

## Writing spot-check (deep review)

Scope: README zh and EN (install, Cowork, version), CHANGELOG header,
limits and entry, REQ-030, the FU rows; against `writing.md`. Results:
bilingual content matches; terms consistent; the Cowork steps match
Issue #3; unexplained "Reading A" and "ref" and the missing Cowork limits
were findings or notes (fixed above). Limit: no full ASD-STE100 check.

## Residual risk and limits

- `docs/design-proposal.md` and `skills/dev-core/deltas.md` (DL-039) say in
  the present tense that FU-036 evaluates the floor; FU-036 is now done.
  `deltas.md` is rule text, outside the scope of Issue #114 (no card
  decided a rule text change); left as is.
- No deterministic check keeps `version` out of the manifests
  (`check_pack` allows the key); REQ-030 states the rule.
- The CHANGELOG date and the tag date can differ (plan D3 has the
  procedure).
- FU-069 item 5 records the loaded commit only; it does not run the skills
  again at the release commit.
