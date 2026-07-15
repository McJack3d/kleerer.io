#!/usr/bin/env python3
"""
kleerer. — Health & Compo Score builder (v1.1)

Reads the curated v1 dataset (data/products_raw.json, already coded) AND the
French-market agent datasets (data/fr/*.json, free-text labels), normalizes the
latter through scripts/autotag.py (the same module the pipeline uses), scores
everything on one code path, and writes data.js.

Every rule mirrors METHODOLOGY.md. Change one, change both.
"""
import json, os, sys, datetime, hashlib, glob, re
import autotag

HERE = os.path.dirname(os.path.abspath(__file__))
V1   = os.path.join(HERE, "..", "data", "products_raw.json")
FRDIR= os.path.join(HERE, "..", "data", "fr")
OUT  = os.path.join(HERE, "..", "data.js")

# --------------------------------------------------------------------------- #
#  v1.2 purity penalties. Mirrors METHODOLOGY.md §2.
#  Heavier penalties for the most evidence-backed harms; sugar > any sweetener.
#  "banned" carries no penalty here — it is a RED CARD handled in main() (score→0).
# --------------------------------------------------------------------------- #
PURITY_PENALTIES = {
    "hydrogenated_fat": 25,     # fully hydrogenated (saturated); partial = trans = red card
    "undisclosed_doses": 10, "proprietary_blend": 10,
    "severe_antioxidant": 10,   # BHA/BHT — IARC 2B / endocrine suspicion
    "added_sugar": 8,           # strongest harm evidence of any additive here
    "sweetener_d": 6,           # sucralose, erythritol, xylitol — mechanistic/CV signal
    "sweetener_c": 4,           # aspartame, acesulfame-K — cohort cancer/CVD signal
    "artificial_colour": 3,     # azo dyes needing the EU child-attention warning
    "sweetener_b": 2,           # saccharin, cyclamate — reassuring but not natural
    "polyol": 2, "synthetic_carrier": 2, "artificial_flavour": 2,
    "lecithin": 2, "thickener": 2, "bulking_filler": 2, "anticaking": 2, "coating": 2,
    "unknown": 2,               # provisional — also surfaced for human review
    "banned": 0,                # red card handled separately in main()
}

def purity_score(tags):
    total = 0
    for t in tags:
        base = next((k for k in PURITY_PENALTIES if t.startswith(k)), None)
        if base is None:
            raise ValueError(f"Unknown purity tag: {t}")
        total += PURITY_PENALTIES[base]
    return max(0, 30 - total)

def transparency_score(t):
    s = 0
    if t.get("coa_published"): s += 12
    if t.get("third_party_cert"): s += 10
    if t.get("branded_ingredient"): s += 4
    if t.get("full_label"): s += 4
    return s

# --------------------------------------------------------------------------- #
#  Dose scores. Categories with entry-level logic carry a pre-computed
#  dose_tier (multivitamin from v1; zinc/vitamin_c/collagen/probiotics/
#  melatonin from normalize). The rest are formula-scored here.
# --------------------------------------------------------------------------- #
def dose_score(p):
    if "dose_tier" in p:
        return p["dose_tier"]
    c = p["category"]
    if c == "whey":
        d = p["active_per_100g"]; return 20 if d>=80 else 17 if d>=75 else 14 if d>=70 else 10
    if c == "creatine":
        g = p["active_per_serving_g"]; return 20 if 3<=g<=5 else 12
    if c == "vitamin_d3":
        iu = p["active_per_unit"]*p["units_per_day"]
        if iu>4000: return 8
        if 800<=iu<=2000: return 20
        if 400<=iu<800: return 14
        if 200<=iu<400: return 10
        return 6
    if c == "magnesium":
        mg = p["active_per_unit"]*p["units_per_day"]
        if 100<=mg<=250: return 20
        if 250<mg<=400: return 17
        if mg<100: return 8
        return 12
    if c == "omega3":
        mg = p["active_per_unit"]*p["units_per_day"]
        return 20 if mg>=1000 else 17 if mg>=500 else 12 if mg>=250 else 8
    raise ValueError(f"No dose rule for {c}")

