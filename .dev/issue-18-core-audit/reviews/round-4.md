# Review round 4 (narrow confirmation), Issue #18

- Target: working tree against HEAD `a1d42a6`, `git diff HEAD --binary` sha256 `bf4fcd85…` (after user decision
  card 7a). Reviewer: `dev-skills:dev-reviewer` (opus, high), read-only; it created no file. CB-4 before and
  after: HEAD and status hash `9a2fc022…` and diff hash unchanged.
- Commands (reviewer): `PYTHONDONTWRITEBYTECODE=1 bash scripts/validate.sh` exit 0 (131 tests); `man git-fetch`;
  Core contracts read for the CF-009 line numbers.
- Confirmed: the header cannot be read as voiding a project tightening; R-WRT-1 misstates nothing in Core items
  1 to 6 and the spot-check and keeps the DL-014 tightenings; the `--prune` sentence matches git behaviour; no
  project tightening regresses (only the three `dev-core` files change; the R-WRT-1 literal rule now applies
  "for the writing rules", a conflict fix with R-REV-8 masking, not a regression); every finding of rounds 1 to
  3 has one final disposition; CF-009 points 1 to 6 have correct Core lines.

## Findings

| ID | Relation | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- | --- |
| R4-001 | in-scope | SHOULD-FIX | CF-009 point 7 has no Core file and line (REQ-023 acceptance) | necessary fix | Fixed: "no single Core line; related `exact-head-and-evidence.md:58`" in both languages |

Residual risks named by the reviewer, fixed in the same edit (wording only): the header's list of stricter rules
now says "for example", so a stricter rule without a DL row (R-AUTH-7 dry-run) is kept, and FU-005's checklist
names such rules; the `--prune` sentence says that it is the policy that Core `auth-destructive` checks against,
that it has no separate preview, and that there is no recovery path (commits that only the removed refs
reached can be lost to garbage collection); `source-map.md` and `audit.md` wording; CF-009 point 6 zh now says
「預設」 refspec. Not changed (residual): `dev-implement` step 4 cites R-REV-9 without restating the refspec limit
(no other skill changes in PR-A); FU-004's trigger wording is older than card 5.

Writing spot-check (reviewer): terms consistent; CF-009 point 6 bilingual gap (fixed); the R-REV-9 bullet holds
several topics (residual). Limits: no full ASD-STE100 check. Written per ASD-STE100 principles; full conformance
not verified.
