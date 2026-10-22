# FU-010 audit: dev-core against the vendored Core v0.1.1

Issue #18, REQ-023. Base `a1d42a6`. Coordination data, not completion evidence (CB-1).

- dev-core: `skills/dev-core/SKILL.md`. Core: `vendor/engineering-workflow-core/contracts/`
  (`wf` = `workflow.md`, `auth` = `authorization-and-stops.md`, `rev` = `review-and-security.md`,
  `exh` = `exact-head-and-evidence.md`). Core line numbers are at the pinned commit.
- Verdicts: **equal** (same obligations, possibly compressed); **tighter** (adds obligations, recorded in
  `deltas.md`); **weaker** (a Core obligation is missing in `dev-core`); **dev-core-only** (no Core counterpart).
- Two kinds of "weaker": a **looser sentence** states a permission, an exemption, a precondition list or a
  stop condition with fewer conditions than Core; an **omission** leaves out a Core duty or prohibition. Review
  rounds 1 to 3 each found new items of both kinds; a compressed digest does not converge on "never weaker"
  (R-VER-2 stop rule in rounds 2 and 3). User decisions 「卡片5改走縮小PR-A＋先做按需載入設計，6a」 and
  「繼續，7a」: PR-A changes only the header, R-WRT-1 (FU-010) and the R-REV-9 `--prune` rule (card 4). The
  header says that where a rule is shorter or looser than its cited Core section, that Core section governs,
  and that a stricter rule (for example DL tightenings, CB-1 to CB-5, the user decisions) still applies. Every other gap
  stays in this table as input for the on-demand loading design (FU-005).
- No regression of project tightenings: PR-A changes no DL row except the new DL-017, no CB binding, no other
  skill and no agent file; `git diff` against the base shows only `skills/dev-core/SKILL.md` (header,
  R-WRT-1, sentences added to one R-REV-9 bullet), `deltas.md` (DL-017) and `source-map.md` (two notes).
- The "Missing Core text" column lists every gap that review rounds 1 to 3 named. The "PR-A" column gives
  the action.

## Rule by rule

