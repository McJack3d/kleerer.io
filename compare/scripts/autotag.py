#!/usr/bin/env python3
"""
kleerer. — auto-tagger / normalization core (v1.1)

Turns a free-text supplement label (additives list + form description, FR or EN)
into the coded fields the Health & Compo Score needs:
  - purity_tags        (penalty tags, see METHODOLOGY.md)
  - additives_detail   (cleaned human-readable list)
  - form_tier          (0–20 form-quality score, per category)
  - form_note

This same module is imported by the collection pipeline (pipeline/), so a scraped
product and a hand-curated one go through EXACTLY the same normalization. That is
the point: the rules live in one auditable place.
"""
import re, unicodedata

# ----------------------------------------------------------------------------- #
#  Additive classification: map a free-text ingredient string to ONE penalty tag
# ----------------------------------------------------------------------------- #
# Order matters: first matching rule wins (worst offenders first). A rule is
# (tag, [keywords]). Keywords are matched on a normalized (accent-free, lower)
# string. `None` tag => neutral ingredient (no penalty).

_NEUTRAL = "neutral"

# Capsule/shell materials and benign carriers are neutral even though they share
# keywords (e.g. "cellulose") with fillers — detected first.
CAPSULE_HINTS = ["gelule", "capsule", "tunique", "k-caps", "kcaps", "drcaps",
                 "pullulan", "hpmc vegetal", "gelatine", "gelatin", "softgel",
                 "enveloppe", "vegecaps"]

RULES = [
    ("titanium_dioxide", ["dioxyde de titane", "titanium dioxide", "e171"]),
    ("hydrogenated_fat", ["hydrogen", "hydrogene"]),
    ("added_sugar",      ["sirop de glucose", "glucose syrup", "sucre", "sugar",
                          "saccharose", "sirop de", "dextrose"]),
    ("sucralose",        ["sucralose"]),
    ("acesulfame_k",     ["acesulfame", "acesulphame", "ace-k", "ace k"]),
    ("artificial_sweetener", ["aspartame", "saccharin", "saccharinate",
                              "cyclamate", "edulcorant de synthese"]),
    ("polyol",           ["maltitol", "sorbitol", "xylitol", "erythritol",
                          "polyol", "isomalt", "mannitol"]),
    ("artificial_colour",["azoique", "e102", "e104", "e110", "e122", "e124",
                          "e129", "e133", "e151", "colorant azo"]),
    ("synthetic_carrier",["polyethylene glycol", "peg ", "(peg)", "polyethylene-glycol"]),
    ("artificial_flavour",["arome artificiel", "artificial flavour",
                           "artificial flavor", "aromatisant artificiel"]),
    ("lecithin",         ["lecithine", "lecithin"]),
    ("thickener",        ["gomme xanthane", "xanthan", "gomme guar", "guar",
                          "gomme gellane", "gellan", "carraghenane", "carrageenan"]),
    ("bulking_filler",   ["maltodextrine", "maltodextrin", "amidon", "starch",
                          "cellulose microcristalline", "microcrystalline cellulose",
                          "phosphate dicalcique", "phosphate tricalcique",
                          "dicalcium phosphate", "gomme d'acacia", "gomme arabique",
                          "acacia", "caroube", "carob", "citrate de calcium"]),
    ("anticaking",       ["stearate de magnesium", "magnesium stearate",
                          "sels de magnesium d'acides gras", "acide stearique",
                          "stearic", "dioxyde de silicium", "silicon dioxide",
                          "silice", "silica", "talc", "carbonate de magnesium"]),
    ("coating",          ["enrobage", "coating", "cire de carnauba", "carnauba",
                          "shellac", "e903", "e904", "carbonate de calcium",
                          "hydroxypropylcellulose", "hydroxypropylmethylcellulose"]),
]

