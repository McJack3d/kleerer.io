# kleerer. — Health & Compo Score methodology (v1.2)

**Goal.** Give every supplement a transparent, reproducible 0–100 score based only on what is on the label and what the brand publicly proves — never on marketing claims. Free-text labels are turned into coded tags by an open auto-tagger ([`scripts/autotag.py`](scripts/autotag.py)) — the **same module the collection pipeline uses** — and scored by an open script ([`scripts/build_scores.py`](scripts/build_scores.py)).

**Open method, proprietary data.** The *scoring code and rules* are open so anyone can audit and challenge them. The *dataset and its history* are not published: the daily price-and-label time-series accumulated by our pipeline is kleerer's core asset and cannot be regenerated retroactively by a competitor. Openness of method earns trust; privacy of the archive is the moat.

**What the score is not.** It is not medical advice, not a measure of whether *you* need the product, and not a lab test — we score label composition and public transparency, not actual batch content.

**Scope.** 163 products, 11 categories, EU with a French-market focus. Snapshot July 2026. Scoring methodology v1.2; personalised dosing model v2.

---

## Score structure

`Health & Compo Score = Composition & Efficacy (0–40) + Purity & Additives (0–30) + Transparency & Testing (0–30)`

| Grade | Score |
|---|---|
| **A** | ≥ 80 |
| **B** | 65–79 |
| **C** | 50–64 |
| **D** | 35–49 |
| **E** | < 35 |

**🟥 Red card (automatic 0 / grade E).** If a product contains a substance banned, restricted, or with authorisation withdrawn by *any* of EU-EFSA, US-FDA or WHO, its total score is forced to **0** regardless of everything else. A banned additive is not a deduction to be offset by good dosing — it is a disqualification.

---

## 1. Composition & Efficacy (0–40)

**1a. Form quality (0–20)** — how bioavailable the chemical/physical form is (chelate vs oxide, rTG vs ethyl ester, Creapure® vs generic, strain-coded probiotics, bioactive vitamins…). Full per-category ladder in [`autotag.py`](scripts/autotag.py).

**1b. Effective dosing (0–20)** — daily dose at label serving vs published effective ranges and EFSA reference values, with penalties for exceeding EU upper limits (e.g. vitamin D > 4 000 IU, zinc > 25 mg, melatonin > 1.9 mg).

## 2. Purity & Additives (0–30)
Start at 30, subtract per additive (floor 0). Every ingredient string is classified by `autotag.classify_additive`. **The penalties are proportionate to the strength of the health evidence**, and the most evidence-backed harm here is *added sugar* — so no sweetener is penalised more than sugar.

| Tag | Penalty | Basis |
|---|---|---|
| **Banned substance** | **RED CARD → 0** | banned/withdrawn/restricted by EU, FDA or WHO (see §2b) |
| Fully hydrogenated fat | −25 | saturated; near-disqualifying (partially hydrogenated = trans fat = red card) |
| Undisclosed doses / proprietary blend | −10 | you can't assess what isn't quantified |
| BHA / BHT (E320/E321) | −10 | IARC 2B / endocrine suspicion |
| Added sugar | −8 | strongest harm evidence of any additive here |
| Sweetener — Tier D (sucralose, erythritol, xylitol) | −6 | mechanistic / cardiovascular signal (see §2a) |
| Sweetener — Tier C (aspartame, acesulfame-K) | −4 | cohort cancer/CVD signal |
| Artificial azo colour (E102/E110/E129…) | −3 | EU child-attention warning required |
| Sweetener — Tier B (saccharin, cyclamate) | −2 | reassuring evidence but not natural |
| Polyol (maltitol, sorbitol) · PEG carrier · artificial flavour · emulsifier · thickener · filler · anti-caking · coating | −2 each | technological additives, minor concern |
| Unrecognised ingredient | −2 **+ flagged for human review** | never silently ignored (see §2c) |

Neutral (0): water, glycerine, gelatine and capsule shells, carrier oils, natural tocopherol/rosemary antioxidants, natural flavours, plant-based colour concentrates, citric acid, pectin, lactase, prebiotic fibres, and **Tier-A natural sweeteners (stevia, monk fruit)** — no credible harm signal.

### 2a. Our position on sweeteners (evidence-based, not alarmist)
The balance of current evidence is that regulator-approved sweeteners are safe at realistic intakes: EFSA, the FDA and WHO/JECFA continue to uphold their acceptable daily intakes, and in July 2023 JECFA reaffirmed aspartame's ADI even as IARC placed it in Group 2B — its weakest "possibly carcinogenic" hazard tier. Large observational cohorts (NutriNet-Santé, >100 000 adults) report modest associations between some sweeteners — aspartame, acesulfame-K, sucralose — and cancer or cardiovascular endpoints, and laboratory studies have flagged genotoxicity of a sucralose impurity and platelet effects of erythritol and xylitol. **These are cohort signals and in-vitro findings, not established causation**, and several are weakened by reverse causality (blood polyol levels are partly produced by the body). Notably, the evidence that *added sugar* harms health is stronger and more consistent than for any sweetener — which is why we penalise sugar more. WHO (2023) advises against using sweeteners for weight control, a conditional, low-certainty recommendation. kleerer therefore applies a **mild precaution proportional to the evidence** (Tier B < C < D), never a blanket "sweeteners cause cancer" verdict.

