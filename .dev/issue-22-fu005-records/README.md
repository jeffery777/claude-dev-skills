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
