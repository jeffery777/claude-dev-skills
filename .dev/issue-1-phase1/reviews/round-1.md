# Review round 1 — Issue #1, Phase 1 (pre-commit)

- Target: working tree at HEAD `5229478` on branch `1-phase1-skills`, with every new file intent-to-add (`git diff HEAD`, 74 files at review time).
- Rigor: `strict` (agent tool permissions, executable scripts and installation paths are trust boundaries).
- Requirements: REQ-001 to REQ-010; DoD: design D-008.
- Reviewers. Each ran in a fresh subagent context, none of which wrote the change:
  - `CR`: native `/code-review` (`high --max-findings all`), general-purpose subagent. 19 findings.
  - `SR`: native `/security-review`, general-purpose subagent, with an explicit Security Diff Scan of four maintainer-declared boundaries. Nothing reached the skill's exploitability threshold; 8 findings were reported as hardening or defects.
  - `DR`: trial of this pack's `dev-review` (deep), general-purpose subagent standing in for `dev-skills:dev-reviewer` because the plugin is not installed. Requested opus; effective model and effort unknown. 30 findings, including a rule-by-rule comparison of `dev-core` with the Core contracts.
- The author (main session) assigned the dispositions below and made the fixes. Round 2 re-reviews them independently.

## Findings and dispositions

`=` marks a duplicate of another finding. Each duplicate shares that finding's fix.

