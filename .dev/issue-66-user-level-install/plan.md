# Issue #66 plan: user-level install without permission allow rules

- Objective: REQ-028. The pack's skills read their own pack files without a
  "Read outside the working directories" prompt in a user-level install,
  with the narrowest grant that works (user goal, 2026-10-26; cards A1, B1,
  C1, D1 and the FU-025 record, 2026-10-27: 「A1、B1、C1、D1，FU-025 照建議」).
- Rigor `strict`: a permission grant is a trust boundary (R-RIG-1). Deep
  review and Security Diff Scan, R-REV-9 scans, an exact-head gate and the
  user's merge decision.
- Review units: one high-risk unit (task node T1), alone in this PR.
- Step 1 (experiments, no pack change; Claude Code 2.1.310, headless
  `claude -p`, a throwaway plugin outside this repository):
  - `Read(${CLAUDE_PLUGIN_ROOT}/**)` and `Read(${CLAUDE_SKILL_DIR}/**)` do
    not match; with a leading `/` the read is allowed without a prompt.
  - The grant holds only in the invoking turn, also for subagents (plugin
    agent and `general-purpose`) dispatched in that turn; the next turn
    (same process or resumed) is denied.
  - `..` out of the allowed tree, a symlink to a file outside, a deny rule
    given with the CLI `--disallowedTools`, Write and Edit: all denied. A bare `Read` allows any read in that
    turn. Outside a plugin, `${CLAUDE_PLUGIN_ROOT}` is not expanded.
  - The YAML list of the two narrow rules works, also for a
    `vendor/<x>/contracts/` tree, next to `disallowed-tools`.
  - A security review (read-only) rejected a rule for the whole plugin root:
    in a directory install the plugin root is the repository root
    (`.claude-plugin/marketplace.json` source `./`), with `.git/` and local
    files.
- Implementer: `dev-skills:dev-implementer`, model `opus`, effort `high`
  (R-DEL-2 floor for trust-boundary work); effective effort `unknown`.
- Verification before the PR (card C1; 2026-10-27, headless `claude -p`,
  Claude Code 2.1.310, `--plugin-dir <worktree>`, a throwaway project
  outside this repository):
  - The turn that invokes `/dev-skills:dev-core` read
    `contracts/workflow.md` and `skills/dev-core/deltas.md` without a
    denial; a `general-purpose` subagent dispatched in that turn read
    `deltas.md` without a denial.
  - The next turn (same process, no skill): Read of `deltas.md` denied.
  - A later turn that invokes `/dev-skills:dev-continue`: Read of
    `deltas.md` allowed again.
  - `README.md` at the plugin root, a file outside the plugin, and the same
    `skills/dev-core/deltas.md` path in another checkout outside the plugin
    root: denied (the rules are anchored; raw output for the other checkout:
    `<scratch>/out/w-anchor.jsonl`).
- Not verified (FU-031): interactive sessions (headless shows a denial, not
  a prompt); a load from a real installed plugin, including what
  `${CLAUDE_PLUGIN_ROOT}` expands to in a directory install (the installed
  record names a cache path while the skills load from the source checkout;
  if it expands to the cache, pack reads still prompt, which fails closed);
  a plugin agent dispatched with the two rules (only `general-purpose` was
  tested); Grep and Glob; a deny rule from a settings file (only the CLI
  `--disallowedTools` was tested); Bash (the grant names only Read).
- `check_pack.py` runs in `scripts/validate.sh` and CI, not when Claude Code
  loads the plugin. It checks a closed world (card I66-R2-C1 (a)): the
  plugin root holds only the 13 tracked names and `.git` and `.claude`
  (allowed root names, not plugin components; `.claude` holds local
  session worktrees in this repository), in exact case; `.claude-plugin/`
  holds exactly `plugin.json` and `marketplace.json`, valid JSON (a clear
  error, not a traceback) with keys inside allowlists of the keys in use, and one marketplace entry,
  `dev-skills` with source `./`; `skills/` holds only non-hidden
  directories with a regular `SKILL.md`, `agents/` only non-hidden regular
  `*.md` files; hidden names count, and names that differ only in case in
  one directory under `skills/`, `agents/` or `vendor/` fail. It checks the
  raw front matter of each skill (printable ASCII with LF line ends, five
  allowed keys, each once, `allowed-tools` exactly the two item lines) and
  agent file (the same text rules, only the seven keys in use; card
  I66-R1-C1 (a)); no value contains `---`, and a value that starts with a
  quote must end with the same quote, with no other such quote and no
  backslash inside. It refuses a `skills`, `agents` or `vendor` root entry
  that is a symlink, and symlinks and hardlinked files under `skills/` and
  `vendor/`.
