#!/usr/bin/env python3
"""Verify vendor/engineering-workflow-core against its lock file (D-001).

Checks every file digest and size, that no file is missing or extra, and both
set digests (algorithm utf8-path-tab-sha256-lf/v1: UTF-8 byte-sorted paths,
"path<TAB>sha256<LF>" lines, SHA-256 of the concatenation). Symlinks under
vendor/ are rejected. OS metadata files (.DS_Store, Thumbs.db) are ignored and
reported.

Integrity only: the lock lives in this repository, so a match proves the
vendored bytes equal the lock, not that they equal upstream. Compare against
the upstream tag with --upstream <clone> when the vendor or lock changes. A
match proves neither trust nor authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDOR = os.path.join(ROOT, "vendor", "engineering-workflow-core")
LOCK = os.path.join(ROOT, "vendor", "engineering-workflow-core.lock.json")
IGNORED = {".DS_Store", "Thumbs.db"}


def set_digest(entries: list[tuple[str, str]]) -> str:
    entries = sorted(entries, key=lambda e: e[0].encode("utf-8"))
    return hashlib.sha256("".join(f"{p}\t{h}\n" for p, h in entries).encode("utf-8")).hexdigest()


def upstream_files(clone: str, revision: str) -> dict[str, str]:
    """Path -> sha256 of every file in the upstream clone at the locked revision."""
    out = subprocess.run(["git", "-C", clone, "ls-tree", "-r", "-z", "--name-only", revision],
                         check=True, capture_output=True).stdout
    names = [n.decode("utf-8") for n in out.split(b"\0") if n]
    result = {}
    for name in names:
        blob = subprocess.run(["git", "-C", clone, "show", f"{revision}:{name}"], check=True, capture_output=True).stdout
        result[name] = hashlib.sha256(blob).hexdigest()
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify the vendored Core against its lock.")
    parser.add_argument("--upstream", metavar="CLONE", help="clone of engineering-workflow-core to compare with")
    try:
        args = parser.parse_args(argv or [])
    except SystemExit as exc:
        return 2 if exc.code else 0
    upstream = args.upstream
    with open(LOCK, encoding="utf-8") as fh:
        lock = json.load(fh)
    errors = []
    notes = []
    actual: dict[str, tuple[str, int]] = {}
    for path in (os.path.dirname(VENDOR), VENDOR):
        if os.path.islink(path):
            errors.append(f"symlink not allowed: {path}")
    for dirpath, dirs, files in os.walk(VENDOR):
        for name in dirs + files:
            if os.path.islink(os.path.join(dirpath, name)):
                errors.append(f"symlink not allowed: {os.path.relpath(os.path.join(dirpath, name), VENDOR)}")
        for name in files:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, VENDOR).replace(os.sep, "/")
            if name in IGNORED:
                notes.append(f"ignored OS metadata file: {rel}")
                continue
            if os.path.islink(full):
                continue
            with open(full, "rb") as fh:
                data = fh.read()
            actual[rel] = (hashlib.sha256(data).hexdigest(), len(data))
    locked = {f["path"]: (f["sha256"], f["size_bytes"]) for f in lock["files"]}
    for path in sorted(locked.keys() - actual.keys()):
        errors.append(f"missing: {path}")
    for path in sorted(actual.keys() - locked.keys()):
        errors.append(f"not in lock: {path}")
    for path in sorted(locked.keys() & actual.keys()):
        if locked[path] != actual[path]:
            errors.append(f"digest or size mismatch: {path}")
    entries = [(p, h) for p, (h, _) in actual.items()]
    digests = lock["set_digests"]
    if set_digest([e for e in entries if e[0] != "LICENSE"]) != digests["markdown_only"]:
        errors.append("markdown_only set digest mismatch")
    if set_digest(entries) != digests["all_files"]:
        errors.append("all_files set digest mismatch")
    src = lock["source"]
    if upstream:
        try:
            tagged = subprocess.run(["git", "-C", upstream, "rev-parse", f"refs/tags/{src['tag']}^{{commit}}"],
                                    check=True, capture_output=True, text=True).stdout.strip()
            if tagged != src["revision"]:
                errors.append(f"upstream tag {src['tag']} resolves to {tagged}, lock says {src['revision']}")
            tag_object = subprocess.run(["git", "-C", upstream, "rev-parse", f"refs/tags/{src['tag']}"],
                                        check=True, capture_output=True, text=True).stdout.strip()
            if src.get("tag_object") and tag_object != src["tag_object"]:
                errors.append(f"upstream tag object {tag_object} differs from lock {src['tag_object']}")
            remote = upstream_files(upstream, src["revision"])
        except (OSError, subprocess.CalledProcessError) as exc:
            errors.append(f"cannot read upstream {src['revision']} from {upstream}: {exc}")
        else:
            for path in sorted(set(remote) | set(locked)):
                if remote.get(path) != locked.get(path, (None,))[0]:
                    errors.append(f"lock differs from upstream {src['tag']}: {path}")
            if not errors:
                notes.append(f"upstream match: {upstream} at {src['revision'][:12]}")
    for n in notes:
        print("  note: " + n)
    if errors:
        print("core vendor: FAIL")
        for e in errors:
            print("  - " + e)
        return 1
    print(f"core vendor: OK ({src['repository']} {src['tag']} {src['revision'][:12]}, {len(actual)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
