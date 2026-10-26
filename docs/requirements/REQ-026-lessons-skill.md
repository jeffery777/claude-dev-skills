---
id: REQ-026
title: Lessons - the user-invoked `dev-retro` skill and a Lesson candidates section in reports (D-019)
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-22 (PR #2 Merge Review 5 orchestrator session), user message at 01:52 UTC, user requirements U1 and U2 on lessons (the relevant part of the message; 「龻得」 is in the original (sic; 變得))"
    quote: '另外，我很在意你的建議"另一個值得記下的心得"，這讓我有個想法，是不是能變成一個主動的技能，日後發現問題時，可以主動學起來，自我改進。並且，隨著往後模型龻得更聰明、能力更強，新模型會自動Review這些記下來的規則或者技能，並建議適度的修改？'
  - type: chat
    locator: "Claude Code session 2026-10-22 (PR #2 Merge Review 5 orchestrator session), user message at 01:59 UTC, user requirement U3 on lessons (the full message)"
    quote: '同意，但唯一有問題的是"教訓要存在 repo 裡"這句話，以目前這repo為例，教訓只寫在這repo裡。但有些問題可能其它專案也會發生，只寫在repo裡就只有該專案本身才知道，例如︰a專案執行git操作出錯了，把教訓寫在a專案的repo，但只有a專案本身不會再犯同樣的錯。而後續新加的b專案可能會再犯相同的錯。所以也要有個機制來識別教訓的層級。'
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the D-019 design session), user answer to the D-019 design cards D19-C1 to D19-C7 (C7 (a): decide the direction now and move the fixes of design review round 2 and the security design review into the spec phase; C1 (a): a user-invoked `dev-retro` that writes no file, with `capture` and `review`, plus a Lesson candidates section in reports; C2 (a): no store for L4 lessons, one suggested line with its source that the user may add to the user's own instructions; C3 (a): answer to REQ-GAP D1-013, review the lessons that have new evidence and the rules that they point to, invoked by the user; C4 (a): no lessons file, only the existing records; C5 (a): when the level is unclear, capture asks the user in a card and the draft stays in the report until the user decides; C6: only the order, the R-REV-9 backlog PR first; C6 (c) not taken)"
    quote: "C7 選 a；C1a C2a C3a C4a C5a；C6 先做 R-REV-9 backlog PR"
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the D-019 spec session), user instruction to start the D-019 spec phase"
    quote: "繼續"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the D-019 spec session), user answer to the D-019 spec cards D19-S1 (the R-VER-2 stop rule after spec review rounds 1 and 2; option a: one round of fixes that only narrow, restore or add missing words, then one narrow confirmation), D19-A2 (option a: PR-4 writes the deferred lessons as FU rows and records the judgments of cases (b) to (e) and the first review report, masked and abstracted, in the PR description), D19-A3 (option a: `dev-retro` supports only Claude Code, and README and SKILL.md say so) and D19-A4 (option a: an L4 line names only the source category and the date; the full source stays in the report of the source project)"
    quote: "D19-S1 選 a，A2 選 a，A3 選 a，A4 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the D-019 spec session), user answer to the D-019 spec card D19-S2 (the R-VER-2 stop rule after spec review rounds 2 and 3; option a) with two conditions: (1) fix the outdated text of spec section 0 and section 10 item 3 before card D19-A1, then adopt spec v4 with no further confirmation round; (2) the PR-1 deep review and security review check the spec v4 additions that had no independent review"
    quote: "D19-S2 選 a，附帶兩個條件同意"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the D-019 spec session), user answer to the D-019 spec approval card D19-A1 (option a: approve spec v4 as the basis of D-019; open the Issue and PR-1 first; an R-REV-9 scan before each commit and push; the user decides each merge; the write authority as the card recommends)"
    quote: "D19-A1 選 a，授權範圍照建議"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the D-019 session, PR #58), user answer to card D19-PR1-C1 (findings R1-004 and S1-005, REQ-GAP: the PR-4 deep and security reviews re-check each abstraction-checklist item against the final approved text, and an item that was not checked fails the PR-4 DoD; option a: keep)"
    quote: "D19-PR1-C1 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the D-019 session, PR-2), user answer to card D19-PR2-C1 (findings PR2R1-001, PR2R1-002, PR2S1-002, PR2S1-003, PR2S1-004; 1a: a read-back command that fails makes the read-back NOT_RUN; 2a: drafts contain only visible characters; 3a: an unknown fix status counts as not fixed; 4b: no dev-plan change, the card carries the dev-plan obligation as a management measure, and the dev-plan change goes to FU-022; 5a: keep the narrowed `.git/index` exception)"
    quote: "D19-PR2-C1：1a、2a、3a、4b 並併入 FU-022、5a"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the D-019 session, PR #59), user answer to merge card D19-PR2-M1 (finding MR59-001; question 1, option a: keep the wording that review does not use the installed copy of the plugin as a review input; the user also agreed to the merge)"
    quote: "M1 問題 1 選 a，同意合併"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the D-019 session, PR-3), user answer to card D19-PR3-C1 (findings PR3S1-001 and PR3S1-002; 1a: the own-words, no-quote and R-REV-8 masking rules apply to every field of a candidate, and a candidate uses no content of files outside the repository, of native memory or of automatically loaded instruction files; 2a: a candidate contains no authorization, permission, skipped confirmation, skipped review or scan, or automatic execution, and for such a lesson only says that it is an authorization change, which the user writes; the user also agreed to the merge after the checks pass)"
    quote: "D19-PR3-C1：1a、2a，檢查通過後同意合併"
