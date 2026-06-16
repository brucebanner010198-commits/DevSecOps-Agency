from broker.stylometry import normalize_style
from broker.surrogates import SurrogateMap, find_real_entities


REAL = (
    "Hey there, I'm Solomon Joseph (solomon@acme.com). "
    "Charge card 4242 4242 4242 4242, call +1 555 867 5309, "
    "and save to /Users/sj1136/secret.txt — Cheers, Sol"
)
NAMES = ["Solomon Joseph", "Sol"]


def test_mask_removes_all_real_entities():
    smap = SurrogateMap()
    masked = smap.mask(REAL, names=NAMES)
    for entity in ("Solomon Joseph", "solomon@acme.com", "4242 4242 4242 4242",
                   "/Users/sj1136/secret.txt", "Sol"):
        assert entity not in masked, f"{entity!r} leaked into masked text"


def test_unmask_is_inverse():
    smap = SurrogateMap()
    masked = smap.mask(REAL, names=NAMES)
    assert smap.unmask(masked) == REAL


def test_surrogates_are_stable_within_a_map():
    smap = SurrogateMap()
    s1 = smap.mask("email solomon@acme.com twice: solomon@acme.com", names=[])
    # the same real value maps to the same surrogate
    assert s1.count("user1@example.test") == 2


def test_find_real_entities_detects_patterns():
    found = find_real_entities(REAL, NAMES)
    assert "solomon@acme.com" in found
    assert any("/Users/sj1136" in f for f in found)
    assert "Solomon Joseph" in found


def test_masked_text_has_no_real_entities_left():
    smap = SurrogateMap()
    masked = smap.mask(REAL, names=NAMES)
    assert [e for e in find_real_entities(REAL, NAMES) if e in masked] == []


def test_style_normalization_strips_fingerprints():
    out = normalize_style("Hey there, all good!! Cheers, Sol")
    assert "Hey there" not in out
    assert "Cheers" not in out
    assert "!!" not in out
