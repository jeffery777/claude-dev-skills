"""Pins of the Issue #101 review-loop rule text (REQ-029): the value rule of the completeness checks
is copied word for word into the files that subagents read, and the dev-plan bullet group holds the
command forms exactly. The tests only read files."""

import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VALUE_RULE = (
    "Before a value from a plan or a brief goes into a completeness-check command, check it in the text, "
    "never with a command that contains it: the whole of a commit ID matches `[0-9a-f]{40}` or "
    "`[0-9a-f]{64}`; a search string is not empty and holds only printable characters, with no `'`, `\\`, "
    "line break or Unicode format character; the whole of a folder matches "
    "`[A-Za-z0-9._][A-Za-z0-9._/-]*`, and it is the requirements folder of the project. A value that "
    "fails is never put into a command: report it, and that check did not run."
)

VALUE_RULE_FILES = (
    "skills/dev-plan/SKILL.md",
    "skills/dev-deliver/references/task-brief.md",
    "agents/dev-reviewer.md",
    "agents/dev-security-reviewer.md",
    "agents/dev-implementer.md",
)

GIT_PREFIX = "git --no-replace-objects --literal-pathspecs -c core.quotePath=false"
GREP_FORM = f"`{GIT_PREFIX} grep --cached -c -F -i -e '<string>' --`"
HEAD_GREP_FORM = f"`{GIT_PREFIX} grep -c -F -i -e '<string>' '<head ID>' --`"
DIFF_OPTIONS = ("--no-relative --no-ext-diff --no-textconv --no-renames --no-color "
                "--ignore-submodules=none")
DIFF_NAMES_FORM = f"`{GIT_PREFIX} diff --cached {DIFF_OPTIONS} --name-only -- '<requirements folder>'`"
DIFF_LOG_FORM = f"`{GIT_PREFIX} diff --cached {DIFF_OPTIONS} -U0 -- '<requirements folder>/log.md'`"
READING_LIMIT = (
    "Reading shows this only on a target that holds that change alone: on a cumulative diff it cannot tell the "
    "rounds apart, the report says so, and this item does not count as passed."
)
READING_LIMIT_REVIEW = (
    "on a cumulative diff its report says that it cannot tell the rounds apart and that this item does not count "
    "as passed."
)
RULE_1_LIMIT = (
    "Limit: the commands see one row for the whole commit, so a second change of one requirement file in "
    "one commit without its own row is found only by reading."
)
REV_LIST_FORM = "`git --no-replace-objects rev-list --reverse '<base ID>..<head ID>'`"
COMMIT_PAIR_FORM = "`'<commit ID>^1' '<commit ID>'` in place of `--cached`"
REVIEWER_LIST = (
    "Bash may also run `git rev-parse --show-prefix` and the `git rev-list`, `git grep` and `git diff` "
    "forms of the brief"
)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def flat(text):
    return " ".join(text.split())


def completeness_group(text):
    """The dev-plan step 6 bullet group: from its first line to step 7."""
    start = text.index("Then plan the completeness checks")
    end = text.index("7. **Write the task graph**")
    return text[start:end]


def review_step_2(text):
    """The dev-review workflow step 2: from its first line to step 3."""
    start = text.index("2. Gather the context the reviewer needs")
    end = text.index("3. Dispatch the reviewer subagent")
    return text[start:end]


class ValueRule(unittest.TestCase):
    def test_value_rule_word_for_word(self):
        for rel in VALUE_RULE_FILES:
            with self.subTest(rel=rel):
                self.assertEqual(flat(read(rel)).count(VALUE_RULE), 1)

    def test_value_rule_in_the_dev_plan_group(self):
        self.assertIn(VALUE_RULE, flat(completeness_group(read("skills/dev-plan/SKILL.md"))))

    def test_value_rule_in_the_brief_field(self):
        lines = [line for line in read("skills/dev-deliver/references/task-brief.md").splitlines()
                 if line.startswith("Completeness checks: ")]
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith(
            "Completeness checks: <search list and co-change rules from the plan, with their commands> "
            "| none. "))
        self.assertTrue(lines[0].endswith(VALUE_RULE))

    def test_flat_finds_a_changed_copy(self):  # negative case: one changed word fails the pin
        changed = VALUE_RULE.replace("is never put", "is not put")
        self.assertNotIn(VALUE_RULE, flat(changed))


class CommandForms(unittest.TestCase):
    def test_dev_plan_group_holds_the_command_forms_exactly(self):
        group = completeness_group(read("skills/dev-plan/SKILL.md"))
        for form in (GREP_FORM, DIFF_NAMES_FORM, DIFF_LOG_FORM):
            with self.subTest(form=form):
                self.assertEqual(group.count(form), 1)

    def test_limit_of_co_change_rule_1(self):
        group = flat(completeness_group(read("skills/dev-plan/SKILL.md")))
        self.assertEqual(group.count(RULE_1_LIMIT), 1)

    def test_limit_of_the_reading_check(self):
        group = flat(completeness_group(read("skills/dev-plan/SKILL.md")))
        self.assertEqual(group.count(READING_LIMIT), 1)
        step = flat(review_step_2(read("skills/dev-review/SKILL.md")))
        self.assertEqual(step.count(READING_LIMIT_REVIEW), 1)

    def test_merge_review_forms_in_dev_review(self):
        step = flat(review_step_2(read("skills/dev-review/SKILL.md")))
        for form in (REV_LIST_FORM, COMMIT_PAIR_FORM, HEAD_GREP_FORM):
            with self.subTest(form=form):
                self.assertEqual(step.count(form), 1)

    def test_tree_commands_are_gone(self):
        texts = {"skills/dev-plan/SKILL.md": read("skills/dev-plan/SKILL.md"),
                 "skills/dev-review/SKILL.md step 2": review_step_2(read("skills/dev-review/SKILL.md"))}
        for rel, text in texts.items():
            for word in ("git write-tree", "cat-file -t"):
                with self.subTest(rel=rel, word=word):
                    self.assertNotIn(word, text)

    def test_replaced_d5_text_is_gone(self):
        text = read("skills/dev-plan/SKILL.md")
        for word in ("Node commits", "without `--cached`", "write-tree"):
            with self.subTest(word=word):
                self.assertNotIn(word, text)
        self.assertNotIn("working tree", flat(review_step_2(read("skills/dev-review/SKILL.md"))))

    def test_reviewer_bash_lists(self):
        for rel in ("agents/dev-reviewer.md", "agents/dev-security-reviewer.md"):
            self.assertEqual(flat(read(rel)).count(REVIEWER_LIST), 1)


if __name__ == "__main__":
    unittest.main()
