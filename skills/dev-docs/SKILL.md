---
name: dev-docs
description: Update project documentation from verified code, specs, requirements or behavior, and check code-docs coherence. Use when docs must match implemented behavior, when behavior changed, or for bilingual docs that must stay aligned.
---

# dev-docs

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first. The writing rules are in
R-WRT-1.

## Workflow

1. Read the code, tests, requirements, and the docs in scope. Name the reader
   and the purpose of each doc.
2. List the claims the docs make: commands, paths, flags, feature states,
   compatibility and limits. Check each claim against the source. Keep
   verified facts apart from inferences (R-EXH-2).
3. Update only the docs in scope. Keep the required technical detail, the
   prerequisites, the safety notes and the limits. Do not change code,
   commands, paths or license text for style (R-WRT-1).
4. For bilingual docs, compare the obligations, risks and limits in both
   languages. The authoritative language wins. Do not claim ASD-STE100
   conformance (R-WRT-1).
5. Do not add private paths, credentials, machine-specific details or runtime
   state (R-AUTH-7).
6. Run the cheap checks that exist: link checks, a markdown lint, or `grep`
   for the old names you replaced.
7. When behavior changed and no docs change is needed, write down why.

## Output

- Docs changed, and the source evidence for each claim
- Verification run
- Writing checks: the sample scope, the results and the unverified limits
- Unverified assumptions
