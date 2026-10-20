"""Tests for skills/dev-plan/scripts/graph.py (run: python3 -m unittest discover tests)."""

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES = os.path.join(ROOT, "tests", "fixtures", "graph")
spec = importlib.util.spec_from_file_location("graph", os.path.join(ROOT, "skills", "dev-plan", "scripts", "graph.py"))
graph = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graph)


def fixtures(kind):
    folder = os.path.join(FIXTURES, kind)
    return sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".json"))


class ValidFixtures(unittest.TestCase):
    def test_valid_fixtures_have_no_errors(self):
        for path in fixtures("valid"):
            with self.subTest(path=os.path.basename(path)):
                errors, _ = graph.check_graph(graph.load(path), os.path.join(FIXTURES, "requirements"))
                self.assertEqual(errors, [])

    def test_ready(self):
        g = graph.load(os.path.join(FIXTURES, "valid", "rate-limit.json"))
        self.assertEqual(graph.ready_nodes(g), ["T2", "T3"])


class InvalidFixtures(unittest.TestCase):
    def test_each_invalid_fixture_reports_expected_code(self):
        paths = fixtures("invalid")
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(path=os.path.basename(path)):
                g = graph.load(path)
                errors, _ = graph.check_graph(g)
                # Exact match: each fixture isolates one defect.
                self.assertEqual({e["code"] for e in errors}, set(g["_expect"]))


REQS = os.path.join(FIXTURES, "requirements")


