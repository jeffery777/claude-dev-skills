# Issue #73 review round 1

Target: uncommitted candidate on `f7b2ea8` (diff SHA-256 prefix `1487a64f`;
HEAD and `git status --porcelain` equal at start and end of both reviews).

- Deep review R1: `dev-reviewer`, requested `opus`/`xhigh`; recorded
  `opus` (`claude-opus-5-5`)/`xhigh`; effective `unknown`. BLOCKED.
- Security Diff Scan S1: `dev-security-reviewer`, requested `opus`/`xhigh`;
  recorded `opus` (`claude-opus-5-5`)/`xhigh`; effective `unknown`. BLOCKED.
- `bash scripts/validate.sh`: passed (main agent and R1).

## Findings and proposed dispositions

| ID | Severity | Relation | Location | Summary | Class / proposed disposition |
| --- | --- | --- | --- | --- | --- |
| R1-001 = S1-005 | SHOULD-FIX (S1: NIT) | in-scope | `skills/dev-deliver/SKILL.md:81`, `:112-113` | The text-scan row and the Gate line lack "that runs on its own" and "text scanned with a push scan keeps the push scan settings" | necessary fix |
| S1-001 | MUST-FIX | in-scope | `skills/dev-core/SKILL.md:153` and copies | "Locally installed scanner" does not exclude a scanner that sends content or found values to a service, verifies them online or checks for updates | necessary fix: local-only processing, no network; otherwise counts as not installed |
| S1-002 | MUST-FIX | in-scope | `skills/dev-core/SKILL.md:153`, `:157`; `agents/dev-security-reviewer.md`; `review-report.md:9` | No deterministic binding between the scanned file, the text the reviewer reads and the posted text; a title passed as an argument is never in the file | necessary fix (details depend on card I73-R1-C1) |
| S1-003 | SHOULD-FIX | in-scope | `skills/dev-core/SKILL.md:153` | "Clean pass" has no deterministic definition (pipe hides the exit code; config, allowlist, ignore files) | worth improving: fix |
| S1-006 | NIT | in-scope | `skills/dev-deliver/SKILL.md:55-65` | The floor check covers only implementation; with the new default, a floor-level explore node can run in a session below the floor | worth improving: check before any node under the floor that this session runs |
| R1-002 | REQ-GAP | gap | `skills/dev-core/SKILL.md:184,186`; `skills/dev-review/SKILL.md:29-44` | Whether a C4 trigger keeps `opus`/`high` for the rest of the node | Needs Human Decision: card I73-R1-C2 |
| R1-003 | REQ-GAP | gap | `review-report.md:9-10`; `skills/dev-gate/SKILL.md:28,120` | The C3 precondition evidence is only in the brief, not in a kept record | Needs Human Decision: card I73-R1-C1 |
| S1-004 | REQ-GAP | gap | `skills/dev-core/SKILL.md:153,156`; DL-005; D-022 | A secret scanner covers keys and tokens, not private paths, hostnames, private emails or real names | Needs Human Decision: card I73-R1-C1 |

Residual risk noted by the reviewers (not findings): the reviewer and the
main agent judge C4 triggers; the module term is not defined; no explicit
ban on reusing a `sonnet` text-scan result as commit, push or merge-readiness
evidence; scanner false positives; draft file lifetime outside the repo;
the plan was written by a main session below the floor (R-DEL-2 covers
implementation only; unrelated).

Cards: shared notes folder, `issue73-cards.md` (outside the repository).
Fix round 1 waits for the answers (R-REV-3: no REQ-GAP fix in this round).

## Fix round 1, part A (safe work before the cards, decision-card rule)

- `dev-implementer` T1-F1, requested `opus`/`high`; recorded `opus`
  (`claude-opus-5-5`)/`high`; effective `unknown`. Fixed R1-001 (= S1-005)
  and S1-006 in `skills/dev-deliver/SKILL.md`, `skills/dev-core/SKILL.md`
  (R-DEL-2), DL-038, design proposal (zh and en), REQ-009 and CHANGELOG.
- Main agent: the same sentence in `docs/requirements/log.md` (REQ-009 row of
  Issue #73), one record line (the main session is below the floor; a record
  sync, not a rule change).
- Not reviewed yet. `bash scripts/validate.sh`: passed. Diff SHA-256 prefix
  `7f4a5768`.
- Open: REQ-009 Notes "Limit" (card C8, before Issue #73) still says the
  floor check runs "before it implements"; decide in fix round 1 part B.
- Waiting: cards I73-R1-C1 and I73-R1-C2.
