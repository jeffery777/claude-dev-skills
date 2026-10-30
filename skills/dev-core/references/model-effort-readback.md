# Model and effort read-back script (Issue #89)

This file describes a script; it is not a rule. No dev-* skill tells an
agent to run it; Issue #79 slice C decides whether and how. Until then the
manual reading of R-DEL-2 stays as it is.

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

- `subagent` is the only mode. A session mode is slice D of Issue #79.
- `DIR` is an absolute path, equal to its normalized form, without a
  trailing `/` (`/` itself is refused).
- `ID` is exactly 17 lowercase hexadecimal digits.
- `--expect-model` is `haiku`, `sonnet` or `opus`; `--expect-effort` is
  `low`, `medium`, `high`, `xhigh` or `max`. Give both or neither.
- A repeated, abbreviated or unknown option, `-h`, `--help`, a missing or
  unknown subcommand and any other bad argument give `STOP BAD_ARGS`. No
  output echoes an argument.

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
     exactly.
- The script reads no other field: not `requestedModel`, `advisorModel`,
  `tools`, the `params` of an `api-request`, `version`, or any text.
- The result is the lowest model and, separately, the lowest effort over
  all records read. No record left gives `NO_RECORD`.

## Output and exit codes

A result of this script is exactly one line in the grammar below with its
exit code; any other output is not a result. `OK` is not a comparison;
`PASS` means not below the expected values, not equal to them.

| Output line | Exit code |
| --- | --- |
| `OK model=<alias> effort=<level> records=<n>` (no expected values given) | 0 |
| `PASS model=<alias> effort=<level> expected=<alias>/<level>` (neither value is below the expected one) | 0 |
| `BELOW model=<alias> effort=<level> expected=<alias>/<level>` (a value is below the expected one) | 3 |
| `STOP <REASON>` | 2 |

stderr stays empty; any other error is `STOP INTERNAL`, a missing open
flag on the platform included. A closed or broken stdout gives no line and
exit code 2. No line carries a path, an ID or transcript text. The orders
are `haiku`, `sonnet`, `opus` and `low`, `medium`, `high`, `xhigh`, `max`.

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
| `MODEL_NOT_ALLOWED` | A model ID is not in the allowlist. |
| `EFFORT_NOT_ALLOWED` | An effort is not one of the levels. |
| `INTERNAL` | Any other error. |

This file gives no action for a token. Slice C of Issue #79 decides what a
token means for the work.

## Allowlist

`MODEL_ALLOWLIST` in the script holds the model IDs that count. The
allowlist policy is in REQ-009
(`docs/requirements/REQ-009-subagent-model-effort.md`, item "Allowlist");
this file does not restate it (REQ-022). FU-049 tracks the Sonnet and
Haiku IDs.

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

The statements that the script reads no environment variable and writes
no file rest on a code review of the current code. The static test of the
script is a regression aid only: it checks the imports, the direct
`os.<name>` attributes and a list of names, and it does not cover every
way of writing a call (for example `os.path` functions, chained attributes
or `__builtins__`). FU-050 tracks a stricter check.

## What it cannot prove

- A recorded value is not the effective value; the effective setting stays
  `unknown`.
- The transcript is in a location that the user can write. It can be
  rewritten or deleted; the lowest value only stops appended lines. Card
  I77-R2-C2 is for slice C to decide.
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
- Bedrock and Vertex model IDs always give `MODEL_NOT_ALLOWED`.
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
