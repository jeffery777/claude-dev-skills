"""Issue #106 PR-3: R-REV-9 against Core v0.5.0 `review-publication-data`, and SEC105B-01 (DL-050)."""

import os
import re
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return " ".join(fh.read().split())


def rev9():
    text = read("skills", "dev-core", "SKILL.md")
    start = text.index("- **R-REV-9**")
    return text[start:text.index("[core: review-and-security.md#review-security", start)]


class PublicationData(unittest.TestCase):
    def test_each_scan_counts_only_by_r_del_2_and_r_rev_1(self):
        self.assertIn("Each scan of this rule (commit, push, text and merge readiness) that does not count by R-DEL-2 "
                      "and R-REV-1 counts as no scan, also when push step 5 counts it as passed", rev9())
        req = read("docs", "requirements", "REQ-011-security-review-before-commit-push.md")
        self.assertIn("The session binding and R-REV-1 apply to each scan", req)
        self.assertNotIn("the note on Issue #95 above stays for it alone", req)

    def test_scope_payload_and_destination(self):
        text = rev9()
        for words in ("a Release title or notes, the tag name and target of a Release",
                      "before attaching a file to any of them",
                      "makes the scan `NOT_RUN`",
                      "The post names its repository (`--repo <owner/name>` of the task) and sends the scanned file itself",
                      "whether Git will sign",
                      "says only whether `user.signingkey` is set",
                      "certificates, private files, confidential files, private paths, hosts and addresses, accounts",
                      "unneeded execution logs",
                      "An approved public identity with a source and full license notices are not removed for a literal match alone",
                      "a rendered view, for example of a PDF or a notebook, does not count",
                      "A scan never claims that it found every secret"):
            self.assertIn(words, text)
        push = read("skills", "dev-core", "references", "push-scan.md")
        self.assertNotIn("names the repository of the task", push)
        self.assertNotIn("When step 2 prints `STOP`", push)  # card I106-C11 (a): no allow path for a URL difference

        self.assertIn("The labels, milestone and assignees that a post sets, and the ref names that a push sends (both sides "
                      "of each tab-separated ref line of the dry-run), go into a separate text file; the same `awk` runs on it",
                      text)  # MR108-02, finding P2D-04
        self.assertIn("or, for a signature finding (push step 8, or a signature that Git will make at a commit)", text)  # MR108-03
        self.assertIn("and whether Git will sign it (R-REV-9)", read("skills", "dev-implement", "SKILL.md"))

    def test_agent_copy_follows(self):
        agent = read("agents", "dev-security-reviewer.md")
        for words in ("a Release title or notes, the tag name and target of a Release, an attached file",
                      "whether Git will sign it", "unneeded execution logs",
                      "a rendered view, for example of a PDF or a notebook, does not count) makes the scan `NOT_RUN`",
                      "are not removed for a literal match alone"):
            self.assertIn(words, agent)

    def test_text_check_matches_any_begin_block(self):
        command = re.search(r"`(LC_ALL=C awk '[^`]*\{print NR\}') <text file>`", read("skills", "dev-core", "SKILL.md")).group(1)
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "text")
            with open(path, "wb") as fh:
                fh.write(b"clean\n" + b"-----BEGIN " + b"CERTIFICATE-----\n")
            result = subprocess.run(["bash", "-c", f"{command} '{path}'"], capture_output=True)
        self.assertEqual((result.returncode, result.stdout), (0, b"2\n"))

    def test_step_2_stops_on_a_push_rewrite(self):
        push = read("skills", "dev-core", "references", "push-scan.md")
        command = re.search(r"`(test \"\$\(git remote get-url --all '<remote>' 2>/dev/null\)\" = [^`]*)`", push).group(1)
        with tempfile.TemporaryDirectory() as tmp:
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", HOME=tmp)
            subprocess.run(["git", "init", "-q", tmp], check=True, env=env)
            subprocess.run(["git", "-C", tmp, "remote", "add", "origin", "git@example.invalid:o/r.git"], check=True, env=env)
            filled = command.replace("<remote>", "origin")
            run = lambda: subprocess.run(["bash", "-c", filled], cwd=tmp, env=env, capture_output=True, text=True).stdout.strip()
            self.assertEqual(run(), "PASS")  # any host and URL form passes when push and fetch agree
            subprocess.run(["git", "-C", tmp, "config", "url.https://other.invalid/.pushInsteadOf", "git@example.invalid:"],
                           check=True, env=env)
            self.assertEqual(run(), "STOP")

