---
name: dev-plan
description: Clarify a development request and plan it before code changes - objective, requirements, DoD, risk and rigor tier, smallest slices, and (standard/strict) a validated task graph. Use when scope, assumptions, acceptance or task order are unclear, or before multi-step delivery.
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
3. **Assess risk and choose a tier** (R-RIG-1, R-RIG-2, R-REV-6). Write the
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
