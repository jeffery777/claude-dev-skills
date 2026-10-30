#!/usr/bin/env python3
"""Read back the model and effort that one subagent transcript records (Issue #89, Issue #79 slice B; REQ-009;
stdlib only, one file, no other module of this repository).

Usage (as `python3 -I`):
  model_effort_readback.py subagent --projects-dir DIR --agent-id ID [--expect-model ALIAS --expect-effort LEVEL]

DIR is an absolute, normalized path without a trailing `/`. ID is exactly 17 lowercase hexadecimal digits. ALIAS is
haiku, sonnet or opus; LEVEL is low, medium, high, xhigh or max; give both or neither. A repeated, abbreviated or
unknown option, -h, --help, a missing or unknown subcommand and any other bad argument give `STOP BAD_ARGS`.

The script finds DIR/<slug>/<session>/subagents/agent-<ID>.jsonl through directory file descriptors. It follows no
symlink at DIR or under it (the path above DIR resolves as usual) and does not look into a directory whose name is
not in the slug or session format. It needs exactly one such file, reads it up to its size at open, and takes the
lowest model and the lowest effort over all assistant records that are not `<synthetic>`. Of each record it reads
only the fields type, message.model, isSidechain, agentId, sessionId, effort and perTurnEffort. A model counts only
when MODEL_ALLOWLIST holds its exact ID.

Output: exactly one line on stdout, ending in a newline; stderr stays empty. No line carries a path, an ID or
transcript text. A closed or broken stdout gives no line and exit 2.
  OK model=<alias> effort=<level> records=<n>                   exit 0: no expected values given; not a comparison
  PASS model=<alias> effort=<level> expected=<alias>/<level>    exit 0: neither value is below the expected one
  BELOW model=<alias> effort=<level> expected=<alias>/<level>   exit 3: a value is below the expected one
  STOP <REASON>                                                 exit 2: no result
<n> is the number of assistant records that were read. Any other output is not a result.

REASON tokens (a closed set):
  BAD_ARGS            an argument is missing, repeated, unknown or not in its format
  NOT_FOUND           DIR is not a directory, or no matching transcript file exists
  AMBIGUOUS           more than one session holds a matching transcript file
  SYMLINK             DIR, a subagents directory or the transcript file is a symlink, or one was swapped for a
                      symlink during the walk
  NOT_REGULAR         the transcript file is not a regular file
  OWNER               the transcript file belongs to another user
  LINK_COUNT          the transcript file has more than one hard link
  PERMISSION          a directory or the transcript file cannot be read
  TOO_LARGE           the file, a line or the number of lines is over its limit
  MALFORMED           a line is not one strict JSON object in UTF-8, or the file is cut short or does not end
                      in a newline
  BINDING_MISMATCH    an assistant record has no isSidechain true, or its agentId or sessionId differs from the
                      ID or the session directory name
  MISSING_FIELD       an assistant record lacks message.model or effort, or one of them or perTurnEffort is not
                      a string
  INCONSISTENT        perTurnEffort differs from effort
  NO_RECORD           the file has no assistant record that is not `<synthetic>`
  MODEL_NOT_ALLOWED   a model ID is not in MODEL_ALLOWLIST
  EFFORT_NOT_ALLOWED  an effort is not one of the levels
  INTERNAL            any other error

skills/dev-core/references/model-effort-readback.md describes the limits of this script; it is not a rule.
"""

from __future__ import annotations

import argparse
import errno
import json
import os
import re
import stat
import sys

