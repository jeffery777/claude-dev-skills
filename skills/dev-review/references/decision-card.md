# Decision card

Use one card for every `Needs Human Decision` finding, every `REQ-GAP`, and
every other decision handed to the user (R-AUTH-6, R-REV-3).

## Rules

- One card asks one question. Put each card in the review report, the gate
  output or the message to the user.
- Before you raise the card, finish the safe work that does not depend on it (R-AUTH-6).
- Write the card in the user's language.
  - English follows the ASD-STE100 principles (R-WRT-1).
  - Traditional Chinese uses the plain-writing adaptation: one idea per
    sentence, an explicit subject, consistent terms, a plain explanation of
    each technical term at first use, and no vague words. Do not apply
    English word-count rules (R-WRT-1).
  - Never claim STE conformance (R-WRT-1).
- List every real option. For a `REQ-GAP`, the options are: add a
  requirement, defer, or reject (R-REV-3).
- Keep facts apart from inferences in the evidence. A fact has a source: a
  `path:line`, a command and its output, or a quote. Mark everything else as
  an inference.
- Mask secrets and private identifiers, as in the review report (R-REV-8).
- The card grants no authority. Only the user's answer decides. When the
  answer adds a requirement, `dev-plan` ingests it, and the REQ sources record
  the finding ID and the user's answer (R-AUTH-1, R-REV-3).

## Template

```markdown
### Decision card <n>: <short title>

- **Question:** <one sentence>
- **Why you must decide:** <the requirement, rule or authority limit that
  keeps the agent from deciding>
- **Options:**
  - **(a) <name>**
    - What it does: <the change or action>
    - Result: <what is true afterwards>
    - Risk: <what can go wrong>
    - Cost: <work, time, review or run cost>
  - **(b) <name>** … (same four lines)
- **Recommendation:** <option> — <reason>
- **If you do not decide:** <what is blocked> / <what can continue>
- **Evidence:**
  - Facts: <path:line, command and output, quote>
  - Inferences: <marked conclusions>
```

## Positive example

Adapted from PR-A decision card 1 (Issue #4). The user answered (a), and
REQ-011 records the answer. The original card did not separate facts from
inferences or give each option all four lines; this version does.

```markdown
### Decision card 1: Scan PR text before posting

- **Question:** Must the R-REV-9 scan also check PR titles, bodies and
  comments before they are posted?
- **Why you must decide:** REQ-011 quotes you about commits and pushes only.
  PR text is outside that requirement (`requirement_relation: gap`). Only you
  can add a requirement.
- **Options:**
  - **(a) Add it to REQ-011**
    - What it does: R-REV-9 also scans each PR title, body and comment
      before it is posted.
    - Result: everything that this workflow publishes gets a scan, including
      the Merge Review comment.
    - Risk: low; the scan can delay a post.
    - Cost: one `dev-security-reviewer` run per post.
  - **(b) Defer to a later PR**
    - What it does: records a follow-up and changes no rule now.
    - Result: this PR stays narrow.
    - Risk: this PR posts its review comments without a rule that scans
      them.
    - Cost: a later PR and its reviews.
  - **(c) Reject**
    - What it does: keeps the rule at commits and pushes.
    - Result: PR text is never scanned by rule.
    - Risk: a finding that quotes a secret can be posted in public.
    - Cost: none now.
- **Recommendation:** (a) — this workflow posts review records as PR
  comments, and those records can quote findings.
- **If you do not decide:** the rule change is blocked, so PR text stays
  out of the rules. / The implementation and the commit scan can continue.
  The agent still scans this PR's own comments by hand.
- **Evidence:**
  - Facts: finding SR-A-002 in
    `.dev/issue-4-commit-security/reviews/round-1.md`; REQ-011 sources quote
    only commits and pushes.
  - Inferences: review comments will quote findings that could contain
    private data.
```
