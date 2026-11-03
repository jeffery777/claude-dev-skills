#!/usr/bin/env python3
"""Read back the model and effort that one subagent transcript records (Issue #89, Issue #79 slice B, Issue #96;
REQ-009; stdlib only, one file, no other module of this repository).

Usage (as `python3 -I`):
  model_effort_readback.py subagent --projects-dir DIR --agent-id ID --expect-model FAMILY --expect-effort LEVEL
      --floor FLOOR
  git --no-replace-objects cat-file blob BASE:skills/dev-core/scripts/model_effort_readback.py
      | python3 -I - subagent --config-base BASE --floor FLOOR --projects-dir DIR --agent-id ID
        --expect-model FAMILY --expect-effort LEVEL
  model_effort_readback.py check --projects-dir DIR --agent-id ID --candidate-config FILE   (also from stdin)

DIR is an absolute, normalized path without a trailing `/`. ID is exactly 17 lowercase hexadecimal digits. FAMILY
is a family of the configuration file whose tier is not null; LEVEL is low, medium, high, xhigh or max; both are
required. FLOOR is required and is one key of FLOORS: work (tier 3, high), review-scan (tier 3, xhigh),
review-routine (tier 3, high), review-light (tier 2, medium) or none (no floor check) (Issue #96 PR-2). BASE is a
full commit ID, 40 or 64 lowercase hexadecimal digits: `subagent` needs it when the script runs from stdin and
refuses it when the script runs by its path. `check` takes neither BASE, FLOOR nor expected values. A missing
FLOOR, a repeated, abbreviated or unknown option, -h, --help, a missing or unknown subcommand and any other bad
argument give `STOP BAD_ARGS`.

The configuration file (Issue #96) is `skills/dev-core/model-config.json`. Run from stdin, the script reads it from
the commit BASE with two git calls (rev-parse, whose output must be BASE itself, then cat-file); run by its path, it
reads the `model-config.json` next to the `scripts` folder of the real path of this file (os.path.realpath: a
symlink and `..` on the path to the script are resolved; the configuration file itself is opened without following
a symlink, as below); `check` reads FILE instead. validate_config() checks the file; any failure gives
`STOP CONFIG`.

The script finds DIR/<slug>/<session>/subagents/agent-<ID>.jsonl through directory file descriptors. It follows no
symlink at DIR or under it (the path above DIR resolves as usual) and does not look into a directory whose name is
not in the slug or session format. It needs exactly one such file and reads it up to its size at open. Of each
record it reads only the fields type, message.model, isSidechain, agentId, sessionId, effort and perTurnEffort, and
it skips the records whose model is `<synthetic>`. Each model value is classified by the configuration file: an
exact listed ID ("listed"), the form claude-<family>-<digits>[-<digits>...] of a family of the file ("version"), a
value with a word that names a family below the expected one or with a null tier ("lower"), or "unrecognized".

Output: exactly one line on stdout, ending in a newline; stderr stays empty. No line carries a path, an ID, a model
value or transcript text. A closed or broken stdout gives no line and exit 2.
  PASS model=<F> tier=<n> effort=<level> expected=<F>/<level> expected_tier=<n> floor=<FLOOR>      exit 0
  WARN model=<F> tier=<n> effort=<level> expected=<F>/<level> expected_tier=<n> floor=<FLOOR>      exit 4: an ID
                                                                                                   is not listed
  BELOW model=<F|unrecognized> tier=<n|null|none> effort=<level> expected=<F>/<level> expected_tier=<n>
        floor=<FLOOR>   (one line)                                                                 exit 3
  STOP <REASON>                                                                                    exit 2: no result
  CHECK model=<F|unrecognized> match=<listed|version|name|none> tier=<n|null|none> effort=<level> records=<n>
                                                                                       exit 5: `check` only
model= and tier= come from the lowest record (unrecognized < null < 1 < 2 ...; on a tie a "version" record),
effort= is the lowest effort, <n> after records= is the number of assistant records that were read, and floor= is
the FLOOR of the call. Any other output is not a result.

The order of the `subagent` result: (1) the STOP lines that come at once: the arguments, the files, the parse, the
binding, the fields, the effort format and the configuration file; (2) the classification of each record; (3) BELOW
when a record is below the expected values; (4) else BELOW when FLOOR is not none and the tier that the
configuration file of this call gives to the expected family is below the tier of FLOOR, or the expected effort is
below the effort of FLOOR (a dispatch below its floor); (5) else STOP MODEL_NOT_RECOGNIZED when the records name
more than one family or a value is unrecognized; (6) else WARN when a record is a "version" ID; (7) else PASS.

REASON tokens (a closed set):
  BAD_ARGS              an argument is missing, repeated, unknown or not in its format
  CONFIG                the configuration file cannot be read, is not valid, or the commit BASE cannot be shown
  NOT_FOUND             DIR is not a directory, or no matching transcript file exists
  AMBIGUOUS             more than one session holds a matching transcript file
  SYMLINK               DIR, a subagents directory or the transcript file is a symlink, or one was swapped for a
                        symlink during the walk
  NOT_REGULAR           the transcript file is not a regular file
  OWNER                 the transcript file belongs to another user
  LINK_COUNT            the transcript file has more than one hard link
  PERMISSION            a directory or the transcript file cannot be read
  TOO_LARGE             the file, a line or the number of lines is over its limit
  MALFORMED             a line is not one strict JSON object in UTF-8, or the file is cut short or does not end
                        in a newline
  BINDING_MISMATCH      an assistant record has no isSidechain true, or its agentId or sessionId differs from the
                        ID or the session directory name
  MISSING_FIELD         an assistant record lacks message.model or effort, or one of them or perTurnEffort is not
                        a string
  INCONSISTENT          perTurnEffort differs from effort
  NO_RECORD             the file has no assistant record that is not `<synthetic>`
  MODEL_NOT_RECOGNIZED  a model value is unrecognized, or the records name more than one family and none is below
  EFFORT_NOT_ALLOWED    an effort is not one of the levels
  INTERNAL              any other error

skills/dev-core/references/model-effort-readback.md describes the limits of this script; it is not a rule.
"""

