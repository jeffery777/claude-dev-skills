# Model and effort read-back script (Issue #89)

This file describes a script; it is not a rule. No dev-* skill tells an
agent to run it; Issue #79 slice C decides whether and how. Until then the
manual reading of R-DEL-2 stays as it is. Issue #93 (slice C1 of
Issue #79) now tells the main agent to run it for every subagent
read-back, and the gate of R-DEL-2 covers the dispatches of work under the
floor; R-DEL-2 has the rule. The second and the third sentence of this
paragraph describe the state before Issue #93. Issue #95 (slice C2) adds
the required reviews and scans to the gate.
From Issue #96 on (PR-1), the script reads the model configuration file
`skills/dev-core/model-config.json`, classifies each recorded model ID
through it, and has a `check` mode; it gives a `WARN` line and the new
tokens `CONFIG` and `MODEL_NOT_RECOGNIZED`, and no longer gives an `OK`
line or `MODEL_NOT_ALLOWED`. Each section below that changes has a note
that starts "From Issue #96 on"; the earlier text of that section describes
the state before Issue #96, as the Issue #93 sentence above does for its
own change. From Issue #96 PR-2 on, `subagent` needs `--floor`, compares
the expected values with that floor, and prints `floor=` on its result
lines; the sections that change for PR-2 have a note that starts "From
Issue #96 PR-2 on". From Issue #96 PR-3 on, `subagent` run by its path
first checks where its copy lies (the repository check) and can give the
new tokens `IN_REPO` and `REPO_CHECK`; the sections that change for PR-3
have a note that starts "From Issue #96 PR-3 on", and the earlier text of
those sections describes the state before PR-3.

The script is `scripts/model_effort_readback.py` in this skill folder:
one file, Python 3.9 or later, standard library only, no other module of
this repository. It reads the model and effort that one subagent
transcript records and prints closed tokens only. Issue #89 is slice B of
Issue #79; REQ-009 records the scope.

## Interface

Example:

```
python3 -I ${CLAUDE_SKILL_DIR}/../dev-core/scripts/model_effort_readback.py subagent --projects-dir DIR --agent-id ID --expect-model opus --expect-effort high
```

From Issue #96 PR-3 on, the call by path that R-DEL-2 names also passes
`--floor` (from PR-2 on), and the script runs the repository check of the
Threat model section before it reads the configuration file:

```
python3 -I ${CLAUDE_SKILL_DIR}/../dev-core/scripts/model_effort_readback.py subagent --floor FLOOR --projects-dir DIR --agent-id ID --expect-model opus --expect-effort high
```

- `subagent` is the only mode. A session mode is slice D of Issue #79.
- `DIR` is an absolute path, equal to its normalized form, without a
  trailing `/` (`/` itself is refused).
- `ID` is exactly 17 lowercase hexadecimal digits.
- `--expect-model` is `haiku`, `sonnet` or `opus`; `--expect-effort` is
  `low`, `medium`, `high`, `xhigh` or `max`. Give both or neither.
- A repeated, abbreviated or unknown option, `-h`, `--help`, a missing or
  unknown subcommand and any other bad argument give `STOP BAD_ARGS`. No
  output echoes an argument.

From Issue #96 on (the bullets above describe the state before Issue #96
where they differ):

- `subagent` needs both `--expect-model` and `--expect-effort`; without
  them it gives `STOP BAD_ARGS`. The mode without expected values and its
  `OK` line are gone; the `check` mode below replaces them.
- `--expect-model` is a family of the configuration file whose tier is not
  null (in this repository `haiku`, `sonnet`, `opus` or `fable`);
  `--expect-effort` is one of `low`, `medium`, `high`, `xhigh` or `max`.
  Any other value gives `STOP BAD_ARGS`.
- `--config-base BASE`: `BASE` is a full commit ID of 40 or 64 lowercase
  hexadecimal digits, matched in full. A `subagent` run from stdin
  (`python3 -I -`) needs it; a run by path with it gives `STOP BAD_ARGS`.
  The call of the copy at the bound base is:

  ```
  git --no-replace-objects cat-file blob BASE:skills/dev-core/scripts/model_effort_readback.py | python3 -I - subagent --config-base BASE --projects-dir DIR --agent-id ID --expect-model opus --expect-effort high
  ```

  The two `BASE` literals are the same characters; R-DEL-2 says that the
  main agent checks this and what the outcome is when they differ.
- `check --projects-dir DIR --agent-id ID --candidate-config PATH` reads one
  transcript with a candidate configuration file, so that the user can
  decide on a change of the file. It runs by path or from stdin;
  `--config-base`, `--expect-model` and `--expect-effort` give
  `STOP BAD_ARGS`. It is not a read-back of R-DEL-2.

From Issue #96 PR-2 on (the bullets above describe the state before PR-2
where they differ):

