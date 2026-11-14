---
id: REQ-030
title: Plugin version policy - no version in the manifests; a tag marks a reviewed snapshot (Issue #114)
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-11-14 (orchestrator session, relayed to the Issue #114 session), user answer to cards C1 to C6 of `.dev/issue-114/cards-1.md` (the orchestrator asked whether all six cards follow the recommendations: C1 c, C2 a, C3 a, C4 a, C5 a, C6 a); card C1 (c): both manifests drop `version`, the answer becomes this requirement, no Cowork re-test in Issue #114, FU-069 records a check after the release; it answers the REQ-GAP findings DR-D-02 and DR-S-06 of `.dev/issue-114/reviews/design-round-1.md`"
    quote: "全照建議"
  - type: external
    locator: "https://code.claude.com/docs/en/plugins/host-marketplace.md, section \"Release a new version\" (read 2026-11-14)"
    quote: "Omit `version`: users track your commits instead. Leave `version` out of both `plugin.json` and the marketplace entry."
  - type: chat
    locator: "Claude Code session 2026-11-14 (orchestrator session, relayed to the Issue #114 session), user answer to card C7 of `.dev/issue-114/cards-2.md` (option (a): `scripts/check_pack.py` fails when a manifest has `version`, with tests; answers the REQ-GAP findings IRU2-D-02 and IRU2-S-01 of `.dev/issue-114/reviews/impl-u2-round-1.md`)"
    quote: "C7 a"
non_goals:
  - A stable release channel (card C1 (c), risk line).
  - Pin instructions in the README; the `#ref` syntax of `claude plugin marketplace add` is not tested here (card C1 (c), recommendation; finding DR-S-06).
  - A Cowork re-test in Issue #114 (card C1 (c)).
depends_on: [REQ-001]
refines: [REQ-018]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

The plugin manifests set no `version`, so an install follows the commits of
`main`, and every reviewed merge reaches a user at that user's next update
(Claude Code: official docs; Cowork: not verified, FU-069).
A tag (for example `v0.1.0`) marks a reviewed snapshot, and its GitHub
Release carries the matching section of `CHANGELOG.md`.

## Acceptance

- `.claude-plugin/plugin.json` and the plugin entry of
  `.claude-plugin/marketplace.json` have no `version` key.
- `scripts/check_pack.py` fails when `.claude-plugin/plugin.json` or the
  plugin entry of `.claude-plugin/marketplace.json` has a `version` key
  (card C7 (a)); `test_manifest_key_outside_the_allowlist_fails` in
  `tests/test_core_checks.py` covers both.
- `consumer.version` in `vendor/engineering-workflow-core.lock.json` names
  the commit SHA as the version.
- The README (zh and EN) says what an install follows and that a tag is a
  reviewed snapshot.
- FU-069 has the check after the release: in Cowork, Check for updates, then
  record the loaded commit.

## Notes

- Official docs (read 2026-11-14): without `version`, a relative-path plugin
  in a Git-hosted marketplace has the version "The commit SHA of the
  installed directory" (`https://code.claude.com/docs/en/plugins/loading.md`).
  The Cowork plugin guide (`https://claude.com/docs/cowork/guide/plugins.md`)
  names "Check for updates" and "Sync automatically" and does not say how
  Cowork compares versions.
- Before Issue #114, both manifests set `0.1.0`; the known installs held
  `0.1.0` at commit `e37a990` (Issue #114 plan, Facts).
- Consequence (inference): updates replace the installed copy more often,
  so a user who edits their copy of `skills/dev-core/model-config.json` can
  lose the edit more often (`docs/design-proposal.md`, D-029, "Residual
  risks and limits", item 9, says that an update can replace an edited
  configuration file).
- The `dev-retro` "released" definition (REQ-026) depends on this
  requirement (Issue #114 card C2 (a)).

Related: [[REQ-001]], [[REQ-018]], [[REQ-026]]
