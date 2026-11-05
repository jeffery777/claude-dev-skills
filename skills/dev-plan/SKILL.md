---
name: dev-plan
description: Clarify a development request and plan it before code changes - objective, requirements, DoD, risk and rigor tier, smallest slices, and (standard/strict) a validated task graph. Use when scope, assumptions, acceptance or task order are unclear, or before multi-step delivery.
allowed-tools:
  - Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)
  - Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)
---

# dev-plan

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first, then the Core files that its stage map lists for `dev-plan`.
Read, run or copy each file that this skill names with a `${CLAUDE_SKILL_DIR}`
path only with that full absolute path, never with a path relative to the
working directory; when such a path does not resolve or cannot be read, stop
and report it (CB-6).
`dev-core` and the Core files it lists hold the rules
cited below.

For a single obvious change, skip this skill and use `dev-implement`. For
interactive planning, use plan mode; this skill adds what plan mode lacks
(requirement anchors, rigor tier, task graph).

## Workflow

When the main session does this itself for work under the R-DEL-2 floor,
the floor check of R-DEL-2 applies (`dev-core`).

1. **Discover** (R-STG-2). Read CLAUDE.md or AGENTS.md, README, the relevant
   code, `docs/requirements/` and the Git state. Separate facts, inferences and
   unknowns.
2. **Ingest requirements** (R-RIG-3). Every requested outcome maps to a
   `REQ-…` file in the target project's own `docs/requirements/`. The format
   is in `${CLAUDE_SKILL_DIR}/references/requirements-wiki.md`.
   - Location: `requirements_dir` in `.dev/config.json` if it is set,
     otherwise `docs/requirements/`. If the folder does not exist, **ask the
     user before you create it**. Then copy `index.md` and `log.md` from
     `${CLAUDE_SKILL_DIR}/templates/`.
   - If the project already has a formal requirements system (Jira,
     Confluence, a PRD), the wiki is an index only: each REQ links back with
     `type: external` and a precise locator. Confidential text never leaves
     the project.
   - For each new need, copy `${CLAUDE_SKILL_DIR}/templates/REQ-template.md` to
     `REQ-<next-number>-<slug>.md`. Add one `sources` entry per original:
     a `type`, a precise `locator` and the verbatim `quote`. Write your own
     summary only in `## Need`. Record the stated non-goals. Anything you
     inferred stays `status: proposed` until the user confirms it.
   - If an existing REQ already covers the need, add the source to that REQ
     instead of creating a duplicate.
   - For every spec or REQ from a user decision (a card answer or the
     user's own words), including a spec from a `dev-retro` card (the rule
     path in `${CLAUDE_SKILL_DIR}/../dev-retro/SKILL.md`), name for each
     rule sentence the user sentence that it comes from, and check that
     every condition of those words has a place in the spec. List a
     condition that the spec does not keep, with its reason, and show it to
     the user; never drop it silently. Put this source trace in the plan.
     The review of the spec checks the trace; a missing trace, or a
     condition dropped without a reason, is a finding. The trace does not
     limit a fix of a Core blocker (R-REV-4) or the `REQ-GAP` path
     (R-REV-3).
   - If sources contradict each other, keep both sides with their locators
     under `## Conflicts`, set `status: conflict`, and ask the user. Never
     pick a side or overwrite one.
   - If a need replaces an older one, set the old REQ to
     `status: superseded`, fill in `superseded_by` and `superseded_reason`,
     and never delete it.
   - Record the typed relations between REQs: `depends_on`, `refines`,
     `conflicts_with` and `superseded_by`, each a list of existing REQ ids.
   - A review finding of type `REQ-GAP` becomes a requirement only after
     the user decides to add it. Its `sources` then record the finding ID and
     the user's decision, quoted verbatim. Never turn a `REQ-GAP` into a
     requirement on your own (R-REV-3).
   - Update `index.md`, and append one line to `log.md` for every change.
     Never widen a requirement on your own.
   - Ingest applies to every tier. If the user declines to create the wiki,
     list the requirements inline in the plan with the same `sources`
     fields, and say that no REQ files exist.
