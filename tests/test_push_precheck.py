"""Tests for skills/dev-gate/scripts/push_precheck.py and the R-REV-9 scan commands (Issue #68, REQ-011).

Temporary repositories only, git config isolated (GIT_CONFIG_GLOBAL and
GIT_CONFIG_SYSTEM are /dev/null, HOME is a temporary directory), a bare
repository as the remote, real `git push --dry-run --porcelain`, no network.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "dev-gate", "scripts", "push_precheck.py")
NAME, EMAIL = "Test", "test@example.invalid"
MAIN = "refs/heads/main"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        home = os.path.join(self.tmp, "home")
        os.mkdir(home)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "XDG_CONFIG_HOME"}
        env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null", GIT_CONFIG_NOSYSTEM="1",
                   HOME=home, LC_ALL="C", TZ="UTC")
        self.env = env
        self.counter = 0

    def git(self, cwd, *args, stdin=None):
        p = subprocess.run(["git", *args], cwd=cwd, env=self.env, input=stdin, capture_output=True)
        if p.returncode != 0:
            self.fail(f"git {args} failed: {p.stderr!r}")
        return p.stdout

    def script(self, cwd, *args):
        p = subprocess.run([sys.executable, "-I", "-B", SCRIPT, *args], cwd=cwd, env=self.env, capture_output=True)
        out = p.stdout + p.stderr
        for value in (NAME, EMAIL, self.tmp):
            self.assertNotIn(value.encode(), out, "output carries an identity or a path")
        self.assertNotIn(b"Traceback", out)
        return p.returncode, p.stdout.decode()

    def init(self, name="work", fmt="sha1", remote=True):
        path = os.path.join(self.tmp, name)
        self.git(self.tmp, "init", "-q", "-b", "main", f"--object-format={fmt}", path)
        self.git(path, "config", "user.name", NAME)
        self.git(path, "config", "user.email", EMAIL)
        if remote:
            bare = os.path.join(self.tmp, name + "-remote.git")
            self.git(self.tmp, "init", "-q", "--bare", "-b", "main", f"--object-format={fmt}", bare)
            self.git(path, "remote", "add", "origin", bare)
        return path

    def write(self, repo, rel, data):
        path = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(data)

    def head(self, repo):
        return self.git(repo, "rev-parse", "HEAD").decode().strip()

    def plain_commit(self, repo, name):
        self.write(repo, name, f"{name}\n")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", f"plain {name}")
        return self.head(repo)

    def pushed_base(self, fmt="sha1"):
        """A repository whose root commit is on the remote main."""
        repo = self.init(fmt=fmt)
        base = self.plain_commit(repo, "a.txt")
        self.git(repo, "push", "-q", "--no-recurse-submodules", "origin", f"{MAIN}:{MAIN}")
        return repo, base

    def push_inputs(self, repo, *refspecs):
        p = subprocess.run(["git", "push", "--no-recurse-submodules", "--dry-run", "--porcelain", "origin", *refspecs],
                           cwd=repo, env=self.env, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        ids = sorted({line.split("\t")[0] for line in self.git(repo, "ls-remote", "--heads", "--tags", "origin")
                      .decode().splitlines() if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", line.split("\t")[0])})
        return self.files(p.stdout.decode(), "".join(i + "\n" for i in ids))

    def files(self, dry_text, ids_text):
        self.counter += 1
        dry = os.path.join(self.tmp, f"dry-run-{self.counter}.txt")
        rem = os.path.join(self.tmp, f"remote-ids-{self.counter}.txt")
        with open(dry, "w") as fh:
            fh.write(dry_text)
        with open(rem, "w") as fh:
            fh.write(ids_text)
        return dry, rem

    def verify(self, repo, *refspecs):
        dry, rem = self.push_inputs(repo, *refspecs)
        return self.script(repo, "verify", "--dry-run", dry, "--remote-ids", rem)

    def verify_text(self, repo, dry_text, ids_text):
        dry, rem = self.files(dry_text, ids_text)
        return self.script(repo, "verify", "--dry-run", dry, "--remote-ids", rem)


class PassingPush(Base):
    def assert_pass(self, rc, out, lines):
        self.assertEqual(rc, 0, out)
        self.assertEqual(out, f"R-REV-9 step 4a: checks passed for {lines} ref lines; steps 6 to 8 still run\n")

    def test_new_commits_branch_and_tag(self):
        for fmt in ("sha1", "sha256"):
            with self.subTest(fmt):
                self.tmp = os.path.realpath(tempfile.mkdtemp())
                self.addCleanup(shutil.rmtree, self.tmp)
                repo, _ = self.pushed_base(fmt)
                self.plain_commit(repo, "b.txt")
                self.git(repo, "tag", "-a", "-m", "release", "v1")
                rc, out = self.verify(repo, f"{MAIN}:{MAIN}", f"{MAIN}:refs/heads/topic", "refs/tags/v1:refs/tags/v1")
                self.assert_pass(rc, out, 3)

    def test_up_to_date_only(self):
        repo, _ = self.pushed_base()
        self.assert_pass(*self.verify(repo, f"{MAIN}:{MAIN}"), 1)


class VerifyStop(Base):
    def setUp(self):
        super().setUp()
        self.repo, self.base = self.pushed_base()
        self.tree = self.git(self.repo, "rev-parse", "HEAD^{tree}").decode().strip()

    def assert_stop(self, dry, ids, reason, repo=None):
        rc, out = self.verify_text(repo or self.repo, dry, ids)
        self.assertEqual(rc, 2, out)
        self.assertEqual(out, f"STOP {reason}\n")

    def test_bad_source_name(self):
        for src in ("refs/heads/a$(id)", "refs/heads/a b", "refs/heads/ä", "HEAD~1"):
            with self.subTest(src):
                self.assert_stop(f"To x\n*\t{src}:refs/heads/x\t[new branch]\nDone\n", "", "name")
        self.assert_stop(f"*\t{MAIN}:refs/heads/a$(id)\t[new branch]\n", "", "name")

    def test_source_kind(self):
        for src in ("HEAD", "refs/remotes/origin/main", "refs/worktree/x", self.base[:12]):
            with self.subTest(src):
                self.assert_stop(f"*\t{src}:refs/heads/x\t[new branch]\n", "", "source")
        self.assert_stop(f"*\t{self.tree}:refs/heads/x\t[new branch]\n", "", "source-type")
        tag_of_tree = self.git(self.repo, "mktag", stdin=(
            f"object {self.tree}\ntype tree\ntag t\ntagger {NAME} <{EMAIL}> 0 +0000\n\nm\n").encode()).decode().strip()
        self.git(self.repo, "update-ref", "refs/tags/t", tag_of_tree)
        self.assert_stop("*\trefs/tags/t:refs/tags/t\t[new tag]\n", "", "source-type")
        self.assert_stop("*\trefs/heads/nope:refs/heads/x\t[new branch]\n", "", "git cat-file failed (exit 128)")

    def test_force_delete_and_rejected_lines(self):
        self.assert_stop(f"+\t{MAIN}:{MAIN}\t{self.base[:7]}...{self.base[:7]} (forced update)\n",
                         self.base + "\n", "force-or-delete")
        self.assert_stop(f"-\t:{MAIN}\t[deleted]\n", self.base + "\n", "force-or-delete")
        self.assert_stop(f"!\t{MAIN}:{MAIN}\t[rejected] (fetch first)\n", self.base + "\n", "rejected")

    def test_old_value_not_in_remote_ids(self):
        new = self.plain_commit(self.repo, "x.txt")
        for sep in ("..", "..."):
            with self.subTest(sep):
                self.assert_stop(f" \t{MAIN}:{MAIN}\tdeadbee{sep}{new[:7]}\n", self.base + "\n", "old-value")

    def test_bad_remote_id(self):
        line = f"*\t{MAIN}:refs/heads/x\t[new branch]\n"
        for ids in ("xyz\n", self.base[:39] + "\n", self.base.upper() + "\n", "\n", self.base + "\n\n",
                    self.base + "0" * 24 + "\n"):
            with self.subTest(ids):
                self.assert_stop(line, ids, "remote-id")

    def test_bad_ref_lines(self):
        self.assert_stop("To x\nDone\n", "", "no-ref-line")
        self.assert_stop(f"*\t{MAIN}:a:b\t[new branch]\n", "", "refspec")
        self.assert_stop(f"*\t{MAIN}\t[new branch]\n", "", "refspec")
        self.assert_stop(f"?\t{MAIN}:{MAIN}\t[new branch]\n", "", "flag")

    def test_bad_input_files(self):
        dry, rem = self.files(f"*\t{MAIN}:refs/heads/x\t[new branch]\n", "")
        link = os.path.join(self.tmp, "link.txt")
        os.symlink(dry, link)
        for args in (["--dry-run", os.path.join(self.tmp, "missing"), "--remote-ids", rem],
                     ["--dry-run", link, "--remote-ids", rem], ["--dry-run", self.tmp, "--remote-ids", rem]):
            with self.subTest(args):
                rc, out = self.script(self.repo, "verify", *args)
                self.assertEqual((rc, out), (2, "STOP input file unreadable\n"))
        with open(dry, "wb") as fh:
            fh.write(b"*\trefs/heads/\xff:refs/heads/x\t[new branch]\n")
        rc, out = self.script(self.repo, "verify", "--dry-run", dry, "--remote-ids", rem)
        self.assertEqual((rc, out), (2, "STOP input file not UTF-8\n"))

    def test_help_is_no_pass(self):
        for args in (["-h"], ["verify", "-h"], ["verify", "--help"]):
            rc, _ = self.script(self.tmp, *args)
            self.assertNotEqual(rc, 0, args)

    def test_not_a_repository(self):
        outside = os.path.join(self.tmp, "outside")
        os.mkdir(outside)
        env = dict(self.env, GIT_CEILING_DIRECTORIES=self.tmp)
        dry, rem = self.files(f"*\t{MAIN}:refs/heads/x\t[new branch]\n", "")
        p = subprocess.run([sys.executable, "-I", "-B", SCRIPT, "verify", "--dry-run", dry, "--remote-ids", rem],
                           cwd=outside, env=env, capture_output=True)
        self.assertEqual((p.returncode, p.stdout), (2, b"STOP git rev-parse failed (exit 128)\n"))

    def test_unexpected_error_stops(self):
        wrap = ("import importlib.util, sys\n"
                "spec = importlib.util.spec_from_file_location('push_precheck', sys.argv[1])\n"
                "m = importlib.util.module_from_spec(spec)\n"
                "spec.loader.exec_module(m)\n"
                "def boom(*a, **k):\n"
                "    raise RuntimeError('boom /private/path')\n"
                "m.read_text = boom\n"
                "sys.exit(m.main(sys.argv[2:]))\n")
        cache = os.path.join(os.path.dirname(SCRIPT), "__pycache__")
        before = sorted(os.listdir(cache)) if os.path.isdir(cache) else None
        dry, rem = self.push_inputs(self.repo, f"{MAIN}:{MAIN}")
        p = subprocess.run([sys.executable, "-I", "-B", "-c", wrap, SCRIPT, "verify", "--dry-run", dry,
                            "--remote-ids", rem], cwd=self.repo, env=self.env, capture_output=True)
        self.assertEqual((p.returncode, p.stdout, p.stderr), (2, b"STOP error\n", b""))
        self.assertEqual(sorted(os.listdir(cache)) if os.path.isdir(cache) else None, before)  # no bytecode


def rule_command(pattern):
    """A backtick command of R-REV-9 in skills/dev-core/SKILL.md."""
    with open(os.path.join(ROOT, "skills", "dev-core", "SKILL.md"), encoding="utf-8") as fh:
        found = re.findall(pattern, fh.read())
    assert len(found) == 1, (pattern, found)
    return found[0]


class RuleCommands(Base):
    """The exact commands of R-REV-9 step 8 and the range scan, taken from dev-core (card I68-R1-C1a)."""

    def bash(self, repo, command):
        p = subprocess.run(["bash", "-c", command], cwd=repo, env=self.env, capture_output=True)
        return p.returncode, p.stdout

    def gitlink_repo(self):
        repo = self.init(remote=False)
        self.git(repo, "config", "diff.ignoreSubmodules", "all")
        self.write(repo, "a.txt", "a\n")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", "base")
        base = self.head(repo)
        self.git(repo, "update-index", "--add", "--cacheinfo", f"160000,{base},sub")
        self.git(repo, "commit", "-q", "-m", "gitlink")
        return repo, base

    def test_step8_and_range_show_ignored_gitlink(self):
        repo, base = self.gitlink_repo()
        head = self.head(repo)
        step8 = rule_command(r"`(printf '%s\\n' <IDs> \| git [^`]*--stdin '<source>')`")
        ranged = rule_command(r"`(git --no-replace-objects -c core.quotePath=false log [^`]*'<base>\.\.<head>')`")
        commands = {"step 8": step8.replace("<IDs>", base).replace("'<source>'", f"'{MAIN}'"),
                    "range": ranged.replace("'<base>..<head>'", f"'{base}..{head}'")}
        marker = b"Subproject commit " + base.encode()
        for label, command in commands.items():
            with self.subTest(label):
                self.assertIn("--ignore-submodules=none", command)
                rc, out = self.bash(repo, command)
                self.assertEqual(rc, 0, out)
                self.assertIn(marker, out)
                self.assertIn(head.encode(), out)
                rc, control = self.bash(repo, command.replace(" --ignore-submodules=none", ""))
                self.assertEqual(rc, 0)
                self.assertNotIn(marker, control)  # the setting hides it without the option


    def test_commit_scan_commands_show_ignored_gitlink(self):
        """The commit-scan view (dev-core) and hash command (dev-gate step 1) show a staged gitlink (S4-002)."""
        repo = self.init(remote=False)
        self.git(repo, "config", "diff.ignoreSubmodules", "all")
        self.git(repo, "config", "diff.submodule", "log")
        self.write(repo, "a.txt", "a\n")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", "base")
        base = self.head(repo)
        self.git(repo, "update-index", "--add", "--cacheinfo", f"160000,{base},sub")
        view = rule_command(r"`(git --no-replace-objects -c core.quotePath=false diff --cached [^`]*)`")
        with open(os.path.join(ROOT, "skills", "dev-gate", "SKILL.md"), encoding="utf-8") as fh:
            found = re.findall(r"`(git --no-replace-objects diff --cached [^`]*)`", fh.read())
        self.assertEqual(len(found), 1, found)
        marker = b"Subproject commit " + base.encode()
        for label, command in {"view": view, "hash": found[0]}.items():
            with self.subTest(label):
                self.assertIn("--ignore-submodules=none --submodule=short", command)
                rc, out = self.bash(repo, command)
                self.assertEqual(rc, 0, out)
                self.assertIn(marker, out)
                rc, control = self.bash(repo, command.replace(" --ignore-submodules=none", ""))
                self.assertEqual(rc, 0)
                self.assertNotIn(marker, control)  # the setting hides it without the option

if __name__ == "__main__":
    unittest.main()
