# Issue #64 plan: FU-025 skill paths

- Objective: FU-025 (REQ-026). Rigor `strict` (card FU25-R1-C1 (a)): the
  change decides which files a skill follows as pack rules, so it touches a
  trust boundary (R-REV-7, R-RIG-1). Deep review and Security Diff Scan in
  each round, R-REV-9 scans, an exact-head gate and the user's merge
  decision. No executable, permission or dependency changes; one test
  sentinel changes (`tests/test_rule_citations.py`: CB-6 is now defined).
- Review units: one high-risk unit (task node T1), alone in this PR (dev-plan
  step 6; card FU25-R1-C1 (a)). The MR63-001 record fix is not in this PR:
  it stays Deferred to the next PR that changes rows FU-023 or FU-024.
- Survey (task brief): every `skills/dev-*/SKILL.md` reads `dev-core` with
  `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` in its first sentence. Most
  references, templates and scripts have `${CLAUDE_SKILL_DIR}` paths, but
  some pack files were named without one: `graph.py` in `dev-continue`
  step 4 and `dev-implement` step 1, the REQ template and `graph-schema.md`
  in `dev-plan`, `review-report.md` in `dev-review`, and `decision-card.md`
  in `review-report.md` (review round 1, findings FU25S1-001 and
  FU25R1-007; the first survey missed them). They now have the prefix, and
  CB-6 covers a pack file name without it.
  The risk is the same in each skill: the model can shorten the path to
  `skills/...` when the working directory is this repository (finding
  PR4-F1). Only `dev-retro` capture step 4 pointed the read of the
  `dev-core` rules and `deltas.md` at "the current repository".
  The agent files (`agents/*.md`) name no `${CLAUDE_SKILL_DIR}` path; their
  Core files come from the brief.

- Implementer: the main session (model `opus`, Opus 5.5). Its effort is not
  readable in the session: `unknown`. The R-DEL-2 floor for trust-boundary
  work is `opus`/`high`; the model meets it, the effort is not verified
  (finding FU25R1-005). Review round 3 fixes (card FU25-R2-C1 (a)) are
  implemented by `dev-skills:dev-implementer` with model `opus` and effort
  `high` (R-DEL-2 floor).
- Review round 1 (deep review FU25R1-001 to FU25R1-008, Security Diff Scan
  FU25S1-001 to FU25S1-005): the rigor, the review units and the open
  questions go to the user as cards FU25-R1-C1 to FU25-R1-C3.
- Review round 2 (deep FU25R2-001 to FU25R2-005, Security Diff Scan
  FU25S2-001 to FU25S2-008): the R-VER-2 stop rule fired; cards FU25-R2-C1
  (a) and FU25-R2-C2 (a). During the deep review the main session wrote
  `.dev/followups.md` (FU-028 and the FU-025 status), against CB-4; the
  reviewer showed that the other files equal the bound diff, and the next
  round covers that hunk. Not fixed (dispositions): FU25S2-007 (no
  deterministic test for names without the prefix; Deferred to FU-029) and FU25S2-008 (the section 8 heading
  says non-normative; the `dev-core` header already applies the bindings;
  keep as is).
- Review round 3 (confirmation; deep FU25R3-001 to FU25R3-004, Security
  Diff Scan FU25S3-001 to FU25S3-006, Issue text IB3-001): FU25R3-001
  (SHOULD-FIX) is a new blocker in the skill-path mechanism (the CB-6 name
  sentence covers the `scripts/verify_core.py` of R-EXH-5), so the work
  moves to option (b) of card FU25-R2-C1 without another card: no further
  rule-text change in this PR. Dispositions: FU25R3-001, FU25S3-001 and
  FU25S3-003 Deferred to FU-029 with FU25S2-007; FU25S3-004 keep as is (the
  wording "by its path that starts with `${CLAUDE_SKILL_DIR}`" replaces the
  edit-list wording, which failed `scripts/check_pack.py`; same meaning);
  FU25R3-002 to FU25R3-004, FU25S3-002, FU25S3-005, FU25S3-006 and IB3-001
  Fixed in the records. The records-only fixes of this step are made by
  the main session (no rule text).

