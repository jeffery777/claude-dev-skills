#!/usr/bin/env python3
"""Read back a GitHub provider profile for the dev-gate merge gate (stdlib only).

Usage:
  platform_profile.py --repo-dir DIR --repo OWNER/NAME --pr N --base SHA --head SHA [--pack-dir DIR]

The profile is `platform_profile` in `.dev/config.json` at the bound base
commit; the PR head and the working tree are never read for it. The format and
the rules are in skills/dev-gate/references/platform-profile.md (REQ-021).
This script makes read calls only (`git`, `gh api` GET). It implements only the
properties listed there; a new edge case goes to the user as a REQ-GAP (R-REV-3).

Output: one line per item, then `platform_enforcement: <RESULT>`, the policy
change line and the FU-008 lines. Exit 0 for VERIFIED or NOT_CONFIGURED,
1 for UNVERIFIED or BLOCKED, 2 for bad arguments.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
from typing import Any

CONFIG_PATH = ".dev/config.json"
TOP_KEYS = {"requirements_dir", "commit_state", "platform_profile"}
PROFILE_KEYS = {"provider", "repository", "base_branch", "required_checks"}
CHECK_KEYS = {"name", "app_id"}
REPO_RE = re.compile(r"[A-Za-z0-9-]+/(?!\.\.?\Z)[A-Za-z0-9._-]+")
SHA_RE = re.compile(r"[0-9a-f]{40}")
PR_RE = re.compile(r"[0-9]+")
# FU-008: files that define or feed the checks (a hint, never complete).
CHECK_PATHS = (".github/", ".dev/config.json", "scripts/", "tests/",
               ".gitleaks.toml", ".gitleaksignore", ".gitattributes")
ORDER = {"BLOCKED": 2, "UNVERIFIED": 1, "VERIFIED": 0}


class ConfigError(ValueError):
    pass


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ConfigError(f"duplicate key {key!r}")
        seen[key] = value
    return seen


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def parse_config(text: str) -> dict[str, Any] | None:
    """The profile, or None when no profile is selected. Raises ConfigError."""
    try:
        data = json.loads(text, object_pairs_hook=_no_duplicates)
    except ConfigError:
        raise
    except ValueError as exc:
        raise ConfigError(f"invalid JSON: {exc}") from None
    if not isinstance(data, dict):
        raise ConfigError("the top level must be a JSON object")
    unknown = sorted(set(data) - TOP_KEYS)
    if unknown:
        raise ConfigError(f"unknown key(s): {', '.join(unknown)}")
    if "platform_profile" not in data:
        return None
    profile = data["platform_profile"]
    if not isinstance(profile, dict):
        raise ConfigError("platform_profile must be an object")
    if set(profile) != PROFILE_KEYS:
        missing = sorted(PROFILE_KEYS - set(profile))
        extra = sorted(set(profile) - PROFILE_KEYS)
        raise ConfigError(f"platform_profile keys: missing {missing}, unknown {extra}")
    if profile["provider"] != "github":
        raise ConfigError("provider must be \"github\"")
    if not isinstance(profile["repository"], str) or not REPO_RE.fullmatch(profile["repository"]):
        raise ConfigError("repository must be \"owner/name\"")
    if not isinstance(profile["base_branch"], str) or not profile["base_branch"]:
        raise ConfigError("base_branch must be a non-empty string")
    checks = profile["required_checks"]
    if not isinstance(checks, list) or not checks:
        raise ConfigError("required_checks must be a non-empty list")
    names = set()
    for check in checks:
        if not isinstance(check, dict) or set(check) != CHECK_KEYS:
            raise ConfigError("each required check must have exactly name and app_id")
        if not isinstance(check["name"], str) or not check["name"]:
            raise ConfigError("check name must be a non-empty string")
        if not _positive_int(check["app_id"]):
            raise ConfigError(f"check {check['name']!r}: app_id must be a positive integer")
        if check["name"] in names:
            raise ConfigError(f"duplicate check name {check['name']!r}")
        names.add(check["name"])
    return profile


def _pin(value: Any) -> int | None:
    return value if _positive_int(value) else None


def platform_required(rule_pages: list[Any], branch: dict[str, Any]) -> dict[str, set[int | None]]:
    """Required check name -> pins, from every ruleset rule page and classic protection."""
    required: dict[str, set[int | None]] = {}
    for page in rule_pages:
        if not isinstance(page, list):
            raise ValueError("rules page is not a list")
        for rule in page:
            if rule.get("type") != "required_status_checks":
                continue
            for item in rule["parameters"]["required_status_checks"]:
                required.setdefault(item["context"], set()).add(_pin(item.get("integration_id")))
    classic = (branch.get("protection") or {}).get("required_status_checks") or {}
    for item in classic.get("checks") or []:
        required.setdefault(item["context"], set()).add(_pin(item.get("app_id")))
    for name in classic.get("contexts") or []:
        required.setdefault(name, set()).add(None)
    return required


def evaluate(profile: dict[str, Any], bound: dict[str, str], pr: dict[str, Any],
             platform: dict[str, set[int | None]], run_pages: list[Any],
             head_after: str) -> list[tuple[str, str]]:
    """Items (status, message). Pure: all inputs are already read."""
    items: list[tuple[str, str]] = []
    base_repo = pr["base"]["repo"]["full_name"]
    if base_repo.lower() != profile["repository"].lower():
        items.append(("BLOCKED", f"PR base repository {base_repo} is not {profile['repository']}"))
    if pr["base"]["ref"] != profile["base_branch"]:
        items.append(("BLOCKED", f"PR base branch {pr['base']['ref']} is not {profile['base_branch']}"))
    if pr["base"]["sha"] != bound["base"]:
        items.append(("UNVERIFIED", f"PR base {pr['base']['sha']} is not the bound base {bound['base']}"))
    if pr["head"]["sha"] != bound["head"]:
        items.append(("UNVERIFIED", f"PR head {pr['head']['sha']} is not the reviewed head {bound['head']}"))

    wanted: set[tuple[str, int]] = set()
    profile_names = set()
    for check in profile["required_checks"]:
        name, app_id = check["name"], check["app_id"]
        profile_names.add(name)
        if name not in platform:
            items.append(("BLOCKED", f"{name}: in the profile but not required by the platform"))
        else:
            for pin in platform[name]:
                if pin is not None and pin != app_id:
                    items.append(("BLOCKED", f"{name}: platform app id {pin} is not profile app id {app_id}"))
        wanted.add((name, app_id))
    for name, pins in sorted(platform.items()):
        for pin in pins:
            if pin is not None:
                wanted.add((name, pin))
            elif name not in profile_names:
                items.append(("UNVERIFIED", f"{name}: required by the platform, source not pinned; add it to the profile"))

    runs = []
    for page in run_pages:
        runs.extend(page["check_runs"])
    for name, app_id in sorted(wanted):
        matching = [r for r in runs if r["head_sha"] == bound["head"] and r["name"] == name
                    and (r.get("app") or {}).get("id") == app_id]
        if not matching:
            items.append(("UNVERIFIED", f"{name} (app {app_id}): no check run on the head"))
            continue
        newest: dict[Any, dict[str, Any]] = {}
        for run in matching:
            suite = (run.get("check_suite") or {}).get("id")
            if suite not in newest or run["id"] > newest[suite]["id"]:
                newest[suite] = run
        for suite, run in sorted(newest.items(), key=lambda kv: str(kv[0])):
            if run["status"] != "completed":
                items.append(("UNVERIFIED", f"{name} (app {app_id}, suite {suite}): {run['status']}"))
            elif run["conclusion"] != "success":
                items.append(("BLOCKED", f"{name} (app {app_id}, suite {suite}): {run['conclusion']}"))
            else:
                items.append(("VERIFIED", f"{name} (app {app_id}, suite {suite}): success"))
    if head_after != bound["head"]:
        items.append(("UNVERIFIED", f"PR head changed during the read-back to {head_after}"))
    return items


def overall(items: list[tuple[str, str]]) -> str:
    if not items:
        return "UNVERIFIED"
    return max((status for status, _ in items), key=ORDER.__getitem__)


def check_path_changes(names: list[str], pack_prefix: str | None) -> list[str]:
    """Changed files under CHECK_PATHS or the pack directory ("" = the whole repository)."""
    if pack_prefix == "":
        return list(names)
    prefixes = CHECK_PATHS + ((pack_prefix,) if pack_prefix else ())
    return [n for n in names if any(n == p or (p.endswith("/") and n.startswith(p)) for p in prefixes)]


# ---- reading (git and gh, read-only) ----

def _run(args: list[str], cwd: str, binary: bool = False) -> tuple[int, Any]:
    env = dict(os.environ, LC_ALL="C")
    proc = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=not binary)
    return proc.returncode, proc.stdout


def read_config(repo_dir: str, commit: str) -> tuple[str, bytes | None]:
    """("ok", bytes) | ("absent", None) | ("unreadable", None) at a commit; repo_dir is the top level."""
    if _run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], repo_dir)[0] != 0:
        return "unreadable", None
    rc, out = _run(["git", "ls-tree", "--name-only", commit, "--", CONFIG_PATH], repo_dir)
    if rc != 0:
        return "unreadable", None
    if not out.strip():
        return "absent", None
    rc, out = _run(["git", "cat-file", "blob", f"{commit}:{CONFIG_PATH}"], repo_dir, binary=True)
    return ("ok", out) if rc == 0 else ("unreadable", None)


def blob_id(repo_dir: str, commit: str) -> str:
    state, _ = read_config(repo_dir, commit)
    if state != "ok":
        return state
    rc, out = _run(["git", "rev-parse", f"{commit}:{CONFIG_PATH}"], repo_dir)
    return out.strip() if rc == 0 else "unreadable"


def gh(path: str, repo_dir: str, paginate: bool = False) -> Any:
    args = ["gh", "api", "--hostname", "github.com"]
    if paginate:
        args += ["--paginate", "--slurp"]
    rc, out = _run(args + [path], repo_dir)
    if rc != 0:
        raise RuntimeError(f"gh api {path.split('?')[0]} failed")
    return json.loads(out)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-dir", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--pr", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("--pack-dir")
    a = ap.parse_args(argv)
    if not (REPO_RE.fullmatch(a.repo) and PR_RE.fullmatch(a.pr) and SHA_RE.fullmatch(a.base) and SHA_RE.fullmatch(a.head)):
        print("bad arguments: --repo owner/name, --pr digits, --base and --head 40 hex", file=sys.stderr)
        return 2
    rc, top = _run(["git", "rev-parse", "--show-toplevel"], os.path.realpath(a.repo_dir))
    if rc != 0 or not top.strip():
        print(f"UNVERIFIED: {a.repo_dir} is not inside a git repository")
        print("platform_enforcement: UNVERIFIED")
        return 1
    repo_dir = os.path.realpath(top.strip())
    bound = {"base": a.base, "head": a.head}

    def inside(path: str) -> bool:
        return os.path.commonpath([os.path.realpath(path), repo_dir]) == repo_dir

    items: list[tuple[str, str]] = []
    if inside(__file__):
        items.append(("UNVERIFIED", "this checker runs from the repository under review; run the copy from the bound base"))

    state, text = read_config(repo_dir, a.base)
    profile = None
    if state == "unreadable":
        items.append(("UNVERIFIED", f"cannot read {CONFIG_PATH} at the bound base {a.base}"))
    elif state == "ok":
        try:
            profile = parse_config((text or b"").decode("utf-8"))
        except UnicodeDecodeError:
            items.append(("BLOCKED", f"{CONFIG_PATH} at the bound base: invalid JSON: not UTF-8"))
        except ConfigError as exc:
            items.append(("BLOCKED", f"{CONFIG_PATH} at the bound base: {exc}"))

    base_blob, head_blob = blob_id(repo_dir, a.base), blob_id(repo_dir, a.head)
    policy = "no" if base_blob == head_blob and base_blob != "unreadable" else \
        f"yes ({CONFIG_PATH} base {base_blob}, head {head_blob}) - decision card for the user (R-AUTH-2)"

    if profile is None and not items:
        print("platform_enforcement: NOT_CONFIGURED")
        print(f"policy change: {policy}")
        return 0

    if profile is not None:
        if profile["repository"].lower() != a.repo.lower():
            items.append(("BLOCKED", f"profile repository {profile['repository']} is not the bound repository {a.repo}"))
        else:
            r = profile["repository"]
            branch = urllib.parse.quote(profile["base_branch"], safe="")
            try:
                pr = gh(f"repos/{r}/pulls/{a.pr}", repo_dir)
                platform = platform_required(
                    gh(f"repos/{r}/rules/branches/{branch}?per_page=100", repo_dir, paginate=True),
                    gh(f"repos/{r}/branches/{branch}", repo_dir))
                runs = gh(f"repos/{r}/commits/{a.head}/check-runs?filter=all&per_page=100", repo_dir, paginate=True)
                head_after = gh(f"repos/{r}/pulls/{a.pr}", repo_dir)["head"]["sha"]
                items.extend(evaluate(profile, bound, pr, platform, runs, head_after))
            except (RuntimeError, ValueError, KeyError, TypeError, AttributeError) as exc:
                items.append(("UNVERIFIED", f"read-back failed: {exc}"))

    pack_prefix = None
    if a.pack_dir and inside(a.pack_dir):
        rel = os.path.relpath(os.path.realpath(a.pack_dir), repo_dir)
        pack_prefix = "" if rel == "." else rel.rstrip("/") + "/"
    rc, out = _run(["git", "diff", "--name-only", "--no-renames", "-z", f"{a.base}...{a.head}"], repo_dir)
    changed = None
    if rc != 0:
        items.append(("UNVERIFIED", f"git diff {a.base}...{a.head} failed"))
    else:
        changed = check_path_changes([n for n in out.split("\0") if n], pack_prefix)

    for status, message in items:
        print(f"{status}: {message}")
    result = overall(items)
    note = " (checks ran this PR's own definitions)" if result == "VERIFIED" else ""
    print(f"platform_enforcement: {result}{note}")
    print(f"policy change: {policy}")
    if changed is not None:
        print("checks changed by this PR: " + (", ".join(changed) if changed else "none in the listed paths"))
    return 0 if result == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