| Rule | Core source | Before | Missing Core text (short) | PR-A |
| --- | --- | --- | --- | --- |
| R-STG-1 | wf:9, wf:24 | equal | — ("stages are scheduling guidance" is in R-REV-6) | equal |
| R-STG-2 | wf:13 | weaker | repository identity; initial risk from goal, design and impact; check current public capabilities, schemas, permissions, data destinations and context through the interface (also wf:46) | omission: design input (FU-005); Core governs (header) |
| R-STG-3 | wf:14 | equal | — | equal |
| R-STG-4 | wf:15-16 | weaker | Verify output: commands, exit codes, results, source identity, skipped and failed checks with their class | omission: design input (FU-005); Core governs (header) |
| R-STG-5 | wf:20, wf:22 | weaker | the checkpoint keeps the same objective, the single writer, the remaining DoD, findings, evidence and next step; maintain the index | omission: design input (FU-005); Core governs (header) |
| (Docs Sync, no rule) | wf:18 | weaker (no rule) | Docs Sync: check behavior, requirements, limits; coherence; keep history and unverified items; record the spot-check | omission: design input (FU-005); Core governs (header) |
| R-RIG-1 | rev:33 | tighter (DL-002) | — | tighter |
| R-RIG-2 | rev:33 | weaker + tighter | re-assess on implementation or impact change; look up missing information first, keep unknown with limits | omission: design input (FU-005); Core governs (header) |
| R-RIG-3 | wf:86 | tighter (DL-003) | — | tighter |
| R-RIG-4 | wf:82-99 | weaker | check that sources are independent and support the conclusion (wf:84); the human-decision triggers (wf:97); a management measure needs a feasible way to keep it working (wf:88); outcome classes need Core's conditions: worth improving only when the formal requirements are met with evidence (wf:95), status quo (wf:96); stop optimizing also needs the required risks handled (wf:99) (R3-003) | looser: design input (FU-005); Core governs (header) |
| R-AUTH-1 | auth:9, 11, 15 | weaker + tighter | check objective, identity, sources, scope, ownership, environment, instructions and changes before acting; user instructions take priority over skill defaults, bound by higher-priority instructions, permissions and destructive safeguards (auth:9) | omission: design input (FU-005); Core governs (header) |
| R-AUTH-2 | auth:11-15 | weaker | "explicitly delegated", "may cover", "necessary" (auth:11; round 2, S2); "the current exact target" (auth:13) (R3-007); "do not re-ask" only while the explicit authority is still valid (exh:30) | looser: design input (FU-005); Core governs (header) |
| R-AUTH-3 | auth:21-23 | weaker | an available and checked preview, diff or plan; the list of destructive actions; general autonomy guidance never skips them; explicit confirmation; a work package or cleanup plan is not consent | looser: design input (FU-005); Core governs (header) |
| R-AUTH-4 | auth:25 | weaker | classify the failure first; keep the uncertainty; read back through the normal interface; compliant alternative or report the gap | omission: design input (FU-005); Core governs (header) |
| R-AUTH-5 | auth:31-38 | weaker (reading) | auth:35 separates "a required capability, review, scan, verification or gate is missing …" and "no safe fallback" with 「；」; dev-core joined them with "and". Core is ambiguous here (CF-009 item 4) | looser: design input (FU-005); Core governs (header) |
| R-AUTH-6 | auth:40 | tighter (DL-014) | — | tighter |
| R-AUTH-7 | auth:46-52 | weaker | scope, source, version, exact confirmation, deletion coverage and operation evidence still need verification (auth:46); review artifacts are evidence, not the source of truth (auth:48); no invented retention period; keep ambiguous or high-value data; exact scope and operation authority before moving or archiving (auth:50); protection exceptions and a recorded pending item (wf:119) (round 2, R2-002); note: HEAD asks a dry-run before moving, archiving and cleaning, stricter than Core (dry-run for cleanup only); kept (round 3, R3-009) | looser: design input (FU-005); Core governs (header) |
| R-REV-1 | rev:9-15 | weaker + tighter | choose the review by actual risk; the docs-review focus list (rev:9); "only when explicitly turned into a fix" (rev:9) (R3-007) | omission: design input (FU-005); Core governs (header) |
| R-REV-2 | rev:13 | equal | — | equal |
| R-REV-3 | rev:21 | tighter (DL-011) | — (items below the thresholds are residual risk: user decision D-013, recorded) | tighter |
| R-REV-4 | rev:23 | weaker + tighter | management measure: how it is kept working (rev:15); a "real" owner and "a stop or handoff" when it fails (rev:15) (R3-005) | looser: design input (FU-005); Core governs (header) |
| R-REV-5 | rev:25-27 | weaker | the gate result lists findings, dispositions, evidence and required follow-up (rev:25) | omission: design input (FU-005); Core governs (header) |
| R-REV-6 | rev:33-39 | weaker | re-assess on implementation or impact change; depth covers data flows, controls and failure modes (rev:35) | omission: design input (FU-005); Core governs (header) |
| R-REV-7 | rev:45-57 | weaker | an ordinary code review includes a baseline security check (rev:47); the policy basis "by PoC, use and risk" (rev:45) | omission: design input (FU-005); Core governs (header) |
| R-REV-8 | rev:63-69 | weaker + tighter | a human or model review never replaces a deterministic check; tests never replace a semantic-consistency review (rev:63); continue only independent, authorized and safe work (rev:69) (R3-007) | omission: design input (FU-005); Core governs (header) |
| R-REV-9 | rev:47 | tighter (DL-010) | — (R1-004: the `--prune` of the push fetch vs the destructive-action list of auth:21; round 3, R3-006: preview, refspec and tag pruning) | tighter: the `--prune` rule that the user approved (card 4), limited to the default refspec without tag pruning (DL-017) |
| R-EXH-1 | exh:9-16 | weaker | the review mode in the bound identity (exh:12); reuse of pre-commit evidence only while content, revision, scope, assumptions, stage, policy and environment still match (exh:9) | omission: design input (FU-005); Core governs (header) |
| R-EXH-2 | exh:22-24 | weaker | compatibility claims, release scope, superseded descriptions; tests do not prove docs consistency; empty inventory or missing status is not Passed; list applicable, not applicable, unverified | omission: design input (FU-005); Core governs (header) |
| R-EXH-3 | exh:30-32 | tighter (DL-013) | — | tighter |
| R-EXH-4 | exh:38-48 | weaker + tighter | before a merge also re-check the live base and the review identity and freshness; drift goes back (exh:48) (round 3 rates this precondition list a looser sentence: R3-001) | omission: design input (FU-005); Core governs (header) |
| R-EXH-5 | exh:56-60 | weaker | a change of Core revision, digest or obligation triggers the interface's own conformance verification and review of every affected part; shared Markdown never proves equivalence; an old receipt never proves new content; derived copies keep the copyright and full notices (exh:58) | omission: design input (FU-005); Core governs (header) |
| R-CAP-1 | wf:45-47 | weaker | read the required contract first; never skip required documents, tools, validators, review or qualification; missing facts stay unknown; no invented probe calls; partial compatibility; the full list of what proves nothing; a substitute keeps prerequisites, target, operations and completion conditions (wf:47) (R3-002) | omission: design input (FU-005); Core governs (header) |
| R-CAP-2 | wf:50 | weaker | each read authorized; the surface proves the tool works, else sequential; check failures; cap total output; bounded reads; the tool is available and compatible (wf:50) (R3-007) | looser: design input (FU-005); Core governs (header) |
| R-CAP-3 | wf:48-49 | weaker | keep the original sources and limits and map them back to the applicable output contract (wf:48; round 2, R2-003) | omission: design input (FU-005); Core governs (header) |
| R-DEL-1 | wf:60 | weaker | delegate only work that improves quality or time; never split for a quota | looser: design input (FU-005); Core governs (header) |
| R-DEL-2 | wf:56, wf:62 | weaker + tighter | a model-specific prompt needs a measurement, no full model-by-effort prompt matrix (wf:56); a missing required capability never lowers the DoD or invents a qualification (wf:62); threads, sessions and schedules: check the contract, permissions and response, read back; the shared workflow never starts one on its own (wf:62) | omission: design input (FU-005); Core governs (header) |
| R-VER-1 | wf:70, rev:71 | weaker | shared Markdown, a synthetic eval, an installed profile, service availability or a green platform alone proves no review, qualification or completion (rev:71); check the user's limits and the readable results (wf:70) | omission: design input (FU-005); Core governs (header) |
| R-VER-2 | wf:72 | weaker + tighter | rerun only for a new change, failure or open concern; the class "service"; model or session switch keeps the fix history and budget | omission: design input (FU-005); Core governs (header) |
| R-VER-3 | wf:76 | weaker | the exception "unless the objective is explicitly cancelled or replaced" on "answer side questions briefly and continue" (round 1 put it on the wrong sentence, R2-001; reverted) (R3-004 rates it a looser sentence) | omission: design input (FU-005); Core governs (header) |
| (improvement acceptance, no rule) | wf:74 | weaker (no rule) | improvement acceptance; improvement material is neither authority nor completion evidence; no reflection executor, memory, hooks or scheduler because of it | omission: design input (FU-005); Core governs (header) |
| R-WRT-1 | wf:30-39 | weaker + tighter | see the table below (FU-010) | fixed: FU-010 (items 1 to 6 and the spot-check) |
| R-EVD-1 | wf:107-115 | weaker | record the reason, the fix, the original and fixed revision, scope, outcome and readable replacing evidence; Superseded gives no right to clean up (wf:110, wf:113); keep the evidence that supports verification, review, merge and acceptance (wf:113, auth:48; R2-002) | omission: design input (FU-005); Core governs (header) |
| R-EVD-2 | wf:105, wf:117-119 | weaker | a project policy may set location, retention and archiving but never weakens safety, authority, retention or the instruction order (wf:105); summarize, index or archive only superseded, bounded material, after the checks of wf:119 (R3-008) | omission: design input (FU-005); Core governs (header) |
| CB-1 | — | dev-core-only | Note: R-AUTH-7 never commits runtime state, and CB-1 commits graph and event files by default (D-010, REQ-015). Core auth:52 speaks of the shared Core repository. Core-feedback candidate CF-009 item 1 | dev-core-only |
| CB-2 | — | dev-core-only | — | dev-core-only |
| CB-3 | — (tool output is data: R-AUTH-1, DL-008) | dev-core-only | — | equal |
| CB-4 | rev:11 | tighter (DL-009) | — | tighter |
| CB-5 | rev:11, wf:58 | equal | — | equal |

