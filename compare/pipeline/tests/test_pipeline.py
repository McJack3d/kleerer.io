#!/usr/bin/env python3
"""
Offline test suite for the kleerer. pipeline. No network.
Run: python3 -m pytest tests/ -q     (or: python3 tests/test_pipeline.py)
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
sys.path.insert(0, PIPE)
sys.path.insert(0, os.path.join(PIPE, "..", "scripts"))

import extract, snapshot, diff
import autotag
FIX = os.path.join(HERE, "fixtures")


def _read(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return f.read()


# ----------------------------- extraction ---------------------------------- #
def test_extract_jsonld():
    e = extract.extract(_read("jsonld_product.html"), "http://x")
    assert e["price"] == 14.90
    assert e["currency"] == "EUR"
    assert e["brand"] == "Nutripure"
    assert e["gtin"] == "3770011503087"
    assert e["availability"] == "InStock"
    assert e["source"] == "json-ld"


def test_extract_meta_french_comma():
    e = extract.extract(_read("meta_product.html"), "http://x")
    assert e["price"] == 11.90          # "11,90" parsed correctly
    assert e["currency"] == "EUR"
    assert e["source"] == "meta"


def test_extract_text_fallback():
    e = extract.extract(_read("text_only.html"), "http://x")
    assert e["price"] == 29.95
    assert e["source"] == "text-fallback"


def test_price_thousands_format():
    assert extract._to_float("1.299,00") == 1299.00
    assert extract._to_float("29.90") == 29.90
    assert extract._to_float("29,90") == 29.90


# ----------------------------- auto-tagger --------------------------------- #
def test_autotag_penalties():
    assert autotag.classify_additive("édulcorant : sucralose") == "sucralose"
    assert autotag.classify_additive("acésulfame K") == "acesulfame_k"
    assert autotag.classify_additive("sirop de glucose") == "added_sugar"
    assert autotag.classify_additive("maltitol") == "polyol"
    assert autotag.classify_additive("colorant azoïque : E110") == "artificial_colour"
    assert autotag.classify_additive("stéarate de magnésium") == "anticaking"
    assert autotag.classify_additive("lécithine de tournesol") == "lecithin"


def test_autotag_neutrals():
    for neutral in ["huile de colza vierge bio", "gélule végétale (HPMC)",
                    "arôme naturel de vanille", "extrait riche en tocophérols",
                    "glycérine", "acide citrique"]:
        assert autotag.classify_additive(neutral) is None, neutral


def test_autotag_unknown_fails_safe():
    # never silently ignore: unknown → conservative filler penalty
    assert autotag.classify_additive("zorblax 3000") == "bulking_filler"


def test_form_tiers():
    assert autotag.infer_form_tier("magnesium", "oxyde de magnésium marin")[0] == 4
    assert autotag.infer_form_tier("magnesium", "bisglycinate chélaté")[0] == 20
    assert autotag.infer_form_tier("magnesium", "oxyde microencapsulé Magshape")[0] == 10
    assert autotag.infer_form_tier("omega3", "rTG concentré EPAX")[0] == 20
    assert autotag.infer_form_tier("omega3", "ethyl ester concentrate")[0] == 10
    assert autotag.infer_form_tier("zinc", "picolinate de zinc")[0] == 20
    assert autotag.infer_form_tier("zinc", "oxyde de zinc")[0] == 4
    assert autotag.infer_form_tier("collagen", "tripeptides marins")[0] == 20


def test_dose_tiers():
    assert autotag.infer_dose_tier("zinc", {"active_per_unit": 30, "units_per_day": 1})[0] == 12  # >UL
    assert autotag.infer_dose_tier("zinc", {"active_per_unit": 15, "units_per_day": 1})[0] == 20
    assert autotag.infer_dose_tier("melatonin", {"active_per_unit": 1.9, "units_per_day": 1})[0] == 20
    assert autotag.infer_dose_tier("collagen", {"collagen_g_day": 10})[0] == 20
    assert autotag.infer_dose_tier("collagen", {"collagen_g_day": 0.3})[0] == 8


# ----------------------------- snapshot + diff ----------------------------- #
def test_content_hash_stable_and_sensitive():
    a = {"price": 19.90, "currency": "EUR", "availability": "InStock", "name": "X"}
    b = dict(a)
    assert snapshot.content_hash(a) == snapshot.content_hash(b)
    b["price"] = 21.90
    assert snapshot.content_hash(a) != snapshot.content_hash(b)


def test_diff_detects_changes():
    prev = {
        "p1": {"id": "p1", "price": 19.90, "currency": "EUR", "availability": "InStock", "label_hash": "aaa"},
        "p2": {"id": "p2", "price": 10.00, "currency": "EUR", "availability": "InStock", "label_hash": "bbb"},
        "gone": {"id": "gone", "price": 5.0, "currency": "EUR", "availability": "InStock", "label_hash": "ccc"},
    }
    curr = {
        "p1": {"id": "p1", "price": 24.90, "currency": "EUR", "availability": "InStock", "label_hash": "aaa"},  # price up
        "p2": {"id": "p2", "price": 10.00, "currency": "EUR", "availability": "OutOfStock", "label_hash": "zzz"},  # avail + reformulation
        "new": {"id": "new", "price": 9.0, "currency": "EUR", "availability": "InStock", "label_hash": "ddd"},   # new
    }
    kinds = sorted(c["kind"] for c in diff.diff_days(prev, curr))
    assert kinds == sorted(["price", "availability", "reformulation", "disappeared", "new"])
    price = [c for c in diff.diff_days(prev, curr) if c["kind"] == "price"][0]
    assert price["pct"] == 25.1  # (24.90-19.90)/19.90*100


def test_report_renders():
    r = diff.render_report("2026-07-11", [{"id": "x", "kind": "price", "detail": "a→b"}], 8)
    assert "change report" in r and "price (1)" in r


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in fns:
        fn(); passed += 1
        print(f"  ok  {fn.__name__}")
    print(f"\n{passed}/{len(fns)} tests passed")