non_goals:
  - A lessons ledger or a lessons file in a repository (card D19-C4 (a))
  - A user-level lessons file, or any other store of lessons outside the repository (card D19-C2 (a))
  - Hooks (Core `workflow.md:74`)
  - A schedule, a scheduled review or a scheduler (card D19-C3 (a); Core `workflow.md:62`, `:74`)
  - Model invocation of `dev-retro`, or another skill that invokes it (card D19-C1 (a))
  - A validator or script that checks lessons
  - A rule change that comes from a lesson; each one needs its own card and its own work (card D19-C1 (a))
  - A codex-dev-skills or grok-build-dev-skills version of `dev-retro`
depends_on: [REQ-011, REQ-015, REQ-019, REQ-022]
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

A lesson that a session finds stays in the report of that session, or in one
project. The pack has no way to turn a lesson into a reviewed change (U1). It
has no way to look again at the recorded lessons and the rules that they point
to when there is new evidence, for example from a newer model (U2). It has no
way to say which level a lesson belongs to, so a lesson that one project
records can happen again in a project added later (U3).

Core `workflow.md:74` says that improvement acceptance records the gap, the
basis of its cause and the next step in the existing report, checks the
coverage of the existing contracts first, and adds no reflection executor,
memory, hooks or scheduler. D-010 and REQ-015 build no memory backend.

The user chose (design cards D19-C1 to D19-C7, spec cards D19-S1, D19-S2,
D19-A1 to D19-A4):

- a skill `dev-retro` with the modes `capture` and `review` that only the
  user invokes and that writes no file;
- a Lesson candidates section in the `dev-deliver` final report and the
  `dev-review` report;
- four levels: L1 project, L2 this pack, L3 Core, L4 the user's own
  instructions;
- one path from a lesson to a rule: a card, the user's answer, a separate
  instruction, dev-plan, review, R-REV-9 and a PR that the user merges.

The work is four sequential PRs (decision D-019). Each PR starts after the
previous one merges; the user decides each merge.

## Acceptance

Each item names its source: U1 to U3 (the user requirements) or a card.

- All PRs (`strict`, card D19-A1 (a)):
  - Each PR has an independent deep review, an R-REV-7 security review, an
    R-REV-9 scan before every commit, push and post, and an exact-head gate.
  - Each PR also owns its records: `CHANGELOG.md`, this file,
    `docs/requirements/log.md` and `.dev/<objective-id>/`.