Key sources: [IARC/JECFA aspartame assessment, WHO 2023](https://www.who.int/news/item/14-07-2023-aspartame-hazard-and-risk-assessment-results-released) · [Debras et al., sweeteners & cancer, PLOS Medicine 2022](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1003950) · [Debras et al., sweeteners & CVD, BMJ 2022](https://www.bmj.com/content/378/bmj-2022-071204) · [Schiffman et al., sucralose-6-acetate, J. Toxicol. Environ. Health 2023](https://www.tandfonline.com/doi/full/10.1080/10937404.2023.2213903) · [Witkowski et al., erythritol & cardiovascular risk, Nature Medicine 2023](https://www.nature.com/articles/s41591-023-02223-9) · [Witkowski et al., xylitol, European Heart Journal 2024](https://academic.oup.com/eurheartj/article-abstract/45/27/2439/7683453) · [WHO guideline on non-sugar sweeteners, 2023](https://www.who.int/news/item/15-05-2023-who-advises-not-to-use-non-sugar-sweeteners-for-weight-control-in-newly-released-guideline) · [FDA, Aspartame and Other Sweeteners, 2025](https://www.fda.gov/food/food-additives-petitions/aspartame-and-other-sweeteners-food) · [Added-sugar harms umbrella review, Annual Review of Nutrition 2023](https://www.annualreviews.org/content/journals/10.1146/annurev-nutr-062322-020650).

### 2b. Red-card registry — strictest-guideline-wins
For every additive we compare the positions of the EU (EFSA), the US FDA and the WHO (JECFA/IARC), and we adopt the **most cautious** of the three. If any single body bans a substance, withdraws its authorisation, or restricts it, we flag it — even where the other two still permit it. Regulators genuinely diverge (titanium dioxide is banned in EU food yet allowed by the FDA), and a health score should not wait for the slowest jurisdiction.

| Substance | Red card because | Most recent action |
|---|---|---|
| Titanium dioxide (E171) | EU food ban (possible genotoxicity) | EU 2022 |
| Partially hydrogenated oil / industrial trans fat | WHO elimination target; FDA GRAS revoked; EU 2% cap | 2018–2021 |
| Brominated vegetable oil (BVO) | FDA authorisation revoked; EU never allowed | FDA 2024 |
| Potassium bromate (E924) | IARC 2B; EU-banned; California ban | 2023 |
| Red Dye No. 3 / erythrosine (E127) | FDA authorisation revoked (thyroid tumours) | FDA 2025 |
| Propylparaben (E216/E217) | EU food authorisation removed (endocrine concern) | EU 2006 |

*Fully hydrogenated fat is not a red card — it is saturated, not trans — but scores −25. Calcium carbonate, the clean E171 replacement, is neutral.*

### 2c. Unrecognised ingredients → human review
When the tagger meets an ingredient it can't classify, it does **not** guess it away: the product is marked *needs review* on its card and in the dataset, and takes a conservative −2 in the meantime. This turns the long tail of odd label strings into a visible worklist (and, later, a community-contribution hook) instead of silent scoring errors.

## 3. Transparency & Testing (0–30)
Published COAs (+12) · recognised third-party certification (Informed Sport, Cologne List, IFOS, Sport Protect, AFNOR NF, Friend of the Sea…) (+10) · branded traceable ingredient (Creapure®, EPAX®, Peptan®, Quali-C®…) (+4) · fully quantified label, no proprietary blend (+4).

## Value & price level (separate from the health score)
Price never contaminates a health score. Alongside it we show two things:
- **€ / standard dose**, normalised per category (€ / 25 g protein · 3 g creatine · 1000 IU D3 · 300 mg elemental Mg · 500 mg EPA+DHA · 15 mg zinc · 1000 mg vitamin C · 10 g collagen · € / day for multis, probiotics, melatonin).
- **Price level 1–5** — a simple affordability band within each category (1 = cheapest per standard dose, 5 = priciest), computed from the z-score of the €/dose distribution. It is a "how expensive is this" badge, not a quality judgement.

## Provenance (separate axis — deliberately NOT in the health score)
We flag each product's **country of manufacture** and a zone: 🇫🇷 made in France · 🇪🇺 EU/EEA · 🌍 outside the EU. kleerer has a French-market focus, so we attach a small **proximity malus** (0 for France, 1 for EU, 3 for extra-EU). **This malus is shown separately and is not folded into the Health & Compo Score** — a clean German product is not "less healthy" than a French one, and mixing sovereignty preference into a health metric would undermine its credibility. Displaying both lets a user weigh health and provenance for themselves.

## Known limitations (v1.2)
Scores rely on label data and public documents, not independent lab work; per-flavour variations exist; the auto-tagger is keyword-based and fails safe to *review* on unusual strings; form and dose tiers compress live scientific debate into single numbers; sweetener science in particular is still evolving. Corrections and pull requests to the scoring rules are welcome — that is the point of an open method.

## Personalised dosing — "dosage vs your needs" (model v2)

An optional profile (weight, age, sex, activity; height optional) turns every product's
label dose into an answer to *"is this right for me?"*. **It never touches the Health &
Compo Score** — two people looking at the same product see the same grade.

### Two questions, deliberately kept apart

The model answers them separately, because conflating them is how a dosage checker
becomes noise:

1. **Is it in your effective band?** — a personalised `lo–hi` range, built from your
   profile where the evidence supports scaling.
2. **Does it breach a regulatory limit?** — an `ul`, identical for everyone. A matter of
   law and safety, not preference.

| State | Meaning | Colour |
|---|---|---|
| **✓ fits you** | inside your personalised band | green |
| **↓ under-dosed for you** | below the band — the label serving won't get you there | amber |
| **↑ more than you need** | above your band, **within every regulatory limit** — safe, just more than you need; a cost question | neutral |
| **⚠ over the *n* limit** | breaches a statutory upper limit | red |

Only the last state is red. Earlier versions painted *any* dose above the optimal band in
red, which flagged 10 of 11 vitamin C products and 8 of 11 zinc products as if they were
dangerous when none breached any limit — the same false-alarm inflation the additive
penalties are explicitly designed to avoid.

### Upper limits, and what they actually mean

A UL breach is reported with its **consequence**, because ULs are not all the same kind of
thing. Proportionate wording matters as much here as it does for sweeteners (§2a):

| Nutrient | Limit | What the limit is actually about |
|---|---|---|
| Vitamin D3 | 4000 IU/day (EFSA) | genuine toxicity ceiling — hypercalcaemia |
| Zinc | 25 mg/day (EFSA) | competes with copper absorption |
| Magnesium | 250 mg/day supplemental (EFSA) | **gut tolerance** (osmotic diarrhoea), not toxicity; applies to supplements, not food |
| Vitamin C | 1000 mg/day (ANSES advisory) | gut tolerance, not toxicity |
| Melatonin | 1.9 mg (French ceiling) | regulatory: above it the product is a medicine, not a supplement |
| Omega-3 | 5000 mg EPA+DHA (EFSA: no concern below) | rarely reached by any product |

13 of 19 magnesium products in the catalogue exceed the 250 mg supplemental UL — mostly
well-tolerated chelates dosed there on purpose. The product says so rather than implying harm.

### What we personalise, and what we honestly don't

Scaling is applied **only where the literature scales**. Where it doesn't, the band is the
same for everyone and the interface says so out loud instead of inventing a number.

| Category | Personalised by | Reference |
|---|---|---|
| Whey / protein | weight, activity, age | 0.83 g/kg (sedentary RDA) → 1.4–2.2 g/kg ([ISSN](https://jissn.biomedcentral.com/articles/10.1186/s12970-017-0177-8), [Morton 2018](https://bjsm.bmj.com/content/52/6/376)); floor 1.0–1.2 g/kg at 65+ (ESPEN / PROT-AGE) |
| Vitamin D3 | age, BMI | 800–2000 IU; floor 1000 at 65+; up to 4000 at BMI ≥ 30 ([Endocrine Society](https://academic.oup.com/jcem/article/96/7/1911/2833671)) |
| Magnesium | weight, sex | total need ~6 mg/kg capped at the ANSES PRI (360 F / 420 M); supplement fills ~25–60% of it |
| Zinc | sex, activity | EFSA PRI 8/11 mg (F/M), +7–10 mg for heavy training, capped at UL 25 |
| Omega-3 | activity | 250 mg EFSA adequate intake → 1–2 g when very active (ISSN) |
| Vitamin C | age, activity | ANSES PRI 110 mg (120 at 65+), ~200 mg in heavy training |
| Creatine | weight **above ~100 kg only** | ISSN maintenance is a **flat 3–5 g/day**; heavier bodies to ~0.05 g/kg |
| Collagen | activity only | trials dose 5–15 g as **absolute** amounts — the literature does not scale by body weight |
| Probiotics | **not personalised** | effect is strain-specific and not dose-linear; studied range ~1–50 bn CFU; no weight/sex/age scaling established |
| Melatonin | **not personalised** | 0.5–1.9 mg regardless of body size; a note flags that endogenous melatonin declines past 55 |
| Multivitamin | **no single target exists** | 20+ nutrients each with their own target; we say so and point to the single-nutrient categories rather than fake one number |

A previous version scaled creatine as `0.04 g/kg` capped at 3–5 g, which collapsed the band
to `3–3 g` for anyone under ~85 kg and flagged a standard scoop as "above target" until
125 kg. Flat 3–5 g is what ISSN actually says.

The verdict is general guidance for healthy adults — **not medical advice**, and no
substitute for blood work or a professional.
