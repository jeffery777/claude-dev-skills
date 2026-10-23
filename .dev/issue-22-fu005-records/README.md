# FU-005 design record (Issue #22, REQ-025)

Coordination data, not completion evidence (CB-1). Written per ASD-STE100
principles; full conformance not verified.

- `fu005-spec.md`: the approved FU-005 design spec (Traditional Chinese).
  The user approved it: 「核准 FU-005 規格」.
- `fu005-checklist.md`: its no-regression checklist (tables A to F). The PR-4
  review uses table D.

Both files are the approved final text, copied word for word from the design
session's notes on 2026-10-22. The user chose this location for the design
record (decision card PR1-006: 「PR1-006 選 a」). Masking was the only change:

- `fu005-spec.md`, one place (section 2.3): a local checkout path became
  `<main checkout>/skills/...`. SHA-256 of this masked copy:
  `03db9aff115fe8ea0a69e6b2b111dba0c1f61907674cc20d7992ee79146c8f23`. The hash of the unmasked original is kept only outside the
  repository, because it would let a reader guess the masked value.
- `fu005-checklist.md`: no change; the same bytes as the original. SHA-256:
  `fcd93faa1c682558b10de8fc940e8fb81ccc622f3c49c4e3f874894575580d72`.

The spec names companion files (`fu005-cards.md`, `fu005-review.md`,
`fu005-stop-rule.md`) that stay outside the repository. The card decisions
are quoted in REQ-025 and recorded in D-020 (`docs/design-proposal.md`).

## Differences in FU-005 PR-4 (Issue #35)

The spec and the checklist above stay as approved. PR-4 differs from them
as follows:

- Spec 1.1 (C) and (D), checklist table D: R-STG-4, R-AUTH-4 and R-VER-1
  stay word for word and are not index lines. Each has a sentence that is
  literally stricter than Core (user decision card PR4-C1 (a): 「同意你的建議，C1a C2a」;
  `skills/dev-core/deltas.md` DL-031 to DL-033). So 33 items stay word for
  word and 13 rules become index lines.
- "Stricter" means the protective direction: a sentence whose broader
  prohibition makes the agent do less (for example R-AUTH-2 "Do not re-ask",
  R-RIG-4 "stop optimizing") is looser, not stricter (card PR4-C2 (a)).
- Spec 1.3, the notes on DL-007 and DL-009: they are in a list below the
  `deltas.md` table, because the spec keeps the columns of these rows
  unchanged. The list also has a note on DL-028.

Known stale cross-references in the checklist (not changed):

- Table C, item C-1 cites spec section 8 item 5; the dry-run candidate is
  item 4. Item C-7 cites item 6; the `workflow.md:115` candidate is item 5.
- Table A, row DL-010: "FU-014 may change the `--prune` sentence of
  R-REV-9". FU-014 is done (Issue #24, PR #25): the push scan uses
  `git ls-remote` and runs no `git fetch`, so R-REV-9 has no `--prune`
  sentence.
- Table D cites `task-brief.md:18`; since PR-3 that line is 19.
