#!/usr/bin/env python3
"""
Extract structured product facts from a fetched HTML page.

Priority order (most reliable first):
  1. schema.org JSON-LD  (<script type="application/ld+json">)  — price, availability, name, brand, GTIN
  2. OpenGraph / product meta tags (og:price:amount, product:price:amount)
  3. plain-text price fallback (regex, last resort)

Ingredient/additive extraction from arbitrary merchant HTML is deliberately NOT
attempted here in v0 — it is brittle and better sourced from OpenFoodFacts
(offtake.py) or a per-merchant adapter (Phase 1). What we reliably get today is
the thing that changes most often and matters most for the archive: PRICE and
AVAILABILITY, plus enough identity to match a product.

Standard library only.
"""
import json, re, html
from urllib.parse import urlparse

PRICE_META = [
    r'<meta[^>]+property=["\']product:price:amount["\'][^>]+content=["\']([\d.,]+)["\']',
    r'<meta[^>]+property=["\']og:price:amount["\'][^>]+content=["\']([\d.,]+)["\']',
    r'<meta[^>]+itemprop=["\']price["\'][^>]+content=["\']([\d.,]+)["\']',
]
CURRENCY_META = r'<meta[^>]+(?:product:price:currency|og:price:currency)["\'][^>]+content=["\']([A-Z]{3})["\']'


def _to_float(s):
    if s is None:
        return None
    s = str(s).strip().replace(" ", "").replace(" ", "")
    # handle "1.299,00" and "29,90" and "29.90"
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return round(float(re.sub(r"[^\d.]", "", s)), 2)
    except ValueError:
        return None


def _iter_jsonld(html_text):
    for m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                         html_text, re.S | re.I):
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        yield from (data if isinstance(data, list) else [data])
        if isinstance(data, dict) and "@graph" in data:
            yield from data["@graph"]


def _find_product(node):
    t = node.get("@type", "")
    types = t if isinstance(t, list) else [t]
    return any(str(x).lower() == "product" for x in types)


def extract(html_text, url=""):
    """Return dict: {name, brand, price, currency, availability, gtin, source}."""
    out = {"name": None, "brand": None, "price": None, "currency": None,
           "availability": None, "gtin": None, "source": None, "url": url}

    # 1) JSON-LD
    for node in _iter_jsonld(html_text):
        if not isinstance(node, dict) or not _find_product(node):
            continue
        out["name"] = out["name"] or node.get("name")
        brand = node.get("brand")
        if isinstance(brand, dict):
            brand = brand.get("name")
        out["brand"] = out["brand"] or brand
        out["gtin"] = out["gtin"] or node.get("gtin13") or node.get("gtin") or node.get("gtin8")
        offers = node.get("offers")
        if isinstance(offers, list):
            offers = offers[0] if offers else None
        if isinstance(offers, dict):
            out["price"] = _to_float(offers.get("price") or offers.get("lowPrice"))
            out["currency"] = offers.get("priceCurrency")
            avail = offers.get("availability", "")
            out["availability"] = avail.split("/")[-1] if isinstance(avail, str) else None
            if out["price"] is not None:
                out["source"] = "json-ld"
        if out["price"] is not None:
            return {k: (html.unescape(v) if isinstance(v, str) else v) for k, v in out.items()}

    # 2) meta tags
    for pat in PRICE_META:
        m = re.search(pat, html_text, re.I)
        if m:
            out["price"] = _to_float(m.group(1))
            cm = re.search(CURRENCY_META, html_text, re.I)
            out["currency"] = cm.group(1) if cm else out["currency"]
            out["source"] = "meta"
            break

    # 3) plain-text euro fallback
    if out["price"] is None:
        m = re.search(r'(\d{1,3}(?:[.,]\d{2}))\s*€|€\s*(\d{1,3}(?:[.,]\d{2}))', html_text)
        if m:
            out["price"] = _to_float(m.group(1) or m.group(2))
            out["currency"] = out["currency"] or "EUR"
            out["source"] = "text-fallback"

    if not out["name"]:
        t = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.S | re.I)
        if t:
            out["name"] = html.unescape(t.group(1)).strip()[:120]
    return out