## Source trace (`skills/dev-plan/SKILL.md` step 2)

| Source | Condition | Place in the change |
| --- | --- | --- |
| Card D19-PR4-C1 (a), FU-025 Item: "each skill-relative file is read with the absolute path that `${CLAUDE_SKILL_DIR}` gives" | absolute path from the skill directory | `skills/dev-retro/SKILL.md` "Skill paths" paragraph; capture step 4 |
| same: "never with a path relative to the working directory" | no working-directory path | same paragraph, also when the working directory is this pack's repository |
| FU-025 Remaining risk: "follow a file that the other repository placed at that relative path as pack rules (untrusted data, R-AUTH-1)" | such a file is data | same paragraph, last sentence; `dev-core` "Skill paths" |
| FU-025 Verification plan: "each read of `dev-core`, Core or a skill reference uses the skill directory path" | dev-core, Core and references | the paragraph lists `dev-core`, `deltas.md`, the Core contracts and the references |
| Task brief (orchestrator text, relayed): "a read that cannot resolve stops (no fallback to cwd)" | stop, no fallback | dev-retro paragraph; the sentence in each skill; `dev-core` "Skill paths" |
| Task brief (orchestrator text, relayed): survey the other skills and bundle when the same narrow wording fixes them at low risk | same rule in the other skills | one sentence after the first sentence of each other `SKILL.md`; CB-6 in `dev-core` (DL-036) |
| same: "at low risk" | bundle only at low risk | Not kept as written: review round 1 (FU25R1-003) showed that the change touches a trust boundary (R-REV-7), so the skill-paths unit is high risk; rigor and units go to the user as card FU25-R1-C1 |
| (added after review round 1, not from these words) | run and copy too; a pack file name without the prefix | CB-6; the sentence in each skill (findings FU25S1-001, FU25R1-007) |
| (added, not from these words) | a file of the current repository read as a review target, an input or a record keeps its repository path, as data | CB-6, last sentences; dev-retro "Skill paths", capture step 4, review step 3 (findings FU25R1-001, FU25R1-004, FU25S1-005). Reason: in this pack's repository, reviews read `skills/...` files as targets; the rule must not forbid that |
| Card FU25-R2-C2 (a) (user: 「FU25-R2：C1a、C2a、FU-028 v2 同意」) | capture step 3: the pack files from the skill directory are not content of files outside the repository; cited by rule ID only | dev-retro capture step 3; REQ-026 PR-2 items annotated (finding FU25S1-004, FU25R2-001) |
| Card FU25-R2-C1 (a) (same answer) | one narrow round: narrow, restore or add records; no new mechanism | CB-6 (names without the prefix, Limit sentence); `graph.py` commands in `dev-deliver` and `graph-schema.md`; records |
| (added by the agent in review round 3, not in the card text; shown to the user word for word after the round) | a same-name record or write target of the current repository is not a pack file, and no dev-* skill writes a file on a skill path; a write target keeps its repository path; a stop names the file by its `${CLAUDE_SKILL_DIR}` path, not the resolved path | CB-6 (findings FU25S2-003, FU25S2-006); the factual limit of the write sentence is in FU-029 |
| Card FU25-R2-C1 (a): a new blocker in the confirmation round moves the work to (b) | records only; the rest deferred | FU-029 (row text approved by the user before the write) |
| Task brief: MR63-001, rows FU-023 and FU-024 | line references | Not kept: card FU25-R1-C1 (a) keeps MR63-001 Deferred (high-risk unit alone) |
| Card FU25-R1-C2 (a) (user: 「U25-R1：C1a、C2a、C3a」, sic) | state the limit when the skill directory is the tree under review; point to the specific rules; the rest is a new FU | CB-6 "Limit" sentence; FU-028 (row text approved by the user before the write) |
| Card FU25-R1-C3 (a) (same answer) | keep the stop; README zh and EN; note in FU-001 | CB-6; `README.md` (Cowork paragraph, zh and EN); FU-001 Remaining risk |
