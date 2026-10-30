---
name: dev-docs
description: Update project documentation from verified code, specs, requirements or behavior, and check code-docs coherence. Use when docs must match implemented behavior, when behavior changed, or for bilingual docs that must stay aligned.
allowed-tools:
  - Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)
  - Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)
---

# dev-docs

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first, then the Core files that its stage map lists for `dev-docs`.
Read, run or copy each file that this skill names with a `${CLAUDE_SKILL_DIR}`
path only with that full absolute path, never with a path relative to the
working directory; when such a path does not resolve or cannot be read, stop
and report it (CB-6).
The writing rules are in
R-WRT-1.

## Workflow

When the main session does this itself for work under the R-DEL-2 floor,
the floor check of R-DEL-2 applies (`dev-core`).

1. Read the code, tests, requirements, and the docs in scope. Name the reader
   and the purpose of each doc (R-WRT-1).
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
7. When behavior changed and no docs change is needed, write down why (R-EXH-2).

## Output

- Docs changed, and the source evidence for each claim
- Verification run
- Writing checks: the sample scope, the results and the unverified limits
- Unverified assumptions