- `subagent` needs `--floor FLOOR`, where `FLOOR` is exactly one of the
  values of the table below. A missing or repeated `--floor`, or any other
  value, gives `STOP BAD_ARGS`. The constant `FLOORS` of the script holds
  the table; the tests pin it, and `scripts/check_pack.py` checks that it
  equals this table:

  | `--floor` | Floor tier | Floor effort |
  | --- | --- | --- |
  | `work` | 3 | `high` |
  | `review-scan` | 3 | `xhigh` |
  | `review-routine` | 3 | `high` |
  | `review-light` | 2 | `medium` |
  | `none` | none (no floor check) | none |

  R-DEL-2 says which value each dispatch passes. The script does not check
  that the value fits the dispatch.
- `check` does not accept `--floor`: it gives `STOP BAD_ARGS`.
- The call of the copy at the bound base is then:

  ```
  git --no-replace-objects cat-file blob BASE:skills/dev-core/scripts/model_effort_readback.py | python3 -I - subagent --config-base BASE --floor FLOOR --projects-dir DIR --agent-id ID --expect-model opus --expect-effort high
  ```

  A copy of the script from before PR-2 does not accept `--floor` and
  gives `STOP BAD_ARGS`; R-DEL-2 makes that outcome `unknown`.

## Location

The script looks for `DIR/<slug>/<session>/subagents/agent-<ID>.jsonl`
with directory file descriptors only, without glob and without resolving
paths.

- `DIR`: a symlink gives `SYMLINK`, a path that is not a directory gives
  `NOT_FOUND`. The path above `DIR` resolves as usual.
- Slug and session level: only names that fully match
  `[A-Za-z0-9._-]+` (slug) or the lowercase UUID form (session) and that
  are directories, not symlinks, are entered. Every other entry (a
  symlink, a file, a directory whose name is out of format) is skipped: not
  followed, not read, no error. An entry that turns into a symlink between
  the listing and the open gives `SYMLINK`.
- `subagents`: a session without it, or where it is not a directory, is
  skipped; a symlink gives `SYMLINK`.
- The transcript file: a symlink gives `SYMLINK`; a FIFO, a socket, a
  directory or any other file that is not regular gives `NOT_REGULAR`
  before it is opened.
- A directory that cannot be listed or opened gives `PERMISSION`: then the
  script cannot show that only one file matches.
- After the whole walk: no matching file gives `NOT_FOUND`, more than one
  gives `AMBIGUOUS`. The script never picks a file by time.
- The one file is opened without following a symlink and without
  blocking, then checked again: a regular file, owned by the user who runs
  the script, one hard link, at most 64 MiB.

## Reading and parsing

- The file is read up to the size it had at open; lines added later are
  not read. Less data than that size gives `MALFORMED`, and so does a file
  that does not end in a newline (it may still be written). An empty file
  gives `NO_RECORD`.
- Lines are split at `\n` only (U+2028 and other line separators are
  content). Each line is at most 1 MiB, at most 200,000 lines.
- Each line is one JSON object in strict UTF-8, without a BOM, without a
  duplicate key (also when spelled with an escape), without `NaN` or
  `Infinity`, with numbers of at most 100 characters. Anything else,
  including an empty line and very deep nesting, gives `MALFORMED`.
- Only records whose `type` is exactly the string `assistant` count. For
  each such record, in this order:
  1. `message` must be an object and `message.model` a string
     (`MISSING_FIELD`).
  2. A record whose model is `<synthetic>` is skipped.
  3. `isSidechain` must be `true`, `agentId` must equal `ID` and
     `sessionId` must equal the session directory name
     (`BINDING_MISMATCH`). A record that fails is never filtered out,
     because filtering could raise the lowest value.
  4. `effort` must be a string (`MISSING_FIELD`); `perTurnEffort`, when
     present, must be a string (`MISSING_FIELD`) equal to `effort`
     (`INCONSISTENT`).
  5. The model must be in the allowlist (`MODEL_NOT_ALLOWED`) and the
     effort one of the levels (`EFFORT_NOT_ALLOWED`), each compared
     exactly. From Issue #96 on, the effort check of this item stays, and
     the model is classified through the configuration file as the
     paragraph after this list says; `MODEL_NOT_ALLOWED` no longer occurs.
- The script reads no other field: not `requestedModel`, `advisorModel`,
  `tools`, the `params` of an `api-request`, `version`, or any text.
- The result is the lowest model and, separately, the lowest effort over
  all records read. No record left gives `NO_RECORD`.

