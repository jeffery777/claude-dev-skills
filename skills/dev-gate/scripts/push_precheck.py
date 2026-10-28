#!/usr/bin/env python3
"""Deterministic pre-check of R-REV-9 push step 4a (Issue #68, REQ-011; stdlib only).

Usage (run in the worktree of the dry-run, as `python3 -I`):
  push_precheck.py verify --dry-run FILE --remote-ids FILE

FILE of --dry-run is the saved output of the real push command with
`--dry-run --porcelain` added; FILE of --remote-ids is the step 6 ID list (one
full object ID per line). verify runs the source checks of step 7 on the
tab-separated ref lines: at least one ref line; one `:` per refspec; no `+`
(forced update), `-` (delete) or `!` (rejected) line; a known flag; for each
line except `=` (up to date), source and destination names of
[A-Za-z0-9._/-]+, a source that starts with refs/heads/ or refs/tags/ or is a
full object ID, an old value (`<old>..<new>` or `<old>...<new>`) that is the
start of a remote ID, and a source that is a commit or a tag whose target is a commit.

It does not replace any scan: steps 6 to 8 of R-REV-9 always run.

Every git call is `git --no-replace-objects ...` without a shell; a git error is
a STOP, never an empty result. Output carries only counts and reason codes.

Exit codes: 0 the checks passed; 2 `STOP <reason>` (a failed check, bad input,
a git error or an unexpected error): stop the push.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import subprocess
import sys

NAME_RE = re.compile(r"[A-Za-z0-9._/-]+")
ID_RE = {"sha1": re.compile(r"[0-9a-f]{40}"), "sha256": re.compile(r"[0-9a-f]{64}")}
OLD_NEW_RE = re.compile(r"([0-9a-f]+)\.\.\.?[0-9a-f]+")
PORCELAIN_FLAGS = {" ", "*", "="}


class Stop(Exception):
    pass


def git(*args: str) -> bytes:
    """stdout of `git --no-replace-objects <args>`; any nonzero exit raises Stop."""
    proc = subprocess.run(["git", "--no-replace-objects", *args], input=b"", capture_output=True,
                          env=dict(os.environ, LC_ALL="C"))
    if proc.returncode != 0:
        raise Stop(f"git {args[0]} failed (exit {proc.returncode})")
    return proc.stdout


def ascii_line(out: bytes) -> str:
    if not out.endswith(b"\n") or b"\n" in out[:-1]:
        raise Stop("unexpected git output")
    try:
        return out[:-1].decode("ascii")
    except UnicodeDecodeError:
        raise Stop("unexpected git output") from None


def read_text(path: str) -> str:
    """The UTF-8 text of a regular file (not a symlink)."""
    try:
        if not stat.S_ISREG(os.lstat(path).st_mode):
            raise Stop("input file unreadable")
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with open(fd, "rb") as fh:
            if not stat.S_ISREG(os.fstat(fh.fileno()).st_mode):
                raise Stop("input file unreadable")
            data = fh.read()
    except OSError:
        raise Stop("input file unreadable") from None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise Stop("input file not UTF-8") from None


def verify(dry_run: str, remote_ids_file: str) -> int:
    fmt = ascii_line(git("rev-parse", "--show-object-format"))
    if fmt not in ID_RE:
        raise Stop("unknown object format")
    rid = ID_RE[fmt]
    dry = read_text(dry_run)
    remote_ids = read_text(remote_ids_file).split("\n")
    if remote_ids[-1] == "":
        remote_ids.pop()
    if not all(rid.fullmatch(i) for i in remote_ids):
        raise Stop("remote-id")

    ref_lines = [line.split("\t") for line in dry.split("\n") if line.count("\t") >= 2]
    if not ref_lines:
        raise Stop("no-ref-line")
    sources: list[str] = []
    for f in ref_lines:
        flag, spec, summary = f[0], f[1], f[2]
        if spec.count(":") != 1:
            raise Stop("refspec")
        if flag in ("+", "-"):
            raise Stop("force-or-delete")
        if flag == "!":
            raise Stop("rejected")
        if flag not in PORCELAIN_FLAGS:
            raise Stop("flag")
        if flag == "=":
            continue
        src, dst = spec.split(":")
        if not NAME_RE.fullmatch(src) or not NAME_RE.fullmatch(dst):
            raise Stop("name")
        if not (src.startswith("refs/heads/") or src.startswith("refs/tags/") or rid.fullmatch(src)):
            raise Stop("source")
        m = OLD_NEW_RE.match(summary)
        if m and not any(i.startswith(m.group(1)) for i in remote_ids):
            raise Stop("old-value")
        sources.append(src)

    for src in sources:  # every name above is checked before it goes into a command
        kind = ascii_line(git("cat-file", "-t", src))
        if kind == "tag":
            lines = git("cat-file", "-p", src).split(b"\n")
            if len(lines) < 2 or lines[1] != b"type commit":
                raise Stop("source-type")
        elif kind != "commit":
            raise Stop("source-type")

    print(f"R-REV-9 step 4a: checks passed for {len(ref_lines)} ref lines; steps 6 to 8 still run")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], add_help=False)
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("verify", add_help=False)  # -h is no exit-0 pass
    p.add_argument("--dry-run", required=True)
    p.add_argument("--remote-ids", required=True)
    a = ap.parse_args(argv)
    try:
        return verify(a.dry_run, a.remote_ids)
    except Stop as exc:
        print(f"STOP {exc}")
        return 2
    except Exception:  # an unexpected error: never a pass, never a traceback (it can show paths)
        print("STOP error")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
