# Review report format

```markdown
# Review <round> — <objective-id or target>

- Target: <base>..<head> | working tree at <HEAD> (+ uncommitted)
- Diff identity: sha256 of `git diff <base> <head> --binary` (or `git diff HEAD --binary` after `git add -N .`)
- Mode: routine | deep | security | commit / push scan
- Commit / push scan only (R-REV-9): sha256 of `git diff --cached --binary`, or the refs and commit range the push sends, or the PR or Issue text; the author, committer and message checked (masked)
- Reviewer: <agent> (requested model/effort: <model>/<effort>; effective: unknown)
- Scope: <paths>  Requirements: REQ-…  DoD: <ref>
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-001 | in-scope | MUST-FIX | src/a.py:42 | … | … | … | necessary fix | Fixed / Deferred / Rejected / Needs Human Decision |

Relation (`requirement_relation`, R-REV-3): `in-scope`, `gap`,
`no-requirement` or `unrelated`. The reviewer fills it in.

Severity (R-REV-3 thresholds): `MUST-FIX` only for Core blockers (an unclear
case counts as `MUST-FIX`); `SHOULD-FIX` a reproducible failure that affects a
requirement, the DoD or documented behavior; `NIT` only a regression of this
change or false documentation; `SCOPE-CREEP` for `no-requirement`; `REQ-GAP`
for `gap`. A Core blocker is `MUST-FIX` for every relation. Items below the
thresholds go to residual risk, not to this table. An `unrelated` item goes to
residual risk or a follow-up and does not block.

Class (R-REV-4, filled in before any fix): necessary fix, worth improving,
keep as is, or needs human decision.

`REQ-GAP` covers a problem that no requirement covers but one seemingly
should. It is not fixed in the same round: it gets a decision card
(`decision-card.md`) with the options add a requirement, defer, or reject
(R-REV-3).

`SCOPE-CREEP` covers an addition that no requirement covers: an abstraction,
an option, a fallback, a validator, a layer, or a generalized requirement.
State which requirement it fails to trace to (R-RIG-3).

## Requirement trace

| REQ | Covered by | Verified by |
| --- | --- | --- |

## Security scan

Applicable: yes | no (scope examined, reason). A commit / push scan (R-REV-9) is always applicable.
Status: PASSED | FINDINGS | NOT_RUN (capability: UNAVAILABLE, reason, coverage)

## Verification evidence

Commands run, their results, and what was skipped and why.

## Residual risk and limits
```

Mask every secret or private identifier in the report: give its kind,
location and length or class only; for an email, say only whether it is a
noreply address and its provider; replace the account or host part of a path
or hostname with a placeholder. Never paste raw command output that contains
such a value (R-REV-8).

## Disposition requirements (R-REV-3)

- `Fixed` needs the fix revision, the verification and the re-review round.
- `Rejected` needs the source and the reason.
- `Deferred` needs a target, an owner, the reason, the remaining risk, a
  verification plan, and a trigger that makes it blocking.
- `Needs Human Decision` needs the exact question as a decision card
  (`decision-card.md`).
