"""Routing rule ported from JARVIS-2.0/brain/orchestrator.py, plus the two documented fixes."""

import pytest

from voice.brain.router import (
    HEAVY_KEYWORDS,
    TOOL_KEYWORDS,
    Route,
    RouterRules,
    Target,
    choose_target,
    classify,
    decide,
)


def test_plain_conversation_is_chat():
    assert classify("good morning, how are you") is Route.CHAT
    assert classify("") is Route.CHAT
    assert classify("   ") is Route.CHAT


@pytest.mark.parametrize("word", HEAVY_KEYWORDS)
def test_every_heavy_keyword_routes_heavy(word):
    assert classify(f"please {word} this for me") is Route.HEAVY


@pytest.mark.parametrize("word", TOOL_KEYWORDS)
def test_every_tool_keyword_routes_tool_when_tools_exist(word):
    assert classify(f"can you {word} it", has_tools=True) is Route.TOOL


def test_tool_keywords_without_tools_do_not_route_tool():
    # Same rule as the prototype: the tool branch only fires when tools were offered.
    assert classify("search the web for the score", has_tools=False) is Route.CHAT


def test_tool_beats_heavy_when_both_match():
    assert classify("run the code", has_tools=True) is Route.TOOL
    assert classify("run the code", has_tools=False) is Route.HEAVY


def test_case_insensitive():
    assert classify("EXPLAIN quantum tunnelling") is Route.HEAVY
    assert classify("Search for it", has_tools=True) is Route.TOOL


def test_whole_word_matching_fixes_prototype_false_positives():
    # The prototype's substring test misrouted all three of these.
    assert classify("recall my last note", has_tools=True) is Route.CHAT  # "call" inside "recall"
    assert classify("that sounds reasonable") is Route.CHAT  # "reason" inside "reasonable"
    assert classify("decode this message") is Route.CHAT  # "code" inside "decode"
    assert classify("open the website", has_tools=True) is Route.CHAT  # "web" inside "website"


def test_zip_code_is_a_known_limit_of_keyword_routing():
    # "code" is a whole word here, so the keyword rule still calls it heavy.
    # Kept as a test so the behaviour is visible, not hidden.
    assert classify("what is the zip code for Boston") is Route.HEAVY


def test_choose_target_matrix():
    assert choose_target(Route.CHAT, cloud_available=True) is Target.LOCAL
    assert choose_target(Route.CHAT, cloud_available=False) is Target.LOCAL
    assert choose_target(Route.HEAVY, cloud_available=True) is Target.CLOUD
    assert choose_target(Route.HEAVY, cloud_available=False) is Target.LOCAL
    assert choose_target(Route.TOOL, cloud_available=True) is Target.CLOUD
    assert choose_target(Route.TOOL, cloud_available=False) is Target.LOCAL


def test_decide_combines_both_steps():
    d = decide("analyze this log", cloud_available=True)
    assert d.route is Route.HEAVY and d.target is Target.CLOUD
    d = decide("analyze this log", cloud_available=False)
    assert d.route is Route.HEAVY and d.target is Target.LOCAL
    d = decide("hi there", cloud_available=True)
    assert d.route is Route.CHAT and d.target is Target.LOCAL


def test_custom_rules_from_env_style_lists():
    rules = RouterRules(tool_keywords=("fetch",), heavy_keywords=("prove",))
    assert classify("fetch the report", has_tools=True, rules=rules) is Route.TOOL
    assert classify("prove the lemma", rules=rules) is Route.HEAVY
    assert classify("explain this", rules=rules) is Route.CHAT  # default keyword no longer applies


def test_empty_rule_list_matches_nothing():
    rules = RouterRules(tool_keywords=(), heavy_keywords=())
    assert classify("run search execute code", has_tools=True, rules=rules) is Route.CHAT


def test_regex_special_characters_in_keywords_are_escaped():
    rules = RouterRules(tool_keywords=("c++",), heavy_keywords=("a.b",))
    assert classify("compile my c++ file", has_tools=True, rules=rules) is Route.TOOL
    assert classify("what is axb", rules=rules) is Route.CHAT
