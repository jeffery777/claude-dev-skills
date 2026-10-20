"""Tests for skills/dev-core/scripts/tree_fingerprint.py."""

import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tf", os.path.join(ROOT, "skills", "dev-core", "scripts", "tree_fingerprint.py"))
tf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tf)

# Isolate the tests from the user's global and system git configuration.
ENV = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}


@unittest.skipUnless(shutil.which("git"), "git not installed")
class Fingerprint(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in ENV}
        os.environ.update(ENV)
        self.repo = tempfile.mkdtemp()
        self.git("init", "-q")
        self.write("tracked.txt", "v1\n")
        self.git("add", "tracked.txt")
        self.git("-c", "commit.gpgsign=false", "commit", "-q", "-m", "init")
        os.makedirs(os.path.join(self.repo, "notes"))
        self.write("notes/review.md", "MUST-FIX open\n")
        self.write(".gitignore", "build/\n")
        os.makedirs(os.path.join(self.repo, "build"))
        self.write("build/out.txt", "a\n")
        self.base = tf.fingerprint(self.repo)

    def tearDown(self):
        shutil.rmtree(self.repo)
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def git(self, *args, cwd=None):
        subprocess.run(["git", "-C", cwd or self.repo, *args], check=True, capture_output=True)

    def write(self, rel, text, base=None):
        with open(os.path.join(base or self.repo, rel), "w", encoding="utf-8") as fh:
            fh.write(text)

    def changed(self):
        return tf.fingerprint(self.repo) != self.base

    def test_stable(self):
        self.assertFalse(self.changed())

    def test_untracked_edit(self):
        self.write("notes/review.md", "Fixed\n")
        self.assertTrue(self.changed())

    def test_ignored_edit(self):
        self.write("build/out.txt", "b\n")
        self.assertTrue(self.changed())

    def test_mode_change(self):
        os.chmod(os.path.join(self.repo, "notes", "review.md"), 0o755)
        self.assertTrue(self.changed())

    def test_hook_and_info(self):
        os.makedirs(os.path.join(self.repo, ".git", "hooks", "sub"), exist_ok=True)
        self.write(".git/hooks/sub/a", "x\n")
        self.assertTrue(self.changed())

    def test_info_attributes(self):
        os.makedirs(os.path.join(self.repo, ".git", "info"), exist_ok=True)
        self.write(".git/info/attributes", "* filter=x\n")
        self.assertTrue(self.changed())

    def test_staged_swap(self):
        self.write("tracked.txt", "evil\n")
        self.git("add", "tracked.txt")
        self.write("tracked.txt", "v1\n")
        self.assertTrue(self.changed())

    def test_assume_unchanged(self):
        self.git("update-index", "--assume-unchanged", "tracked.txt")
        self.assertTrue(self.changed())

    def test_read_only_git_commands_keep_fingerprint(self):
        os.utime(os.path.join(self.repo, "tracked.txt"))  # stat-dirty, content unchanged
        before = tf.fingerprint(self.repo)
        self.git("diff", "HEAD")
        self.git("status")
        self.assertEqual(tf.fingerprint(self.repo), before)

    def test_edit_of_preflagged_file(self):
        self.git("update-index", "--assume-unchanged", "tracked.txt")
        before = tf.fingerprint(self.repo)
        self.write("tracked.txt", "changed\n")
        self.assertNotEqual(tf.fingerprint(self.repo), before)

    def test_new_branch_and_stash(self):
        self.git("branch", "x")
        self.assertTrue(self.changed())

    def test_nested_repo_content(self):
        nested = os.path.join(self.repo, "sub")
        os.makedirs(nested)
        self.git("init", "-q", cwd=nested)
        self.write("g", "1\n", base=nested)
        before = tf.fingerprint(self.repo)
        self.write("g", "2\n", base=nested)
        self.assertNotEqual(tf.fingerprint(self.repo), before)

    def test_linked_worktree_sees_common_hooks(self):
        wt = tempfile.mkdtemp()
        shutil.rmtree(wt)
        self.git("worktree", "add", "-q", wt)
        try:
            before = tf.fingerprint(wt)
            self.write(".git/hooks/pre-commit", "#!/bin/sh\n")
            self.assertNotEqual(tf.fingerprint(wt), before)
        finally:
            shutil.rmtree(wt, ignore_errors=True)

    def test_subdirectory_argument_covers_whole_repo(self):
        before = tf.fingerprint(os.path.join(self.repo, "notes"))
        self.git("update-index", "--assume-unchanged", "tracked.txt")
        self.write("tracked.txt", "changed\n")
        self.assertNotEqual(tf.fingerprint(os.path.join(self.repo, "notes")), before)

    def test_tool_caches_ignored_and_fifo_safe(self):
        os.makedirs(os.path.join(self.repo, "build", "__pycache__"))
        before = tf.fingerprint(self.repo)
        self.write("build/__pycache__/m.cpython-313.pyc", "x")
        self.assertEqual(tf.fingerprint(self.repo), before)
        nested = os.path.join(self.repo, "sub")  # status lists a nested repository as one entry
        os.makedirs(nested)
        self.git("init", "-q", cwd=nested)
        before = tf.fingerprint(self.repo)
        os.mkfifo(os.path.join(nested, "pipe"))
        self.assertNotEqual(tf.fingerprint(self.repo), before)  # recorded by type, never opened (no hang)

    def test_bare_pyc_outside_cache_detected(self):
        self.write("notes/json.pyc", "x")
        self.assertTrue(self.changed())

    def test_staged_rename(self):
        self.git("mv", "tracked.txt", "renamed.txt")
        self.assertTrue(self.changed())

    def test_repo_without_commits(self):
        fresh = tempfile.mkdtemp()
        try:
            self.git("init", "-q", cwd=fresh)
            self.assertEqual(len(tf.fingerprint(fresh)), 64)
        finally:
            shutil.rmtree(fresh)


if __name__ == "__main__":
    unittest.main()
