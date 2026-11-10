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
    return text[start:text.index("[core: review-and-security.md#review-security]", start)]


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

        self.assertIn("the labels, milestone and assignees that a post sets, and a push scan reads the ref names", text)
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

if __name__ == "__main__":
    unittest.main()