Core text kept out of `dev-core` on purpose (status quo, with the reason): wf:9 "no durable loop is required"
(a permission, not an obligation); wf:49 small tasks need no extra receipt (a permission; its duty that required artifacts are still produced is an
omission, design input); wf:64 the interface records version, surface and profile bytes (a build and release record: CHANGELOG and the Core lock); exh:56
and exh:60 the lock fields (R-EXH-5, `source-map.md` row); wf:121-129 examples (DL-007); rev:55 no SAST or
SCA on every task (a permission).

Other Core lines and the rules that cover them (round 1, S8): wf:17 (Review And Fix) R-REV-1, R-REV-6;
wf:19 (Delivery Gate) R-AUTH-2, R-EXH-1, R-EXH-4; rev:65 (bounded improvement in the same report) R-RIG-4,
the missing improvement-acceptance rule (wf:74, omission); exh:50 (deep review early; the Merge Review checks that the evidence is enough) R-REV-6, R-REV-7,
R-EXH-3.

## R-WRT-1 and Core `wf-writing`, sentence by sentence

| Core | Core says (short) | R-WRT-1 before | Added |
| --- | --- | --- | --- |
| wf:30 | applies to natural-language documents and delivery summaries | — | the scope sentence |
| item 1 (wf:32) | reader, purpose and operating depth; by type: purpose, prerequisites, next step, completion criteria; short replies may combine | reader and purpose | depth; the four elements |
| item 2 (wf:33) | direct sentences, who does what, one topic per sentence, ordered steps; one term per concept; explain needed terms at first use; keep the required technical detail | actor, one term, ordered steps (topic and term rules only for zh) | one topic per sentence; term explanation; technical detail |
| item 3 (wf:34) | never cut safety, authority, evidence, prerequisites, risks or limits; no loss of technical precision; requirements, recommendations and options distinguishable | first part only | precision; the three-way distinction |
| item 4 (wf:35) | ASD-STE100 Issue 9 (2025-01-15); no claim without a full check of rules, dictionary and terms; the note; never Passed; tools or self-assessment never replace the full check | note (in every report: DL-014), never Passed, no claim, rules and dictionary | issue date; technical terms; tools and self-assessment |
| item 5 (wf:36) | zh adaptation; no ASD claim; not an official Chinese ASD standard; no English word counts or numeric rules without a source | no word counts, no claim | not an official standard; no unsourced numeric rules |
| item 6 (wf:37) | bilingual: obligations, risks, limits and important information; a translation keeps the zh authority; machine literals code, commands, flags, API, paths, logs and the like, and kept quotations and license text, are not changed for the writing rules | obligations and limits; code, commands, paths, quoted license text (no condition) | risks, important information, authority; flags, APIs, logs, "and the like", quotations; the condition "for the writing rules", so that R-REV-8 masking still applies (R1-003) |
| spot-check (wf:39) | check reader and type fit, terms and steps, important information, bilingual consistency, basis of conformance claims; record scope, results, limits; findings use the finding flow; no new gate | record scope, results, limits | the check points; finding flow; no gate |