from __future__ import annotations

import argparse
import errno
import json
import os
import re
import select
import signal
import stat
import subprocess
import sys
import time

EFFORT_ORDER = ("low", "medium", "high", "xhigh", "max")
FLOORS = {  # Issue #96 PR-2: --floor value -> (the lowest tier, the lowest effort) of the expected values, or None
    "work": (3, "high"), "review-scan": (3, "xhigh"), "review-routine": (3, "high"), "review-light": (2, "medium"),
    "none": None}
ROLE_NAMES = ("orchestration", "explore", "explore-synthesis", "implement", "implement-reduced", "review-routine",
              "review-routine-light", "review-deep", "review-security", "scan")
AGENT_NAMES = ("dev-explorer", "dev-implementer", "dev-reviewer", "dev-security-reviewer")
RESERVED_FAMILY_NAMES = frozenset({"unrecognized", "none", "null", "unknown", "inherit", "default", *EFFORT_ORDER})
CONFIG_KEYS = frozenset({"schema", "validated_with", "responsibility", "families", "roles"})
VALIDATED_WITH_KEYS = frozenset({"generation", "note"})
FAMILY_KEYS = frozenset({"tier", "ids", "basis"})
ROLE_KEYS = frozenset({"family", "effort", "agent", "agent_default"})
REASONS = frozenset({
    "BAD_ARGS", "CONFIG", "NOT_FOUND", "AMBIGUOUS", "SYMLINK", "NOT_REGULAR", "OWNER", "LINK_COUNT", "PERMISSION",
    "TOO_LARGE", "MALFORMED", "BINDING_MISMATCH", "MISSING_FIELD", "INCONSISTENT", "NO_RECORD",
    "MODEL_NOT_RECOGNIZED", "EFFORT_NOT_ALLOWED", "INTERNAL"})
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_LINE_BYTES = 1024 * 1024
MAX_LINES = 200000
MAX_NUMBER_CHARS = 100
MAX_CONFIG_BYTES = 64 * 1024
MAX_CONFIG_DEPTH = 8
MAX_TIER = 99
MAX_ID_CHARS = 100
MAX_SCAN_CHARS = 200  # the part of an unrecognized model value that is searched for a family word
GIT_TIMEOUT = 20  # seconds for both git calls together; shorter than the time limit of the caller
SLUG_RE = r"[A-Za-z0-9._-]+"
SESSION_RE = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
AGENT_ID_RE = r"[0-9a-f]{17}"
BASE_RE = r"(?:[0-9a-f]{40}|[0-9a-f]{64})"
FAMILY_RE = r"[a-z]{1,20}"
MODEL_ID_RE = r"[a-z0-9.-]{1,100}"
VERSION_RE = r"claude-([a-z]+)-[0-9]+(?:-[0-9]+)*"
WORD_SPLIT_RE = r"[^a-z0-9]+"
ASCII_LOWER = {code: code + 32 for code in range(ord("A"), ord("Z") + 1)}  # only A-Z, no other case mapping
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