- PR-1 (records, Issue #57; card D19-A1 (a)):
  - This file records the sources U1 to U3 with their original locators,
    the design card answer, the instruction that started the spec phase,
    the spec card answers, finding ID D1-013 and card IDs D19-C1 to D19-C7
    (R-REV-3), the non-goals and the Notes below.
  - `docs/design-proposal.md` records D-019 in zh and EN with the same
    obligations (REQ-005): the origin, new scope outside Phase 1 (as D-017
    did), the decision, the four PRs and "Core feedback: no" with its
    reason. Section 4 has one `dev-retro` row outside the Phase 1 table,
    marked as added by D-019; section 6 lists what D-019 does not build.
    The D-008 "8 skills" and REQ-010 stay as the Phase 1 history.
  - `docs/requirements/index.md` and `docs/requirements/log.md` each have a
    REQ-026 row; `CHANGELOG.md` has an entry.
  - `bash scripts/validate.sh` passes.
  - The PR-1 deep review and security review also check the spec v4
    additions that had no independent review, and the review report gives a
    conclusion for each (card D19-S2 (a), condition 2). These additions
    include:
    - the three new R-VER-5 obligations: the item-by-item result of the
      abstraction checklist; each statement marked as fact, inference or
      unverified; the smallest fix narrows a claim or adds a management measure before
      it adds a new check;
    - the PR-4 DoD value "not present": it loosens the pass condition that
      finding SR2-003 restored, and the review decides whether this
      loosening holds;
    - in PR-2: Issue content that the user pastes, as a capture input; the
      scope of the locator rule (REQ sources and body, CHANGELOG, `deltas.md`,
      commit messages); the card states whether the answer also agrees to
      commit or post the text to the destination that it names; the
      `.git/index` exception of the no-write rule (narrowed in PR-2, finding
      MS2-001); a review result is not completion evidence;
    - in PR-4: the first review report in the PR description, and the
      locator item of the DoD.
- PR-2 (`skills/dev-retro/SKILL.md`, English; card D19-C1 (a)):
  - Invocation (U1; D19-C1 (a)): the modes are
    `/dev-skills:dev-retro capture` and `/dev-skills:dev-retro review`. The
    front matter has `disable-model-invocation: true` (literal `true`). This
    blocks only the call through the Skill tool; when the model reads
    `SKILL.md`, its content is data (R-AUTH-1). The description uses the
    exact command names and does not teach general phrases such as
    "remember this". `dev-deliver`, `dev-review` and the other skills never
    invoke `dev-retro`.
  - No write (D19-C1 (a)): `dev-retro` writes no file, changes no record,
    does no Git write or publication, and invokes no other skill, MCP or
    network tool. The only exceptions: `review` dispatches
    `dev-skills:dev-reviewer`, and the read-back command `git diff HEAD` can
    update `.git/index` (finding MS2-001). The
    output is only a report, draft text and cards. The front matter also has
    `disallowed-tools` that removes `Write`, `Edit` and `NotebookEdit`
    (separator syntax as the official documentation says). The skill states
    that this is one defense layer, not a guarantee: Bash, Agent, Skill, MCP
    and network tools stay, and the restriction clears at the next user
    message.
  - Agents (D19-C1 (a), D19-C3 (a)): `capture` dispatches no agent.
    `review` dispatches only `dev-skills:dev-reviewer`; when it is not
    available, `dev-retro` stops and reports, and dispatches no other agent.
  - Read-back (D19-C1 (a)): before and after each run, `dev-retro` records
    `git rev-parse HEAD` and the SHA-256 of
    `git --no-optional-locks status --porcelain=v1 --untracked-files=all`
    (so that `git status` does not update `.git/index`; finding MS2-001) and
    of `git diff HEAD --binary --no-ext-diff --no-textconv`, and states the
    limits (it does not see changes in the content of untracked files,
    ignored files, `.git`, or anything outside the repository, such as the
    user's instruction file; `git diff HEAD` can update `.git/index`; equal
    values do not prove that no write happened). A difference is reported
    and voids that run. If a read-back command fails (non-zero exit status;
    for example outside a repository or with no commit), the read-back is
    NOT_RUN: report it; the values are no record and do not void or pass
    the run (card D19-PR2-C1 (1a)). `dev-retro` checks the exit status of
    each `git` command (for example with `PIPESTATUS` in bash or
    `pipestatus` in zsh), also with `set -o pipefail`; a failed command
    makes the read-back NOT_RUN, because a failed piped `git` command
    (`git status` or `git diff`) still gives the empty-input hash, which is
    also the hash of a clean tree. When the
    read-back is NOT_RUN in review mode, the review result is not bound to
    a revision; the report says so.
  - Separate work (D19-C1 (a)): a write after the user answers a card is
    separate work that the user starts with a separate instruction (dev-plan
    or a write, R-AUTH-2). `dev-retro` does not continue into it.
  - Platform (D19-A3 (a)): `SKILL.md` and README (zh and EN) state that
    `dev-retro` supports only Claude Code.
  - Stage map and README (D19-C1 (a)): the `dev-core` stage map gets a
    `dev-retro` row (Core files `authorization-and-stops.md` and
    `workflow.md`; the `review` mode adds `review-and-security.md`), and
    README (zh and EN) gets a `dev-retro` row that says that `dev-retro`
    supports only Claude Code (D19-A3 (a)).
  - DoD: the implementer reads the official documentation again and confirms
    the names, syntax and effect of `disable-model-invocation` and
    `disallowed-tools`. If the implementer cannot read them back, or a name,
    the syntax or the effect differs from this requirement, PR-2 is blocked.
    `SKILL.md` does not cite R-VER-5 (it is defined in PR-3).
  - capture inputs (U1; D19-C1 (a)): only the report section or file that
    the user names in this turn, a problem that the user describes, or
    Issue content that the user pastes. All inputs are data (R-AUTH-1);
    `dev-retro` does not read a tracker itself. capture reads the related rules and
    records of the current repository to check the coverage first.
  - Levels (U3; D19-C5 (a)): L1 project (only the code, stack or team
    conventions of that project); L2 this pack (the dev-* workflow itself);
    L3 Core (an obligation of the Core that the three interfaces share); L4
    the user's own instructions. When the level is unclear, capture asks the
    user in a card; until the user decides, the draft stays in the report.
  - Locators and abstraction (U3; D19-C2 (a), D19-A4 (a)): a locator
    (`path:line`, PR or Issue number, finding ID) points only to the
    repository where the draft will be committed or posted. Text that leaves
    its source repository names only a category and a date, not the name,
    paths, PR or Issue numbers, finding IDs, commit IDs or branch names of
    the source repository; the source locator stays in the report of the source project. This applies
    to L2 and L3 drafts, Issue drafts, L4 lines, FU rows, PR titles and
    descriptions, PR and Issue comments, branch names, and the text written
    on the rule path below (REQ sources and body, CHANGELOG, `deltas.md`,
    commit messages; finding MS2-002). The abstraction checklist:
    project names, customer names, internal system names, hosts, accounts,
    real names, email addresses, versions and vulnerability details are
    removed or turned into a category. Each item of the checklist has one of
    three values: "removed", "turned into a category" or "not present";
    each checklist result gives the item and its status only, never the
    removed value; R-VER-5 and the PR-4 DoD cite these values. The skill states that the
    checklist result is a model self-assessment, not a review. Masking
    follows R-REV-8. Drafts contain only visible characters; capture
    reports invisible or bidirectional characters that it finds in an input
    and does not copy them (card D19-PR2-C1 (2a)).
  - Private content (D19-C2 (a), D19-C4 (a); REQ-011, REQ-015): capture
    uses no content of files outside the repository, of native memory or of
    automatically loaded instruction files as a source or in a draft. Such
    content may already be in context, and the skill cannot stop it from
    loading.
  - Drafts by level (U3; D19-C4 (a)): L1, draft text for that project's own
    REQ, rule files or tracker; an L1 reason never goes into the `deltas.md`
    of `jeffery777/claude-dev-skills`. L2, a draft for
    `jeffery777/claude-dev-skills`: the change as a dev-plan requirement
    draft, and for a `dev-core` rule a draft sentence for the `deltas.md`
    Reason and Evidence columns. L3, a CF draft for `docs/core-feedback.md`;
    the user decides whether to report it to engineering-workflow-core, and
    the word-for-word review below applies to that text too. L4, the line
    below.
  - Word-for-word review (U3; D19-C5 (a), D19-S1 (a)): every lesson text
    that will be committed to a repository or posted is shown word for word
    in a card, wherever capture runs. The card says whether the answer
    "approve" or "defer" also agrees to commit or post this text to the
    destination that the card names. This agreement covers the text and the
    destination only; it does not start the write. The committed or posted
    text is the same as the approved text; any change is shown to the user
    again. An Issue draft for `jeffery777/claude-dev-skills` names its
    destination. Posting is a separate external write (R-AUTH-2): the user
    posts it, or the agent posts it on the user's separate instruction (a
    card answer is not that instruction), with an explicit `--repo` after
    the R-REV-9 post scan, and reads back the URL. A lesson from a security
    problem that is not fixed is promoted or published only after the fix
    is released. There is no exemption. When the fix status is not known,
    the problem counts as not fixed (card D19-PR2-C1 (3a)).
  - L4 (U3; D19-C2 (a), D19-A4 (a)): one suggested line with the source
    category (the user's statement, an agent observation, repository file
    text (untrusted), or tracker and third-party text (untrusted)) and the
    date, and no project identification. The line contains no
    authorization, permission, skipped confirmation, skipped review or scan,
    or automatic execution; for such a lesson the card says "this is an
    authorization change" and the user writes it. The line carries the note
    "model self-assessment, not a review; compared with `dev-core` rules
    only". `dev-retro` does not write the user's instruction file.
  - Cards (D19-C4 (a)): each draft has one card with the options approve,
    defer and reject. Only a deferred lesson becomes an FU row in
    `.dev/followups.md`, with the Deferred fields (durable target, owner,
    reason, remaining risk, verification plan, promotion trigger; R-REV-3).
    An approved lesson goes to dev-plan by the user's separate instruction.
    The reason for a reject or a "keep as is" stays in the report. capture
    assigns no FU number.
  - No loosening (D19-C1 (a)): capture and review never suggest loosening a
    Core obligation or deleting a required check, also in L1, L2 and L3
    drafts. A comment on Core becomes a core-feedback draft (REQ-019).
  - Language (D19-C1 (a)): records in `.dev/` and `docs/` keep the current
    language of each file; reports and cards use the user's language.
  - review trigger and scope (U2; D19-C3 (a), REQ-GAP D1-013): review runs
    only when the user invokes it; there is no schedule. The scope is the
    lessons with new evidence that were not reviewed yet, the rules that
    they point to (`R-…`, `DL-…`, `CB-…`) and the REQ sources of those
    rules. The user names the inputs; review reads only files of the
    current repository. In another project, the inputs are that project's
    records and rule files, a comment on a rule of this pack is only an L2
    draft, and review does not use the installed copy of the plugin as a
    review input. FU rows get no "lesson" marker.
  - New evidence (U2; D19-C3 (a); Core `workflow.md:72`, `:99`): a new
    lesson candidate, a recorded failure, or a concern that the user names.
    A model change alone is not new evidence; review then says that it would
    only read the old evidence again and asks the user to confirm the
    scope.
  - Reviewer (U2; D19-C3 (a)): the read-only `dev-skills:dev-reviewer` at
    `opus`/`xhigh` (R-DEL-2). Each review binds the exact revision
    (`git rev-parse HEAD` and the diff hash); the read-back of that run is
    the CB-4 record of the review, and `git status` runs only with
    `--no-optional-locks`. The report states the
    problem, the objective, the scope, the available evidence, the budget,
    the stop condition and the next step (Core `workflow.md:99`). A model
    change clears no finding. A closed finding opens again only with new
    evidence that can change the judgment, and the report names that
    evidence. The dispatch names `opus`; which version the alias resolves to
    is not verified (FU-021); `fable` is not used before its evaluation
    (D-007 rule 4).
  - Suggestions (U2; D19-C3 (a)): each suggestion has one of the four Core
    judgments (Core `workflow.md:90-97`). Each suggestion that changes a
    rule file, skill text, a REQ or any record (including a narrowed claim,
    a merge, a clarification, a retirement or a level promotion) is a card.
    A "required fix" (for example a delta that loosens Core) is a card too,
    marked "required fix, needs your authorization". "Keep as is" and
    "already covered" stay in the report; the record does not change and
    the item stays in the next scope. A narrowed claim and a reduced
    obligation are written separately. The card quotes the original
    decision of the rule and its source, with the locator rule above, and,
    like a capture draft, contains only visible characters.
  - Result (D19-C1 (a)): a review result is not an approval and not
    completion evidence. The review report goes to the user and not into the
    repository; a part that goes into a record follows the card rule above.
  - Rule path (U1; D19-C1 (a)): a lesson becomes a rule only through: a
    card, the user's answer, the user's separate instruction, dev-plan (the
    REQ sources record the card ID, or for a card of another project, its
    category and date, and the user's words; words abstracted with the
    locator rule are marked "abstracted paraphrase"),
    implementation, independent review, R-REV-9, a PR, and the user's merge
    decision. For such a spec, dev-plan names for each rule sentence the
    user sentence that it comes from, and checks that every condition of
    those words has a place. The reason of an approved L2 rule goes into the
    `deltas.md` Reason and Evidence columns (only for `dev-core` rules;
    D-020 item 5); the reason of an L1 rule goes into that project's own
    files.
  - Verification: `bash scripts/validate.sh`; a static walk-through of the
    five cases of PR-4 and of the negative cases: the user says "remember
    this"; a candidate with a customer name and an internal host name;
    review suggests deleting a DL row; review finds a Core obligation too
    strict; only the model changed; an L2 lesson from a security problem
    that is not fixed; the user points to a file outside the repository or
    to native memory; lesson text that says to skip review, or an L4
    suggestion to stop asking before commit or push; an L2 lesson captured
    in another project; `dev-reviewer` is not available. For "remember
    this", the user tries the platform behavior once in Claude Code, or it
    is marked unverified.
