#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 kleerer.
#
# This file is part of the kleerer scoring engine and collection pipeline.
# Licensed under the GNU Affero General Public License v3.0 ONLY; see LICENSE.
# A separate commercial licence is available for parties who cannot accept the
# AGPL's obligations: hello@kleerer.com. The commercial licence covers this code
# only -- it conveys NO right in the collected archive, which is unpublished and
# all rights reserved. See NOTICE.md.

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
#  v1.2 additive classification.
#
#  A free-text ingredient string maps to ONE tag. Tags fall in three buckets:
#    • RED-CARD substances   -> classify_additive returns "banned:<name>"; the
#      scorer forces the whole product to 0 (grade E). Basis: banned/withdrawn
#      by at least one of EU-EFSA / US-FDA / WHO (strictest-guideline-wins).
#    • penalty tags          -> subtract from the 30-pt purity base (see
#      build_scores.PURITY_PENALTIES).
#    • "unknown"             -> not silently ignored: small provisional penalty
#      AND surfaced on the product card for human review.
#  Sweetener tiers (A→D) encode strength-of-evidence-of-harm from recent
#  independent cohorts/RCTs — see METHODOLOGY.md. Sugar is penalised MORE than
#  any sweetener because the evidence for added-sugar harm is stronger.
# ----------------------------------------------------------------------------- #

CAPSULE_HINTS = ["gelule", "capsule", "tunique", "k-caps", "kcaps", "drcaps",
                 "pullulan", "hpmc vegetal", "gelatine", "gelatin", "softgel",
                 "enveloppe", "vegecaps"]

# Red-card: banned / authorisation-withdrawn / restricted by EU, FDA or WHO.
BANNED = [
    ("titanium_dioxide",   ["dioxyde de titane", "titanium dioxide", "e171"]),
    ("trans_fat",          ["partiellement hydrogen", "partially hydrogen",
                            "graisse trans", "trans fat", "acides gras trans"]),
    ("brominated_veg_oil", ["huile vegetale bromee", "brominated vegetable", "bvo"]),
    ("potassium_bromate",  ["bromate de potassium", "potassium bromate", "e924"]),
    ("red_3_erythrosine",  ["erythrosine", "e127", "red 3", "red no. 3", "rouge 3"]),
    ("propylparaben",      ["propylparaben", "propylparabene", "e216", "e217"]),
]

# Order matters: first match wins (worst offenders first).
RULES = [
    ("hydrogenated_fat", ["hydrogen", "hydrogene"]),   # FULLY hydrogenated = saturated (partial caught by BANNED above)
    ("added_sugar",      ["sirop de glucose", "glucose syrup", "sucre", "sugar",
                          "saccharose", "sirop de", "dextrose"]),
    ("severe_antioxidant",["e320", "e321", "bha", "bht", "butylhydroxy",
                          "hydroxyanisole", "hydroxytoluene"]),
    ("proprietary_blend",["blend without", "without individual dose", "proprietary blend",
                          "melange proprietaire", "non detaille", "non precis",
                          "undisclosed", "not disclosed", "excipients non"]),
    # sweeteners, tiered by evidence of harm (strongest signal first)
    ("sweetener_d",      ["sucralose", "erythritol", "erythritol", "xylitol"]),
    ("sweetener_c",      ["aspartame", "acesulfame", "acesulphame", "ace-k", "ace k"]),
    ("sweetener_b",      ["saccharin", "saccharinate", "cyclamate"]),
    ("polyol",           ["maltitol", "sorbitol", "polyol", "isomalt", "mannitol"]),
    # stevia / monk fruit = Tier A (natural, no harm signal) -> handled as neutral
    ("artificial_colour",["azoique", "e102", "e104", "e110", "e122", "e124", "e129",
                          "tartrazine", "sunset yellow", "allura", "ponceau",
                          "carmoisine", "azorubine", "quinoline", "colorant azo"]),
    ("synthetic_carrier",["polyethylene glycol", "peg ", "(peg)", "polyethylene-glycol"]),
    ("artificial_flavour",["arome artificiel", "artificial flavour",
                           "artificial flavor", "aromatisant artificiel"]),
    ("lecithin",         ["lecithine", "lecithin"]),
    ("thickener",        ["gomme xanthane", "xanthan", "gomme guar", "guar",
                          "gomme gellane", "gellan", "carraghenane", "carrageenan"]),
    ("bulking_filler",   ["maltodextrine", "maltodextrin", "amidon", "starch",
                          "cellulose microcristalline", "microcrystalline cellulose",
                          "cellulose", "croscarmellose", "phosphate dicalcique",
                          "phosphate tricalcique", "dicalcium phosphate", "gomme d'acacia",
                          "gomme arabique", "acacia", "caroube", "carob", "citrate de calcium"]),
    ("anticaking",       ["stearate de magnesium", "magnesium stearate",
                          "sels de magnesium d'acides gras", "acide stearique",
                          "stearic", "dioxyde de silicium", "silicon dioxide",
                          "silice", "silica", "talc", "carbonate de magnesium"]),
    ("coating",          ["enrobage", "coating", "cire de carnauba", "carnauba",
                          "shellac", "e903", "e904", "carbonate de calcium",
                          "hydroxypropylcellulose", "hydroxypropylmethylcellulose"]),
]