- Review round 3 (confirmation): deep review I66R3-001 to I66R3-003,
  Security Diff Scan I66S3-001 to I66S3-007. The Security Diff Scan found
  no new `MUST-FIX` or `SHOULD-FIX` in the detection mechanism. I66R3-001
  (`MUST-FIX`) is a test gap: the detection is correct, and two
  independent checks fire for a symlinked skill entry; the main agent
  judged it not a new blocker in the mechanism, so the work does not move
  to option (b) of card I66-R2-C1 (stated for the user in the merge card).
  Dispositions: I66R3-001 Fixed (negative tests for a symlink directly
  under `skills/`, a `SKILL.md` that is a symlink or a directory, two
  `agents/` names that differ only in case, an `agents/*.md` symlink; the
  case tests call `skipTest` on a case-insensitive file system); I66R3-002
  Fixed (the quote rule is stated exactly); I66R3-003 and I66S3-007 Fixed
  (README validation item in both languages; the closed-world error names
  both causes, a new component or a local file such as `.DS_Store`);
  I66S3-001 Fixed (a symlinked `agents` root entry fails); I66S3-002 Fixed
  (`.git` and `.claude` are allowed root names, not plugin components);
  I66S3-004 Fixed (deep-nested manifest JSON and a non-UTF-8 `SKILL.md`,
  agent file or skill `*.md` file give a clear error); I66S3-005 Fixed
  (with I66R3-001); I66S3-006 Fixed (CHANGELOG case sentence scoped to
  `skills/`, `agents/` and `vendor/`); I66S3-003 Deferred to FU-032.
- Review round 1: deep review I66R1-001 to I66R1-004, Security Diff Scan
  I66S1-001 to I66S1-005. Dispositions: I66R1-001 and I66S1-001 Fixed (the
  guard reads the raw front matter text, not the permissive subset parser);
  I66R1-002 and I66S1-004 Fixed (evidence and verified statements
  corrected); I66R1-003 Fixed by the 2026-10-27 measurements above;
  I66R1-004 reclassified in scope (Core `workflow.md#wf-writing`: limits are
  kept and both languages match) and Fixed in the README; I66S1-003 Fixed
  (README Cowork paragraph); I66S1-005 Fixed (symlink-to-file, broken
  symlink and hardlink tests and the hardlink check); I66S1-002 `REQ-GAP`,
  Fixed by the user answer to card I66-R1-C1: 「I66-R1-C1 選 a」 (agent
  front matter key allowlist; no `hooks/`, `commands/`, `.mcp.json`, and no
  hooks, settings or MCP keys in `plugin.json`). The checks for `.lsp.json`
  and `settings.json` and the manifest key allowlists were the main
  agent's additions to close A1 bypasses, not part of card I66-R1-C1; the
  closed-world check of card I66-R2-C1 (a) now subsumes them.
- Review round 2: deep review I66R2-001 to I66R2-006, Security Diff Scan
  I66S2-001 to I66S2-007. The R-VER-2 stop rule fired: the same mechanism
  (the check_pack guard) had new blockers in two rounds. Card
  I66-R2-C1 (a), user answer 「I66-R2-C1 選 a」: replace the listed checks
  with the closed-world check. Dispositions: I66R2-001 and I66S2-001,
  I66R2-002 and I66S2-003, I66R2-003 and I66S2-004, I66S2-002, I66S2-005,
  I66S2-006 and I66S2-007 Fixed by the closed-world check; I66R2-004
  (`REQ-GAP`) and I66R2-005 (`SCOPE-CREEP`) resolved by the card and the
  provenance fix above; I66R2-006 Fixed (FU-031 Item cell: the cache-layout
  test used only the whole-root and skill-dir rules). Fallback: if the
  confirmation review finds a new blocker in this mechanism, the work moves
  to option (b) of the card without another card.