SUBAGENT_OPTIONS = ("--projects-dir", "--agent-id", "--expect-model", "--expect-effort", "--config-base", "--floor")
CHECK_OPTIONS = ("--projects-dir", "--agent-id", "--candidate-config")


def parse_args(argv):
    """(mode, {option name: its one value or None}) from the arguments; the checks that need no file."""
    top = Parser(prog="model_effort_readback.py", allow_abbrev=False, add_help=False)
    modes = top.add_subparsers(dest="mode")
    for mode, options in (("subagent", SUBAGENT_OPTIONS), ("check", CHECK_OPTIONS)):
        sub = modes.add_parser(mode, allow_abbrev=False, add_help=False)
        for option in options:
            sub.add_argument(option, action="append")  # a list, so that a repeated option is seen
    args = top.parse_args(argv)
    if args.mode not in ("subagent", "check"):
        raise Stop("BAD_ARGS")
    if args.mode == "subagent":
        lists = (args.projects_dir, args.agent_id, args.expect_model, args.expect_effort, args.config_base,
                 args.floor)
    else:
        lists = (args.projects_dir, args.agent_id, args.candidate_config)
    values = {}
    for option, given in zip(SUBAGENT_OPTIONS if args.mode == "subagent" else CHECK_OPTIONS, lists):
        if given is not None and len(given) != 1:
            raise Stop("BAD_ARGS")
        values[option] = None if given is None else given[0]
    projects_dir, agent_id = values["--projects-dir"], values["--agent-id"]
    if projects_dir is None or agent_id is None:
        raise Stop("BAD_ARGS")
    if ("\x00" in projects_dir or not os.path.isabs(projects_dir) or os.path.normpath(projects_dir) != projects_dir
            or projects_dir.endswith("/")):
        raise Stop("BAD_ARGS")
    if not re.fullmatch(AGENT_ID_RE, agent_id):
        raise Stop("BAD_ARGS")
    if args.mode == "check":
        if values["--candidate-config"] is None or "\x00" in values["--candidate-config"]:
            raise Stop("BAD_ARGS")
        return args.mode, values
    if values["--expect-model"] is None or values["--expect-effort"] not in EFFORT_ORDER:
        raise Stop("BAD_ARGS")
    if values["--floor"] not in FLOORS:  # also a missing --floor (Issue #96 PR-2)
        raise Stop("BAD_ARGS")
    base = values["--config-base"]
    if base is not None and not re.fullmatch(BASE_RE, base):
        raise Stop("BAD_ARGS")
    return args.mode, values


def from_stdin() -> bool:
    """Whether the script runs from stdin (`python3 -I -`); asked in run(), never at import."""
    return __file__ == "<stdin>" or sys.argv[:1] == ["-"]


def own_config_path() -> str:
    """The `model-config.json` next to the `scripts` folder of the real path of this file, for a run by its path;
    the realpath resolves a symlink and `..` on the path to this file, never the configuration file (IR1-S-05)."""
    here = os.path.realpath(__file__)
    scripts = os.path.dirname(here)
    if os.path.basename(here) != "model_effort_readback.py" or os.path.basename(scripts) != "scripts":
        raise Stop("BAD_ARGS")
    return os.path.join(os.path.dirname(scripts), "model-config.json")


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


