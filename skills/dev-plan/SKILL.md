---
name: dev-plan
description: Clarify a development request and plan it before code changes - objective, requirements, DoD, risk and rigor tier, smallest slices, and (standard/strict) a validated task graph. Use when scope, assumptions, acceptance or task order are unclear, or before multi-step delivery.
---

# dev-plan

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first. It holds the rules
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
   - For each new need, copy `templates/REQ-template.md` to
     `REQ-<next-number>-<slug>.md`. Add one `sources` entry per original:
     a `type`, a precise `locator` and the verbatim `quote`. Write your own
     summary only in `## Need`. Record the stated non-goals. Anything you
     inferred stays `status: proposed` until the user confirms it.
   - If an existing REQ already covers the need, add the source to that REQ
     instead of creating a duplicate.
   - If sources contradict each other, keep both sides with their locators
     under `## Conflicts`, set `status: conflict`, and ask the user. Never
     pick a side or overwrite one.
   - If a need replaces an older one, set the old REQ to
     `status: superseded`, fill in `superseded_by` and `superseded_reason`,
     and never delete it.
   - Record the typed relations between REQs: `depends_on`, `refines`,
     `conflicts_with` and `superseded_by`, each a list of existing REQ ids.
   - Update `index.md`, and append one line to `log.md` for every change.
     Never widen a requirement on your own.
   - Ingest applies to every tier. If the user declines to create the wiki,
     list the requirements inline in the plan with the same `sources`
     fields, and say that no REQ files exist.
3. **Assess risk and choose a tier** (R-RIG-1, R-RIG-2, R-REV-6). Write the
   reason. Unknown risk means `standard` or higher.
4. **Check impact** (advisory). When GitNexus has indexed the repo, run
   `gitnexus impact <symbol>` for the symbols you plan to change. Report the
   blast radius and say whether the index is stale or the tree is dirty.
5. **Check premises and options** when R-RIG-4 triggers. Keep simple
   low-risk plans short.
6. **Slice.** Use the smallest coherent slices. Each slice has an owner, owned
   paths, DoD, verification commands and a review mode. Apply the fake-edge
   test: a dependency exists only when the later slice consumes a concrete
   output of the earlier one.
7. **Write the task graph** (standard and strict tiers). Create
   `.dev/<objective-id>/graph.json` as described in
   `${CLAUDE_SKILL_DIR}/references/graph-schema.md`, then run:

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/graph.py validate .dev/<objective-id>/graph.json
   python3 ${CLAUDE_SKILL_DIR}/scripts/graph.py ready .dev/<objective-id>/graph.json
   ```

   This step needs a shell with Python 3 (Claude Code). Without one, follow the
   manual procedure at the end of `graph-schema.md` and say so in the plan.
   `validate` fails when a task cites a REQ without an existing file whose
   `id` matches. Fix every error. Review `UNUSED_REQUIREMENT` and
   `INACTIVE_REQUIREMENT` warnings with the user.
8. **Stop** before editing source files unless the user asked you to continue
   into implementation (R-STG-3: a plan authorizes nothing).

## Output

- Objective and requirement IDs (with non-goals)
- Rigor tier and reason; risk and unknowns
- Slices (or the graph path plus the `ready` output)
- DoD and verification plan
- Review and security plan with timing
- Human gates and open decisions