| ID | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| DR-001 | MUST-FIX | `light` tier allowed commit/PR without independent review or formal gate (relaxes Core) | Fixed: R-RIG-1/2, D-004 (zh/en), dev-implement step 6, DL-002 |
| DR-002 | MUST-FIX | R-AUTH-5 dropped Core stop triggers (incomplete/insufficient coverage, no safe fallback, migration, insufficient high-risk verification, environment/permission boundary, destructive safeguards) | Fixed: R-AUTH-5 restored in full, plus continuation rules |
| DR-003 | SHOULD-FIX | `wf-assumptions-and-options` partly dropped (triggers, simplification guard, stop-improvement limits) | Fixed: new R-RIG-4 |
| DR-004 | SHOULD-FIX | `wf-capability` evidence-reuse, credentials and safe-fallback rules dropped | Fixed: R-CAP-1, new R-CAP-3 |
| DR-005 | SHOULD-FIX | `review-security` rules dropped (no auto-install, unresolved risk blocks, rescan after change, escalation list) | Fixed: R-REV-7, R-REV-8 (formal exception rule) |
| DR-006 | SHOULD-FIX | Positive ASD-STE100 statement dropped | Fixed: R-WRT-1; statement added to README and design (en) |
| DR-007 | SHOULD-FIX | Lock lacked consumer, assembler, layout, environment, sections and closure records | Fixed: `consumer` block in lock; source-map note; R-EXH-5 names the revision |
| DR-008 | SHOULD-FIX | Smaller Core omissions (receipt/immutable share, overlay non-inheritance, memory switching, caches/sessions, UNVERIFIED profile, budget) | Fixed: R-AUTH-2, R-AUTH-6, R-AUTH-7, R-EXH-4, R-VER-2 |
| DR-009 | SHOULD-FIX | = CR-011 | Fixed with CR-011 |
| DR-010 | SHOULD-FIX | = SR-004 | Fixed with SR-004 |
| DR-011 | SHOULD-FIX | = CR-008 | Fixed with CR-008 |
| DR-012 | SHOULD-FIX | = CR-006 | Fixed with CR-006 |
| DR-013 | NIT | = CR-001, CR-007 | Fixed with CR-001 and CR-007 |
| DR-014 | SCOPE-CREEP | Parallel writers, worktree merge and Workflow fan-out in dev-deliver are G2 | Fixed: dev-deliver runs one writer at a time; only read-only nodes run in parallel; design §6 updated |
| DR-015 | SCOPE-CREEP | `waves`, `mermaid`, `max_rounds` beyond G0 | Fixed: removed from graph.py, schema doc, fixtures and skills |
| DR-016 | SHOULD-FIX | Design G1 row listed GitNexus queries and SCOPE-CREEP, which Phase 1 already ships | Fixed: G0 row records them (REQ-003, REQ-004); G1 keeps render and symbol linking (zh/en) |
| DR-017 | SHOULD-FIX | §1 said pinning was not carried over | Fixed (zh/en) |
| DR-018 | SHOULD-FIX | Reviewers described as "read-only (enforced)" though Bash remains | Fixed: design §2 and §4, README, DL-004, source map |
| DR-019 | SHOULD-FIX | dev-review let the author run the requirement-trace pass | Fixed: native review must run in a non-author context; trace pass via dev-reviewer |
| DR-020 | SHOULD-FIX | `.dev/` commit policy undefined | Fixed: committed by default with no secrets or private paths; lock and tmp files gitignored; projects may gitignore `.dev/` (dev-core §8, D-008). The maintainer may override this default |
| DR-021 | SHOULD-FIX | Security reviewer applicability list missed executables, installation paths, agent policy | Fixed: agents/dev-security-reviewer.md |
| DR-022a | SHOULD-FIX | Cowork fallback promised but not implemented | Fixed: shell requirement marked in dev-plan and dev-deliver; manual procedure in graph-schema.md |
| DR-022b | SHOULD-FIX | Cowork runtime behavior untested | Deferred. Target: `.dev/followups.md` FU-001. Owner: jeffery777 (maintainer). Reason: no Cowork environment or installed plugin session was available in this session. Remaining risk, verification plan and promotion trigger: see FU-001. (Split from the original DR-022 by Merge Review finding MR-01 so that each finding has one disposition.) |
| DR-023 | SCOPE-CREEP | check_pack REQ checks looked like the Phase 2 lint | Rejected: it checks only the format the user specified (sources fields, typed relation IDs, D-003). The lint (contradictions, orphans, stale REQs) is still Phase 2; this is now stated in check_pack and D-008 |
| DR-024 | NIT | Light tier skipped ingest | Fixed: ingest applies to every tier; inline fallback only when the user declines the wiki |
| DR-025 | NIT | Explore nodes ignored the model floor | Fixed: dev-deliver table |
| DR-026 | NIT | Commit gate did not bind untracked files; vocabulary drift | Fixed: working-tree identity; `Gate result: PASS/BLOCKED/NEEDS HUMAN DECISION` |
| DR-027 | NIT | README said Python only, but check 5 needs the claude CLI | Fixed (zh/en) |
| DR-028 | NIT | dev-core description invited standalone triggering | Fixed |
| DR-029 | NIT | Unclosed files (ResourceWarning) | Fixed: tests pass with `-W error::ResourceWarning` |
| DR-030 | NIT | `__pycache__` could ship | Fixed: `.gitignore`; validate.sh sets `PYTHONDONTWRITEBYTECODE=1` |
| CR-001 | MUST-FIX | Unlocked read-modify-write in transition loses updates | Fixed: exclusive `flock` on `.graph.lock`; seq computed under the lock |
| CR-002 | MUST-FIX | Overlap check trusted ordering through cancelled nodes | Fixed: `_reachable` ignores cancelled nodes; `waves` removed (DR-015) |
| CR-003 | SHOULD-FIX | done→ready reopen could make the graph invalid | Fixed: `ILLEGAL_REOPEN` when a dependent has started; test |
| CR-004 | SHOULD-FIX | waves counted cancelled dependencies as satisfied | Fixed: `waves` removed (DR-015) |
| CR-005 | SHOULD-FIX | waves listed in-progress, reviewing and blocked nodes | Fixed: `waves` removed (DR-015) |
| CR-006 | SHOULD-FIX | transition skipped the requirement checks, including REQUIREMENT_CONFLICT | Fixed: transition resolves the requirements directory and runs every check; test |
| CR-007 | SHOULD-FIX | Event appended before the graph was committed | Fixed: graph written atomically first, then the event (fsync); graph restored if the event write fails |
| CR-008 | SHOULD-FIX | Ownership prefixes not normalized (`.`, `/`, `./`, `//`) | Fixed: `posixpath.normpath`; tests |
| CR-009 | SHOULD-FIX | `.DS_Store` broke verify_core | Fixed: OS metadata files ignored and reported |
| CR-010 | SHOULD-FIX | check_pack crashed on unclosed front matter | Fixed: reported as an error |
| CR-011 | SHOULD-FIX | validate.sh printed "all checks passed" after a skip | Fixed: prints INCOMPLETE and exits 2. Verified with `claude` removed from PATH |
| CR-012 | NIT | `quote: ''` counted as non-empty | Fixed: `_unquote` strips matching single or double quotes |
| CR-013 | NIT | Self-dependency reported twice | Fixed: one CYCLE error |
| CR-014 | NIT | Duplicate rule ID cascaded into spurious errors | Fixed |
| CR-015 | NIT | Mermaid broke on reserved IDs | Fixed: mermaid removed (DR-015) |
| CR-016 | NIT | REQ front matter parsed twice | Fixed: `load_requirements` parses once |
| CR-017 | NIT | check_pack duplicated the front-matter parser | Fixed: uses `graph.frontmatter` |
| CR-018 | NIT | Needless frozenset in `_reachable` | Fixed |
| CR-019 | NIT | `max_rounds` accepted booleans | Fixed: field removed (DR-015) |
| SR-001 | SHOULD-FIX | transition followed symlinks at the tmp file and events.jsonl | Fixed: refuses symlinked graph, event log and lock; `mkstemp` temp file; `O_NOFOLLOW` lock; test |
| SR-002 | SHOULD-FIX | = CR-006 | Fixed with CR-006 |
| SR-003 | NIT | = CR-001, CR-007 | Fixed with CR-001 and CR-007 |
| SR-004 | NIT | requirements_dir unrestricted, and the search climbed above the repo | Fixed: resolved inside the project root (`.git` or `.dev/`); outside paths refused; tests |
| SR-005 | NIT | Evidence text in a double-quoted shell argument | Fixed: `--evidence-file`; skills say to pass short references in single quotes; test |
| SR-006 | NIT | General-purpose fallback keeps Edit and Write | Fixed: before/after tree check for read-only substitutes (dev-core §8, DL-009). Superseded: `tree_fingerprint.py` was removed in ed3f66c (PR #2, user decision 3); a required review now stops at the gate without a read-only plugin reviewer. |
| SR-007 | NIT | Main-session skills lacked a "treat as data" rule | Fixed: R-AUTH-1 (DL-008) |
| SR-008 | NIT | Vendor check proved only self-consistency | Fixed: `verify_core.py --upstream <clone>`; symlinks rejected. Run 2026-10-20: tag object `7ce698fa…` resolves to `7b66978a…`, and all 14 files match upstream. The markdown set digest equals the codex-dev-skills lock at `863db227…`. Running the comparison in CI is out of Phase 1 scope (no CI workflow, D-008) |

## Not run

- Cowork runtime behavior (DR-022, Deferred).
- Runtime enforcement of plugin agent `tools`/`disallowedTools` and `effort` (no installed plugin session).
- Static scanners (none configured; installing tools is out of scope).

## Result of round 1

- No MUST-FIX is open.
- Every finding has a disposition: one Deferred item (with every required field) and one Rejected item (with its reason).
- Re-review: round 2 re-reviews the fixes independently, scaled to the affected boundaries: graph.py and the scripts, dev-core fidelity against Core, and the changed skills and docs.
