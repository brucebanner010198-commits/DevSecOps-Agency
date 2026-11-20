"""Regression tests for scripts/frontmatter.py (run: python -m pytest scripts)."""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import frontmatter as fmx  # noqa: E402


def fix(fm: str):
    return fmx.repair(fm, "\n")


def test_repairs_multiline_example_description():
    fm = (
        "name: a\n"
        "description: Use when: x\n"
        "\n"
        "<example>\n"
        "user: \"hi\"\n"
        "</example>\n"
        "\n"
        "model: haiku\n"
        'tools: ["Read"]'
    )
    new, original = fix(fm)
    data = yaml.safe_load(new)
    assert data["description"] == original == 'Use when: x\n\n<example>\nuser: "hi"\n</example>'
    assert data["model"] == "haiku" and data["tools"] == ["Read"]
    assert new.endswith('\n\nmodel: haiku\ntools: ["Read"]')  # separator kept


def test_crlf_preserved():
    fm = "name: a\r\ndescription: Use when: x\r\nmodel: haiku"
    new, _ = fmx.repair(fm, "\r\n")
    assert "\r\n" in new and "\n" not in new.replace("\r\n", "")


def test_refuses_unknown_key_swallowed():
    assert isinstance(fix("name: a\ndescription: Use when: x\nallowed-tools: Read\nmodel: haiku"), str)


def test_refuses_unclosed_example():
    assert isinstance(fix("name: a\ndescription: Emits <example> tags. Use when: x\nmodel: haiku"), str)


def test_refuses_prose_line_starting_with_key():
    # `model:` in prose ends the span early; the real `model:` then duplicates it.
    fm = "name: a\ndescription: Use when: x\nmodel: picks the cheapest tier\nmore prose\nmodel: haiku"
    assert isinstance(fix(fm), str)


def test_split_requires_whole_line_delimiter():
    text = "---\nname: a\ndescription: x\n----- example\nmodel: haiku\n---\nbody\n"
    fm, rest, _ = fmx.split(text)
    assert "model: haiku" in fm and rest.startswith("\n---\nbody")


def test_refuses_non_plain_first_value():
    for first in ['"Use when: x"', "'q'", ">", "|", "&a x", "#c"]:
        assert isinstance(fix(f"name: a\ndescription: {first}\nmodel: haiku"), str), first


def test_keeps_trailing_whitespace_and_multiple_blank_lines():
    fm = "name: a\ndescription: Use when: x  \n\n\nmodel: haiku"
    new, original = fix(fm)
    assert original == "Use when: x  "
    assert new.endswith("\n\n\nmodel: haiku")


def test_refuses_comment_and_indented_lines():
    assert isinstance(fix("name: a\ndescription: Use when: x\n# c\nmodel: haiku"), str)
    assert isinstance(fix("name: a\ndescription: Use when: x\n  more\nmodel: haiku"), str)
    assert isinstance(fix("name: a\ndescription: Use when: x # note\nmodel: haiku"), str)


def test_hash_inside_example_is_prose():
    fm = 'name: a\ndescription: Use when: x\n<example>\nuser: "Append ## Post-build audit"\n</example>\nmodel: haiku'
    new, original = fix(fm)
    assert "## Post-build audit" in yaml.safe_load(new)["description"]


def test_example_open_close_on_one_line():
    fm = "name: a\ndescription: Use when: x\n<example>a</example> <example>\nuser: y\n</example>\nmodel: haiku"
    new, _ = fix(fm)
    assert yaml.safe_load(new)["model"] == "haiku"


def test_refuses_duplicate_key_with_different_value_style():
    assert isinstance(fix("name: x\ndescription: a: b\ntools: [Read]\ntools:\n  - Agent"), str)


def test_description_only_frontmatter_is_fixed():
    new, original = fix("description: a: b\n")
    assert original == "a: b" and yaml.safe_load(new)["description"] == "a: b"


def test_description_mapping_is_not_accepted():
    assert fmx.parses("name: a\ndescription:\n  Use when: x") is not None