def read_config_file(path: str) -> bytes:
    """The bytes of a configuration file, opened as strictly as the transcript file; any failure is CONFIG."""
    try:
        fd = open_at(path, FILE_FLAGS)
    except Stop:
        raise Stop("CONFIG") from None
    try:
        st = os.fstat(fd)
        if (not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid() or st.st_nlink != 1
                or st.st_size > MAX_CONFIG_BYTES):
            raise Stop("CONFIG")
        data = b""
        while len(data) < st.st_size:
            chunk = os.read(fd, st.st_size - len(data))
            if not chunk:
                raise Stop("CONFIG")  # cut short while it was read
            data += chunk
        return data
    except OSError:
        raise Stop("CONFIG") from None
    finally:
        os.close(fd)


def run_git(argv: list, deadline: float) -> bytes:
    """The stdout of one git call, at most MAX_CONFIG_BYTES; a timeout, an overflow, an exit code other than 0 and
    any error are CONFIG, and a call that has not ended is killed with its process group."""
    proc, ended = None, False
    try:
        proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                start_new_session=True)
        out_fd, data = proc.stdout.fileno(), b""
        while True:
            left = deadline - time.monotonic()
            if left <= 0 or not select.select([out_fd], [], [], left)[0]:
                raise Stop("CONFIG")  # the time budget is used up
            chunk = os.read(out_fd, MAX_CONFIG_BYTES + 1 - len(data))
            if not chunk:
                break
            data += chunk
            if len(data) > MAX_CONFIG_BYTES:
                raise Stop("CONFIG")
        left = deadline - time.monotonic()
        if left <= 0:
            raise Stop("CONFIG")
        code = proc.wait(timeout=left)
        ended = True
        if code != 0:
            raise Stop("CONFIG")
        return data
    except Stop:
        raise
    except Exception:
        raise Stop("CONFIG") from None
    finally:
        if proc is not None:
            if not ended:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except Exception:
                    pass
                try:
                    proc.wait(timeout=1)
                except Exception:
                    pass
            try:
                proc.stdout.close()
            except Exception:
                pass


def config_from_git(base: str) -> bytes:
    """The configuration file of the commit `base`: the commit must resolve to exactly the literal `base`."""
    deadline = time.monotonic() + GIT_TIMEOUT
    shown = run_git(["git", "--no-replace-objects", "rev-parse", "--verify", "--quiet", base + "^{commit}"],
                    deadline)
    if shown != (base + "\n").encode("ascii"):
        raise Stop("CONFIG")
    return run_git(["git", "--no-replace-objects", "cat-file", "blob", base + ":skills/dev-core/model-config.json"],
                   deadline)


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


def is_family_word(word: str, family: str) -> bool:
    """A word names a family when it is the family name, or the name followed by digits only."""
    return word.startswith(family) and re.fullmatch(r"[0-9]*", word[len(family):]) is not None