def isolated_env(home):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", HOME=home)
    return env


class PushOptionsAndLfs(unittest.TestCase):
    """Issue #106 PR-2, cards I106-C12 (a) and I106-C13 (a): push options and Git LFS objects stop the push."""

    def test_push_option_check(self):
        push = read("skills", "dev-core", "references", "push-scan.md")
        command = re.search(r"`(git config --get-all push\.pushOption [^`]*)`", push).group(1)
        with tempfile.TemporaryDirectory() as tmp:
            env = isolated_env(tmp)
            subprocess.run(["git", "init", "-q", tmp], check=True, env=env)
            run = lambda: subprocess.run(["bash", "-c", command], cwd=tmp, env=env, capture_output=True, text=True).stdout
            self.assertEqual(run(), "PASS\n")
            subprocess.run(["git", "-C", tmp, "config", "--add", "push.pushOption", "ci.skip"], check=True, env=env)
            self.assertEqual(run(), "STOP\n")  # the value itself is not printed

    def test_lfs_pointer_count(self):
        push = read("skills", "dev-core", "references", "push-scan.md")
        pattern = re.search(r"`LC_ALL=C grep -Ec '([^']*)' <file>`", push).group(1)
        oid = "oid sha256:" + "a" * 64  # built at run time, so no committed line matches (finding P2D-07)
        samples = {"added": f"+version https://git-lfs.github.com/spec/v1\n+{oid}\n+size 3\n",
                   "changed": f" version https://git-lfs.github.com/spec/v1\n-{oid}\n+oid sha256:{'b' * 64}\n",  # finding S2R-01
                   "colored": f"\x1b[32m+\x1b[m\x1b[32m{oid}\x1b[m\n"}
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "view")
            for name, text in list(samples.items()) + [("clean", "+plain text\n")]:
                with self.subTest(name=name):
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(text)
                    result = subprocess.run(["grep", "-Ec", pattern, path], capture_output=True, text=True,
                                            env=dict(os.environ, LC_ALL="C"))
                    if name == "clean":
                        self.assertEqual((result.returncode, result.stdout), (1, "0\n"))
                    else:
                        self.assertEqual(result.returncode, 0)
                        self.assertNotEqual(result.stdout, "0\n")

    def test_no_verify_dry_run_runs_no_hook(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = isolated_env(tmp)
            remote, work, marker = (os.path.join(tmp, n) for n in ("r.git", "w", "marker"))
            subprocess.run(["git", "init", "-q", "--bare", remote], check=True, env=env)
            subprocess.run(["git", "init", "-q", work], check=True, env=env)
            subprocess.run(["git", "-C", work, "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                            "commit", "-q", "--allow-empty", "-m", "a"], check=True, env=env)
            hook = os.path.join(work, ".git", "hooks", "pre-push")
            with open(hook, "w", encoding="utf-8") as fh:
                fh.write(f"#!/bin/sh\necho ran >> '{marker}'\n")
            os.chmod(hook, 0o755)
            head = subprocess.run(["git", "-C", work, "symbolic-ref", "HEAD"], check=True, env=env,
                                  capture_output=True, text=True).stdout.strip()
            push = ["git", "-C", work, "push", "--dry-run", "--porcelain"]
            subprocess.run(push + ["--no-verify", remote, f"{head}:{head}"], check=True, env=env, capture_output=True)
            self.assertFalse(os.path.exists(marker))
            subprocess.run(push + [remote, f"{head}:{head}"], check=True, env=env, capture_output=True)
            self.assertTrue(os.path.exists(marker))  # the base form ran the hook in the dry-run (finding P2D-01)

    def test_steps_and_not_covered(self):
        push = read("skills", "dev-core", "references", "push-scan.md")
        self.assertIn("with `--dry-run --porcelain --no-verify` added after `push`", push)
        self.assertIn("without `--dry-run --porcelain --no-verify`", push)
        self.assertIn("6a. The main agent runs the `log` command of step 8", push)
        self.assertIn("prints `0` and exits 1", push)
        self.assertIn("leaves the push scan `NOT_RUN`", push)
        self.assertNotIn("push options and Git LFS objects (FU-007)", push)
        self.assertIn("a pointer that the diff of step 6a does not show", push)
        self.assertIn("`--dry-run --porcelain --no-verify` added", read("skills", "dev-implement", "SKILL.md"))


if __name__ == "__main__":
    unittest.main()
