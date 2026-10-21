# Provider profile and platform read-back (REQ-021)

A project selects a provider profile only with `platform_profile` in
`.dev/config.json` (Core: a profile is an opt-in project overlay). Without it,
`platform_enforcement` is `NOT_CONFIGURED`, unless the no-profile read of
`dev-gate` step 6 fails or shows another base or head (then `UNVERIFIED`). This file defines the format and
the GitHub read-back of the merge gate (`dev-gate` step 6). The checker
`${CLAUDE_SKILL_DIR}/scripts/platform_profile.py` implements exactly these
rules and nothing more. A new edge case goes to the user as a `REQ-GAP`
decision card; it is never added to the checker directly (REQ-021).

## Format

```json
{
  "platform_profile": {
    "provider": "github",
    "repository": "owner/name",
    "base_branch": "main",
    "required_checks": [
      {"name": "validate", "app_id": 15368}
    ]
  }
}
```

- `provider`: only `github`.
- `repository`: the GitHub repository, `owner/name`.
- `base_branch`: the branch that PRs merge into.
- `required_checks`: at least one check. `name` is the check-run name (unique
  in the list). `app_id` is the GitHub App that must create the check run, a
  positive integer. GitHub Actions is app 15368.
- Allowed top-level keys in `.dev/config.json`: `requirements_dir`,
  `commit_state`, `platform_profile`. The profile has exactly the four keys
  above, all required.
- A selected profile is a required profile: `UNVERIFIED` or `BLOCKED` blocks
  formal merge readiness (Core exact-dimensions).

## Where the setting is read

Only from the bound base commit, never from the PR head or the working tree:

1. `git cat-file -e <base>^{commit}`: the base commit is missing → `UNVERIFIED`.
2. `git ls-tree <base> -- .dev/config.json`: no file → no profile.
3. `git cat-file blob <base>:.dev/config.json` → parse.

Git runs with `LC_ALL=C` from the repository's top level
(`git rev-parse --show-toplevel`), so the path never depends on the current
directory; no result depends on a message text.

## Fail closed

Each case gives a visible message that names the problem:

- `BLOCKED`: invalid JSON (including bytes that are not UTF-8), a duplicate key, an unknown key (at either level), a
  missing key, a wrong type (`true` or `1.5` is not an app id), a duplicate
  check name, an empty `required_checks`, a provider other than `github`, or a
  `repository` that is not the bound repository.
- `UNVERIFIED`: the base commit or the file cannot be read.

## Read-back (GitHub)

Inputs: the bound repository `R` (`owner/name`), the PR number, and the bound
base and head SHAs (40 hex). The branch name is percent-encoded in API paths.
Every call is `gh api --hostname github.com repos/R/...`, so no default remote,
default repository or `GH_HOST` changes the target. All calls are reads.

1. `repos/R/pulls/<n>`: the base repository must be `R` and the base branch
   `base_branch`, else `BLOCKED`. The base SHA must be the bound base and the
   head SHA the reviewed head, else `UNVERIFIED`.
2. Platform required checks: every `required_status_checks` rule of
   `repos/R/rules/branches/<base_branch>` (rulesets, all pages) and
   `repos/R/branches/<base_branch>` `protection.required_status_checks`
   (classic: `checks[]` and `contexts`). A failed or unreadable read is
   `UNVERIFIED`, never "no rule".
3. Required set = profile checks ∪ platform checks.
   - A profile check that the platform does not require → `BLOCKED`: the
     platform does not enforce the profile.
   - The platform pin (`integration_id`, classic `app_id`) differs from the
     profile `app_id` → `BLOCKED`.
   - A platform-only check without a pin (missing, `null` or `-1`) →
     `UNVERIFIED`: add it to the profile to pin its source.
4. `repos/R/commits/<head>/check-runs?filter=all` (all pages). For each
   required (name, app id), keep the runs with that name, that app id and
   `head_sha` = head. Group them by check suite and take the newest run of
   each suite.
   - No run → `UNVERIFIED`. A newest run not `completed` → `UNVERIFIED`.
   - A newest run with a conclusion other than `success` (`failure`,
     `cancelled`, `timed_out`, `skipped`, `neutral`, `stale`,
     `action_required`) → `BLOCKED`. "Passed" means only `success`.
   - Commit statuses never satisfy a check.
5. Read the PR head again; a different head → `UNVERIFIED`.
6. Result: `BLOCKED` if any item is `BLOCKED`, else `UNVERIFIED` if any item
   is `UNVERIFIED`, else `VERIFIED`. The report lists every item with its
   reason.
7. If the checker fails or prints no `platform_enforcement:` line, the gate
   result is `UNVERIFIED`, never `NOT_CONFIGURED` (user decision Q6 (a)).

Without a profile, `dev-gate` step 6 reads the PR's base, head and checks in
one call (`gh pr view --repo github.com/<owner/name>`, user decision Q8 (a)); a base that is not the bound base is `UNVERIFIED`, because a stale
base may lack a profile that the PR's real base has (user decision Q5 (a)).

The read-back is valid only for that head. Run it again right before a merge,
and pin the merge to the head (`gh pr merge --match-head-commit <head>`).

## Which checker runs

Run the installed pack's copy. When that copy lies inside the repository under
review (for example in the pack's own repository), the PR could change the
checker that judges it: run the copy from the bound base instead
(`git cat-file blob <base>:<path>` into a temporary file outside the
repository, run with `python3 -I`). The checker reports `UNVERIFIED` when it runs from inside the
repository. When the copy is missing at the bound base: if
`.dev/config.json` is absent at the bound base (`git cat-file -e <base>^{commit}`
succeeds and `git ls-tree --full-tree <base> -- .dev/config.json` prints
nothing), use the no-profile path of step 6; otherwise the result is
`UNVERIFIED`.

## A PR that changes the policy or its own checks

- Policy change (R-AUTH-2): `.dev/config.json` differs between the bound base
  and the head (added, removed, any byte changed, or unreadable at the head).
  The gate gives the user a decision card, and the gate result is
  `NEEDS HUMAN DECISION` until the user answers. The answer binds to the head
  blob SHA of `.dev/config.json`; another blob needs a new answer. The
  platform result still uses the base profile.
- FU-008 (report only; no rule blocks such a PR): GitHub runs `pull_request`
  workflows from the PR's own merge commit, so a green check certifies only
  the PR's own check definitions. With a profile, `VERIFIED` is always
  reported as `VERIFIED (checks ran this PR's own definitions)`. The gate also
  lists the files changed in `base...head` (`git diff --name-only --no-renames`)
  under `.github/`, `.dev/config.json`, `scripts/`, `tests/`,
  `.gitleaks.toml`, `.gitleaksignore`, `.gitattributes` and, when it lies in
  the repository, the pack directory. A failed diff is `UNVERIFIED`. The list
  is a hint for the Merge Review, never complete: any file a check reads can
  weaken it.

## What this does not protect

- A PR that weakens its own checks still gets green checks (FU-008, report
  only).
- App 15368 means "any GitHub Actions workflow in R", not one job. A PR or
  another workflow can create a check run with the same name and app.
- Admin or bypass merges; bypass actors are visible only to admins.
- With `strict` off, the checks may have run against an older base.
- Other ruleset rules (PR required, merge method, approvals, deletion) are not
  read.
- The truth of the GitHub API answers; providers other than GitHub.
- Anyone who can write to the base branch controls the profile.
- The reviewers' read-only Bash use is not technical isolation.
- A failed run in an old check suite keeps the result `BLOCKED` until that
  suite runs again; a PR into another branch than `base_branch` is `BLOCKED`.