# --------------------------------------------------------------------------- #
#  Value metrics — normalised to a standard daily dose per category. §Value.
# --------------------------------------------------------------------------- #
STD = {
    "whey":        {"amount": 25,   "label": "€ / 25 g protein"},
    "creatine":    {"amount": 3,    "label": "€ / 3 g creatine"},
    "vitamin_d3":  {"amount": 1000, "label": "€ / 1000 IU"},
    "magnesium":   {"amount": 300,  "label": "€ / 300 mg Mg"},
    "omega3":      {"amount": 500,  "label": "€ / 500 mg EPA+DHA"},
    "multivitamin":{"amount": None, "label": "€ / day"},
    "zinc":        {"amount": 15,   "label": "€ / 15 mg Zn"},
    "vitamin_c":   {"amount": 1000, "label": "€ / 1000 mg C"},
    "collagen":    {"amount": 10,   "label": "€ / 10 g collagen"},
    "probiotics":  {"amount": None, "label": "€ / day"},
    "melatonin":   {"amount": None, "label": "€ / day"},
}

def value_metrics(p):
    c, price = p["category"], p["price_eur"]
    std = STD[c]
    if "pack_g" in p:                                   # gram-based
        total_active = p["pack_g"] * p["active_per_100g"] / 100.0
        servings = p["pack_g"] / p["serving_g"]
        cost_day = price / servings
        value_std = price / total_active * std["amount"]
        days = servings
    else:                                               # unit-based
        days = p["units_pack"] / p["units_per_day"]
        cost_day = price / days
        if std["amount"] is None:
            value_std = cost_day
        else:
            total_active = p["units_pack"] * p["active_per_unit"]
            value_std = price / total_active * std["amount"]
    return round(cost_day, 3), round(value_std, 3), round(days), std["label"]

def grade(s):
    return "A" if s>=80 else "B" if s>=65 else "C" if s>=50 else "D" if s>=35 else "E"

# --------------------------------------------------------------------------- #
#  Provenance (v1.2). Country of MANUFACTURE per brand + a proximity malus.
#  IMPORTANT: this malus is kept OUT of the Health & Compo Score — a clean
#  German product is not "less healthy" than a French one. It is shown as a
#  separate, transparent axis (kleerer has a French-market focus). See
#  METHODOLOGY.md. Zones: FR (made in France) · EU (EU/EEA) · EXTRA_EU (outside).
# --------------------------------------------------------------------------- #
ZONE_MALUS = {"FR": 0, "EU": 1, "EXTRA_EU": 3, "UNKNOWN": 0}
PROVENANCE = {  # accent-free lowercase brand key -> (country, zone)
    "myprotein": ("United Kingdom", "EXTRA_EU"), "optimum nutrition": ("USA/UK", "EXTRA_EU"),
    "esn": ("Germany", "EU"), "bulk": ("United Kingdom", "EXTRA_EU"),
    "nutrimuscle": ("Belgium", "EU"), "prozis": ("Portugal", "EU"),
    "nutripure": ("France", "FR"), "nutri&co": ("France", "FR"), "nutri&co ": ("France", "FR"),
    "sunday natural": ("Germany", "EU"), "solgar": ("USA", "EXTRA_EU"),
    "now foods": ("USA", "EXTRA_EU"), "mivolis": ("Germany", "EU"),
    "novoma": ("France", "FR"), "whc": ("Belgium", "EU"), "norsan": ("Norway", "EU"),
    "foodspring": ("Germany", "EU"), "eiyolab": ("France", "FR"),
    "eric favre": ("France", "FR"), "protealpes": ("France", "FR"),
    "superphysique": ("France", "FR"), "am nutrition": ("France", "FR"),
    "yam nutrition": ("France", "FR"), "dynveo": ("France", "FR"), "unae": ("France", "FR"),
    "argalys": ("France", "FR"), "mium lab": ("France", "FR"), "biocyte": ("France", "FR"),
    "vitavea": ("France", "FR"), "onatera": ("France", "FR"), "d-lab": ("France", "FR"),
    "granions": ("France", "FR"), "forte pharma": ("France", "FR"), "juvamine": ("France", "FR"),
    "lescuyer": ("France", "FR"), "arkopharma": ("France", "FR"), "aroma-zone": ("France", "FR"),
    "aime": ("France", "FR"), "holidermie": ("France", "FR"), "colnatur": ("Spain", "EU"),
    "epycure": ("France", "FR"), "cuure": ("France", "FR"), "pileje": ("France", "FR"),
    "dijo": ("France", "FR"), "apyforme": ("France", "FR"), "sanofi": ("France", "FR"),
    "zzzquil": ("EU", "EU"),
}