def validate_config(data) -> dict:
    """The configuration file as a dict, from its bytes; any rule it breaks raises Stop("CONFIG").

    A pure function: it reads no file, no argument and no process data, and starts no process. The rules: strict
    JSON in UTF-8 without a BOM, at most MAX_CONFIG_BYTES and MAX_CONFIG_DEPTH levels; closed key sets; schema 1;
    family names in FAMILY_RE and not reserved; a tier is an int from 1 to MAX_TIER or null, and no two tiers that
    are not null are equal; each ID is a string in MODEL_ID_RE, is listed once, and has a word that names its own
    family and no word that names another family; a basis is a string that is not empty; the roles are exactly
    ROLE_NAMES, each with a family whose tier is not null, an effort [min, max] of two levels with min <= max, an
    agent of AGENT_NAMES when it has one, and agent_default only true, only with an agent, at most once per agent.
    It does not check floors: a role value under a floor is not an error here (card I96-C4 (a)).
    """
    def fail():
        raise Stop("CONFIG")

    if type(data) is not bytes or len(data) > MAX_CONFIG_BYTES:
        fail()
    try:
        text = data.decode("utf-8", errors="strict")
        if text.startswith("\ufeff"):
            fail()
        config = json.loads(text, object_pairs_hook=unique_pairs, parse_int=short_int, parse_float=short_float,
                            parse_constant=no_constant)
    except (ValueError, RecursionError):
        raise Stop("CONFIG") from None
    stack = [(config, 1)]
    while stack:
        value, depth = stack.pop()
        if isinstance(value, (dict, list)):
            if depth > MAX_CONFIG_DEPTH:
                fail()
            stack.extend((item, depth + 1) for item in (value.values() if isinstance(value, dict) else value))
    if type(config) is not dict or set(config) != CONFIG_KEYS:
        fail()
    if type(config["schema"]) is not int or config["schema"] != 1:
        fail()
    validated_with = config["validated_with"]
    if (type(validated_with) is not dict or set(validated_with) != VALIDATED_WITH_KEYS
            or not all(type(v) is str for v in validated_with.values())):
        fail()
    if type(config["responsibility"]) is not str:
        fail()
    families, roles = config["families"], config["roles"]
    if type(families) is not dict or not families or type(roles) is not dict:
        fail()
    tiers = []
    for name, family in families.items():
        if not re.fullmatch(FAMILY_RE, name) or name in RESERVED_FAMILY_NAMES:
            fail()
        if type(family) is not dict or set(family) != FAMILY_KEYS:
            fail()
        tier = family["tier"]
        if tier is not None:
            if type(tier) is not int or not 1 <= tier <= MAX_TIER:
                fail()
            tiers.append(tier)
        if type(family["basis"]) is not str or not family["basis"]:
            fail()
        if type(family["ids"]) is not list:
            fail()
    if len(tiers) != len(set(tiers)):
        fail()
    seen_ids = set()
    for name, family in families.items():
        for model_id in family["ids"]:
            if type(model_id) is not str or not re.fullmatch(MODEL_ID_RE, model_id) or model_id in seen_ids:
                fail()
            seen_ids.add(model_id)
            words = re.split(WORD_SPLIT_RE, model_id)
            if not any(is_family_word(word, name) for word in words):
                fail()
            if any(is_family_word(word, other) for word in words for other in families if other != name):
                fail()
    if set(roles) != set(ROLE_NAMES):
        fail()
    defaults = set()
    for role in roles.values():
        if type(role) is not dict or not {"family", "effort"} <= set(role) <= ROLE_KEYS:
            fail()
        if type(role["family"]) is not str or role["family"] not in families:
            fail()
        if families[role["family"]]["tier"] is None:
            fail()
        effort = role["effort"]
        if (type(effort) is not list or len(effort) != 2 or not all(type(e) is str for e in effort)
                or not all(e in EFFORT_ORDER for e in effort)
                or EFFORT_ORDER.index(effort[0]) > EFFORT_ORDER.index(effort[1])):
            fail()
        if "agent" in role and (type(role["agent"]) is not str or role["agent"] not in AGENT_NAMES):
            fail()
        if "agent_default" in role:
            if role["agent_default"] is not True or "agent" not in role or role["agent"] in defaults:
                fail()
            defaults.add(role["agent"])
    return config


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


def read_back(lines: list, agent_id: str, session: str) -> list:
    """The (model value, effort) of each assistant record that is not `<synthetic>`; the checks of each record that
    stop at once (MISSING_FIELD, BINDING_MISMATCH, INCONSISTENT, EFFORT_NOT_ALLOWED) come before any classification."""
    records = []
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
        if effort not in EFFORT_ORDER:
            raise Stop("EFFORT_NOT_ALLOWED")
        records.append((model, effort))
    if not records:
        raise Stop("NO_RECORD")
    return records


