# Exact-head Merge Review 1 — PR #2 (closes #1)

- Identity:
  - repository: jeffery777/claude-dev-skills, PR #2
  - base and merge-base: `5229478aead42cc2d70b7843dd5db3548c08c562`
  - head: `9f38f06a9c58ef37c17b1038f16904cbc7c43ef8`
  - diff: sha256(`git diff 5229478 9f38f06 --binary`) = `38f8b72daf8481457c4432c5c226be49591ad27a2e8252fc7ad04d2ef7347f9b` (82 files)
- Reviewer: a fresh opus subagent that did not write the change. It ran native `/code-review` (high, every finding) over the full range and checked a clean clone of the head.
- Result:
  - `content_review: BLOCKED`, because of MR-01 (MUST-FIX) and because the new findings had no disposition yet.
  - `platform_enforcement: NOT_CONFIGURED`: no provider profile is selected, there is no CI, and main has no branch protection or rulesets.
  - Neither result authorizes a merge.
- Deterministic checks at the head: `validate.sh` and `verify_core.py --upstream` passed. The head content, apart from the gate record, is byte-identical to the content the commit gate bound (`790a1600…`).

## Findings and dispositions

The fixes below form a new head, and that head needs a new complete Merge Review.

| ID | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| MR-01 | MUST-FIX | DR-022 Deferred lacked a reason and a durable target, and the row held two dispositions | Fixed: split into DR-022a (Fixed) and DR-022b (Deferred). DR-022b has a reason, an owner and, as its durable target, `.dev/followups.md` FU-001, which holds every required field. No new Issue was opened, because Issue creation was authorized only for the Phase 1 Issue. The commit gate record stays as a point-in-time record. |
| MR-02 | SHOULD-FIX | The fingerprint failed open when run from a subdirectory | Fixed: it resolves `--show-toplevel` first and always fingerprints the whole repository; test |
| MR-03 | SHOULD-FIX | `${CLAUDE_SKILL_DIR}` paths in dev-core broke when a sibling skill loaded the file | Fixed: every dev-core path goes through `../dev-core/` or `../../vendor/`, so it resolves from any sibling; the rule is stated in dev-core. (The fingerprint path was missed at head c72c64d and fixed under MR2-01; check_pack now enforces the rule.) |
| MR-04 | SHOULD-FIX | `ready` stalled while a parked writer had a REQUIREMENT_CONFLICT | Fixed: planned or blocked writers get a `WAITING_ON_CONFLICT` warning instead of an error; `ready` leaves them out and lists them under `waiting_on_conflict`; moving forward stays a `REQUIREMENT_CONFLICT` error; tests (Superseded by MR2-02: `validate` again fails for every open writer on a conflicting REQ; only `ready` continues, and the `WAITING_ON_CONFLICT` warning was removed.) |
| MR-05 | SHOULD-FIX | Running tests made every substitute review fail the fingerprint | Fixed: tool caches (`__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `*.pyc`) are excluded, with the limit stated in the script and dev-core §8; substitutes are told to set `PYTHONDONTWRITEBYTECODE=1`; test (Narrowed by MR2-06: bare `*.pyc` files are no longer excluded; only the named cache folders are.) |
| MR-06 | SHOULD-FIX | `claude plugin validate .` checked only marketplace.json | Fixed: validate.sh also runs `claude plugin validate .claude-plugin/plugin.json` |
| MR-07 | NIT | The source map still said read-only was enforced | Fixed. The round 1 DR-018 edit had silently missed this row. |
| MR-08 | NIT | The design called the explorer "read-only" without the Bash caveat | Fixed in both languages |
| MR-09 | NIT | MISSING_REQUIREMENTS_DIR was described inaccurately, and its exit code was not stated | Fixed: description corrected; exit 1 documented for both codes |
| MR-10 | NIT | `key:` followed by an indented scalar parsed as `[]` | Fixed; test |
| MR-11 | NIT | Flow lists were cut at a `]` inside quotes | Fixed: quote-aware scan; test |
| MR-12 | NIT | `sources()` missed column-0 items and quotes on the next line | Fixed; test |
| MR-13 | NIT | A symlinked `.dev` parent folder was followed | Fixed: transition refuses a graph folder that resolves outside the project root; test |
| MR-14 | NIT | No lock without fcntl | Fixed: `LOCK_UNAVAILABLE`; POSIX-only is documented |
| MR-15 | NIT | A crash between the graph write and the event append loses the event | Rejected as a defect: an accepted trade-off of writing the graph first (CR-007). The schema doc now states it and how to check after an interrupted run. |
| MR-16 | NIT | The overlap check included finished writers; the overlap error had no node | Fixed: only unfinished writers are compared, and the error is reported on both nodes, so unrelated nodes can still move; test |
| MR-17 | NIT | The fingerprint opened FIFOs and sockets | Fixed: non-regular files are recorded by type and mode; test with a FIFO inside a nested repository |
| MR-18 | NIT | Every ignored file is hashed in full (slow in large trees) | Deferred. Target: `.dev/followups.md` FU-002. Owner: jeffery777. Reason: a faster scheme weakens detection and needs a design decision. Risk, plan and trigger: see FU-002. |
| MR-19 | NIT | One `git show` process per upstream file | Rejected: Core has 14 files; the cost is negligible and the code stays simple |
| MR-20 | NIT | Review rounds 1 to 5 were not bound to a diff hash | Fixed: the review report template now has a required "Diff identity" line. Past round records stay as point-in-time records; the content they reviewed is bound by the commit gate hash `790a1600…`, which the head content matched. (Single disposition per MR2-14.) |
| MR-21 | NIT | Two YAML-subset parsers | Rejected: `sources()` parses nested mappings, which `graph.frontmatter` does not support on purpose; one shared engine would add a YAML parser beyond the requirement (R-RIG-3). Both now share `strip_comment` and `_unquote`. |

## Verification after the fixes

- `./scripts/validate.sh`: all checks passed.
  - 73 tests, also run with `-W error::ResourceWarning`.
  - Marketplace and plugin manifests both validate.