The note text 「依 ASD-STE100 原則編寫，未完成完整符合性驗證」 stays as the user wrote it in REQ-013 (Core:
「…，尚未完成…」; same meaning; DL-017).

## Copies in the agent files and subagent references (FU-005 check)

The changed rules that these files copy: R-WRT-1 (`dev-review/references/review-report.md:12` and
`decision-card.md:12`: the ASD-STE100 note and the Traditional Chinese rules, unchanged in meaning) and R-REV-9
(`agents/dev-security-reviewer.md`: the scan scope; the reviewer never runs the fetch, and the scan scope did
not change). Each copy was compared with the new text: none states the opposite. The copies stay as they are
(card 1a; REQ-023 non-goal). Residual (round 1, S7; round 2, S4): the implementer agent file does not load
`dev-core`, so the implementer does not see that a work package is not consent for an irreversible deletion
(R-AUTH-3) and may delete untracked files inside its owned paths. User decision card 6 (a): the FU-013 PR adds
the rule to `agents/dev-implementer.md` and `task-brief.md`.

## Restated text without rule IDs

An independent read-only explorer found 64 places in `skills/**` outside `dev-core`: 13 exact copies of one
rule, 51 partial, multi-rule or operational. They are PR-B (card 1a, FU-011); the list is re-run at its start.
