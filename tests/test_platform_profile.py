"""Tests for skills/dev-gate/scripts/platform_profile.py (REQ-021). Each property has a negative case."""

import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "dev-gate", "scripts", "platform_profile.py")
spec = importlib.util.spec_from_file_location("platform_profile", SCRIPT)
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

BASE, HEAD = "a" * 40, "b" * 40
REPO = "owner/repo"
PROFILE = {"provider": "github", "repository": REPO, "base_branch": "main",
           "required_checks": [{"name": "validate", "app_id": 15368}, {"name": "gitleaks", "app_id": 15368}]}


def cfg(**profile):
    return json.dumps({"platform_profile": dict(PROFILE, **profile)})


def pr(base_sha=BASE, head_sha=HEAD, ref="main", repo=REPO):
    return {"base": {"repo": {"full_name": repo}, "ref": ref, "sha": base_sha}, "head": {"sha": head_sha}}


def rule(*checks):
    return {"type": "required_status_checks",
            "parameters": {"required_status_checks": [{"context": n, "integration_id": i} for n, i in checks]}}


def run(name, conclusion="success", status="completed", app=15368, suite=1, rid=1, sha=HEAD):
    return {"id": rid, "name": name, "status": status, "conclusion": conclusion,
            "head_sha": sha, "app": {"id": app}, "check_suite": {"id": suite}}


PLATFORM = {"validate": {15368}, "gitleaks": {15368}}
GOOD_RUNS = [{"check_runs": [run("validate", rid=1), run("gitleaks", rid=2)]}]


def statuses(items):
    return sorted(s for s, _ in items)


class ParseConfig(unittest.TestCase):
    def test_valid_profile(self):
        self.assertEqual(pp.parse_config(cfg())["repository"], REPO)

    def test_no_profile_is_none(self):
        self.assertIsNone(pp.parse_config('{"commit_state": false, "requirements_dir": "docs/req"}'))

    def test_fail_closed(self):
        bad = {
            "invalid json": "{",
            "not an object": "[]",
            "unknown top-level key (typo)": '{"platform_profle": {}}',
            "duplicate top-level key": '{"platform_profile": {}, "platform_profile": {}}',
            "duplicate profile key": cfg()[:-2] + ', "provider": "github"}}',
            "unknown profile key": cfg(extra=1),
            "missing key": json.dumps({"platform_profile": {k: v for k, v in PROFILE.items() if k != "base_branch"}}),
            "provider not github": cfg(provider="gitlab"),
            "bad repository": cfg(repository="owner/repo/x"),
            "dot-segment repository": cfg(repository="owner/.."),
            "empty base branch": cfg(base_branch=""),
            "empty checks": cfg(required_checks=[]),
            "check without app_id": cfg(required_checks=[{"name": "validate"}]),
            "bool app_id": cfg(required_checks=[{"name": "validate", "app_id": True}]),
            "float app_id": cfg(required_checks=[{"name": "validate", "app_id": 1.5}]),
            "duplicate check name": cfg(required_checks=[{"name": "v", "app_id": 1}, {"name": "v", "app_id": 1}]),
            "profile not an object": '{"platform_profile": []}',
        }
        for label, text in bad.items():
            with self.subTest(label), self.assertRaises(pp.ConfigError):
                pp.parse_config(text)


class PlatformRequired(unittest.TestCase):
    def test_union_of_all_rule_pages_and_classic(self):
        branch = {"protection": {"required_status_checks": {
            "contexts": ["legacy"], "checks": [{"context": "classic", "app_id": 7}, {"context": "anyapp", "app_id": -1}]}}}
        got = pp.platform_required([[rule(("validate", 15368))], [{"type": "deletion"}, rule(("gitleaks", None))]], branch)
        self.assertEqual(got, {"validate": {15368}, "gitleaks": {None}, "legacy": {None}, "classic": {7}, "anyapp": {None}})

    def test_bad_page_raises(self):
        with self.assertRaises(ValueError):
            pp.platform_required([{"not": "a list"}], {})


