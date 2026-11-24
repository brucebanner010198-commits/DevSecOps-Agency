"""Tests for scripts/dispatch_names.py (run: python -m pytest scripts)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dispatch_names as dn  # noqa: E402

CARDS = {"pm-lead", "spec-writer", "cro"}


def test_bare_target_after_dispatch_is_qualified():
    assert dn.fix_line("5. Dispatch `pm-lead` with the idea.", CARDS) == "5. Dispatch `devsecops-agency:pm-lead` with the idea."


def test_subject_before_dispatch_is_left_alone():
    line = "`pm-lead` dispatches `spec-writer`."
    assert dn.fix_line(line, CARDS) == "`pm-lead` dispatches `devsecops-agency:spec-writer`."


def test_qualified_names_and_non_agents_are_untouched():
    line = "Dispatch `devsecops-agency:cro` and write `brief.md`."
    assert dn.fix_line(line, CARDS) == line


def test_lines_without_dispatch_are_untouched():
    assert dn.fix_line("The `cro` owns research.", CARDS) == "The `cro` owns research."


def test_repository_has_no_bare_dispatch_targets(capsys):
    assert dn.main(["x", "check"]) == 0, capsys.readouterr().out
