#!/usr/bin/env python3
"""Fingerprint local Git state so a read-only subagent can be checked (dev-core §8).

Run it before and after a read-only role (reviewer, explorer) that ran as a
general-purpose substitute. Any difference means the substitute changed local
state; discard its result and report it.

Covered: HEAD and the branch it names; all refs and the stash; the index
(staged content, modes and assume-unchanged/skip-worktree flags); tracked
working-tree changes, including the working-tree content of files flagged
assume-unchanged or skip-worktree; the paths, modes and contents of every untracked and
ignored file, including files inside untracked nested repositories; and the
common git directory's config, config.worktree, hooks/ and info/ (also for
linked worktrees). Diffs run with --no-ext-diff and --no-textconv.

Not covered, by design: effects outside this repository, such as a push,
comments on a forge, or writes to ~/.gitconfig or other folders. The brief
forbids them; compare `git ls-remote` before and after when that matters.

Usage: python3 tree_fingerprint.py [repo-dir]   (prints one SHA-256 line)
Exit codes: 0 ok, 2 not a git repository or git failed.
"""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import sys

GIT_ENV = {"GIT_OPTIONAL_LOCKS": "0"}  # never refresh the index while fingerprinting


def git(repo: str, *args: str, check: bool = True) -> bytes:
    env = dict(os.environ, **GIT_ENV)
    return subprocess.run(["git", "-C", repo, *args], check=check, capture_output=True, env=env).stdout


def entry_digest(path: str) -> str:
    st = os.lstat(path)
    if stat.S_ISLNK(st.st_mode):
        return f"link:{os.readlink(path)}"
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return f"{oct(st.st_mode)}:{h.hexdigest()}"


def walk(root: str):
    """Yield (relative path, digest) for every file and symlink below root, sorted."""
    if not os.path.lexists(root):
        return
    if not os.path.isdir(root) or os.path.islink(root):
        yield "", entry_digest(root)
        return
    for dirpath, dirs, files in os.walk(root):
        dirs.sort()
        for name in sorted(files + [d for d in dirs if os.path.islink(os.path.join(dirpath, d))]):
            full = os.path.join(dirpath, name)
            yield os.path.relpath(full, root), entry_digest(full)


def fingerprint(repo: str) -> str:
    h = hashlib.sha256()

    def add(label: str, data: bytes) -> None:
        h.update(label.encode() + b"\0" + hashlib.sha256(data).digest())

    add("head", git(repo, "rev-parse", "--verify", "-q", "HEAD", check=False))
    add("symbolic-head", git(repo, "symbolic-ref", "-q", "HEAD", check=False))
    add("refs", git(repo, "for-each-ref", "--format=%(refname) %(objectname)"))
    add("stash", git(repo, "stash", "list", "--format=%H", check=False))
    index = git(repo, "ls-files", "-s", "-v", "-z")  # no --debug: stat data changes on harmless index refreshes
    add("index", index)
    add("staged", git(repo, "diff", "--cached", "--binary", "--no-ext-diff", "--no-textconv"))
    add("worktree", git(repo, "diff", "--binary", "--no-ext-diff", "--no-textconv"))
    status = git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignored")
    add("status", status)
    top = git(repo, "rev-parse", "--show-toplevel").decode().strip()
    # Files flagged assume-unchanged (lowercase tag) or skip-worktree (S) are
    # hidden from diff and status, so hash their working-tree content directly.
    for entry in index.split(b"\0"):
        if entry and (entry[:1].islower() or entry[:1] == b"S"):
            rel = entry.split(b"\t", 1)[1].decode("utf-8", "surrogateescape")
            for sub, digest in walk(os.path.join(top, rel)):
                h.update(f"flagged:{rel}/{sub}\t{digest}\n".encode("utf-8", "surrogateescape"))
    for entry in status.split(b"\0"):
        if entry[:2] in (b"??", b"!!"):
            rel = entry[3:].decode("utf-8", "surrogateescape")
            for sub, digest in walk(os.path.join(top, rel)):
                h.update(f"{rel}/{sub}\t{digest}\n".encode("utf-8", "surrogateescape"))
    common = os.path.realpath(os.path.join(top, git(repo, "rev-parse", "--git-common-dir").decode().strip()))
    own = git(repo, "rev-parse", "--absolute-git-dir").decode().strip()
    for base in sorted({common, own}):
        for name in ("config", "config.worktree", "hooks", "info"):
            for sub, digest in walk(os.path.join(base, name)):
                h.update(f"{base}/{name}/{sub}\t{digest}\n".encode("utf-8", "surrogateescape"))
    return h.hexdigest()


if __name__ == "__main__":
    try:
        print(fingerprint(sys.argv[1] if len(sys.argv) > 1 else "."))
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"tree_fingerprint: cannot read git state: {exc}", file=sys.stderr)
        sys.exit(2)