# Only model IDs that were observed (Issue #89). A new ID, or a new generation that replaces this one, is a strict
# change with a decision card (FU-049); the tests pin this content.
MODEL_ALLOWLIST = {"claude-opus-5-5": "opus"}
MODEL_ORDER = ("haiku", "sonnet", "opus")
EFFORT_ORDER = ("low", "medium", "high", "xhigh", "max")
REASONS = frozenset({
    "BAD_ARGS", "NOT_FOUND", "AMBIGUOUS", "SYMLINK", "NOT_REGULAR", "OWNER", "LINK_COUNT", "PERMISSION", "TOO_LARGE",
    "MALFORMED", "BINDING_MISMATCH", "MISSING_FIELD", "INCONSISTENT", "NO_RECORD", "MODEL_NOT_ALLOWED",
    "EFFORT_NOT_ALLOWED", "INTERNAL"})
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_LINE_BYTES = 1024 * 1024
MAX_LINES = 200000
MAX_NUMBER_CHARS = 100
SLUG_RE = r"[A-Za-z0-9._-]+"
SESSION_RE = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
AGENT_ID_RE = r"[0-9a-f]{17}"
DIR_FLAGS = None  # set by set_flags() inside main(), so that a platform without a flag gives STOP INTERNAL
FILE_FLAGS = None