# Neutral keywords: recognised and explicitly NOT penalised.
NEUTRAL_KEYWORDS = [
    "eau", "water", "glycerine", "glycerin", "glycerol", "glycerol",
    "huile de colza", "huile d'olive", "huile de coco", "huile mct", "mct",
    "huile de tournesol", "huile vegetale", "triglycerides a chaine moyenne",
    "tocopherol", "tocopherols", "vitamine e", "romarin", "rosemary",
    "acide citrique", "citric acid", "citrate de sodium", "arome naturel",
    "natural flavour", "natural flavor", "lactase", "tolerase", "sel", "salt",
    "betterave", "spiruline", "carthame", "carotte", "sureau", "curcuma",
    "concentres de", "jus de", "bioflavonoide", "flavonoide", "microbiomex",
    "inuline", "fos", "fructo-oligosaccharide", "prebiotique", "son de riz",
    "amidon de riz", "riz", "antioxydant naturel", "ascorbyl", "e300",
    "extrait de romarin", "poudre de fruit", "cacao", "vitamine", "vitamin",
    "b8", "b12", "b6", "saccharomyces", "acides gras",
]


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return s.lower().strip()


def classify_additive(raw: str):
    """Return a penalty tag string, or None if neutral. Whole-string match."""
    n = _norm(raw)
    # capsule / shell material → neutral
    if any(h in n for h in CAPSULE_HINTS) and not any(
        k in n for k in ["stearate", "silice", "silica", "dioxyde", "maltodextrine"]
    ):
        return None
    for tag, keys in RULES:
        if any(k in n for k in keys):
            # guard: "carbonate de calcium (whitener)" as coating is fine, but a
            # bare neutral like "arome naturel" must not be caught by 'arome'
            return tag
    if any(k in n for k in NEUTRAL_KEYWORDS):
        return None
    # Unknown ingredient: treat as a minor filler so we never silently ignore it,
    # but flag low so it's visible. Conservative -2.
    return "bulking_filler"


def tags_from_additives(additives):
    """additives: list[str] -> (purity_tags[list], additives_detail[list])."""
    tags, detail = [], []
    for a in additives or []:
        t = classify_additive(a)
        if t:
            tags.append(t)
        detail.append(a)
    return tags, detail


# ----------------------------------------------------------------------------- #
#  Form-quality tiers per category (0–20). Encodes METHODOLOGY.md §1a.
# ----------------------------------------------------------------------------- #
def infer_form_tier(cat, form, entry=None):
    f = _norm(form or "")
    entry = entry or {}

    if cat == "whey":
        if "native" in f and ("isolat" in f or "isolate" in f): return 20, "Native isolate — the top milk-protein form."
        if "native" in f: return 20, "Native whey from milk, not a cheese by-product."
        if "isolat" in f or "isolate" in f or "wpi" in f: return 18, "Isolate-led."
        if "blend" in f or ("concentr" in f and "isolat" in f): return 15, "Concentrate/isolate blend."
        return 14, "Standard whey concentrate."

    if cat == "creatine":
        return (20, "Documented-purity Creapure® monohydrate.") if "creapure" in f \
            else (16, "Monohydrate is the gold-standard form; generic source.")

    if cat == "vitamin_d3":
        if "d2" in f or "ergocalciferol" in f: return 14, "D2 (ergocalciferol) — less potent than D3."
        if "lichen" in f or "lanolin" in f or "lanoline" in f: return 20, "Documented D3 source (lichen or lanolin)."
        return 16, "D3 with undocumented sourcing."

    if cat == "magnesium":
        if "magshape" in f: return 10, "Blend dominated by micro-encapsulated oxide (marketed 'liposomal')."
        if any(k in f for k in ["bisglycinate", "glycinate", "malate", "pidolate", "taurate"]):
            return 20, "Chelated magnesium — high bioavailability."
        if "citrate" in f: return 16, "Citrate — good bioavailability, possible laxative effect."
        if "algue" in f or "algae" in f or "lithothamne" in f: return 16, "Algae-sourced mineral."
        if "marin" in f or "marine" in f or "oxyde" in f or "oxide" in f:
            return 4, "Oxide (incl. seawater 'marine') — lowest bioavailability."
        return 10, "Unspecified magnesium form."

    if cat == "omega3":
        if "rtg" in f or "re-ester" in f or "re-ester" in f or "ré-ester" in _norm(form) or "reesterifi" in f: return 20, "Re-esterified triglycerides (rTG) — best absorbed."
        if "algue" in f or "algae" in f or "algal" in f: return 18, "Algae triglycerides — vegan, low contaminants."
        if "ethyl" in f or "ester ethyl" in f or " ee" in f: return 10, "Ethyl esters (EE) — cheapest, less well absorbed."
        if "tg" in f or "triglycer" in f or "naturelle" in f: return 16, "Natural triglycerides (TG)."
        return 12, "Oil form not clearly declared."

    if cat == "zinc":
        if "bisglycinate" in f or "glycinate" in f: return 20, "Bisglycinate — well-absorbed chelate."
        if "picolinate" in f: return 20, "Picolinate — well-absorbed form."
        if "citrate" in f: return 16, "Citrate — decent bioavailability."
        if "gluconate" in f: return 14, "Gluconate — modest bioavailability."
        if "liposom" in f: return 12, "'Liposomal' — undefined salt, unproven benefit for a mineral."
        if "oxyde" in f or "oxide" in f: return 4, "Oxide — poorly absorbed."
        return 14, "Unspecified zinc form."

    if cat == "vitamin_c":
        if "liposom" in f: return 20, "Liposomal — enhanced absorption evidence."
        if any(k in f for k in ["ester-c", "ester c", "acerola", "acerola", "pureway"]): return 18, "Buffered/whole-food vitamin C, gentle on the stomach."
        return 16, "Plain ascorbic acid — effective, standard form."

    if cat == "collagen":
        if "tripeptide" in f: return 20, "Low-MW tripeptides — high bioavailability."
        if any(k in f for k in ["peptan", "naticol", "verisol", "collactive", "aquacol", "cartidyss"]):
            return 20, "Branded hydrolysed peptides with clinical backing."
        if any(k in f for k in ["membrane", "coquille", "eggshell", "dermeon"]):
            return 12, "Eggshell-membrane collagen — different matrix, very low dose."
        if "hydrolys" in f or "peptide" in f: return 16, "Generic hydrolysed peptides."
        return 14, "Unspecified collagen form."

    if cat == "probiotics":
        coded = entry.get("strains_coded"); gastro = entry.get("gastro_resistant")
        if coded and gastro: return 20, "Strain-coded and gastro-resistant delivery."
        if coded: return 17, "Strain-coded (documented strains)."
        if gastro: return 14, "Gastro-resistant but strains not coded on label."
        return 10, "Strains not coded, no gastro-resistant delivery."

    if cat == "melatonin":
        return (20, "Prolonged/bi-layer release — supports sleep maintenance.") \
            if entry.get("release") == "prolonged" \
            else (16, "Immediate release — supports sleep onset.")

    return 14, "Form not scored for this category."