3. **Assess risk and choose a tier** (R-RIG-1; R-RIG-2: a tier written
   before Discover is a proposal; R-REV-6). Write the
   reason. Unknown risk means `standard` or higher.
4. **Check impact** (advisory). When GitNexus has indexed the repo, run
   `gitnexus impact <symbol>` for the symbols you plan to change. Report the
   blast radius and say whether the index is stale or the tree is dirty (CB-3).
5. **Check premises and options** when R-RIG-4 triggers. Keep simple
   low-risk plans short.
6. **Slice.** Use the smallest coherent slices. Each slice has an owner, owned
   paths, DoD, verification commands and a review mode. Apply the fake-edge
   test: a dependency exists only when the later slice consumes a concrete
   output of the earlier one.
   Then choose the review units by risk and review cost (Core `workflow.md`
   `wf-assumptions-and-options`: maintenance and review cost). A review
   unit is one write node of the task graph (one task of the plan when
   there is no graph). Its slices are reviewed together, in the same review
   rounds, and delivered as one change. The slices stay the smallest
   coherent slices: the node lists the DoD, verification and requirements
   of each of its slices. Record the units in the plan.
   - In a `strict` objective, each slice is a review unit of its own. A
     high-risk slice is always a review unit of its own. Such units go one
     at a time, with the early reviews and scans that R-REV-6 requires.
     High-risk slices include every slice that R-REV-7 names and every
     slice whose risk is unknown (R-RIG-2), whatever its `risk` value.
     When a slice is re-assessed as high risk, re-plan it as a review unit
     of its own.
   - In a `light` or `standard` objective, slices that are not high risk
     by the bullet above (`low` or `medium`) and have a close review scope
     may share one review unit, also when they mix features and fixes, so
     that each small slice does not cost review rounds of its own. The unit gets the highest risk
     and the strictest review mode of its slices.
   - When you judge that joining slices adds risk, or you cannot tell
     whether slices may share a unit, ask the user with a decision card
     (R-AUTH-6) before you join them.
   - How review units map to issues, branches and change requests follows
     the project's own rules (Core `authorization-and-stops.md`
     `auth-scope`). When those rules need separate change requests, the
     slices are separate review units.

   Then plan the completeness checks (Issue #101; cards I101-C2 (a),
   I101-R2-C1 (a) and I101-IR2-C1 (a)). `dev-deliver` step 7 and
   `dev-review` step 2 say who runs them.
   - Value rule. Before a value from a plan or a brief goes into a
     completeness-check command, check it in the text, never with a
     command that contains it: the whole of a commit ID matches
     `[0-9a-f]{40}` or `[0-9a-f]{64}`; a search string is not empty and
     holds only printable characters, with no `'`, `\`, line break or
     Unicode format character; the whole of a folder matches
     `[A-Za-z0-9._][A-Za-z0-9._/-]*`, and it is the requirements folder of
     the project. A value that fails is never put into a command: report
     it, and that check did not run.
   - When the commands run. At `standard` and `strict`, the main agent runs
     the search list and co-change rule 1 before a commit, after it has
     staged the content of that commit and before the R-REV-9 commit scan.
     This rule requires no commit: when the user authorized none, the main agent runs no
     command, and the co-change rules and their reading check still
     apply. Commands run alone (no pipeline) from the top of the worktree
     (`git rev-parse --show-prefix` prints an empty line).
   - Search list (`standard` and `strict` slices that change, rename,
     move or remove a rule, a term, a value, a path or a recorded fact that
     other files state; at `light` the plan may skip it with a reason).
     The plan lists fixed strings with IDs (`K1`, …): the IDs of the
     changed rules, deltas, decisions and findings first, then each
     changed wording and each translation. Command on the index:
     `git --no-replace-objects --literal-pathspecs -c core.quotePath=false grep --cached -c -F -i -e '<string>' --`.
     Exit 0: hits; exit 1: no hit; any other exit code: the check did not
     run. A hit is one matching line. The plan records, for each string,
     one row per file with hits: the path, the count, the disposition and
     a reason in the writer's own words; no line numbers and no hit text.
     Files under the objective's own record folder (`.dev/<objective-id>/`)
     get no rows: they hold the list itself. Dispositions: `changed` (the
     change edits that place), `noted` (the old text stays true, and the
     reason says why, or a note at that place qualifies it), `historical`
     (it records an earlier decision, and a record of this change has a
     sentence that supersedes it). Limit: the search finds only the listed
     strings; a line break inside a phrase, another wording or another
     translation is found only by reading.
   - Co-change rules (`standard` and `strict`).
     1. Each write node and each fix round that changes a requirement file
        adds its own `log.md` row, in that same change, whose REQ column
        names its ID; `log.md` is append-only. The reviewer of a node checks
        this by reading the node's diff, and the reviewer of a fix round by
        reading the fix diff, which the main agent gives when it can. Reading
        shows this only on a target that holds that change alone: on a
        cumulative diff it cannot tell the rounds apart, the report says so,
        and this item does not count as passed. That is no check that did
        not run, so it does not stop the work.
        Before a commit, the main agent also runs these commands, each with
        exit 0 required (any other exit code: the check did not run):
        - `git --no-replace-objects --literal-pathspecs -c core.quotePath=false diff --cached --no-relative --no-ext-diff --no-textconv --no-renames --no-color --ignore-submodules=none --name-only -- '<requirements folder>'`
        - `git --no-replace-objects --literal-pathspecs -c core.quotePath=false diff --cached --no-relative --no-ext-diff --no-textconv --no-renames --no-color --ignore-submodules=none -U0 -- '<requirements folder>/log.md'`

        Each listed name directly in the folder that matches
        `REQ-<digits>.md` or `REQ-<digits>-<slug>.md` must have its ID in
        the REQ column (the second cell) of a line of the second output
        that starts with `+|`. A line that starts with `-|` is a finding.
        Limit: the commands see one row for the whole commit, so a second
        change of one requirement file in one commit without its own row
        is found only by reading.
     2. Each user decision that a write node records is quoted, in the
        same node, in every record of the project that lists the decisions
        of the change. The plan names those records. The reviewer checks
        this by reading, not by a command. A confidential quote follows
        `${CLAUDE_SKILL_DIR}/references/requirements-wiki.md`.
   - Results and severity. A check that did not run (a value that fails
     the value rule, a wrong working directory, an exit code other than
     the ones above) is a required verification that did not run: the
     dependent work stops (R-AUTH-5). A row whose count or
     file is wrong, a file with hits but no row, a missing co-change row
     or quote, or a `-|` log line is a finding: at least `NIT` (a false
     record), and `SHOULD-FIX` when it leaves a place that the change made
     false without a disposition (R-REV-3).
7. **Write the task graph** (standard and strict tiers; R-RIG-1). Create
   `.dev/<objective-id>/graph.json` as described in
   `${CLAUDE_SKILL_DIR}/references/graph-schema.md`, then run:

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/graph.py validate .dev/<objective-id>/graph.json
   python3 ${CLAUDE_SKILL_DIR}/scripts/graph.py ready .dev/<objective-id>/graph.json
   ```

   This step needs a shell with Python 3 (Claude Code). Without one, follow the
   manual procedure at the end of
   `${CLAUDE_SKILL_DIR}/references/graph-schema.md` and say so in the plan.
   `validate` fails when a task cites a REQ without an existing file whose
   `id` matches. Fix every error. Review `UNUSED_REQUIREMENT` and
   `INACTIVE_REQUIREMENT` warnings with the user.
8. **Stop** before editing source files unless the user asked you to continue
   into implementation (R-STG-3: a plan authorizes nothing).

## Output

- Objective and requirement IDs (with non-goals)
- Rigor tier and reason; risk and unknowns
- Source trace, when step 2 requires it
- Slices (or the graph path plus the `ready` output) and review units
- DoD and verification plan
- Review and security plan with timing
- Human gates and open decisions