From Issue #96 on, the model of each record is classified through the
configuration file in these steps (item 5 above describes the state
before Issue #96 for the model):

1. A model value equal to a listed ID of a family (an exact string
   comparison) belongs to that family (class `listed`).
2. Otherwise, a value of at most 100 characters that fully matches
   `claude-([a-z]+)-[0-9]+(-[0-9]+)*` (ASCII lowercase, no case folding),
   and whose first group is a family of the file, belongs to that family
   (class `version`).
3. Otherwise, the first 200 characters, with only ASCII `A` to `Z`
   lowered, are split at `[^a-z0-9]+`. A word equal to a family name, or
   to a family name followed by digits only, of a family whose tier is
   below the expected tier or null gives the lowest such family (class
   `lower`).
4. Every other value is `unrecognized`: for example an empty or
   placeholder value, an ID of another vendor or of a provider platform,
   or an ID without a family name.

A record is below when its family has a null tier or a tier below the
expected one, when its class is `lower`, or when its effort is below the
expected effort; an `unrecognized` record stops; a `listed` record passes,
and a `version` record warns. A `STOP` that the loop gives at once (for
example `EFFORT_NOT_ALLOWED`, `MISSING_FIELD`, `BINDING_MISMATCH` or
`INCONSISTENT`) comes first. When the records belong to more than one
family class (a class is a family name, or `unrecognized`), a record that
is below gives `BELOW`, and otherwise the outcome is
`STOP MODEL_NOT_RECOGNIZED`. Otherwise, over all
records: any record below gives `BELOW`, then any record that stops gives
`STOP MODEL_NOT_RECOGNIZED`, then any record that warns gives `WARN`, and
otherwise the outcome is `PASS`. `model=` and `tier=` come from the record
with the lowest tier (`unrecognized` below a null tier below 1, 2 and so
on; on a tie, the `version` record), and `effort=` is the lowest effort.
In `check` mode there is no expected value: step 3 takes the lowest family
of any family word, and `match=` gives the weakest class of the records
(`none` below `name` below `version` below `listed`).

From Issue #96 PR-2 on, the outcome of `subagent` follows this order (the
paragraph above describes the order before PR-2; the classification of
each record does not change):

1. A `STOP` that the script gives at once: the arguments, the files, the
   parsing, the binding, the fields, the effort format and the
   configuration file.
2. The classification of each record, as above.
3. Any record below gives `BELOW`: a record is below the expected values.
4. Otherwise, when `--floor` is not `none` and the tier of the expected
   family in the configuration file that this call reads is below the
   floor tier, or the expected effort is below the floor effort, the
   outcome is `BELOW`: the dispatch asked for less than its floor.
5. Otherwise, records of more than one family class, or an `unrecognized`
   record, give `STOP MODEL_NOT_RECOGNIZED`.
6. Otherwise, a `version` record gives `WARN`.
7. Otherwise the outcome is `PASS`.

`model=`, `tier=` and `effort=` are taken as above. The floor check of
step 4 can only turn a `PASS`, a `WARN` or a `STOP MODEL_NOT_RECOGNIZED`
into `BELOW`; it never lets a lower setting count.

## Output and exit codes

A result of this script is exactly one line in the grammar below with its
exit code; any other output is not a result. `OK` is not a comparison;
`PASS` means not below the expected values, not equal to them.