def provenance_for(brand):
    n = autotag._norm(brand or "")
    for key, (country, zone) in PROVENANCE.items():
        if key.strip() and key.strip() in n:
            return {"country": country, "zone": zone, "malus": ZONE_MALUS[zone]}
    return {"country": None, "zone": "UNKNOWN", "malus": 0}

def price_tier(value_std, mean, std):
    """1–5 affordability band within a category (1 = cheapest per standard dose,
    5 = priciest), from the z-score of the normalized €/dose. Shown separately
    from the health score."""
    if std < 1e-9:
        return 3
    z = (value_std - mean) / std
    return 1 if z < -0.9 else 2 if z < -0.3 else 3 if z <= 0.3 else 4 if z <= 0.9 else 5

def slug(*parts):
    s = "-".join(parts).lower()
    s = re.sub(r"[àâä]", "a", s); s = re.sub(r"[éèêë]", "e", s)
    s = re.sub(r"[îï]", "i", s); s = re.sub(r"[ôö]", "o", s); s = re.sub(r"[ûü]", "u", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

# --------------------------------------------------------------------------- #
#  Normalize an agent (free-text) entry into the unified scored schema, using
#  the same autotag module the pipeline uses.
# --------------------------------------------------------------------------- #
MULTI_FORM = {"bioactive": (20, "Bioactive / chelated forms."),
              "standard": (12, "Standard vitamin/mineral forms."),
              "cheap": (8, "Cheap forms (oxides, cyanocobalamin, retinol).")}
MULTI_DOSE = {"physiological": (20, "Physiological ~100% NRV coverage."),
              "mixed": (15, "Mixed dosing."),
              "megadose_b": (12, "B-vitamin megadosing far above NRV."),
              "gaps": (10, "Notable gaps (missing minerals or low vitamin D).")}

def normalize(entry):
    c = entry["category"]
    p = dict(entry)
    p["id"] = slug(entry["brand"], entry["name"], entry.get("variant",""))
    # form tier
    if c == "multivitamin":
        p["form_tier"], p["form_note"] = MULTI_FORM.get(entry.get("form_quality","standard"))
        p["dose_tier"], p["dose_note"] = MULTI_DOSE.get(entry.get("dose_style","mixed"))
    else:
        p["form_tier"], p["form_note"] = autotag.infer_form_tier(c, entry.get("form",""), entry)
    # collagen daily dose for dosing/value
    if c == "collagen":
        if entry.get("format") == "powder" or "pack_g" in entry:
            p["collagen_g_day"] = entry.get("active_per_serving_g")
        else:
            p["collagen_g_day"] = entry.get("active_per_unit",0) * entry.get("units_per_day",1)
    # dose tier for override categories
    if c in ("zinc","vitamin_c","collagen","probiotics","melatonin"):
        p["dose_tier"], p["dose_note"] = autotag.infer_dose_tier(c, p)
    # purity (v1.2: also returns red-card substances + unrecognised items to review)
    p["purity_tags"], p["additives_detail"], p["banned"], p["review_flags"] = \
        autotag.tags_from_additives(entry.get("additives"))
    # transparency
    p["transparency"] = {
        "coa_published": bool(entry.get("coa_published")),
        "third_party_cert": bool(entry.get("third_party_cert")),
        "branded_ingredient": entry.get("branded_ingredient"),
        "full_label": bool(entry.get("full_label", True)),
    }
    p.setdefault("flags", [])
    p.setdefault("notes", "")
    return p

def label_hash(p):
    """Stable fingerprint of the label facts we score. The pipeline diffs this
    across daily snapshots to detect silent reformulations."""
    basis = {
        "form": p.get("form"), "additives": sorted(p.get("additives_detail", [])),
        "certifications": sorted(p.get("certifications", [])),
        "active_per_serving_g": p.get("active_per_serving_g"),
        "active_per_100g": p.get("active_per_100g"),
        "active_per_unit": p.get("active_per_unit"),
        "units_per_day": p.get("units_per_day"),
    }
    return hashlib.sha1(json.dumps(basis, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]

# --------------------------------------------------------------------------- #
def main():
    with open(V1, encoding="utf-8") as f:
        v1 = json.load(f)
    snapshot = v1["snapshot"]

    products = []
    for p in v1["products"]:
        p.setdefault("id", slug(p["brand"], p["name"], p.get("variant","")))
        products.append(p)
    for path in sorted(glob.glob(os.path.join(FRDIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            for entry in json.load(f):
                products.append(normalize(entry))

    errors, seen = [], {}
    for p in products:
        if p["id"] in seen:
            errors.append(f"duplicate id: {p['id']}")
        seen[p["id"]] = True
        # Re-tag EVERY product from its additives list through the ONE v1.2 tagger,
        # so curated (v1) and scraped (FR) products are scored identically and the
        # new registry (red cards, sweetener tiers, review) applies uniformly.
        src_additives = p.get("additives_detail") or p.get("additives") or []
        p["purity_tags"], p["additives_detail"], p["banned"], p["review_flags"] = \
            autotag.tags_from_additives(src_additives)
        p["provenance"] = provenance_for(p.get("brand"))

        form = p["form_tier"]; dose = dose_score(p)
        pur = purity_score(p["purity_tags"]); tra = transparency_score(p["transparency"])
        for name, v, mx in (("form",form,20),("dose",dose,20),("purity",pur,30),("transparency",tra,30)):
            if not (0 <= v <= mx):
                errors.append(f"{p['id']}: {name} score {v} out of range 0–{mx}")
        red_card = bool(p["banned"])
        total = 0 if red_card else form + dose + pur + tra
        g = "E" if red_card else grade(total)
        cost_day, value_std, days, vlabel = value_metrics(p)
        p["scores"] = {"form":form,"dose":dose,"purity":pur,"transparency":tra,
                       "total":total,"grade":g,"red_card":red_card,
                       "banned_substances":p["banned"]}
        p["value"] = {"cost_per_day":cost_day,"std":value_std,"std_label":vlabel,"days_per_pack":days}
        p["label_hash"] = label_hash(p)
    if errors:
        sys.exit("SCORING ERRORS:\n" + "\n".join(errors))

    cats = {}
    for p in products:
        cats.setdefault(p["category"], []).append(p)
    for items in cats.values():
        items.sort(key=lambda x:(-x["scores"]["total"], x["value"]["std"]))
        for i,it in enumerate(items,1):
            it["rank_in_category"] = i
        # price tier 1–5, per category, from the €/standard-dose distribution
        vals = [it["value"]["std"] for it in items]
        mean = sum(vals)/len(vals)
        var = sum((v-mean)**2 for v in vals)/len(vals)
        std = var ** 0.5
        for it in items:
            it["value"]["price_tier"] = price_tier(it["value"]["std"], mean, std)

    n_red = sum(1 for p in products if p["scores"]["red_card"])
    n_review = sum(1 for p in products if p.get("review_flags"))
    payload = {
        "meta": {"snapshot":snapshot,"region":"EU/FR","currency":"EUR",
                 "generated":datetime.date.today().isoformat(),
                 "n_products":len(products),"n_categories":len(cats),
                 "n_red_cards":n_red,"n_needs_review":n_review,
                 "methodology_version":"1.2"},
        "products": products,
    }
    js = ("// kleerer. dataset — generated by scripts/build_scores.py (v1.2). Do not edit by hand.\n"
          "// Sources of truth: data/products_raw.json + data/fr/*.json + METHODOLOGY.md\n"
          "const KLEERER_DATA = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n")
    with open(OUT,"w",encoding="utf-8") as f:
        f.write(js)

    print(f"{len(products)} products across {len(cats)} categories → {os.path.relpath(OUT, os.path.join(HERE,'..'))}")
    for cat in sorted(cats):
        items = cats[cat]
        print(f"\n[{cat}]  ({len(items)})")
        for it in items:
            s = it["scores"]
            print(f"  {s['grade']} {s['total']:>3}  F{s['form']:>2} D{s['dose']:>2} P{s['purity']:>2} T{s['transparency']:>2}"
                  f"  {it['value']['std']:>8.3f} {it['value']['std_label']:<18} {it['brand']} — {it['name']}")

if __name__ == "__main__":
    main()