class Evaluate(unittest.TestCase):
    def ev(self, profile=PROFILE, p=None, platform=PLATFORM, runs=GOOD_RUNS, head_after=HEAD):
        return pp.evaluate(profile, {"base": BASE, "head": HEAD}, p or pr(), platform, runs, head_after)

    def test_all_success_is_verified(self):
        items = self.ev()
        self.assertEqual(pp.overall(items), "VERIFIED")

    def test_only_success_passes(self):
        for conclusion in ("failure", "cancelled", "timed_out", "skipped", "neutral", "stale", "action_required", None):
            with self.subTest(conclusion):
                runs = [{"check_runs": [run("validate", conclusion=conclusion), run("gitleaks", rid=2)]}]
                self.assertEqual(pp.overall(self.ev(runs=runs)), "BLOCKED")

    def test_pending_is_unverified(self):
        runs = [{"check_runs": [run("validate", status="in_progress", conclusion=None), run("gitleaks", rid=2)]}]
        self.assertEqual(pp.overall(self.ev(runs=runs)), "UNVERIFIED")

    def test_missing_run_is_unverified(self):
        self.assertEqual(pp.overall(self.ev(runs=[{"check_runs": [run("validate")]}])), "UNVERIFIED")

    def test_precedence_blocked_over_unverified(self):
        runs = [{"check_runs": [run("validate", conclusion="failure")]}]  # gitleaks missing -> UNVERIFIED
        items = self.ev(runs=runs)
        self.assertIn("UNVERIFIED", statuses(items))
        self.assertEqual(pp.overall(items), "BLOCKED")

    def test_empty_items_never_verified(self):
        self.assertEqual(pp.overall([]), "UNVERIFIED")

    def test_other_app_or_other_head_does_not_count(self):
        for label, r in (("other app", run("validate", app=999)), ("other head", run("validate", sha="c" * 40))):
            with self.subTest(label):
                runs = [{"check_runs": [r, run("gitleaks", rid=2)]}]
                self.assertEqual(pp.overall(self.ev(runs=runs)), "UNVERIFIED")

    def test_duplicates_newest_per_suite_all_must_succeed(self):
        rerun_ok = [run("validate", conclusion="failure", rid=1), run("validate", rid=5), run("gitleaks", rid=2)]
        self.assertEqual(pp.overall(self.ev(runs=[{"check_runs": rerun_ok}])), "VERIFIED")
        other_suite_failed = [run("validate", rid=5), run("validate", conclusion="failure", suite=2, rid=3),
                              run("gitleaks", rid=2)]
        self.assertEqual(pp.overall(self.ev(runs=[{"check_runs": other_suite_failed}])), "BLOCKED")

    def test_runs_on_later_pages_are_read(self):
        runs = [{"check_runs": [run("validate")]}, {"check_runs": [run("gitleaks", rid=2)]}]
        self.assertEqual(pp.overall(self.ev(runs=runs)), "VERIFIED")

    def test_profile_check_not_required_by_platform_is_blocked(self):
        self.assertEqual(pp.overall(self.ev(platform={"validate": {15368}})), "BLOCKED")

    def test_platform_only_check_is_required(self):
        platform = dict(PLATFORM, extra={15368})
        self.assertEqual(pp.overall(self.ev(platform=platform)), "UNVERIFIED")  # no run for "extra"
        runs = [{"check_runs": GOOD_RUNS[0]["check_runs"] + [run("extra", rid=9)]}]
        self.assertEqual(pp.overall(self.ev(platform=platform, runs=runs)), "VERIFIED")

    def test_platform_only_unpinned_is_unverified(self):
        platform = dict(PLATFORM, extra={None})
        runs = [{"check_runs": GOOD_RUNS[0]["check_runs"] + [run("extra", rid=9)]}]
        self.assertEqual(pp.overall(self.ev(platform=platform, runs=runs)), "UNVERIFIED")

    def test_pin_mismatch_is_blocked(self):
        self.assertEqual(pp.overall(self.ev(platform={"validate": {42}, "gitleaks": {15368}})), "BLOCKED")

    def test_unpinned_platform_check_in_profile_uses_profile_pin(self):
        self.assertEqual(pp.overall(self.ev(platform={"validate": {None}, "gitleaks": {15368}})), "VERIFIED")

    def test_identity_mismatches(self):
        cases = {
            "other base repository": (pr(repo="fork/repo"), "BLOCKED"),
            "other base branch": (pr(ref="dev"), "BLOCKED"),
            "stale base": (pr(base_sha="c" * 40), "UNVERIFIED"),
            "other head": (pr(head_sha="c" * 40), "UNVERIFIED"),
        }
        for label, (p, want) in cases.items():
            with self.subTest(label):
                self.assertEqual(pp.overall(self.ev(p=p)), want)

    def test_head_moved_during_read_back(self):
        self.assertEqual(pp.overall(self.ev(head_after="c" * 40)), "UNVERIFIED")