# ----------------------------------------------------------------------------- #
#  Dose tiers for categories that need entry-level logic (0–20). §1b.
# ----------------------------------------------------------------------------- #
def infer_dose_tier(cat, entry):
    def daily():
        return entry["active_per_unit"] * entry["units_per_day"]

    if cat == "zinc":
        mg = daily()
        if mg > 25: return 12, f"{mg:g} mg/day — above the EFSA UL (25 mg)."
        if mg >= 5: return 20, f"{mg:g} mg elemental zinc/day — effective, within EFSA UL."
        return 12, f"{mg:g} mg/day — low."
    if cat == "vitamin_c":
        mg = daily()
        if mg >= 200: return 20, f"{mg:g} mg/day — saturating dose."
        if mg >= 80: return 17, f"{mg:g} mg/day — at/above NRV."
        return 12, f"{mg:g} mg/day — below NRV territory."
    if cat == "collagen":
        g = entry.get("collagen_g_day")
        if g is None:
            g = daily()
        if g >= 5: return 20, f"{g:g} g peptides/day — in the studied range."
        if g >= 2.5: return 16, f"{g:g} g/day — modest."
        if g >= 1: return 12, f"{g:g} g/day — below most trials."
        return 8, f"{g:g} g/day — token dose."
    if cat == "probiotics":
        cfu = daily()
        if cfu >= 20: return 20, f"{cfu:g} billion CFU/day — high potency."
        if cfu >= 10: return 18, f"{cfu:g} billion CFU/day — solid."
        if cfu >= 5: return 15, f"{cfu:g} billion CFU/day — moderate."
        if cfu >= 1: return 12, f"{cfu:g} billion CFU/day — low."
        return 8, f"{cfu:g} billion CFU/day — very low."
    if cat == "melatonin":
        mg = daily()
        if mg > 1.9: return 14, f"{mg:g} mg/day — above the French supplement ceiling (1.9 mg)."
        if mg >= 1: return 20, f"{mg:g} mg/day — EFSA sleep-onset dose, within the French ceiling."
        return 12, f"{mg:g} mg/day — below the 1 mg EFSA claim."
    return None