def classify(model: str, tiers: dict, listed: dict, expected_tier):
    """(class, family or None) of one model value; expected_tier is None in the check mode, where step 3 takes any
    family word ("name") instead of a family below the expected one ("lower")."""
    if model in listed:  # step 1: an exact listed ID
        return "listed", listed[model]
    version = re.fullmatch(VERSION_RE, model) if len(model) <= MAX_ID_CHARS else None
    if version is not None and version.group(1) in tiers:  # step 2
        return "version", version.group(1)
    words = re.split(WORD_SPLIT_RE, model[:MAX_SCAN_CHARS].translate(ASCII_LOWER))  # step 3
    named = {family for family in tiers for word in words if is_family_word(word, family)}
    if expected_tier is not None:
        named = {family for family in named if tiers[family] is None or tiers[family] < expected_tier}
    if named:
        return ("lower" if expected_tier is not None else "name"), min(named, key=lambda f: (rank(tiers[f]), f))
    return "unrecognized", None  # step 4


def rank(tier) -> int:
    """unrecognized (-1) < null (0) < 1 < 2 < ..."""
    return 0 if tier is None else tier


def lowest(results: list):
    """The result that model= and tier= show: the lowest rank, and on a tie a "version" result, else the first."""
    return min(range(len(results)),
               key=lambda i: (results[i][2], 0 if results[i][0] == "version" else 1, i))


def tier_text(result) -> str:
    _, family, level = result
    return "none" if family is None else ("null" if level == 0 else str(level))


def run(argv):
    """(output line without the newline, exit code)."""
    mode, values = parse_args(argv)
    if mode == "check":
        data = read_config_file(values["--candidate-config"])
    elif from_stdin():
        if values["--config-base"] is None:
            raise Stop("BAD_ARGS")
        data = config_from_git(values["--config-base"])
    else:
        if values["--config-base"] is not None:
            raise Stop("BAD_ARGS")
        data = read_config_file(own_config_path())
    config = validate_config(data)
    tiers = {name: family["tier"] for name, family in config["families"].items()}
    listed = {model_id: name for name, family in config["families"].items() for model_id in family["ids"]}
    expected_tier = None
    if mode == "subagent":
        family = values["--expect-model"]
        if family not in tiers or tiers[family] is None:
            raise Stop("BAD_ARGS")
        expected_tier = tiers[family]
    fd, session = locate(values["--projects-dir"], values["--agent-id"])
    try:
        lines = read_lines(fd)
    finally:
        os.close(fd)
    records = read_back(lines, values["--agent-id"], session)
    results = []  # (class, family or None, rank)
    for model, _ in records:
        kind, family = classify(model, tiers, listed, expected_tier)
        results.append((kind, family, -1 if family is None else rank(tiers[family])))
    effort = EFFORT_ORDER[min(EFFORT_ORDER.index(e) for _, e in records)]
    low = results[lowest(results)]
    shown = f"model={low[1] or 'unrecognized'} tier={tier_text(low)} effort={effort}"
    if mode == "check":
        match = min(({"unrecognized": 0, "name": 1, "version": 2, "listed": 3}[r[0]] for r in results))
        word = ("none", "name", "version", "listed")[match]
        return (f"CHECK model={low[1] or 'unrecognized'} match={word} tier={tier_text(low)} effort={effort} "
                f"records={len(records)}"), 5
    expected_effort = EFFORT_ORDER.index(values["--expect-effort"])
    below = [EFFORT_ORDER.index(e) < expected_effort or kind == "lower"
             or (kind in ("listed", "version") and (tiers[family] is None or tiers[family] < expected_tier))
             for (kind, family, _), (_, e) in zip(results, records)]
    families = {family for _, family, _ in results}  # None stands for unrecognized
    floor = FLOORS[values["--floor"]]
    if any(below):  # step 3: a record is below the expected values
        word, code = "BELOW", 3
    elif floor is not None and (expected_tier < floor[0] or expected_effort < EFFORT_ORDER.index(floor[1])):
        word, code = "BELOW", 3  # step 4: the expected values are below the floor (Issue #96 PR-2)
    elif len(families) > 1 or any(kind == "unrecognized" for kind, _, _ in results):
        raise Stop("MODEL_NOT_RECOGNIZED")  # more than one family and none below, or an unrecognized value
    elif any(kind == "version" for kind, _, _ in results):
        word, code = "WARN", 4
    else:
        word, code = "PASS", 0
    return (f"{word} {shown} expected={values['--expect-model']}/{values['--expect-effort']} "
            f"expected_tier={expected_tier} floor={values['--floor']}"), code


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