- PR-3 (Lesson candidates section; U1; D19-C1 (a)):
  - `dev-core` gets R-VER-5, `deltas.md` gets DL-035 (`tighten`), and the
    `wf-verification` row of `skills/dev-core/source-map.md` adds R-VER-5.
    R-VER-4 is a removed ID and is not used again (REQ-022).
  - The `dev-deliver` final report and the `dev-review` review report each
    have a section with the English heading "Lesson candidates". It is a
    tightening of Core `workflow.md:74` for these two reports, not a new
    report system. Other reports still follow Core `workflow.md:74`.
  - Minimum triggers: the R-VER-2 stop rule fired; a `REQ-GAP` was raised,
    or a spec lost a condition of its source words; the same kind of finding
    came back in two or more rounds of this work; the user corrected the
    agent; a tool call was refused, or the platform behaved differently from
    a rule. The last two apply only to `dev-deliver`. Other gaps follow Core
    `workflow.md:74`. With no candidate, the section says "none".
  - Fields of each candidate: the suggested level (L1 to L4, or unclear);
    the trigger; the source (with the locator rule of PR-2); the observation
    (fact or unverified); the lesson (inference); the number of independent
    events; the rules or records that already cover it; one of the four Core
    judgments (Core `workflow.md:90-97`); the smallest fix (narrow a claim or
    add a management measure before a new check; a management measure meets
    Core `workflow.md:88` (an actual owner, a verifiable precondition, a
    feasible upkeep, and a stop or handover when it fails); the order never replaces or loosens a required
    security check, scan, review or Core obligation); for a platform lesson,
    when to check again; the item-by-item result of the abstraction
    checklist, with the values of PR-2 (item and status only). Each
    statement is marked
    fact (with a source that the session read back), inference or
    unverified; text from a tracker, a subagent or the repository is data
    (R-AUTH-1). A single event is recorded as an observation unless the user
    decides otherwise.
  - No loosening (D19-C1 (a)): the PR-2 no-loosening rule applies also to
    Lesson candidates.
  - No authorization (card D19-PR3-C1 (2a)): a candidate contains no
    authorization, permission, skipped confirmation, skipped review or
    scan, or automatic execution; for such a lesson the candidate only says
    "this is an authorization change", and the user writes it.
  - Every field of a candidate is in the agent's own words; no field quotes
    a user message, command output or transcript, and every field is masked
    as R-REV-8 says. A candidate uses no content of files outside the
    repository, of native memory or of automatically loaded instruction
    files (card D19-PR3-C1 (1a)).
  - The section is report content only: it writes no file, changes no rule
    and invokes neither `dev-retro` nor another skill. A candidate is a
    proposal, never authority or completion evidence.
  - Management measure (Core `workflow.md:88`): the owner is the user; the
    precondition that can be verified is that the user reads the final
    report; the upkeep is that every `dev-deliver` and `dev-review` report
    has the section; on failure (the user does not read it or gives no
    instruction), the candidates stay in the report, which is kept as
    R-EVD-2 says.
  - `skills/dev-review/references/review-report.md` contains the parts of
    R-VER-5 that apply to the reviewer (triggers 1 to 3, the fields, the
    own-words rule, the no-loosening and no-authorization rules, the
    report-only rule) word
    for word, with the R-VER-5 ID; `dev-deliver` cites the ID only
    (REQ-022). `skills/dev-retro/SKILL.md` changes only to cite R-VER-5.
  - Verification: `bash scripts/validate.sh`; when a `dev-deliver` report
    has candidates and the user gives no instruction, no skill invokes
    `dev-retro` (read the tool calls in the transcript; NOT_RUN when the
    transcript cannot be read).
