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


def card(tools, shell=None, effort="low", turns=20, model="haiku", scope=("x/",), activation="department"):
    return {"file": "agents/a.md", "activation": activation, "enforced": {"tools": tools, "shell": shell, "model": model,
                                                "effort": effort, "maxTurns": turns,
                                                "write_scope": list(scope) if scope is not None else None}}


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


def test_guard_json_matches_the_yaml_cards():
    import json
    cards = rc.load_cards()
    slim = json.loads(rc.GUARD_CARDS.read_text(encoding="utf-8"))["agents"]
    assert set(slim) == set(cards)
    for name, c in cards.items():
        assert slim[name]["file"] == c["file"]
        assert slim[name]["descriptive"]["write_scope_note"] == c["descriptive"].get("write_scope_note", "")


def test_stale_guard_json_fails_check(tmp_path, monkeypatch):
    stale = tmp_path / "role-cards.json"
    stale.write_text('{"agents": {}}\n', encoding="utf-8")
    monkeypatch.setattr(rc, "GUARD_CARDS", stale)
    assert rc.main(["role_cards.py", "check"]) == 1


def test_guard_json_is_lf_and_sorted():
    text = rc.guard_json(rc.load_cards())
    assert "\r" not in text and text.endswith("}\n")
    assert rc.GUARD_CARDS.read_bytes().decode("utf-8").replace("\r\n", "\n") == text


def test_every_qualified_reference_resolves():
    """Each `devsecops-agency:<name>` in agents/, skills/ and councils/ names a role card or a skill.

    A reference to a missing agent is refused at dispatch time, so it is caught here instead.
    Placeholders such as `devsecops-agency:<name>` are allowed."""
    import json
    import re
    root = rc.ROOT
    cards = set(json.loads((root / "hooks" / "role-cards.json").read_text(encoding="utf-8"))["agents"])
    skills = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    bad = []
    for folder in ("agents", "skills", "councils"):
        for p in (root / folder).rglob("*.md"):
            text = p.read_bytes().decode("utf-8")
            for m in re.finditer(r"devsecops-agency:([a-z0-9-]+)(?![a-z0-9>-])", text):
                if m.group(1) not in cards and m.group(1) not in skills:
                    bad.append(f"{p.relative_to(root).as_posix()}: {m.group(1)}")
    assert not bad, bad


@pytest.mark.parametrize("scope", [None, [], [""]])
def test_write_scope_is_required(scope):
    assert any("write_scope" in e for e in rc.rule_errors("x", card(["Read", "Write"], scope=scope)))


@pytest.mark.parametrize("entry", ["/etc/", "C:/x", "../up/", "a/../../b"])
def test_write_scope_must_stay_inside_the_project(entry):
    assert any("relative" in e for e in rc.rule_errors("x", card(["Read", "Write"], scope=[entry])))


def test_orchestrator_may_not_write_everywhere():
    assert any("rule 5" in e for e in rc.rule_errors("x", card(["Read", "Write", "Agent"], scope=["*"])))


@pytest.mark.parametrize("value", [None, "specialist", "Core"])
def test_activation_must_be_a_part2_tier(value):
    assert any("activation" in e for e in rc.rule_errors("a", card(["Read"], activation=value)))


def test_every_card_has_an_activation_tier():
    cards = rc.load_cards()
    assert {c["activation"] for c in cards.values()} <= rc.ACTIVATION
