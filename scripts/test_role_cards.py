"""Tests for scripts/role_cards.py (run: python -m pytest scripts)."""
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent))
import role_cards as rc  # noqa: E402

AGENT = (
    "---\n"
    "name: a\n"
    "description: |-\n"
    "  Use when x.\n"
    "\n"
    "model: haiku\n"
    'tools: ["Read", "Write", "Edit", "Bash", "Task"]\n'
    "color: red\n"
    "---\n"
    "Body text stays.\n"
)


def card(tools, shell=None, effort="low", turns=20, model="haiku"):
    return {"file": "agents/a.md", "enforced": {"tools": tools, "shell": shell, "model": model,
                                                "effort": effort, "maxTurns": turns}}


@pytest.fixture
def agent(tmp_path):
    p = tmp_path / "a.md"
    p.write_bytes(AGENT.encode())
    return p


def fm(text):
    return yaml.safe_load(text.split("---\n")[1])


def test_full_write_sets_tools_and_limits_and_keeps_body(agent):
    out = rc.render(agent, card(["Read", "Write"]), None)
    d = fm(out)
    assert d["tools"] == ["Read", "Write"] and d["effort"] == "low" and d["maxTurns"] == 20
    assert d["model"] == "haiku" and d["color"] == "red" and d["description"] == "Use when x."
    assert out.endswith("---\nBody text stays.\n")


def test_remove_stage_only_removes_and_renames_task(agent):
    d = fm(rc.render(agent, card(["Read", "Agent", "Grep"]), "remove"))
    assert d["tools"] == ["Read", "Agent"]  # Grep is an addition, not applied in the remove stage
    assert "effort" not in d


def test_add_stage_only_adds(agent):
    d = fm(rc.render(agent, card(["Read", "Grep"]), "add"))
    assert d["tools"] == ["Read", "Write", "Edit", "Bash", "Agent", "Grep"]


def test_limits_stage_leaves_tools(agent):
    d = fm(rc.render(agent, card(["Read"]), "limits"))
    assert d["tools"] == ["Read", "Write", "Edit", "Bash", "Task"] and d["maxTurns"] == 20


def test_none_limits_drop_the_keys(agent):
    once = rc.render(agent, card(["Read"]), None)
    agent.write_bytes(once.encode())
    d = fm(rc.render(agent, card(["Read"], effort=None, turns=None), None))
    assert "effort" not in d and "maxTurns" not in d


def test_crlf_is_preserved(tmp_path):
    p = tmp_path / "a.md"
    p.write_bytes(AGENT.replace("\n", "\r\n").encode())
    out = rc.render(p, card(["Read"]), None)
    assert "\n" not in out.replace("\r\n", "")


@pytest.mark.parametrize("tools,shell,name,needle", [
    (["Read", "Agent", "Bash"], "full", "x", "orchestrator holds Bash"),
    (["Read", "WebFetch", "Bash"], "full", "x", "web access with a shell"),
    (["Read", "Edit"], None, "ceo", "ceo holds Edit or Bash"),
    (["Read", "Bash"], None, "x", "shell must be set"),
    (["Read", "Grep"], "full", "x", "shell must be set"),
    (["Read", "TodoWrite"], None, "x", "unknown tool"),
])
def test_rule_errors(tools, shell, name, needle):
    assert any(needle in e for e in rc.rule_errors(name, card(tools, shell)))


def test_clean_card_has_no_rule_errors():
    assert rc.rule_errors("x", card(["Read", "Grep", "Glob", "Write", "Bash"], "sandboxed")) == []


def test_bad_limits_are_errors():
    assert rc.rule_errors("x", card(["Read"], effort="huge"))
    assert rc.rule_errors("x", card(["Read"], turns=0))


def test_repository_cards_are_current():
    assert rc.main(["role_cards.py", "check"]) == 0
