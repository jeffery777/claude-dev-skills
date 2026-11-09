#!/usr/bin/env python3
"""Reviewer write-channel acceptance record: `check` and `accept` (R-REV-1, Issue #106, D-032).

The pack reviewers keep Bash, an effective write channel. Core v0.5.0
`review-required-read-only` lets the user accept that residual risk once for a
specific environment. The record lives on the user's machine, one file per clone:
`~/.claude/dev-skills/reviewer-acceptance/<id>.json`, where `<id>` is the SHA-256
of the real path, `st_dev` and `st_ino` of the clone's common Git directory.
The accepted text is the "Accepted text" section of
`../references/reviewer-acceptance.md` of the version below.

check   Run by the main agent at the top level of the worktree under review. Prints
        exactly one line: `PASS`, or `STOP <CODE>` (GIT, NO_RECORD, BAD_RECORD,
        VERSION, INTERNAL). Exit 0 only for PASS. Prints no value that it reads.
accept  Run only by the user in their own terminal. Refuses without a terminal on
        stdin and stdout (`STOP NO_TTY`). Shows the current record of the clone,
        prints the accepted text, reads the user's own words, and writes the
        record only after the exact answer `yes`.

Standard library only; no network; nothing on stderr.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile

ACCEPTANCE_VERSION = 2
KEYS = ("version", "decision", "date")
TIMEOUT = 20
HERE = os.path.dirname(os.path.realpath(__file__))
REFERENCE = os.path.join(HERE, "..", "references", "reviewer-acceptance.md")
ACCEPTED_HEADING = "## Accepted text"


class Stop(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def record_dir() -> str:
    home = os.path.expanduser("~")
    if not os.path.isabs(home) or os.path.realpath(home) == os.sep:
        raise Stop("NO_RECORD")  # a relative or root home is not the user's home folder
    return os.path.join(home, ".claude", "dev-skills", "reviewer-acceptance")


def clone_id() -> str:
    """SHA-256 of the real path, st_dev and st_ino of the common Git directory of the cwd."""
    try:
        proc = subprocess.run(
            ["git", "--no-replace-objects", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            timeout=TIMEOUT, check=False)
    except (OSError, subprocess.SubprocessError):
        raise Stop("GIT")
    lines = proc.stdout.decode("utf-8", "strict").splitlines() if proc.returncode == 0 else []
    if proc.returncode != 0 or len(lines) != 1 or not os.path.isabs(lines[0]):
        raise Stop("GIT")
    real = os.path.realpath(lines[0])
    try:
        st = os.stat(real)
    except OSError:
        raise Stop("GIT")
    key = f"{real}\0{st.st_dev}\0{st.st_ino}".encode("utf-8", "surrogateescape")
    return hashlib.sha256(key).hexdigest()


def _no_duplicates(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate key")
    return dict(pairs)


def parse_record(raw: bytes) -> dict:
    try:
        data = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=_no_duplicates)
    except (UnicodeDecodeError, ValueError):
        raise Stop("BAD_RECORD")
    if not isinstance(data, dict) or set(data) != set(KEYS):
        raise Stop("BAD_RECORD")
    version, decision, date = data["version"], data["decision"], data["date"]
    if type(version) is not int:  # bool is an int subclass; reject it
        raise Stop("BAD_RECORD")
    if not isinstance(decision, str) or not decision.strip() or not isinstance(date, str) or not date.strip():
        raise Stop("BAD_RECORD")
    if version != ACCEPTANCE_VERSION:
        raise Stop("VERSION")
    return data


def read_record() -> dict:
    path = os.path.join(record_dir(), clone_id() + ".json")
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except FileNotFoundError:
        raise Stop("NO_RECORD")
    except OSError:
        raise Stop("BAD_RECORD")
    return parse_record(raw)


def check() -> str:
    read_record()
    return "PASS"


def existing_record_line() -> str:
    """What `accept` shows before it asks: the current record's date and words, never a path."""
    try:
        record = read_record()
    except Stop as stop:
        if stop.code == "NO_RECORD":
            return "This clone has no record yet."
        return f"This clone has a record that check does not accept ({stop.code}); a new record replaces it."
    return f"Current record of this clone ({record['date']}): {record['decision']}"


def accepted_text() -> str:
    try:
        with open(REFERENCE, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except OSError:
        raise Stop("NO_REFERENCE")
    start = next((i for i, line in enumerate(lines) if line.startswith(ACCEPTED_HEADING)), None)
    if start is None:
        raise Stop("NO_REFERENCE")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end]).rstrip("\n")


def decide(words: str, answer: str) -> bool:
    """The record is written only for non-empty words and the exact answer `yes`."""
    return bool(words.strip()) and answer.strip() == "yes"


def write_record(words: str) -> None:
    folder = record_dir()
    os.makedirs(folder, mode=0o700, exist_ok=True)
    target = os.path.join(folder, clone_id() + ".json")
    record = {"version": ACCEPTANCE_VERSION, "decision": words.strip(),
              "date": datetime.date.today().isoformat()}
    fd, tmp = tempfile.mkstemp(dir=folder, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(record, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.chmod(tmp, 0o600)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def accept() -> str:
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        raise Stop("NO_TTY")
    clone_id()  # fail before any prompt when this is not a Git clone
    print(existing_record_line())
    print()
    print(accepted_text())
    print()
    try:
        words = input("Your own words (your decision, in your words): ")
        answer = input("Type yes to accept, anything else to stop: ")
    except (EOFError, KeyboardInterrupt):
        raise Stop("DECLINED")
    if not decide(words, answer):
        raise Stop("DECLINED")
    write_record(words)
    return "ACCEPTED"


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in ("check", "accept"):
        print("STOP BAD_ARGS")
        return 2
    try:
        result = check() if argv[0] == "check" else accept()
    except Stop as stop:
        print(f"STOP {stop.code}")
        return 1
    except BaseException:  # every other failure becomes a code; nothing goes to stderr
        print("STOP INTERNAL")
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