class Stop(Exception):
    """A `STOP <reason>` result; reason is a token of REASONS."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class Parser(argparse.ArgumentParser):
    """Every argument error is BAD_ARGS: nothing is printed and no argument is echoed."""

    def error(self, message):
        raise Stop("BAD_ARGS")

    def exit(self, status=0, message=None):
        raise Stop("BAD_ARGS")


def parse_args(argv):
    """(DIR, ID, (ALIAS, LEVEL) or None) from the arguments."""
    top = Parser(prog="model_effort_readback.py", allow_abbrev=False, add_help=False)
    modes = top.add_subparsers(dest="mode")
    sub = modes.add_parser("subagent", allow_abbrev=False, add_help=False)
    for option in ("--projects-dir", "--agent-id", "--expect-model", "--expect-effort"):
        sub.add_argument(option, action="append")  # a list, so that a repeated option is seen
    args = top.parse_args(argv)
    if args.mode != "subagent":
        raise Stop("BAD_ARGS")
    for given in (args.projects_dir, args.agent_id, args.expect_model, args.expect_effort):
        if given is not None and len(given) != 1:
            raise Stop("BAD_ARGS")
    if (args.projects_dir is None or args.agent_id is None
            or (args.expect_model is None) != (args.expect_effort is None)):
        raise Stop("BAD_ARGS")
    projects_dir, agent_id = args.projects_dir[0], args.agent_id[0]
    if ("\x00" in projects_dir or not os.path.isabs(projects_dir) or os.path.normpath(projects_dir) != projects_dir
            or projects_dir.endswith("/")):
        raise Stop("BAD_ARGS")
    if not re.fullmatch(AGENT_ID_RE, agent_id):
        raise Stop("BAD_ARGS")
    if args.expect_model is None:
        return projects_dir, agent_id, None
    expect = (args.expect_model[0], args.expect_effort[0])
    if expect[0] not in MODEL_ORDER or expect[1] not in EFFORT_ORDER:
        raise Stop("BAD_ARGS")
    return projects_dir, agent_id, expect


def reason_of(err) -> str:
    """The token for an errno of an open, a listing, a stat or a read."""
    if err in (errno.ELOOP, errno.ENOTDIR):
        return "SYMLINK"
    if err == errno.ENOENT:
        return "NOT_FOUND"
    if err in (errno.EACCES, errno.EPERM):
        return "PERMISSION"
    return "INTERNAL"


def set_flags():
    """Set DIR_FLAGS and FILE_FLAGS; a missing flag raises AttributeError here, not at import."""
    global DIR_FLAGS, FILE_FLAGS
    DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOCTTY


def open_at(name: str, flags: int, dir_fd=None) -> int:
    try:
        return os.open(name, flags, dir_fd=dir_fd)
    except OSError as exc:
        raise Stop(reason_of(exc.errno)) from None


def lstat_at(name: str, dir_fd: int):
    """The lstat result of name in dir_fd, or None when the name does not exist."""
    try:
        return os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            return None
        raise Stop(reason_of(exc.errno)) from None


def subdirs(dir_fd: int, pattern: str) -> list:
    """The names in dir_fd that fully match pattern and are directories, not symlinks; others are skipped unread."""
    names = []
    try:
        with os.scandir(dir_fd) as entries:
            for entry in entries:
                if re.fullmatch(pattern, entry.name) and entry.is_dir(follow_symlinks=False):
                    names.append(entry.name)
    except OSError as exc:
        raise Stop(reason_of(exc.errno)) from None
    return sorted(names)


def open_subagents(session_fd: int):
    """The fd of the subagents directory of a session, or None when the session has none."""
    st = lstat_at("subagents", session_fd)
    if st is None:
        return None
    if stat.S_ISLNK(st.st_mode):
        raise Stop("SYMLINK")
    if not stat.S_ISDIR(st.st_mode):
        return None
    return open_at("subagents", DIR_FLAGS, session_fd)


def has_target(subagents_fd: int, target: str) -> bool:
    st = lstat_at(target, subagents_fd)
    if st is None:
        return False
    if stat.S_ISLNK(st.st_mode):
        raise Stop("SYMLINK")
    if not stat.S_ISREG(st.st_mode):
        raise Stop("NOT_REGULAR")
    return True


def locate(projects_dir: str, agent_id: str):
    """(fd of the one transcript file, its session directory name); the caller closes the fd."""
    try:
        st = os.lstat(projects_dir)
    except OSError as exc:
        raise Stop("NOT_FOUND" if exc.errno == errno.ENOTDIR else reason_of(exc.errno)) from None
    if stat.S_ISLNK(st.st_mode):
        raise Stop("SYMLINK")
    if not stat.S_ISDIR(st.st_mode):
        raise Stop("NOT_FOUND")
    target = "agent-" + agent_id + ".jsonl"
    count, match_fd, session = 0, None, None
    root_fd = open_at(projects_dir, DIR_FLAGS)
    try:
        for slug in subdirs(root_fd, SLUG_RE):
            slug_fd = open_at(slug, DIR_FLAGS, root_fd)
            try:
                for name in subdirs(slug_fd, SESSION_RE):
                    session_fd = open_at(name, DIR_FLAGS, slug_fd)
                    try:
                        subagents_fd = open_subagents(session_fd)
                        if subagents_fd is None:
                            continue
                        keep = False
                        try:
                            if has_target(subagents_fd, target):
                                count += 1
                                if match_fd is None:
                                    match_fd, session, keep = subagents_fd, name, True
                        finally:
                            if not keep:
                                os.close(subagents_fd)
                    finally:
                        os.close(session_fd)
            finally:
                os.close(slug_fd)
        if count == 0:
            raise Stop("NOT_FOUND")
        if count > 1:
            raise Stop("AMBIGUOUS")
        return open_at(target, FILE_FLAGS, match_fd), session
    finally:
        os.close(root_fd)
        if match_fd is not None:
            os.close(match_fd)


def read_lines(fd: int) -> list:
    """The lines of the open transcript file, read up to its size at open, without the final newline."""
    st = os.fstat(fd)
    if not stat.S_ISREG(st.st_mode):
        raise Stop("NOT_REGULAR")
    if st.st_uid != os.getuid():
        raise Stop("OWNER")
    if st.st_nlink != 1:
        raise Stop("LINK_COUNT")
    if st.st_size > MAX_FILE_BYTES:
        raise Stop("TOO_LARGE")
    chunks, total = [], 0
    while total < st.st_size:
        try:
            chunk = os.read(fd, min(MAX_LINE_BYTES, st.st_size - total))
        except OSError as exc:
            raise Stop(reason_of(exc.errno)) from None
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
    if total < st.st_size:
        raise Stop("MALFORMED")  # the file was cut short while it was read
    data = b"".join(chunks)
    if not data:
        return []
    if not data.endswith(b"\n"):
        raise Stop("MALFORMED")  # the last line may still be written
    lines = data[:-1].split(b"\n")
    if len(lines) > MAX_LINES or any(len(line) > MAX_LINE_BYTES for line in lines):
        raise Stop("TOO_LARGE")
    return lines


def unique_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate key")
        obj[key] = value
    return obj


def short_int(text: str) -> int:
    if len(text) > MAX_NUMBER_CHARS:
        raise ValueError("number too long")
    return int(text)


def short_float(text: str) -> float:
    if len(text) > MAX_NUMBER_CHARS:
        raise ValueError("number too long")
    return float(text)


def no_constant(text: str):
    raise ValueError("NaN or Infinity")


def parse_record(line: bytes) -> dict:
    """One line as a JSON object: strict UTF-8 without a BOM, no duplicate key, no NaN or Infinity, short numbers."""
    if not line:
        raise Stop("MALFORMED")
    try:
        text = line.decode("utf-8", errors="strict")
        if text.startswith("\ufeff"):
            raise ValueError("BOM")
        record = json.loads(text, object_pairs_hook=unique_pairs, parse_int=short_int, parse_float=short_float,
                            parse_constant=no_constant)
    except (ValueError, RecursionError):
        raise Stop("MALFORMED") from None
    if not isinstance(record, dict):
        raise Stop("MALFORMED")
    return record


def read_back(lines: list, agent_id: str, session: str):
    """(lowest model alias, lowest effort, number of assistant records read) over the lines."""
    model_rank, effort_rank, count = len(MODEL_ORDER), len(EFFORT_ORDER), 0
    for line in lines:
        record = parse_record(line)
        kind = record.get("type")
        if not isinstance(kind, str) or kind != "assistant":
            continue
        message = record.get("message")
        if not isinstance(message, dict) or not isinstance(message.get("model"), str):
            raise Stop("MISSING_FIELD")
        model = message["model"]
        if model == "<synthetic>":
            continue
        if (record.get("isSidechain") is not True or record.get("agentId") != agent_id
                or record.get("sessionId") != session):
            raise Stop("BINDING_MISMATCH")
        effort = record.get("effort")
        if not isinstance(effort, str):
            raise Stop("MISSING_FIELD")
        if "perTurnEffort" in record:
            if not isinstance(record["perTurnEffort"], str):
                raise Stop("MISSING_FIELD")
            if record["perTurnEffort"] != effort:
                raise Stop("INCONSISTENT")
        if model not in MODEL_ALLOWLIST:
            raise Stop("MODEL_NOT_ALLOWED")
        if effort not in EFFORT_ORDER:
            raise Stop("EFFORT_NOT_ALLOWED")
        model_rank = min(model_rank, MODEL_ORDER.index(MODEL_ALLOWLIST[model]))
        effort_rank = min(effort_rank, EFFORT_ORDER.index(effort))
        count += 1
    if count == 0:
        raise Stop("NO_RECORD")
    return MODEL_ORDER[model_rank], EFFORT_ORDER[effort_rank], count


def run(argv):
    """(output line without the newline, exit code)."""
    projects_dir, agent_id, expect = parse_args(argv)
    fd, session = locate(projects_dir, agent_id)
    try:
        lines = read_lines(fd)
    finally:
        os.close(fd)
    model, effort, count = read_back(lines, agent_id, session)
    if expect is None:
        return f"OK model={model} effort={effort} records={count}", 0
    below = (MODEL_ORDER.index(model) < MODEL_ORDER.index(expect[0])
             or EFFORT_ORDER.index(effort) < EFFORT_ORDER.index(expect[1]))
    word, code = ("BELOW", 3) if below else ("PASS", 0)
    return f"{word} model={model} effort={effort} expected={expect[0]}/{expect[1]}", code


def main(argv=None) -> int:
    try:
        try:
            set_flags()
            line, code = run(sys.argv[1:] if argv is None else argv)
        except Stop as stop:
            line, code = "STOP " + (stop.reason if stop.reason in REASONS else "INTERNAL"), 2
    except BaseException:  # every other error, so that stderr stays empty
        line, code = "STOP INTERNAL", 2
    try:
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
    except BaseException:  # a closed or broken stdout: no line, no traceback
        sys.stdout = None  # so that the flush at exit writes no error to stderr
        return 2
    return code


if __name__ == "__main__":
    sys.exit(main())
