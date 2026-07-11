#!/usr/bin/env python3
"""
kleerer. — Health & Compo Score builder (v1.0)
Reads data/products_raw.json, computes scores + value metrics, writes data.js.
Every rule here mirrors METHODOLOGY.md — if you change one, change both.
"""
import json, math, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "data", "products_raw.json")
OUT = os.path.join(HERE, "..", "data.js")

# ---------- Purity penalties (tag prefixes so duplicates use suffixes: anticaking2 …) ----------
PURITY_PENALTIES = {
    "sucralose": 4, "acesulfame_k": 4,
    "hydrogenated_fat": 6, "undisclosed_doses": 6,
    "artificial_flavour": 2, "lecithin": 2, "thickener": 2,
    "bulking_filler": 2, "anticaking": 2, "coating": 2, "whitening_pigment": 2,
    "titanium_dioxide": 10,
}

def purity_score(tags):
    total = 0
    for t in tags:
        base = next((k for k in PURITY_PENALTIES if t.startswith(k)), None)
        if base is None:
            raise ValueError(f"Unknown purity tag: {t}")
        total += PURITY_PENALTIES[base]
    return max(0, 30 - total)

# ---------- Transparency ----------
def transparency_score(t):
    s = 0
    if t.get("coa_published"): s += 12
    if t.get("third_party_cert"): s += 10
    if t.get("branded_ingredient"): s += 4
    if t.get("full_label"): s += 4
    return s

# ---------- Dose scores per category ----------
def dose_score(p):
    if "dose_tier" in p:                      # manual override (multivitamins)
        return p["dose_tier"]
    c = p["category"]
    if c == "whey":
        d = p["active_per_100g"]
        return 20 if d >= 80 else 17 if d >= 75 else 14 if d >= 70 else 10
    if c == "creatine":
        g = p["active_per_serving_g"]
        return 20 if 3 <= g <= 5 else 12
    if c == "vitamin_d3":
        iu = p["active_per_unit"] * p["units_per_day"]
        if iu > 4000: return 8                # above EFSA UL
        if 800 <= iu <= 2000: return 20
        if 400 <= iu < 800: return 14
        if 200 <= iu < 400: return 10
        return 6
    if c == "magnesium":
        mg = p["active_per_unit"] * p["units_per_day"]
        if 100 <= mg <= 250: return 20        # within EFSA supplemental UL
        if 250 < mg <= 400: return 17
        if mg < 100: return 8
        return 12
    if c == "omega3":
        mg = p["active_per_unit"] * p["units_per_day"]
        return 20 if mg >= 1000 else 17 if mg >= 500 else 12 if mg >= 250 else 8
    raise ValueError(f"No dose rule for {c}")

# ---------- Value metrics ----------
STD = {
    "whey":       {"amount": 25,   "label": "€ / 25 g protein"},
    "creatine":   {"amount": 3,    "label": "€ / 3 g creatine"},
    "vitamin_d3": {"amount": 1000, "label": "€ / 1000 IU"},
    "magnesium":  {"amount": 300,  "label": "€ / 300 mg Mg"},
    "omega3":     {"amount": 500,  "label": "€ / 500 mg EPA+DHA"},
    "multivitamin": {"amount": None, "label": "€ / daily dose"},
}

def value_metrics(p):
    c, price = p["category"], p["price_eur"]
    if c in ("whey", "creatine"):
        total_active = p["pack_g"] * p["active_per_100g"] / 100.0
        servings = p["pack_g"] / p["serving_g"]
        cost_day = price / servings
        value_std = price / total_active * STD[c]["amount"]
        days = servings
    elif c == "multivitamin":
        days = p["units_pack"] / p["units_per_day"]
        cost_day = price / days
        value_std = cost_day
    else:
        total_active = p["units_pack"] * p["active_per_unit"]
        days = p["units_pack"] / p["units_per_day"]
        cost_day = price / days
        value_std = price / total_active * STD[c]["amount"]
    return round(cost_day, 3), round(value_std, 3), round(days), STD[c]["label"]

def grade(score):
    return "A" if score >= 80 else "B" if score >= 65 else "C" if score >= 50 else "D" if score >= 35 else "E"

def main():
    with open(RAW, encoding="utf-8") as f:
        raw = json.load(f)
    out, errors = [], []
    for p in raw["products"]:
        form = p["form_tier"]
        dose = dose_score(p)
        pur = purity_score(p["purity_tags"])
        tra = transparency_score(p["transparency"])
        for name, v, mx in (("form", form, 20), ("dose", dose, 20), ("purity", pur, 30), ("transparency", tra, 30)):
            if not (0 <= v <= mx):
                errors.append(f"{p['id']}: {name} score {v} out of range 0–{mx}")
        total = form + dose + pur + tra
        cost_day, value_std, days, value_label = value_metrics(p)
        q = dict(p)
        q["scores"] = {"form": form, "dose": dose, "purity": pur, "transparency": tra,
                       "total": total, "grade": grade(total)}
        q["value"] = {"cost_per_day": cost_day, "std": value_std, "std_label": value_label,
                      "days_per_pack": days}
        out.append(q)
    if errors:
        sys.exit("SCORING ERRORS:\n" + "\n".join(errors))

    cats = {}
    for q in out:
        cats.setdefault(q["category"], []).append(q)
    # rank within category (1 = best score; ties broken by value)
    for cat, items in cats.items():
        items.sort(key=lambda x: (-x["scores"]["total"], x["value"]["std"]))
        for i, it in enumerate(items, 1):
            it["rank_in_category"] = i

    payload = {
        "meta": {
            "snapshot": raw["snapshot"], "region": raw["region"], "currency": raw["currency"],
            "generated": datetime.date.today().isoformat(),
            "n_products": len(out),
            "methodology_version": "1.0",
        },
        "products": out,
    }
    js = ("// kleerer. dataset — generated by scripts/build_scores.py, do not edit by hand.\n"
          "// Source of truth: data/products_raw.json + METHODOLOGY.md\n"
          "const KLEERER_DATA = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(js)

    # console summary for verification
    print(f"{len(out)} products scored → {os.path.relpath(OUT, os.path.join(HERE, '..'))}")
    for cat, items in cats.items():
        print(f"\n[{cat}]")
        for it in items:
            s = it["scores"]
            print(f"  {s['grade']} {s['total']:>3}  (F{s['form']:>2} D{s['dose']:>2} P{s['purity']:>2} T{s['transparency']:>2})"
                  f"  {it['value']['std']:>7.3f} {it['value']['std_label']:<20} {it['brand']} — {it['name']}")

if __name__ == "__main__":
    main()