| Output line | Exit code |
| --- | --- |
| `OK model=<alias> effort=<level> records=<n>` (no expected values given) | 0 — not produced from Issue #96 on |
| `PASS model=<alias> effort=<level> expected=<alias>/<level>` (neither value is below the expected one) | 0 — from Issue #96 on in the form `PASS model=<family> tier=<n> effort=<level> expected=<family>/<level> expected_tier=<n>`, for listed IDs only |
| `BELOW model=<alias> effort=<level> expected=<alias>/<level>` (a value is below the expected one) | 3 — from Issue #96 on in the form `BELOW model=<family\|unrecognized> tier=<n\|null\|none> effort=<level> expected=<family>/<level> expected_tier=<n>` |
| `STOP <REASON>` | 2 |
| `WARN model=<family> tier=<n> effort=<level> expected=<family>/<level> expected_tier=<n>` (from Issue #96 on: no value is below the expected one, and a record has an ID of the `version` class, which the configuration file does not list) | 4 |
| `CHECK model=<family\|unrecognized> match=listed\|version\|name\|none tier=<n\|null\|none> effort=<level> records=<n>` (from Issue #96 on, `check` mode only) | 5 |

stderr stays empty; any other error is `STOP INTERNAL`, a missing open
flag on the platform included. A closed or broken stdout gives no line and
exit code 2. No line carries a path, an ID or transcript text. Before
Issue #96 the orders were `haiku`, `sonnet`, `opus` and `low`, `medium`,
`high`, `xhigh`, `max`. From Issue #96 on, the model order comes from the
tiers of the configuration file that the call reads, and the effort order
stays as above (the constant `EFFORT_ORDER`). From Issue #96 PR-2 on, the
rules name no model order either: R-DEL-2 takes the tiers from its own
read of the configuration file (the configuration read of R-DEL-2).

From Issue #96 on: `model=` is a family name of the configuration file or
`unrecognized`, never the raw model value. `tier=` is the tier of that
family, `null` for a family without a tier, or `none` for `unrecognized`;
`expected_tier=` is the tier of the expected family. `check` never prints
`PASS`, `WARN` or `BELOW`, and `subagent` never prints `CHECK`. The stderr
of the `git` calls of `--config-base` is discarded, so stderr stays empty.

From Issue #96 PR-2 on, every `PASS`, `WARN` and `BELOW` line ends with
` floor=<value>`, the `--floor` value of the call, for example
`PASS model=opus tier=3 effort=xhigh expected=opus/xhigh expected_tier=3 floor=review-scan`
(the forms in the table above gain this field). A `BELOW` line has two
meanings: a record below the expected values (step 3 of the order above),
or expected values below the floor that the `floor=` value names (step 4).
When the `expected=` values of a `BELOW` line are below the floor of its
`floor=` value, the dispatch was wrong: it asked for less than its floor,
whatever the records show. R-DEL-2 says that the facts given to the user
say so.

## Tokens

| Token | Meaning |
| --- | --- |
| `BAD_ARGS` | An argument is missing, repeated, unknown or not in its format. |
| `NOT_FOUND` | `DIR` is not a directory, or no matching transcript file exists. |
| `AMBIGUOUS` | More than one session holds a matching transcript file. |
| `SYMLINK` | `DIR`, a `subagents` directory or the transcript file is a symlink, or an entry turned into one during the walk. |
| `NOT_REGULAR` | The transcript file is not a regular file. |
| `OWNER` | The transcript file belongs to another user. |
| `LINK_COUNT` | The transcript file has more than one hard link. |
| `PERMISSION` | A directory or the transcript file cannot be read. |
| `TOO_LARGE` | The file, a line or the number of lines is over its limit. |
| `MALFORMED` | A line is not one strict JSON object in UTF-8, or the file is cut short or does not end in a newline. |
| `BINDING_MISMATCH` | An assistant record does not have `isSidechain` true, or its `agentId` or `sessionId` differs. |
| `MISSING_FIELD` | `message.model` or `effort` is missing, or it or `perTurnEffort` is not a string. |
| `INCONSISTENT` | `perTurnEffort` differs from `effort`. |
| `NO_RECORD` | No assistant record that is not `<synthetic>`. |
| `MODEL_NOT_ALLOWED` | A model ID is not in the allowlist. No longer produced (Issue #96); kept so that older records stay readable. |
| `MODEL_NOT_RECOGNIZED` | From Issue #96 on: a model value is `unrecognized` and no record is below, or the records belong to more than one family class and none is below. |
| `CONFIG` | From Issue #96 on: the configuration file cannot be opened or read as the strict open requires, or it fails the validator; or a `git` call of `--config-base` fails, ends with a nonzero exit code, runs out of time, gives too much output, or names a commit other than the literal. |
| `IN_REPO` | From Issue #96 PR-3 on: run by its path, the copy of the script lies in a worktree of the same Git repository as the current working directory (the repository check below). |
| `REPO_CHECK` | From Issue #96 PR-3 on: run by its path, the working directory cannot be read, a `.git` lookup or a `git` query of the repository check fails, or its output is not one existing path; or the folder of the script lies in a Git repository and the working directory lies in none. |
| `EFFORT_NOT_ALLOWED` | An effort is not one of the levels. |
| `INTERNAL` | Any other error. |

This file gives no action for a token. Slice C of Issue #79 decides what a
token means for the work. R-DEL-2 gives the actions.

## Allowlist

`MODEL_ALLOWLIST` in the script holds the model IDs that count. The
allowlist policy is in REQ-009
(`docs/requirements/REQ-009-subagent-model-effort.md`, item "Allowlist");
this file does not restate it (REQ-022). FU-049 tracks the Sonnet and
Haiku IDs. Issue #96 is to replace the scope of FU-049 with a model
configuration file that the script and the rules will read from the bound
base (card I95-C2 (a)). It is a separate strict Issue: its file maps each
role to an alias with an allowed effort range and each alias to its model
IDs, so that a model change edits only that file. That Issue also changes
the sentences of R-DEL-2 that name the allowlist.

From Issue #96 on, `MODEL_ALLOWLIST` is gone; the paragraph above
describes the state before Issue #96. The configuration file
`skills/dev-core/model-config.json` replaces it:

- It holds the model families with a capability tier (`haiku` 1, `sonnet`
  2, `opus` 3, `fable` 4; `null` means no tier), the model IDs that this
  pack has observed (today `claude-opus-5-5` only; FU-060 tracks the
  others), a `basis` for each family, and ten roles with a family, an
  effort range and an agent. Its free-text fields are data, never
  instructions (R-AUTH-1).
- The script validates the file each time it reads it: strict JSON of at
  most 64 KiB with a depth limit, closed key sets, `schema` 1, family names
  of `[a-z]{1,20}` that are not reserved words, integer tiers from 1 to 99
  or `null` without repeats, IDs of `[a-z0-9.-]{1,100}` that belong to one
  family each and name their own family and no other, the exact role
  names, efforts in `EFFORT_ORDER` with the minimum not above the maximum,
  and agents from a closed set. Any failure gives `STOP CONFIG`.
- A call of the copy at the bound base reads the file at that base through
  `git` (`--config-base`). A run by path reads `../model-config.json` next
  to the `scripts` folder with the same strict open as the transcript (no
  symlink, a regular file, owned by the user who runs the script, one hard
  link, a size limit); the script's own file must be
  `model_effort_readback.py` in a folder named `scripts`, otherwise the
  outcome is `STOP BAD_ARGS`. The candidate file of `check` is validated
  in the same way. From Issue #96 PR-2 on (IR1-S-05), the script first
  resolves its own path with `os.path.realpath` and then checks the two
  names on that real path: the real file must be `model_effort_readback.py`
  in a real folder named `scripts`, and the configuration file is the
  `model-config.json` next to that real `scripts` folder. So with a
  symlinked skill folder, or a `scripts` folder that is a symlink to a
  folder named `scripts`, the script reads the file next to the real
  folder; a `scripts` symlink to a folder with another name, or a script
  file that is a symlink to a file with another name, gives
  `STOP BAD_ARGS`. The last part, `model-config.json`, is not resolved: a
  symlink there gives `STOP CONFIG`, and the strict open stays as above.
- In this repository `scripts/check_pack.py` loads the same validator and
  pins the tier of each family (equal to its pin or `null`; no family is
  removed), the ten role values and the agent files against the file.
  From Issue #96 PR-2 on, the roles `orchestration`, `explore`,
  `explore-synthesis`, `implement` and `implement-reduced` have the effort
  range from their row value to `max`, and the review and scan roles keep
  one value; `check_pack` still pins each role exactly, and it also checks
  that `FLOORS` of the script equals the table of the Interface section.
- Retire and restore: a family is retired by setting its tier to `null`
  with its IDs kept; its IDs then give `BELOW`, and a role that still names
  it gives `STOP CONFIG`, so the same change moves that role. A family is
  restored by setting its pin again; a tier that another family holds by
  then fails the validator, and the user decides.

The allowlist policy stays in REQ-009 (REQ-022); R-DEL-2 says how a change
of the file is made and what a read-back means for the work.

## Threat model

The script reads a file that the user can write and that holds text from
models, tools and other sources. It guards against:

- a symlink or a planted directory that points the read at another file;
- a FIFO or another special file that would block or mislead the read;
- a second matching file, and a file picked by time;
- lines of another agent or session, and appended lines with a higher
  value (the lowest value counts);
- fields that look like a model or effort but are not the recorded ones,
  such as `requestedModel`, `advisorModel` or text in a message;
- parser tricks: duplicate keys, escapes, `NaN`, long numbers, deep
  nesting, a BOM, invalid UTF-8;
- output that carries a path, an ID, an argument or transcript text into
  the reader's context.

`-I` is part of this threat model. Without it, `PYTHON*` environment
variables, the user site-packages directory and a module next to the
script or in the current directory can change the code that runs. A caller
that leaves out `-I` loses this guard.

Besides its arguments, the code of the script reads one item of process
data: its own user ID (`os.getuid`, for the `OWNER` check). It reads no
environment variable. The standard library still does: `argparse` reads
`COLUMNS`, and `gettext` reads `LANGUAGE`, `LC_*` and `LANG`; `python3`
comes from `PATH`.

From Issue #96 PR-3 on, the code of the script also reads the current
working directory (`os.getcwd`, once, in the repository check of a run by
path). It still reads no environment variable; the `git` that the
repository check starts gets the environment of the caller (card
I96-P3-C2 (a)).

The statements that the script reads no environment variable and writes
no file rest on a code review of the current code. The static test of the
script is a regression aid only: it checks the imports, the direct
`os.<name>` attributes and a list of names, and it does not cover every
way of writing a call (for example `os.path` functions, chained attributes
or `__builtins__`). FU-050 tracks a stricter check. From Issue #96 PR-2
on (IR1-S-06), the static test also requires that every
`subprocess.Popen` attribute node is the function of the one call; it
lets `os`, `sys` and `os.path` appear only as the value of an attribute,
allows only the `os.path` attributes `abspath`, `basename`, `dirname`,
`isabs`, `join`, `normpath` and `realpath`, and refuses names that start
with `_` (except `_`, `__file__` and `__name__`) and attributes that
start with `_` (except `__init__`). It is still a regression aid only.

From Issue #96 on, a `subagent` run from stdin starts `git` twice for
`--config-base`: `git --no-replace-objects rev-parse --verify --quiet
BASE^{commit}`, whose output must be exactly the literal and a newline, and
then `git --no-replace-objects cat-file blob
BASE:skills/dev-core/model-config.json`. Both calls use a list argv without
a shell, closed stdin, discarded stderr and a new process group; they share
a time limit of 20 seconds and read at most 64 KiB and one byte. A timeout
or too much output kills the process group, and a nonzero exit code or any
error gives `STOP CONFIG`, with no fallback. `git` comes from `PATH` and
gets the environment, the working directory and the Git configuration of
the caller, so it reads the same repository as the outer command and
trusts the same things; in a partial clone it can fetch the blob from the
remote (a lazy fetch). The statements of the previous paragraphs on
environment variables cover the code of the script, not `git`. The
configuration file of the call is the copy at the bound base, so a change
cannot approve its own reviews through its own file; a run by path inside
the repository of the change reads the file of the change (see below).

From Issue #96 PR-3 on, a `subagent` run by its path runs the repository
check (cards I96-IR-P2-C3 (b), I96-P3-C1 (b), I96-P3-C2 (a) and
I96-P3-R2-C2 (a)) after the checks of its arguments and of its own file
name, and before it reads the configuration file next to it. A folder lies
in a Git repository when it or a folder above it has an entry named `.git`
(`os.lstat`: a directory, a file or a symlink, dangling or not). The script
looks for this entry above both the real path of its own folder and the
real path of the current working directory; `ENOENT` and `ENOTDIR` go on to
the folder above, and any other error gives `STOP REPO_CHECK`. When the
folder of the script lies in no Git repository, the check gives nothing.
When it lies in one and the working directory lies in none, the check gives
`STOP REPO_CHECK`. Only when both lie in one does the check start `git`:
`git --no-replace-objects rev-parse --git-common-dir` once in each of the
two folders (`cwd=` is that folder), with the list argv, closed stdin,
discarded stderr, new process group and output limit of the calls above,
and one time limit of 20 seconds for the two calls. That `git` gets the
environment and `PATH` of the caller and the Git configuration that applies
in that folder: `safe.directory` comes only from protected configuration,
which is the system and global scopes, whose files the caller can choose
with `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` (or turn off with
`GIT_CONFIG_NOSYSTEM`), and the command scope: `git -c` and the caller's
`GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_<n>` and `GIT_CONFIG_VALUE_<n>`
(source: `man git-config` of `git` 2.54.0, SCOPES and ENVIRONMENT); the
command scope also takes `GIT_CONFIG_PARAMETERS`, the internal variable by
which an outer `git -c` passes its values to a child `git` (the script
itself passes no `-c`), and `HOME` and `XDG_CONFIG_HOME` choose the files of
the global scope (source: a read-only test with `git config --show-scope`
in the Security Diff Scan of implementation review round 3 of Issue #96
PR-3, `git` 2.54.0 on macOS, and the FILES section of `man git-config`);
`git` also reads the configuration of each repository. A failure, a timeout,
too much output, an output that is not one line in UTF-8 without NUL that
ends in a newline, or a path that does not exist gives `STOP REPO_CHECK`,
with no fallback. A
relative value is joined to its folder, and both values are resolved with
`os.path.realpath` and `os.stat`. Two equal real paths, or an equal
`(st_dev, st_ino)`, give `STOP IN_REPO`; otherwise the run goes on as
before. The `os.stat` step and the inode comparison must stay: on macOS a
path in another letter case and a `/System/Volumes/Data` firmlink path
have another real path string but the same inode, and `git` joins a
relative `GIT_COMMON_DIR` wrongly in a subfolder (exit code 0 and a path
that does not exist), which the `os.stat` stops (security finding S-01 and
S-02 of PR-3 design review round 2, measured with `git` 2.54.0 on macOS).
So, by the answer of `git`, `STOP IN_REPO` comes only when the
current working directory lies in a worktree of the same Git
repository as the copy of the script and both have a `.git` entry;
an absolute `GIT_DIR` or `GIT_COMMON_DIR` in the environment of the
caller can give `STOP IN_REPO` for two different repositories (fail
closed). The sentence above, that a run by path inside the
repository of the change reads the file of the change, still holds
for the cases that the check does not see: residual risk 23 of the
D-029 PR-2 supplement, narrowed by the D-029 PR-3 supplement (a
working directory in another repository, for example after a `cd`;
a worktree that has no `.git` entry; a relative `GIT_DIR` or
`GIT_COMMON_DIR` that makes `git` print two different existing
paths: the exception to the inference of card C2, cards
I96-P3-R2-C2 (a) and I96-P3-IR1-C1 (a); a relative `GIT_DIR`
resolves from the folder of each call, whether or not
`GIT_WORK_TREE` is set (tested: read-only
`git rev-parse --git-common-dir`, `git` 2.54.0, macOS, six cases,
implementation review round 2, IR2-P3-S-01); the full pass of a
relative `GIT_DIR` (two different existing git directories) is not
tested).

## Calls from the rules (read-backs, 2026-10-31)

Seven real background dispatches on this repository (desktop app, macOS,
zsh) gave `PASS` with the copy at the bound base: one `dev-explorer` at
`opus`/`high` (the C1 smoke test) and six dispatches at `opus`/`xhigh`
(`dev-reviewer` and `dev-security-reviewer`; Issue #95). Each task
notification at the end had no `agentId:` line; its structured `<task-id>`
field held the ID of the harness line of the dispatch result (R-DEL-2 says
how the main agent uses both). The base ID written as `$B:skills/...` in
zsh lost the path in the repository, and the empty script exited 0 with no
output; an unset or empty variable names the copy in the index. R-DEL-2
says how to write the base ID. No dispatch that does not run in the
background, no resume and no headless run was read back.

## What it cannot prove

- A recorded value is not the effective value; the effective setting stays
  `unknown`.
- The transcript is in a location that the user can write. It can be
  rewritten or deleted; the lowest value only stops appended lines. Card
  I77-R2-C2 is for slice C to decide. Card I79C-C4 (a) accepted it as a
  residual risk (R-DEL-2; FU-051).
- An agent ID can be swapped, for example when a subagent quotes another
  agent's ID in its report.
- The script cannot show that the file belongs to the session that
  dispatched the agent, or that `DIR` is the real projects directory.
- A copy of the script in a repository under review can be changed by the
  pull request under review.
- The size limits, the 1 MiB line limit included, are not measured.
- The file mode bits are not checked.
- On NFS, in containers and on Windows the script is expected to give
  `STOP` rather than a result (for example `OWNER` for a mapped user ID, or
  `INTERNAL` where a needed open flag is missing), or to hang (see the time
  limit below); this is not tested.
- The script does not check that it runs under `-I` (see the threat
  model).
- The script has no time limit of its own. A FUSE or network file system
  can hang it at a listing, an open or a read; a caller needs its own
  timeout.
- The walk is a snapshot. A copy of the agent file added after its
  directory was listed, or a directory moved after it was listed, is not
  seen. The final open is relative to the `subagents` directory that was
  already opened, which may have been moved since.
- An unrelated directory removed during the walk, between its listing and
  its open, gives `NOT_FOUND`, even when the agent file exists.
- On a file system that ignores case (for example APFS by default), a name
  that differs only in case, such as `Subagents` or an upper-case agent file
  name, matches the lstat of `subagents` or of the agent file.
- A directory with a valid name can be a mount point; the walk enters it.
- `.` and `..` match the slug pattern, but `os.scandir` never lists them,
  so the walk does not enter them.
- Bedrock and Vertex model IDs always give `MODEL_NOT_ALLOWED`. From Issue #96 on, provider IDs are a non-goal: they give
  `STOP MODEL_NOT_RECOGNIZED` or `BELOW` and never count, and a user who
  needs them keeps a fork (the sentence before this one describes the
  state before Issue #96).
- `perTurnEffort` may differ from `effort` for a valid reason; the script
  then gives `INCONSISTENT`.
- The `agentId` format, the binding fields and the line format come from
  observation on one machine and one project only.
- The same agent file in two sessions (for example after a resume or a
  fork) gives `AMBIGUOUS`; two such copies were not observed.
- The static test of the script only guards against regressions (see the
  threat model); the same pull request can change the script and its
  tests.
- A real symlink swap between the listing and the open is not tested: the
  tests mock `os.open` for it. The symlink tests at the lstat level run on
  Linux in CI.
- CI does not run Python 3.9.
- The synthetic fixtures of `tests/test_model_effort_readback.py` prove
  only the outcomes that they list (R-VER-1).
- Headless runs, a read-back after a resume, a dispatch that does not run
  in the background and a read-back in a session that merges a change of
  another session are not tested with a real transcript (FU-056). Windows,
  NFS and containers are not tested either (see above).
- From Issue #96 on, the `version` class infers the family from the model
  ID. The official model documentation advises reading the `line` field of
  the Models API instead of inferring the line from the ID; a transcript
  records no `line`, so the script cannot follow that advice (an
  inference from the ID, against the official advice). An older generation
  (for example `claude-opus-4-8` where `opus` was asked for) or a
  Claude-style name that is not the real model also gives `WARN`.
- From Issue #96 on, the Sonnet, Haiku and Fable IDs are not observed by
  this pack (FU-060): their read-back gives `WARN` at best, and an ID of
  theirs that does not have the `version` form stops.
- From Issue #96 on, a run by path inside the repository of the change
  reads the configuration file of the change itself. From Issue #96 PR-3
  on, such a run gives `STOP IN_REPO` when the current working directory
  lies in a worktree of the same Git repository and both have a `.git`
  entry; the cases that the repository check does not see are in the
  Threat model section.
- From Issue #96 on, a wrong `--config-base` literal (for example the head
  of the change) makes the script trust the configuration file of that
  commit: for the classification and, from PR-2 on, for the floor check.
  From Issue #96 PR-2 on, the rules hold no fixed model order. The alias
  order check of R-DEL-2 (`model=` at or above `expected=`) and the
  comparisons of R-DEL-2 with the floor, the row value and any escalated
  setting use the tiers of the configuration read of R-DEL-2, which the
  main agent makes itself with its own base literal. These checks catch a
  wrong tier in the file that the call reads only when the main agent's
  own read uses another, right copy, for example a wrong `--config-base`
  literal in the call while the main agent's own read uses the right base.
  `--floor` makes the script compare the expected values with the floor of
  the call, so a dispatch below that floor gives `BELOW`; this check is
  added to the comparisons of R-DEL-2 and replaces none of them. These
  checks do not catch: (1) a wrong tier when both reads of the main agent
  use the installed copy that the main agent and the script both read
  outside the pack repository, and the user edited that copy (the narrow
  loosening (i) of DL-045, card I96-P2R2-C4 (a)); the same wrong base
  literal in both reads is not part of (i): by card I96-IR2-P2-C2 (b) it is
  an unauthorized residual risk, and FU-063 tracks a deterministic check of
  the bound base literal, not part of PR-3; a main agent that wrongly
  judges that the skill path lies outside the repository of the change is
  not part of (i) either: by card I96-IR-P2-C3 (b) it is an unauthorized
  residual risk until PR-3 adds a deterministic check (a run by path whose
  realpath is under a worktree of the same Git repository as the current
  working directory gives a STOP and asks for the `--config-base` stdin
  form; the check takes the current working directory as the repository
  of the change, and it fails closed when the working directory is in no
  Git repository, when a git query fails, and when variables like
  `GIT_DIR` are set); (2) a wrong ID list;
  (3) a wrong `--floor` value, for example `none` for a scan (R-DEL-2 says
  to pass the higher floor when this session's own reading cannot tell).
  That the two base literals of the call are the same is checked by the
  main agent only; the script does not compare its own code with the copy
  at `--config-base` (FU-062). From Issue #96 PR-3 on, the deterministic
  check exists, and cards I96-P3-C1 (b) and I96-P3-C2 (a) (the user's words
  in the orchestrator session, relayed: 「C1 b，C2 a」) narrow its premise 2:
  it gives `STOP REPO_CHECK` when the folder of the script lies in a Git
  repository and the working directory lies in none, not whenever the
  working directory lies in none; and it reads no variable such as
  `GIT_DIR`, so it rests on the outcome of `git` and of the `os.stat` step
  instead. The cases that it does not see stay residual risk 23 of the
  D-029 PR-2 supplement, an unauthorized residual risk that the user
  decides at merge (D-029 PR-3 supplement).
- From Issue #96 on, the strict open by path (owner, one hard link) may
  stop every read-back in a managed or system-wide installation, and a
  plugin update may replace a configuration file that a user edited, or
  keep one of an older schema that gives `STOP CONFIG`; neither is tested.
- From Issue #96 on, the internal time limit of the `git` calls is 20
  seconds; an outer time limit that is shorter can leave `git` running
  after the script ends (the outcome is still not a result).
- From Issue #96 PR-2 on, the script cannot show that the `--floor` value
  fits the dispatch. Before the merge of PR-2, `--floor` was tested on the
  synthetic fixtures only, because the reviews of PR-2 read back with the
  copy at a base without `--floor`.
- From Issue #96 PR-2 on (realpath): the Read tool of the host may resolve
  `..` literally, so the copy of the configuration file that the main
  agent reads by R-DEL-2 can differ from the copy that the script reads; a
  real file name other than `model_effort_readback.py` gives
  `STOP BAD_ARGS`; and the path can change between `os.path.realpath` and
  the open.
- From Issue #96 PR-3 on, the repository check stops in these cases, each
  fail closed: a project that lies in no Git repository while the pack
  loads from a Git clone (`STOP REPO_CHECK`); a home folder that is itself
  a Git worktree (dotfiles) with the installed copy under it, when the
  working directory is not in a repository of its own (`STOP IN_REPO`, or
  `STOP REPO_CHECK` when `git` fails there); a repository that
  `git` refuses (dubious ownership) or does not find across a file system
  boundary (`STOP REPO_CHECK`); a sandbox that refuses the `lstat` of a
  `.git` above (`STOP REPO_CHECK`, not tested); a pack in a plain subfolder
  of the project repository (`STOP IN_REPO`; the stdin form then reads the
  file at the root of that repository and usually gives `unknown`). The
  remedy: use an installed copy that lies in no Git repository, or work in
  a Git project. Before `git` 2.13 a relative value in a subfolder may be
  wrong; it usually gives `STOP REPO_CHECK` (not tested). Whether a copy
  installed from a third-party marketplace on GitHub lies in a Git clone is
  not known.