# Explicitly recognised as NON-penalised (incl. Tier-A natural sweeteners and the
# clean E171 replacement, calcium carbonate — already neutral via 'coating' path).
NEUTRAL_KEYWORDS = [
    "eau", "water", "glycerine", "glycerin", "glycerol",
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
    "stevia", "steviol", "glycosides de steviol", "monk fruit", "luo han",
    # English benign ingredients (curated v1 labels are in English)
    "olive oil", "sunflower oil", "rapeseed oil", "coconut oil", "mct oil",
    "fish oil", "fish-gelatine", "fish gelatin", "bovine gelatine", "gelatine",
    "glycerol", "glycerine", "glycerin", "natural flavour", "natural orange flavour",
    "natural flavor", "antioxidant", "rosemary", "tocopherol", "vitamin e",
    "salt", "water", "declared", "none", "rice", "acacia gum (prebiotic",
    "prebiotic", "lactase", "enteric coating", "functional enteric",
    "pectine", "pectin", "chlorure de sodium", "huile essentielle", "citrate de",
]

# Strings the curator/scraper has explicitly marked benign, or that describe the
# ABSENCE/replacement of a banned substance (must never trip the red card).
NEUTRAL_MARKERS = ["(neutral", "neutral)", "e171 replacement", "e171-replacement"]
NEGATION_NEAR_BANNED = ["replacement", "remplac", "sans ", "-free", " free",
                        "free)", "alternative", "instead of", "substitut", "no titanium"]


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return s.lower().strip()


def classify_additive(raw: str):
    """Map an ingredient string to a tag:
       "banned:<name>"  -> red card (force score to 0)
       "<penalty_tag>"  -> purity penalty (see build_scores.PURITY_PENALTIES)
       "unknown"        -> unrecognised, flag for human review (+ small penalty)
       None             -> neutral / benign."""
    n = _norm(raw)
    # annotator-marked benign / "free of X" strings never trip a penalty or red card
    if any(m in n for m in NEUTRAL_MARKERS):
        return None
    negated = any(w in n for w in NEGATION_NEAR_BANNED)
    for name, keys in BANNED:                       # red card checked first
        if any(k in n for k in keys) and not negated:
            return "banned:" + name
    # capsule / shell material → neutral (but not if it also names a filler/anti-caking)
    if any(h in n for h in CAPSULE_HINTS) and not any(
        k in n for k in ["stearate", "silice", "silica", "dioxyde", "maltodextrine"]
    ):
        return None
    # natural Tier-A sweeteners are benign — short-circuit before generic matches
    if any(k in n for k in ["stevia", "steviol", "monk fruit", "luo han"]):
        return None
    for tag, keys in RULES:
        if any(k in n for k in keys):
            return tag
    if any(k in n for k in NEUTRAL_KEYWORDS):
        return None
    return "unknown"                                # never silently ignored


def tags_from_additives(additives):
    """additives -> (purity_tags, additives_detail, banned[list], review[list]).
       banned  = red-card substance names found (force score 0)
       review  = ingredient strings the tagger couldn't classify (needs a human)"""
    tags, detail, banned, review = [], [], [], []
    for a in additives or []:
        t = classify_additive(a)
        detail.append(a)
        if t is None:
            continue
        if t.startswith("banned:"):
            banned.append(t.split(":", 1)[1])
            tags.append("banned")
        elif t == "unknown":
            review.append(a)
            tags.append("unknown")
        else:
            tags.append(t)
    return tags, detail, banned, review


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
