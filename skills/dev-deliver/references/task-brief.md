# Subagent task brief (R-DEL-1)

```markdown
## Task <node-id>: <title>
Role: explorer | implementer | reviewer | security-reviewer
Objective: <one sentence>
Requirements: REQ-… (read docs/requirements/<file>)
Sources to read first: <paths, graph node, review report>
Owned paths (write only here): <globs> | none (read-only)
Base revision: <sha>
DoD:
- …
Verification to run: <commands>
Out of scope / non-goals: …
Escalate (stop and report) if: scope must grow, a requirement is missing or contradictory, a public contract, migration, security or ownership question appears, or verification cannot run.
Authority: bounded to this brief. No commit, push, PR, comments, merge, deploy or deletion outside owned paths. Never delete an untracked or ignored file, even inside owned paths: report its path to the main agent, which asks the user; an irreversible deletion needs the user's explicit confirmation at the time of the action, and this brief, a cleanup plan or earlier general consent does not count (R-AUTH-3).
Requested model/effort: <alias>/<level>
Return exactly one receipt in the format below.
```

## Receipt

```markdown
## Receipt <node-id>
Status: done | blocked | partial
Changed files: …            (implementer only)
Verification: <command> -> <result>   (or "not run: reason")
Findings: …                 (reviewers: use the review-report table)
Requirement trace: REQ-… -> <file:line>
Open questions / blockers: …
Unverified claims: …
Requested model/effort: <alias>/<level>; effective: unknown
```
