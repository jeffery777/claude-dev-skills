# Implementation review round 1, Issue #104

- Target: U1 pointers in `18f6b074702e3c1a814114bf9933fb2f8a8bc511` plus the staged U2 diff; sha256 of `git diff HEAD --binary` `2dcb743a6516bf97714d5c70a6349ba48ac1acf7af5497581dd94934c7432e72`; base `6f7a817933c5f680a32d01ed0e6d6fe6eb3834c5`.
- Tree check: HEAD, status and diff hash are the same before and after both reviews.
- Deep: `dev-reviewer`, requested opus/xhigh. Security: `dev-security-reviewer`, requested opus/xhigh. Read-back of both: see the call form in `design-round-1.md`; result lines in the gate record. Effective setting: `unknown`.
- Writing: written per ASD-STE100 principles; full conformance not verified.
- Result: no `MUST-FIX` and no `SHOULD-FIX`. The deep reviewer ran the tests: 395, OK (3 skipped). The security reviewer ran the text check on 24 samples and compared `push-scan.md` with the base.

## Findings and dispositions

| ID | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- |
| IR1-D-01 | NIT | REQ-009 Acceptance still says "R-VER-2 stop rule" | necessary fix | `Fixed`: word change |
| IR1-D-02 | NIT | `readback-gate.md`: "no review or scan counts" on a host without the parameters is wider than Q2 | necessary fix | `Fixed`: "none of the three counts" |
| IR1-S-01 | NIT | The text-scan clause of the agent file is narrower than R-AUTH-7 | worth improving | `Fixed`: one clause |

Residual items that took a word change, each to keep the meaning of the base or
the disposition list: "A scan that does not count" (no "merge readiness"),
"counts and passes" restored, "`Rejected`, not handled" in R-REV-4, and the
REQ-012 source names the Scope items.

## Residual risk and not handled

- Not handled (deliberate tampering): a forged GitHub committer; a rewritten transcript.
- The text check is a hint for the order of reading: it misses Windows paths, other token forms and text after a NUL on the same line; the reviewer reads the full text.
- Only macOS awk ran here; CI runs the test with the runner's awk.
- A commit that the GitHub web editor made has the same form as a squash commit: the signature key is the platform's (inference).

## Lesson candidates

- L1, trigger: the same kind of finding in two rounds (DR-D-03 then IR1-D-02; DR-D-04 then IR1-D-01). Observation (fact): grouped search rows did not place the REQ-009 hit. Lesson (inference): a row that names places by range can drop a live Acceptance. Judgment: keep as is. Abstraction checklist: each item not present.

## Narrow confirmation (`dev-reviewer`, requested opus/xhigh)

Target: the fixes above, sha256 of `git diff HEAD --binary` `5d12ca304002feb55a0dbb48711489c85f38089f5ace36e9c7d16d11ee8a0334`. The three fixes close their findings; the marker is gone.

| ID | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- |
| NC-D-01 | NIT | The REQ-009 row of `log.md` and its source do not name the Q1 change | necessary fix | `Fixed`: the row of this same uncommitted change and the source say Q1 |
| NC-D-02 | NIT | REQ-009 is in no row of the search list | necessary fix | `Fixed`: two rows name it |

Not a finding: the confirmation saw the user's answer only in `cards-1.md`; the answer is the user's own message in this session.