class CheckPaths(unittest.TestCase):
    def test_listed_paths(self):
        names = [".github/workflows/ci.yml", "scripts/validate.sh", "tests/x.py", ".dev/config.json",
                 ".gitleaks.toml", "skills/dev-gate/SKILL.md", "README.md", "scriptsx/a"]
        self.assertEqual(pp.check_path_changes(names, None), names[:5])
        self.assertEqual(pp.check_path_changes(names, "skills/"), names[:6])


class Seq:
    """Successive answers for repeated reads of one endpoint."""

    def __init__(self, *values):
        self.values = list(values)

    def next(self):
        return self.values.pop(0) if len(self.values) > 1 else self.values[0]


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class Main(unittest.TestCase):
    """End to end with a real temporary git repository and a fake `gh api`."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.repo = os.path.join(self.tmp, "repo")
        os.makedirs(os.path.join(self.repo, ".dev"))
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "t")
        git(self.repo, "config", "user.email", "t@example.invalid")
        self.addCleanup(shutil.rmtree, self.tmp)

    def commit(self, files):
        for path, text in files.items():
            full = os.path.join(self.repo, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            if text is None:
                os.remove(full)
            else:
                with open(full, "w") as fh:
                    fh.write(text)
        git(self.repo, "add", "-A")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", "c")
        return git(self.repo, "rev-parse", "HEAD")

    def main(self, base, head, responses=None, repo=REPO, pack_dir=None):
        responses = responses or {}
        real_run = pp._run

        self.calls = []

        def fake_run(args, cwd, binary=False):
            if args[:1] != ["gh"]:
                return real_run(args, cwd, binary)
            self.calls.append(args)
            # Answer only a GET on github.com for the bound repository; anything else fails.
            path = args[-1]
            paginated = "/rules/branches/" in path or path.endswith("/check-runs?filter=all&per_page=100")
            expected = ["gh", "api", "--hostname", "github.com"] + (["--paginate", "--slurp"] if paginated else [])
            if args[:-1] != expected or not path.startswith(f"repos/{REPO}/"):
                return 1, ""
            for key, value in responses.items():
                if path.split("?")[0].endswith(key):
                    if isinstance(value, Seq):
                        value = value.next()
                    return (0, json.dumps(value)) if value is not None else (1, "")
            return 1, ""

        argv = ["--repo-dir", self.repo, "--repo", repo, "--pr", "7", "--base", base, "--head", head]
        if pack_dir:
            argv += ["--pack-dir", pack_dir]
        out = io.StringIO()
        with mock.patch.object(pp, "_run", fake_run), contextlib.redirect_stdout(out):
            code = pp.main(argv)
        return code, out.getvalue()

    def gh_ok(self, base, head):
        return {"pulls/7": pr(base, head), "rules/branches/main": [[rule(("validate", 15368), ("gitleaks", 15368))]],
                "branches/main": {"protection": {"enabled": False}},
                "check-runs": [{"check_runs": [run("validate", sha=head), run("gitleaks", rid=2, sha=head)]}]}

    def test_no_config_at_base_is_not_configured(self):
        base = self.commit({"README.md": "x"})
        code, out = self.main(base, base)
        self.assertEqual(code, 0)
        self.assertIn("platform_enforcement: NOT_CONFIGURED", out)
        self.assertIn("policy change: no", out)

    def test_profile_only_in_head_is_not_used_and_is_a_policy_change(self):
        base = self.commit({"README.md": "x"})
        head = self.commit({".dev/config.json": cfg()})
        code, out = self.main(base, head)
        self.assertIn("platform_enforcement: NOT_CONFIGURED", out)
        self.assertIn("policy change: yes", out)

    def test_working_tree_is_never_read(self):
        base = self.commit({"README.md": "x"})
        with open(os.path.join(self.repo, ".dev/config.json"), "w") as fh:
            fh.write("{")
        self.assertIn("NOT_CONFIGURED", self.main(base, base)[1])

    def test_missing_base_commit_is_unverified(self):
        base = self.commit({".dev/config.json": cfg()})
        code, out = self.main("c" * 40, base)
        self.assertEqual(code, 1)
        self.assertIn("platform_enforcement: UNVERIFIED", out)

    def test_invalid_config_at_base_is_blocked_with_message(self):
        base = self.commit({".dev/config.json": '{"platform_profle": {}}'})
        code, out = self.main(base, base)
        self.assertIn("BLOCKED: .dev/config.json at the bound base: unknown key(s): platform_profle", out)
        self.assertIn("platform_enforcement: BLOCKED", out)

    def test_verified_with_fu008_note_and_changed_paths(self):
        base = self.commit({".dev/config.json": cfg()})
        head = self.commit({"scripts/validate.sh": "true", "README.md": "y"})
        code, out = self.main(base, head, self.gh_ok(base, head))
        self.assertEqual(code, 0, out)
        self.assertIn("platform_enforcement: VERIFIED (checks ran this PR's own definitions)", out)
        self.assertIn("checks changed by this PR: scripts/validate.sh", out)
        self.assertIn("policy change: no", out)

    def test_rename_out_of_listed_paths_is_listed(self):
        base = self.commit({".dev/config.json": cfg(), ".github/workflows/ci.yml": "on: push"})
        os.makedirs(os.path.join(self.repo, "other"))
        git(self.repo, "mv", ".github/workflows/ci.yml", "other/ci.yml")
        head = self.commit({})
        out = self.main(base, head, self.gh_ok(base, head))[1]
        self.assertIn(".github/workflows/ci.yml", out)

    def test_head_profile_change_is_policy_change(self):
        base = self.commit({".dev/config.json": cfg()})
        head = self.commit({".dev/config.json": cfg(required_checks=[{"name": "validate", "app_id": 15368}])})
        out = self.main(base, head, self.gh_ok(base, head))[1]
        self.assertIn("policy change: yes", out)

    def test_bound_repository_mismatch_is_blocked(self):
        base = self.commit({".dev/config.json": cfg()})
        self.assertIn("platform_enforcement: BLOCKED", self.main(base, base, repo="other/repo")[1])

    def test_failed_read_is_unverified(self):
        base = self.commit({".dev/config.json": cfg()})
        responses = self.gh_ok(base, base)
        responses["rules/branches/main"] = None
        self.assertIn("platform_enforcement: UNVERIFIED", self.main(base, base, responses)[1])

    def test_checker_inside_repository_is_unverified(self):
        base = self.commit({"README.md": "x"})
        with mock.patch.object(pp, "__file__", os.path.join(self.repo, "platform_profile.py")):
            self.assertIn("platform_enforcement: UNVERIFIED", self.main(base, base)[1])

    def test_subdirectory_repo_dir_still_reads_the_profile(self):
        base = self.commit({".dev/config.json": cfg(), "docs/a.md": "x"})
        self.repo_root = self.repo
        responses = self.gh_ok(base, base)
        self.repo = os.path.join(self.repo_root, "docs")
        code, out = self.main(base, base, responses)
        self.assertNotIn("NOT_CONFIGURED", out)
        self.assertIn("platform_enforcement: VERIFIED", out)

    def test_calls_are_get_on_github_com_for_the_bound_repo_with_all_pages(self):
        base = self.commit({".dev/config.json": cfg()})
        code, out = self.main(base, base, self.gh_ok(base, base))
        self.assertEqual(code, 0, out)
        paths = [c[-1] for c in self.calls]
        self.assertTrue(all(c[:4] == ["gh", "api", "--hostname", "github.com"] for c in self.calls))
        self.assertFalse({"-X", "--method", "-f", "-F", "--field", "--raw-field", "--input"} & {a for c in self.calls for a in c})
        self.assertTrue(all(p.startswith(f"repos/{REPO}/") for p in paths))
        self.assertIn(f"repos/{REPO}/commits/{base}/check-runs?filter=all&per_page=100", paths)
        self.assertEqual(sum(p == f"repos/{REPO}/pulls/7" for p in paths), 2)  # head read again at the end

    def test_head_moved_after_check_runs(self):
        base = self.commit({".dev/config.json": cfg()})
        responses = self.gh_ok(base, base)
        responses["pulls/7"] = Seq(pr(base, base), pr(base, "c" * 40))
        self.assertIn("platform_enforcement: UNVERIFIED", self.main(base, base, responses)[1])

    def test_policy_change_names_both_blobs(self):
        base = self.commit({".dev/config.json": cfg()})
        base_blob = git(self.repo, "rev-parse", f"{base}:.dev/config.json")
        head = self.commit({".dev/config.json": cfg(base_branch="dev")})
        head_blob = git(self.repo, "rev-parse", f"{head}:.dev/config.json")
        out = self.main(base, head, self.gh_ok(base, head))[1]
        self.assertIn(f"policy change: yes (.dev/config.json base {base_blob}, head {head_blob})", out)

    def test_non_utf8_config_is_blocked(self):
        base = self.commit({})
        with open(os.path.join(self.repo, ".dev/config.json"), "wb") as fh:
            fh.write(b'{"commit_state": "\xff"}')
        base = self.commit({})
        out = self.main(base, base)[1]
        self.assertIn("invalid JSON: not UTF-8", out)
        self.assertIn("platform_enforcement: BLOCKED", out)

    def test_pack_dir_at_repository_root_lists_every_change(self):
        base = self.commit({".dev/config.json": cfg()})
        head = self.commit({"skills/x.md": "y"})
        out = self.main(base, head, self.gh_ok(base, head), pack_dir=self.repo)[1]
        self.assertIn("checks changed by this PR: skills/x.md", out)

    def test_bad_arguments(self):
        with contextlib.redirect_stderr(io.StringIO()):
            for repo, number, sha in (("a/b", "1;x", BASE), ("a/b", "\u0661", BASE), ("a/b\n", "1", BASE),
                                      ("a/..", "1", BASE), ("a/b", "1", BASE + "\n")):
                with self.subTest(repo=repo, pr=number):
                    self.assertEqual(pp.main(["--repo-dir", ".", "--repo", repo, "--pr", number, "--base", sha, "--head", HEAD]), 2)


class GateRuleText(unittest.TestCase):
    """The REQ-021 rules that live only in rule text: the Q5 and Q6 results are written once, in dev-core
    R-EXH-4, and dev-gate and its reference cite R-EXH-4; the Q8 host pin stays in dev-gate step 6 and
    its reference (REQ-022, card 4b)."""

    CORE_SENTENCE = ("when that read fails or shows another base or head, or the profile checker fails or prints no "
                     "result, it is UNVERIFIED")

    @staticmethod
    def text(*parts):
        with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
            return " ".join(fh.read().split())

    def test_dev_core_r_exh_4_names_base_head_and_checker_failure(self):  # MR-001, R2-001, Q5, Q6
        core = self.text("skills", "dev-core", "SKILL.md")
        self.assertEqual(core.count(self.CORE_SENTENCE), 1)

    def test_no_profile_read_checks_base_and_pins_host(self):  # Q5 (a), Q8 (a)
        gate = self.text("skills", "dev-gate", "SKILL.md")
        self.assertIn("gh pr view <pr> --repo github.com/<owner/name> --json baseRefOid,headRefOid,statusCheckRollup", gate)
        self.assertIn("Compare `baseRefOid` with the bound base and `headRefOid` with the reviewed head; R-EXH-4 gives "
                      "the result when the read fails or either differs", gate)
        ref = self.text("skills", "dev-gate", "references", "platform-profile.md")
        self.assertIn("(`gh pr view --repo github.com/<owner/name>`, user decision Q8 (a)). R-EXH-4 gives the result "
                      "when the PR's base is not the bound base", ref)

    def test_checker_failure_cites_r_exh_4(self):  # Q6 (a)
        gate = self.text("skills", "dev-gate", "SKILL.md")
        self.assertIn("A checker failure or a missing result line gives the result of R-EXH-4", gate)
        ref = self.text("skills", "dev-gate", "references", "platform-profile.md")
        self.assertIn("A checker failure or a missing `platform_enforcement:` line: the gate result follows R-EXH-4", ref)

    def test_no_restated_copy_outside_dev_core(self):
        for parts in (("skills", "dev-gate", "SKILL.md"), ("skills", "dev-gate", "references", "platform-profile.md")):
            text = self.text(*parts)
            self.assertNotIn("never `NOT_CONFIGURED`", text, parts)
            self.assertNotIn("is not the bound base is `UNVERIFIED`", text, parts)


if __name__ == "__main__":
    unittest.main()
