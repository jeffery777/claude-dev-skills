---
id: REQ-028
title: User-level install without permission allow rules - a narrow Read grant for the pack files (Issue #66)
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session), user message on the install goal of this pack (quoted in Issue #66, Goal)"
    quote: "我基本是希望這專案的技能是可以安裝到用戶層級的。這樣的做法比較正式，而不用另外設權限放行"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator session, relayed to the Issue #66 session), user answer to the Issue #66 step 2 cards A (A1: two narrow allowed-tools Read rules in each skill, a check_pack guard, the one-turn limit in the docs), B (B1: accept and document the cross-turn limit, no eager reads), C (C1: no test in the real ~/.claude now; a --plugin-dir check before the PR and a second-repository check after the merge) and D (D1: a follow-up row for the identity item of a remote branch, for a user decision), and to the recommendation for the FU-025 record (Issue #66 Part A)"
    quote: "A1、B1、C1、D1，FU-025 照建議"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator session, relayed to the Issue #66 session), user answer to review card I66-R1-C1 (finding I66S1-002: check agent front matter keys and plugin-level hooks, commands, MCP servers and settings)"
    quote: "I66-R1-C1 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator session, relayed to the Issue #66 session), user answer to review card I66-R2-C1 (R-VER-2 stop rule after review round 2: replace the listed check_pack checks with a closed-world allowlist of the root, .claude-plugin, skills and agents, a pinned marketplace entry and two front matter value rules)"
    quote: "I66-R2-C1 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator session, relayed to the Issue #66 session), user answer to merge card I66-M1 for PR #67 head 2991b4a (question 1: I66R3-001 was not a new blocker in the mechanism, so no move to option (b) of card I66-R2-C1; question 2: one fix commit for MR67-001 and the NITs; merge after the checks pass)"
    quote: "I66-M1：問題 1 選 a，問題 2 選 a，檢查通過後同意合併"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator session, relayed to the Issue #66 session), user answer to merge card I66-M2 for PR #67 head 47f6a77 (option (a): one fix commit for MR67B-001, MR67B-002 and MR67T-001, with the stop condition of the card: if the next exact-head Merge Review finds only test-coverage findings of the same kind, with the detection confirmed correct, they are Deferred to a follow-up row and the round passes; any other blocker goes to a card; merge after the checks pass)"
    quote: "I66-M2 選 a，加停止條件，檢查通過後同意合併"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator session, relayed to the Issue #66 session), user answer to merge card I66-M3 for PR #67 head 3c512ff (option (a): a closed value grammar for every skill and agent front matter value, which closes MR67C-001, MR67U-001, MR67U-002 and FU-032; the stop condition of card I66-M2 still applies, and if the next round finds another detection blocker in the guard, the work moves to option (b) without another card; merge after the checks pass)"
    quote: "I66-M3 選 a，檢查通過後同意合併"
non_goals:
  - No change of the user's settings, no permission allow rule and no `additionalDirectories` setup step (card A1).
  - No rule for the whole plugin root, no bare `Read`, `Grep` or `Glob`, and no grant for another tool, Bash included (card A1).
  - No inlining of Core or reference text into the SKILL.md files (card A1).
  - No eager reads of later references in the invoking turn (card B1).
  - No test in the real `~/.claude` in this Issue (card C1).
  - No deletion of a remote branch; the user decides it separately (card D1).
depends_on: [REQ-026]
refines: [REQ-016]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

The pack is installed at user level and used in any project. Its skills read
their own pack files (`dev-core`, references, templates and the vendored Core
contracts), which lie outside the working directory, so each read raises a
permission prompt. The user wants this to work without adding permission
allow rules.

Issue #66 step 1 (Claude Code 2.1.310, headless runs with a throwaway plugin)
found that a skill can declare `allowed-tools` Read rules with an absolute
`/${CLAUDE_PLUGIN_ROOT}/...` path. The grant holds only in the turn that
invokes the skill, including subagents dispatched in that turn. A rule for the
whole plugin root would also cover `.git/` and other local files in a
directory install, because the plugin root is the repository root.

By card A1, each skill declares exactly two narrow rules, a check keeps them
narrow, and the docs state the limits. By card B1, the cross-turn limit is
accepted: re-invoke a skill or approve the prompt.

## Acceptance

- Each `skills/*/SKILL.md` front matter has `allowed-tools` as a YAML list of
  exactly `Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)` and
  `Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)`;
  the other front matter keys stay (for example `disallowed-tools` of
  `dev-retro`).
- `scripts/check_pack.py` fails a skill whose `allowed-tools` is missing, a
  string, a bare tool, another tool, an extra or other rule, or a rule
  without the leading `/`. It reads the raw front matter text, not only the
  parsed values: it fails any character outside printable ASCII apart from
  LF line ends (CR, tab, U+0085, U+2028 included), any line that is not a
  column-0 `key: value` line with an unquoted key from `name`,
  `description`, `allowed-tools`, `disable-model-invocation` and
  `disallowed-tools`, used once, any `allowed-tools` that is not the
  line `allowed-tools:` followed directly by the two item lines in order
  (card I66-R2-C1 (a)), and any other value outside a closed grammar
  (card I66-M3 (a)): exactly one space after the colon, then a non-empty
  YAML plain scalar that does not start with a space, a backtick or any of
  `- ? : , [ ] { } # & * ! | > ' " % @`, holds no `: `, ` #` or `---`,
  and does not end with `:` or a space. It applies the same text rules to each
  `agents/*.md`, with only the keys that the agents use (`name`, `description`, `model`, `effort`,
  `tools`, `disallowedTools`, `color`), so a key such as `permissionMode`,
  `hooks`, `mcpServers` or `skills` fails (card I66-R1-C1 (a)). It checks
  a closed world (card I66-R2-C1 (a)), hidden names included: it fails
  any name at the plugin root other than the tracked `.claude-plugin`,
  `.dev`, `.github`, `.gitignore`, `CHANGELOG.md`, `LICENSE`, `README.md`,
  `agents`, `docs`, `scripts`, `skills`, `tests` and `vendor` and
  `.git` and `.claude`, which are allowed root names but not plugin
  components (`.claude` holds local session worktrees in this
  repository), in exact case (so `hooks/`, `commands/`,
  `monitors/`, `bin/`, `.mcp.json`, `.lsp.json`, `settings.json`, a root
  `SKILL.md` or `plugin.json`, or `Skills/` fail); any file in
  `.claude-plugin/` other than `plugin.json` and `marketplace.json`, a
  missing one, or one that is not valid JSON, deep nesting included (a
  clear error, not a traceback); a manifest key outside the allowlist of
  the keys in use: `.claude-plugin/plugin.json` (`name`, `displayName`, `version`,
  `description`, `author`, `homepage`, `repository`, `license`,
  `keywords`), `.claude-plugin/marketplace.json` (`name`, `owner`,
  `description`, `plugins`) and its `plugins` entry (`name`, `source`,
  `description`, `version`); a `plugins` value other than exactly one
  entry with name `dev-skills` and source `./`; an entry of `skills/` that
  is hidden, not a directory, a symlink, or without a regular file named
  exactly `SKILL.md`; an entry of `agents/` that is hidden, not a regular
  file or not named `*.md`; and names in one directory under `skills/`,
  `agents/` or `vendor/` that differ only in case. It fails on a
  `SKILL.md`, an agent file or a `*.md` file under a skill directory that
  is not a readable regular file in valid UTF-8, a directory named `*.md`
  included (a clear error, not a traceback). It fails on a
  `skills`, `agents` or `vendor` root entry that is a symlink, and on any
  symlink and any hardlinked regular file under `skills/` or `vendor/`.
  `tests/test_core_checks.py` has a negative test for each case, apart from
  the cases that FU-033 lists (Deferred by the card I66-M2 stop condition);
  `bash scripts/validate.sh` passes. The check runs in
  `scripts/validate.sh` and CI, not when Claude Code loads the plugin.
- A headless run with `--plugin-dir <worktree>` from a directory outside the
  worktree: the turn that invokes a dev-* skill reads `dev-core` and a Core
  contract on their skill paths without a permission denial, and a read of a
  plugin file outside the two trees in that turn is denied.
- `dev-core` CB-7 states the two rules, the one-turn limit, the reach to
  subagents dispatched in that turn, the re-invoke or approve step, a denied
  read handled as CB-6, never widen, the enforcement by `check_pack.py`, and
  what is not verified; DL-037 records the tightening.
- README Install (both languages) says that the skills read their pack files
  without a prompt in the turn that invokes a skill, that a later turn can
  prompt, to re-invoke a skill or approve, that no settings change is
  needed, and never to add a broad Read rule.
- `.dev/followups.md`: FU-025 is closed with the Issue #66 Part A record;
  FU-030 records the identity item (card D1) without any value; FU-031
  records the post-merge check with the real install (card C1).
- An independent deep review and a Security Diff Scan find no open
  `MUST-FIX` or `SHOULD-FIX`.

## Notes

- Experiment facts (Issue #66 step 1, headless): without the leading `/` the
  rule does not match; paths are normalized, so `..` out of a tree and a
  symlink to a file outside are denied; a deny rule given with the CLI
  `--disallowedTools` still wins; Write and Edit stay denied; a bare `Read`
  allows any read in that turn.
- Run of this worktree (2026-10-27, headless `claude -p`, Claude Code
  2.1.310, `--plugin-dir <worktree>`, a throwaway project): the turn that
  invokes `/dev-skills:dev-core` reads `contracts/workflow.md` and
  `skills/dev-core/deltas.md`, and a `general-purpose` subagent dispatched
  in that turn reads `deltas.md`, without a denial; the next turn without a
  skill is denied; a later turn that invokes `/dev-skills:dev-continue` is
  allowed again; `README.md` at the plugin root, a file outside the plugin
  and the same `skills/dev-core/deltas.md` path in another checkout are
  denied (the rules are anchored; the raw output for the other checkout
  is in `<scratch>/out/w-anchor.jsonl`).
- Not verified (FU-031): interactive sessions (headless runs show a denial,
  not a prompt); a load from a real installed plugin, including what
  `${CLAUDE_PLUGIN_ROOT}` expands to there (the installed record names a
  cache path while the skills load from the source checkout; if it expands
  to the cache, pack reads still prompt, which fails closed); a plugin agent
  dispatched in the invoking turn (only `general-purpose` was tested); Grep
  and Glob (not available in that version); a deny rule from a settings
  file; Bash (the grant names only Read).
- Review finding I66S1-002 (agent keys and plugin-level components were not
  checked) is fixed by the user answer to card I66-R1-C1: 「I66-R1-C1 選 a」
  (the agent key allowlist; `hooks/`, `commands/`, `.mcp.json` and
  hooks, settings or MCP keys in `plugin.json`). The checks for `.lsp.json`
  and `settings.json` and the manifest key allowlists were the main
  agent's additions in round 1 to close A1 bypasses, not part of that
  card; the closed-world check of card I66-R2-C1 now subsumes them.
- Review round 2 (deep I66R2-001 to I66R2-006, Security Diff Scan
  I66S2-001 to I66S2-007) found new paths and names that the listed checks
  missed; the R-VER-2 stop rule fired, and the user answer to card
  I66-R2-C1: 「I66-R2-C1 選 a」 replaces the lists with the closed-world
  check. If the confirmation review finds a new blocker in this mechanism,
  the work moves to option (b) of that card without another card.
- The root, agent and manifest allowlists are the sets in use on
  2026-10-27; a new root item, file or key needs a change of
  `check_pack.py` with review.
- `depends_on: [REQ-026]`: a denied pack read is handled as CB-6, which
  comes from FU-025 under REQ-026. `refines: [REQ-016]`: REQ-016 asks for
  the user-scope install; this REQ details its permission side (inference
  of the author, not stated by the user).
