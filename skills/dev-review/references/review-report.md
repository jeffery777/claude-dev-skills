# Review report format

```markdown
# Review <round> — <objective-id or target>

- Target: <base>..<head> | working tree at <HEAD> (+ uncommitted)
- Diff identity: sha256 of `git diff <base> <head> --binary` (or `git diff HEAD --binary` after `git add -N .`)
- Mode: routine | deep | security
- Reviewer: <agent> (requested model/effort: <model>/<effort>; effective: unknown)
- Scope: <paths>  Requirements: REQ-…  DoD: <ref>

## Findings

| ID | Severity | Location | Finding | Evidence | Impact | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | MUST-FIX | src/a.py:42 | … | … | … | Fixed / Deferred / Rejected / Needs Human Decision |

Severity: MUST-FIX, SHOULD-FIX, NIT, SCOPE-CREEP.

`SCOPE-CREEP` covers an addition that no requirement covers: an abstraction,
an option, a fallback, a validator, a layer, or a generalized requirement.
State which requirement it fails to trace to.

## Requirement trace

| REQ | Covered by | Verified by |
| --- | --- | --- |

## Security scan

Applicable: yes | no (scope examined, reason)
Status: PASSED | FINDINGS | NOT_RUN (capability: UNAVAILABLE, reason, coverage)

## Verification evidence

Commands run, their results, and what was skipped and why.

## Residual risk and limits
```

## Disposition requirements

- `Fixed` needs the fix revision, the verification and the re-review round.
- `Rejected` needs the source and the reason.
- `Deferred` needs a target, an owner, the reason, the remaining risk, a
  verification plan, and a trigger that makes it blocking.
- `Needs Human Decision` needs the exact question.