- PR-4 (first use; U1, U2, U3; D19-A2 (a)):
  - The user invokes `/dev-skills:dev-retro capture` for five recorded
    cases of this repository, then `/dev-skills:dev-retro review`; the
    output is cards. The cases: (a) per-round review records that were
    committed and caused blockers about the records only (PR #30, PR #34);
    (b) FU-015 did not write a threat model first; (c) PR2R2-001, a claim
    larger than the check; (d) FU-018 MF-001, a spec that lost the
    "cross-module" condition; (e) the behavior of the `effort` parameter of
    the Agent tool.
  - From the user's answers: deferred lessons become FU rows in
    `.dev/followups.md`. The judgments of cases (b) to (e) and the first
    review report, masked and abstracted, go into the PR description, which
    the user reads word for word before it is posted, after the R-REV-9 post
    scan. Apart from its records, PR-4 owns only `.dev/followups.md`.
  - DoD (D19-A2 (a); the re-check by the PR-4 reviews and the DoD failure
    of an item that was not checked: card D19-PR1-C1 (a)): each public
    text is the same as the text that the user approved;
    each locator points only to the target repository; each item of the
    abstraction checklist has one of the values of PR-2, recorded item by
    item (model self-assessment, not a review); the results are bound to the
    exact public text; an item that was not checked is a DoD failure; the
    PR-4 deep and security reviews re-check each item against the final
    approved text; the before-and-after records of PR-2 (read-back) exist.

## Notes

- Not covered (residual risk): when the user uses `dev-implement`,
  `dev-gate` or `dev-plan` directly, the report has no Lesson candidates
  section.
- Platform limits (PR-2 DoD; read back on 2026-10-26 from the Claude Code
  documentation, https://code.claude.com/docs/en/skills.md, by the main
  agent): `disable-model-invocation: true`: "Description not in context,
  full skill loads when invoked"; "If Claude tries anyway, Claude Code
  blocks the call". `disallowed-tools`: "Tools removed from Claude's
  available pool while this skill is active."; "Accepts a space- or
  comma-separated string, or a YAML list. The restriction clears when you
  send your next message." The fields apply to "Claude Code skills at any
  level, including plugin skills"; claude.ai uploads and the Skills API
  accept only `name`, `description`, `license`, `compatibility`, `metadata`
  and `allowed-tools`. Whether Cowork supports them is not known (the FU-001
  Cowork test is not done). Where a platform does not support them,
  "invoked only by the user" rests on the skill text only. Card D19-A3 (a)
  narrows the claim to Claude Code.
- Exception to REQ-005: the REQ-005 source says that the skills are mainly
  invoked by the agent as needed, and that people can also invoke them.
  `dev-retro` is invoked only by the user; this is the user's own choice
  (card D19-C1 (a)). README and the design document stay bilingual.
- Relation to REQ-001 and section 3 of the design document
  (`docs/design-proposal.md:32`, Cowork): `dev-retro` is a Claude Code-only
  exception chosen by the user (card D19-A3 (a)); the other skills keep the
  Cowork goal.
- Card D19-PR1-C1 (a): the PR-1 reviews (R1-004, S1-005) conclude that
  the PR-4 DoD value "not present" holds, with a measure, and card
  D19-PR1-C1 (a) keeps the measure. The card covers only two clauses of
  the PR-4 DoD: the PR-4 deep and security reviews re-check each item
  against the final approved text, and an item that was not checked is a
  DoD failure. The re-check by the PR-4 reviews is an extra control for
  PR-4 text only. The rest is not part of the card: the rule that a result
  gives the item and its status only, never the removed value (security
  review fixes, findings S1-002 and S2-001), and the three checklist
  values (spec v4 and the round-1 fixes), defined once in PR-2 and cited by R-VER-5 and the PR-4 DoD; the
  PR-4 DoD also binds the results to the exact public text.
- Card D19-PR2-C1 (4b) (finding PR2R1-001): `dev-plan` does not change in
  D-019. The `dev-plan` obligation of the rule path (for each rule sentence
  the user sentence that it comes from, and a place for every condition of
  those words) reaches `dev-plan` through the card, as `SKILL.md` says.
  This is a management measure: the owner is the user, who answers the
  card and starts `dev-plan`; the verifiable premise is that the card text
  states the obligation; when it fails (`dev-plan` runs without it, for
  example in a new session), the `dev-plan` review checks each rule
  sentence against the user's words, and a missing trace is a finding. The
  `dev-plan` change itself goes to a later follow-up (FU-022, to be filed
  by the orchestrator after D-019); until FU-022 changes `dev-plan`, the
  failure path depends on the judgment of the `dev-plan` reviewer.
- Difference from the codex-dev-skills improvement contracts: Core
  (`vendor/engineering-workflow-core/docs/provenance/source-map.md:177-179`)
  lists three codex-dev-skills contracts (operational evidence, improvement
  proposal, candidate evaluation). They keep real proposals and evaluations
  private, and public Git has only synthetic fixtures. This pack publishes
  abstracted lesson text, and the first review report, after the user's
  word-for-word review. The only controls are the abstraction checklist
  (a model self-assessment) and that review. This pack keeps two of their
  principles: a proposal is never authority, and raw run data, logs,
  transcripts and host or user identity stay out of the public repository.
  These contracts are interface data contracts and do not bind this pack;
  Core `authorization-and-stops.md:52` and REQ-011 do. D-019 records this
  difference in its Core feedback reason; there is no CF item.
- R-REV-9 does not check business secrets (customer names, internal system
  names, vulnerabilities that are not fixed). For lesson text, the only
  controls are the abstraction checklist and the user's word-for-word
  review.
- Not verified:
  - whether `disallowed-tools` must also list `MultiEdit` (the names,
    syntax and effect of the invocation control fields were read back on
    2026-10-26 from the Claude Code documentation; see Platform limits);
  - the platform behavior in Cowork (card D19-A3 (a) already limits the
    claim to Claude Code; claude.ai was read back on 2026-10-26 from the
    Claude Code documentation);
  - whether the native auto-memory reacts to "remember this", or saves
    lesson text by itself after capture;
  - whether `claude plugin validate` accepts the new front matter keys
    (PR-2 verification).
- "Core feedback: no" in D-019 is an inference that the review confirms.

Related: [[REQ-001]], [[REQ-005]], [[REQ-010]], [[REQ-011]], [[REQ-015]], [[REQ-019]], [[REQ-022]], [[REQ-025]]