class RequirementFiles(unittest.TestCase):
    def setUp(self):
        self.g = graph.load(os.path.join(FIXTURES, "valid", "rate-limit.json"))
        self.tmp = tempfile.mkdtemp()
        for name in os.listdir(REQS):
            shutil.copy(os.path.join(REQS, name), self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    @staticmethod
    def rewrite(path, old, new):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if old not in text:
            raise AssertionError(f"{old!r} not in {path}")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text.replace(old, new, 1))

    def codes(self, req_dir):
        errors, warnings = graph.check_graph(self.g, req_dir)
        return {e["code"] for e in errors}, {w["code"] for w in warnings}

    def test_existing_files_pass(self):
        self.assertEqual(self.codes(REQS), (set(), set()))

    def test_missing_file(self):
        os.remove(os.path.join(self.tmp, "REQ-002-limit-docs.md"))
        self.assertEqual(self.codes(self.tmp)[0], {"MISSING_REQUIREMENT_FILE"})

    def test_missing_dir(self):
        self.assertEqual(self.codes(os.path.join(self.tmp, "nope"))[0], {"MISSING_REQUIREMENTS_DIR"})

    def test_id_mismatch(self):
        path = os.path.join(self.tmp, "REQ-002-limit-docs.md")
        self.rewrite(path, "id: REQ-002", "id: REQ-007")
        self.assertEqual(self.codes(self.tmp)[0], {"REQUIREMENT_ID_MISMATCH"})

    def test_duplicate_file(self):
        shutil.copy(os.path.join(self.tmp, "REQ-001-login-rate-limit.md"), os.path.join(self.tmp, "REQ-001-copy.md"))
        self.assertEqual(self.codes(self.tmp)[0], {"DUPLICATE_REQUIREMENT_FILE"})

    def test_dropped_requirement_warns(self):
        path = os.path.join(self.tmp, "REQ-002-limit-docs.md")
        self.rewrite(path, "status: active", "status: dropped")
        self.assertEqual(self.codes(self.tmp), (set(), {"INACTIVE_REQUIREMENT"}))

    def test_conflict_blocks_open_writers(self):
        path = os.path.join(self.tmp, "REQ-002-limit-docs.md")
        self.rewrite(path, "status: active", "status: conflict")
        # REQ-008: validate fails while an open writer (T3, planned) cites a conflicting REQ.
        self.assertEqual(self.codes(self.tmp)[0], {"REQUIREMENT_CONFLICT"})

    def test_ready_continues_around_parked_conflict_writer(self):
        project = os.path.join(self.tmp, "proj")
        os.makedirs(os.path.join(project, ".dev", "OBJ"))
        shutil.copytree(self.tmp, os.path.join(project, "docs", "requirements"),
                        ignore=shutil.ignore_patterns("proj"))
        self.rewrite(os.path.join(project, "docs", "requirements", "REQ-002-limit-docs.md"),
                     "status: active", "status: conflict")
        target = os.path.join(project, ".dev", "OBJ", "graph.json")
        shutil.copy(os.path.join(FIXTURES, "valid", "rate-limit.json"), target)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(graph.main(["validate", target]), 1)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(graph.main(["ready", target]), 0)
        result = json.loads(out.getvalue())
        self.assertEqual((result["ready"], result["waiting_on_conflict"]), (["T2"], ["T3"]))
        self.assertIn("warnings", result)

    def test_comment_line_inside_block_list(self):
        self.set_field("REQ-001-login-rate-limit.md", "depends_on: []", "depends_on:\n  # none yet\n  - REQ-002")
        self.assertEqual(graph.frontmatter(os.path.join(self.tmp, "REQ-001-login-rate-limit.md"))["depends_on"], ["REQ-002"])

    def test_single_quote_escape(self):
        path = os.path.join(self.tmp, "q.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("---\nquote: 'user''s login' # c\n---\n")
        self.assertEqual(graph.frontmatter(path)["quote"], "user's login")

    def set_field(self, name, old, new):
        self.rewrite(os.path.join(self.tmp, name), old, new)

    def test_relation_to_missing_req(self):
        self.set_field("REQ-001-login-rate-limit.md", "conflicts_with: []", "conflicts_with: [REQ-404]")
        self.assertEqual(self.codes(self.tmp)[0], {"REQ_RELATION_UNKNOWN"})

    def test_block_list_relation_parsed(self):
        self.set_field("REQ-001-login-rate-limit.md", "depends_on: []", "depends_on:\n  - REQ-405")
        self.assertEqual(self.codes(self.tmp)[0], {"REQ_RELATION_UNKNOWN"})

    def test_depends_on_cycle(self):
        self.set_field("REQ-001-login-rate-limit.md", "depends_on: []", "depends_on: [REQ-002]")
        self.set_field("REQ-002-limit-docs.md", "depends_on: []", "depends_on: [REQ-001]")
        self.assertEqual(self.codes(self.tmp)[0], {"REQ_DEPENDENCY_CYCLE"})

    def test_unindented_block_list_parsed(self):
        self.set_field("REQ-001-login-rate-limit.md", "depends_on: []", "depends_on:\n- REQ-406")
        self.assertEqual(self.codes(self.tmp)[0], {"REQ_RELATION_UNKNOWN"})

    def test_empty_status_is_reported_not_crash(self):
        self.set_field("REQ-002-limit-docs.md", "status: active", "status:")
        self.assertEqual(self.codes(self.tmp)[0], {"BAD_REQUIREMENT_STATUS"})

    def test_bad_status_case(self):
        self.set_field("REQ-002-limit-docs.md", "status: active", "status: Conflict")
        self.assertEqual(self.codes(self.tmp)[0], {"BAD_REQUIREMENT_STATUS"})

    def test_frontmatter_comments_quotes_and_block_scalars(self):
        path = os.path.join(self.tmp, "x.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write('---\ntitle: "Fix C#port"\ntype: chat   # doc | chat\ndesc: >\n  line one\n  line two\n'
                     'ml: short\n  continued here\n---\n')
        meta = graph.frontmatter(path)
        flow = os.path.join(self.tmp, "y.md")
        with open(flow, "w", encoding="utf-8") as fh:
            fh.write('---\na: [x, "b, c", y]\nb: [x, "c #d"]  # note\n---\n')
        self.assertEqual(graph.frontmatter(flow)["a"], ["x", "b, c", "y"])
        self.assertEqual(graph.frontmatter(flow)["b"], ["x", "c #d"])
        nested = os.path.join(self.tmp, "z.md")
        with open(nested, "w", encoding="utf-8") as fh:
            fh.write('---\nk: ["a]b", c]\nd:\n  long text\n---\n')
        self.assertEqual(graph.frontmatter(nested), {"k": ["a]b", "c"], "d": "long text"})
        self.assertEqual((meta["title"], meta["type"], meta["desc"], meta["ml"]),
                         ("Fix C#port", "chat", "line one line two", "short continued here"))

    def test_frontmatter_documented_limits(self):
        doc = graph.frontmatter.__doc__
        self.assertIn("Supported subset", doc)
        self.assertIn("Not supported", doc)
        path = os.path.join(self.tmp, "limits.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write('---\nflag: true\nn: 12\nesc: "x \\" y"\nmulti: [a,\n  b]\n'
                     'items:\n  - type: doc\n    locator: x\nflag: again\n---\n')
        self.assertEqual(graph.frontmatter(path), {"flag": "again", "n": "12", "esc": "x \\",
                                                   "multi": "[a, b]", "items": ["type: doc"]})

    def test_explicit_dir_outside_root_refused(self):
        project = os.path.join(self.tmp, "proj")
        os.makedirs(os.path.join(project, ".dev", "OBJ"))
        target = os.path.join(project, ".dev", "OBJ", "graph.json")
        self.assertEqual(graph.find_requirements_dir(target, self.tmp)[1]["code"], "REQUIREMENTS_DIR_OUTSIDE")

    def test_refines_cycle_is_allowed(self):
        self.set_field("REQ-001-login-rate-limit.md", "refines: []", "refines: [REQ-002]")
        self.assertEqual(self.codes(self.tmp)[0], set())

    def test_root_boundary(self):
        project = os.path.join(self.tmp, "proj")
        os.makedirs(os.path.join(project, ".dev", "OBJ"))
        os.makedirs(os.path.join(self.tmp, "docs", "requirements"))  # above the project root
        target = os.path.join(project, ".dev", "OBJ", "graph.json")
        found, problem = graph.find_requirements_dir(target)
        self.assertEqual(found, os.path.join(project, "docs", "requirements"))
        self.assertIsNone(problem)
        with open(os.path.join(project, ".dev", "config.json"), "w", encoding="utf-8") as fh:
            json.dump({"requirements_dir": "../docs/requirements"}, fh)
        self.assertEqual(graph.find_requirements_dir(target)[1]["code"], "REQUIREMENTS_DIR_OUTSIDE")

    def test_config_sets_requirements_dir(self):
        project = os.path.join(self.tmp, "proj")
        os.makedirs(os.path.join(project, ".dev", "OBJ"))
        shutil.copytree(REQS, os.path.join(project, "spec", "reqs"))
        with open(os.path.join(project, ".dev", "config.json"), "w", encoding="utf-8") as fh:
            json.dump({"requirements_dir": "spec/reqs"}, fh)
        target = os.path.join(project, ".dev", "OBJ", "graph.json")
        self.assertEqual(graph.find_requirements_dir(target)[0], os.path.join(project, "spec", "reqs"))

    def test_cli_finds_nearest_requirements_dir(self):
        project = os.path.join(self.tmp, "proj")
        os.makedirs(os.path.join(project, ".dev", "OBJ"))
        shutil.copytree(REQS, os.path.join(project, "docs", "requirements"))
        target = os.path.join(project, ".dev", "OBJ", "graph.json")
        shutil.copy(os.path.join(FIXTURES, "valid", "rate-limit.json"), target)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(graph.main(["validate", target]), 0)
        os.remove(os.path.join(project, "docs", "requirements", "REQ-001-login-rate-limit.md"))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(graph.main(["validate", target]), 1)


class Transitions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "graph.json")
        shutil.copy(os.path.join(FIXTURES, "valid", "rate-limit.json"), self.path)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_legal_transition_appends_event(self):
        self.assertEqual(graph.transition(self.path, "T2", "in_progress", "claimed by main agent", "test"), [])
        self.assertEqual(graph.load(self.path)["nodes"][1]["status"], "in_progress")
        with open(os.path.join(self.tmp, "events.jsonl"), encoding="utf-8") as fh:
            event = json.loads(fh.readline())
        self.assertEqual((event["seq"], event["from"], event["to"]), (1, "ready", "in_progress"))

    def test_illegal_transition_rejected(self):
        errs = graph.transition(self.path, "T2", "done", "skip review", "test")
        self.assertEqual(errs[0]["code"], "ILLEGAL_TRANSITION")
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "events.jsonl")))

    def test_transition_needs_evidence(self):
        self.assertEqual(graph.transition(self.path, "T2", "in_progress", "  ", "test")[0]["code"], "NO_EVIDENCE")

    def test_conflict_requirement_blocks_transition(self):
        reqs = os.path.join(self.tmp, "reqs")
        shutil.copytree(REQS, reqs)
        path = os.path.join(reqs, "REQ-001-login-rate-limit.md")
        RequirementFiles.rewrite(path, "status: active", "status: conflict")
        errs = graph.transition(self.path, "T2", "in_progress", "start", "test", reqs)
        self.assertIn("REQUIREMENT_CONFLICT", {e["code"] for e in errs})

    def test_reopen_refused_when_dependents_started(self):
        self.assertEqual(graph.transition(self.path, "T2", "in_progress", "start", "test"), [])
        errs = graph.transition(self.path, "T1", "ready", "reopen", "test")
        self.assertEqual(errs[0]["code"], "ILLEGAL_REOPEN")

    def test_symlinked_event_log_refused(self):
        outside = os.path.join(self.tmp, "outside.txt")
        open(outside, "w").close()
        os.symlink(outside, os.path.join(self.tmp, "events.jsonl"))
        errs = graph.transition(self.path, "T2", "in_progress", "start", "test")
        self.assertEqual(errs[0]["code"], "SYMLINK_REFUSED")
        self.assertEqual(os.path.getsize(outside), 0)

    def test_no_temp_files_left(self):
        graph.transition(self.path, "T2", "in_progress", "start", "test")
        leftovers = [f for f in os.listdir(self.tmp) if f.endswith(".tmp")]
        self.assertEqual(leftovers, [])

    def _evidence_project(self):
        project = os.path.join(self.tmp, "proj")
        os.makedirs(os.path.join(project, ".dev", "OBJ"))
        shutil.copytree(REQS, os.path.join(project, "docs", "requirements"))
        target = os.path.join(project, ".dev", "OBJ", "graph.json")
        shutil.copy(self.path, target)
        return project, target

    def _run_evidence_file(self, target, ev):
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            code = graph.main(["transition", target, "T2", "in_progress", "--evidence-file", ev])
        return code, err.getvalue()

    def test_cli_evidence_file_records_path_and_hash_not_content(self):
        project, target = self._evidence_project()
        ev = os.path.join(project, ".dev", "OBJ", "ev.txt")
        body = b"$(touch pwned) commit abc123 SECRET-TOKEN\n"
        with open(ev, "wb") as fh:
            fh.write(body)
        self.assertEqual(self._run_evidence_file(target, ev)[0], 0)
        with open(os.path.join(project, ".dev", "OBJ", "events.jsonl"), encoding="utf-8") as fh:
            raw = fh.read()
        self.assertEqual(json.loads(raw)["evidence"],
                         "file:.dev/OBJ/ev.txt sha256:" + hashlib.sha256(body).hexdigest())
        self.assertNotIn("SECRET-TOKEN", raw)

    def test_cli_evidence_file_outside_project_refused(self):
        project, target = self._evidence_project()
        outside = os.path.join(self.tmp, "private.txt")
        with open(outside, "w", encoding="utf-8") as fh:
            fh.write("SECRET-TOKEN\n")
        code, err = self._run_evidence_file(target, outside)
        self.assertEqual(code, 2)
        self.assertIn("EVIDENCE_FILE_REFUSED", err)
        self.assertFalse(os.path.exists(os.path.join(project, ".dev", "OBJ", "events.jsonl")))
        self.assertEqual(graph.load(target), graph.load(self.path))

    def test_cli_evidence_file_symlink_refused(self):
        project, target = self._evidence_project()
        outside = os.path.join(self.tmp, "private.txt")
        open(outside, "w").close()
        link = os.path.join(project, "ev-link.txt")
        os.symlink(outside, link)
        inner = os.path.join(project, "inner.txt")
        open(inner, "w").close()
        inner_link = os.path.join(project, "inner-link.txt")
        os.symlink(inner, inner_link)
        for path in (link, inner_link):
            with self.subTest(path=os.path.basename(path)):
                code, err = self._run_evidence_file(target, path)
                self.assertEqual(code, 2)
                self.assertIn("EVIDENCE_FILE_REFUSED", err)

    def test_cli_evidence_file_symlinked_parent_outside_refused(self):
        project, target = self._evidence_project()
        outside_dir = os.path.join(self.tmp, "outside")
        os.makedirs(outside_dir)
        with open(os.path.join(outside_dir, "key.txt"), "w", encoding="utf-8") as fh:
            fh.write("SECRET-TOKEN\n")
        os.symlink(outside_dir, os.path.join(project, "linked"))
        code, err = self._run_evidence_file(target, os.path.join(project, "linked", "key.txt"))
        self.assertEqual(code, 2)
        self.assertIn("EVIDENCE_FILE_REFUSED", err)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "needs mkfifo")
    def test_cli_evidence_file_fifo_refused_without_blocking(self):
        project, target = self._evidence_project()
        fifo = os.path.join(project, "pipe")
        os.mkfifo(fifo)
        code, err = self._run_evidence_file(target, fifo)
        self.assertEqual(code, 2)
        self.assertIn("EVIDENCE_FILE_REFUSED", err)

    def test_cli_evidence_file_missing_refused(self):
        project, target = self._evidence_project()
        code, err = self._run_evidence_file(target, os.path.join(project, "missing.txt"))
        self.assertEqual(code, 2)
        self.assertIn("EVIDENCE_FILE_REFUSED", err)

    def test_evidence_file_without_project_root_refused(self):
        with mock.patch.object(graph, "project_root", return_value=None):
            ref, refused = graph.evidence_file_ref(self.path, self.path)
        self.assertIsNone(ref)
        self.assertEqual(refused["code"], "EVIDENCE_FILE_REFUSED")

    def test_cli_evidence_file_not_regular_refused(self):
        project, target = self._evidence_project()
        code, err = self._run_evidence_file(target, os.path.join(project, "docs"))
        self.assertEqual(code, 2)
        self.assertIn("EVIDENCE_FILE_REFUSED", err)

    def test_cancel_that_breaks_ordering_refused(self):
        g = graph.load(self.path)
        nodes = {n["id"]: n for n in g["nodes"]}
        # T3 (docs) now overlaps T2's paths and is ordered only through a new explore node TB.
        g["nodes"].append({"id": "TB", "title": "bridge", "kind": "explore", "requirements": [],
                           "depends_on": [{"node": "T2", "consumes": "limiter API"}], "owns": [],
                           "risk": "low", "review": "none", "status": "planned", "dod": [], "verify": []})
        nodes["T3"]["owns"] = ["src/auth/limiter/README.md"]
        nodes["T3"]["depends_on"] = [{"node": "TB", "consumes": "notes"}]
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(g, fh)
        errs = graph.transition(self.path, "TB", "cancelled", "not needed", "test")
        self.assertEqual(errs[0]["code"], "TRANSITION_BREAKS_GRAPH")

    def test_stranded_warning(self):
        self.assertEqual(graph.transition(self.path, "T3", "cancelled", "dropped", "test"), [])
        _, warnings = graph.check_graph(graph.load(self.path))
        self.assertIn("STRANDED", {w["code"] for w in warnings})
        # `ready` passes the warning on, so the dev-deliver loop sees it.
        project = os.path.join(self.tmp, "proj")
        os.makedirs(os.path.join(project, ".dev", "OBJ"))
        shutil.copytree(REQS, os.path.join(project, "docs", "requirements"))
        target = os.path.join(project, ".dev", "OBJ", "graph.json")
        shutil.copy(self.path, target)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(graph.main(["ready", target]), 0)
        self.assertIn("STRANDED", {w["code"] for w in json.loads(out.getvalue())["warnings"]})

    def test_reopen_refused_when_dependent_blocked(self):
        self.assertEqual(graph.transition(self.path, "T2", "in_progress", "start", "test"), [])
        self.assertEqual(graph.transition(self.path, "T2", "blocked", "waiting", "test"), [])
        self.assertEqual(graph.transition(self.path, "T1", "ready", "reopen", "test")[0]["code"], "ILLEGAL_REOPEN")

    def test_torn_event_log_refused(self):
        with open(os.path.join(self.tmp, "events.jsonl"), "w", encoding="utf-8") as fh:
            fh.write('{"seq": 1')
        self.assertEqual(graph.transition(self.path, "T2", "in_progress", "start", "test")[0]["code"], "EVENTS_CORRUPT")

    def test_non_object_root(self):
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write("[]")
        self.assertEqual(graph.transition(self.path, "T2", "in_progress", "x", "test")[0]["code"], "UNREADABLE")

    def test_mode_preserved(self):
        os.chmod(self.path, 0o644)
        graph.transition(self.path, "T2", "in_progress", "start", "test")
        self.assertEqual(os.stat(self.path).st_mode & 0o777, 0o644)

    def test_unhashable_enum_is_schema_error(self):
        g = graph.load(self.path)
        g["nodes"][1]["kind"] = ["implement"]
        self.assertEqual({e["code"] for e in graph.check_graph(g)[0]}, {"SCHEMA"})

    def conflict_reqs(self):
        reqs = os.path.join(self.tmp, "reqs")
        shutil.copytree(REQS, reqs)
        RequirementFiles.rewrite(os.path.join(reqs, "REQ-001-login-rate-limit.md"), "status: active", "status: conflict")
        return reqs

    def test_conflict_still_allows_parking_and_other_nodes(self):
        reqs = self.conflict_reqs()
        self.assertEqual(graph.transition(self.path, "T2", "blocked", "waiting on user", "test", reqs), [])
        self.assertEqual(graph.transition(self.path, "T3", "ready", "docs can start", "test", reqs), [])

    def test_short_write_rolls_back(self):
        real = os.write
        with mock.patch.object(graph.os, "write", side_effect=lambda fd, b: real(fd, bytes(b[:5])) and 0):
            errs = graph.transition(self.path, "T2", "in_progress", "start", "test")
        self.assertEqual(errs[0]["code"], "EVENT_WRITE_FAILED")
        self.assertEqual(graph.load(self.path)["nodes"][1]["status"], "ready")
        self.assertEqual(os.path.getsize(os.path.join(self.tmp, "events.jsonl")), 0)

    def test_fsync_failure_rolls_back(self):
        calls = []

        def fsync(fd):
            calls.append(fd)
            if len(calls) == 2:  # 1: graph write, 2: event append, 3: graph restore
                raise OSError("disk")

        with mock.patch.object(graph.os, "fsync", side_effect=fsync):
            errs = graph.transition(self.path, "T2", "in_progress", "start", "test")
        self.assertEqual(errs[0]["code"], "EVENT_WRITE_FAILED")
        self.assertEqual(os.path.getsize(os.path.join(self.tmp, "events.jsonl")), 0)

    def test_reopen_refused_when_dependent_ready(self):
        errs = graph.transition(self.path, "T1", "ready", "reopen", "test")
        self.assertEqual(errs[0]["code"], "TRANSITION_BREAKS_GRAPH")

    def test_symlinked_parent_folder_refused(self):
        project = os.path.join(self.tmp, "proj")
        os.makedirs(os.path.join(project, ".dev"))
        outside = os.path.join(self.tmp, "outside")
        os.makedirs(outside)
        shutil.copy(self.path, os.path.join(outside, "graph.json"))
        os.symlink(outside, os.path.join(project, ".dev", "OBJ"))
        errs = graph.transition(os.path.join(project, ".dev", "OBJ", "graph.json"), "T2", "in_progress", "x", "test")
        self.assertEqual(errs[0]["code"], "SYMLINK_REFUSED")

    def test_symlinked_objective_to_other_repo_refused(self):
        project = os.path.join(self.tmp, "proj")
        os.makedirs(os.path.join(project, ".dev"))
        other = os.path.join(self.tmp, "other")
        os.makedirs(os.path.join(other, ".git"))
        shutil.copy(self.path, os.path.join(other, "graph.json"))
        os.symlink(other, os.path.join(project, ".dev", "OBJ"))
        errs = graph.transition(os.path.join(project, ".dev", "OBJ", "graph.json"), "T2", "in_progress", "x", "test")
        self.assertEqual(errs[0]["code"], "SYMLINK_REFUSED")
        self.assertFalse(os.path.exists(os.path.join(other, "events.jsonl")))

    def test_finished_writers_not_compared_for_overlap(self):
        g = graph.load(self.path)
        g["nodes"][2]["owns"] = ["src/auth/limiter/README.md"]   # T3 overlaps T2, no ordering
        self.assertIn("OWNERSHIP_OVERLAP", {e["code"] for e in graph.check_graph(g)[0]})
        g["nodes"][1]["status"] = "done"
        self.assertNotIn("OWNERSHIP_OVERLAP", {e["code"] for e in graph.check_graph(g)[0]})

    def test_owns_outside_repo_is_schema_error(self):
        g = graph.load(self.path)
        g["nodes"][1]["owns"] = ["../../etc/**"]
        self.assertEqual({e["code"] for e in graph.check_graph(g)[0]}, {"SCHEMA"})

    def test_transition_that_shrinks_status_dep_allowed(self):
        g = graph.load(self.path)
        st = {n["id"]: n for n in g["nodes"]}
        st["T2"]["status"], st["T4"]["status"] = "reviewing", "in_progress"   # T4 waits on T2 and T3
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(g, fh)
        self.assertEqual(graph.transition(self.path, "T2", "done", "reviewed", "test"), [])

    def test_cannot_start_before_dependencies(self):
        errs = graph.transition(self.path, "T4", "ready", "early start", "test")
        self.assertEqual(errs[0]["code"], "STATUS_DEP")


class Overlap(unittest.TestCase):
    def test_patterns(self):
        self.assertTrue(graph.patterns_overlap("src/**", "src/auth/x.py"))
        self.assertTrue(graph.patterns_overlap("./src/a.py", "src/a.py"))
        self.assertTrue(graph.patterns_overlap("src//a.py", "src/a.py"))
        self.assertTrue(graph.patterns_overlap(".", "src/a.py"))
        self.assertTrue(graph.patterns_overlap("/", "docs/x.md"))
        self.assertTrue(graph.patterns_overlap("Src/auth/**", "src/auth/x.py"))
        self.assertTrue(graph.patterns_overlap("src/a.py", "src/a.py"))
        self.assertFalse(graph.patterns_overlap("src/auth/**", "src/billing/**"))
        self.assertFalse(graph.patterns_overlap("docs/auth.md", "docs/billing.md"))


if __name__ == "__main__":
    unittest.main()
