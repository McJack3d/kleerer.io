# kleerer. — Health & Compo Score methodology (v1.0)

**Goal.** Give every supplement a transparent, reproducible 0–100 score based only on what is on the label and what the brand publicly proves — never on marketing claims. The score is computed by an open script ([`scripts/build_scores.py`](scripts/build_scores.py)) from an open dataset ([`data/products_raw.json`](data/products_raw.json)). Anyone can audit, criticise or rerun it.

**What the score is not.** It is not medical advice, not a measure of whether *you* need the product, and not a lab test — we score label composition and public transparency, not actual batch content.

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

---

## 1. Composition & Efficacy (0–40)

### 1a. Form quality (0–20)
How bioavailable / well-established is the chemical or physical form of the active? Assigned per category from published absorption and stability evidence:

- **Magnesium** — chelated forms (bisglycinate, malate, taurate) 20 · citrate 16 · blends where micro-encapsulated **oxide dominates by weight** 10 · plain oxide 4. Rationale: oxide has the lowest bioavailability of common forms and an osmotic laxative effect; "liposomal"/"marine" marketing does not change the underlying salt.
- **Omega-3** — re-esterified triglycerides (rTG) 20 · algae TG 18 · natural unconcentrated TG 16 · ethyl esters (EE) 10 · undeclared form scored as worst plausible.
- **Vitamin D** — D3 (cholecalciferol, lanolin or lichen) 20 base, reduced for undocumented sourcing; D2 (ergocalciferol) capped at 14.
- **Creatine** — Creapure® monohydrate 20 · generic monohydrate 16 (monohydrate itself is the gold standard; the premium rewards documented purity).
- **Whey** — native/isolate-led 18–20 · concentrate+isolate blends 15–16 · standard concentrate 14.
- **Multivitamins** — bioactive/chelated forms (methylcobalamin, P-5-P, folate as 5-MTHF, chelated minerals) 20 · standard forms 12–14 · cheap forms (cyanocobalamin, oxide minerals) or D2 8–14.

### 1b. Effective dosing (0–20)
Daily dose at label serving vs. published effective ranges and EFSA reference values:

- **Vitamin D3**: 800–2 000 IU/day = 20 · 400–799 = 14 · 200–399 = 10 · < 200 = 6 · **> 4 000 IU (EFSA UL) = 8** with an explicit flag.
- **Magnesium (elemental/day)**: 100–250 mg = 20 (within EFSA supplemental UL of 250 mg) · 251–400 mg = 17 (effective and common, but above EFSA supplemental UL — flagged) · < 100 mg = 8.
- **Omega-3 (EPA+DHA/daily dose)**: ≥ 1 000 mg = 20 · 500–999 = 17 · 250–499 = 12 · < 250 = 8.
- **Creatine**: 3–5 g/serving = 20 (established effective dose).
- **Whey (protein density per 100 g)**: ≥ 80 g = 20 · 75–79 = 17 · 70–74 = 14 · < 70 = 10.
- **Multivitamins**: broad coverage near 100 % NRV without ULs exceeded = 20 · mixed 14–16 · B-megadosing (> 1 000 % NRV) = 12 · major gaps (missing minerals, vit D ≤ 5 µg) = 10.

## 2. Purity & Additives (0–30)
Start at 30, subtract per additive tag (floor 0):

| Tag | Penalty | Examples |
|---|---|---|
| Artificial sweetener | −4 each | sucralose, acesulfame K |
| Hydrogenated fat | −6 | fully hydrogenated rapeseed fat |
| Undisclosed/partial doses | −6 | botanical blends without amounts |
| Artificial flavouring | −2 | "artificial flavours" |
| Emulsifier / thickener | −2 each | soy/sunflower lecithin, xanthan |
| Filler / bulking agent | −2 each | maltodextrin, starch, MCC, acacia |
| Anti-caking / flow agent | −2 each | magnesium stearate, silica |
| Cosmetic coating / pigment | −2 each | tablet coatings, calcium-carbonate whitener |

Neutral (0): water, glycerine, gelatine*, carrier oils, natural tocopherol/rosemary antioxidants, natural flavours, plant-based colour concentrates, functional enteric coatings. (*Gelatine affects the vegan tag, not purity.)
Titanium dioxide (E171) is banned in EU food since 2022; any product still listing it outside the EU would score −10.

## 3. Transparency & Testing (0–30)

| Criterion | Points |
|---|---|
| Batch analyses / COAs published (contaminants, heavy metals, TOTOX…) | +12 |
| Recognised third-party certification (Informed Sport, Cologne List, Sport Protect, IFOS, Labdoor, Friend of the Sea…) | +10 |
| Branded, traceable raw ingredient (Creapure®, EPAX®, TRAACS®, Quatrefolic®, VitaMK7®, K2VITAL®…) | +4 |
| Fully quantified label (every active dosed, no proprietary blend) | +4 |

## Value metric (separate from the score)
Price should never contaminate a health score, so value is displayed alongside, normalised per category to a **standard daily dose**: whey → € per 25 g protein · creatine → € per 3 g creatine · vitamin D3 → € per 1 000 IU · magnesium → € per 300 mg elemental · omega-3 → € per 500 mg EPA+DHA · multivitamin → € per daily dose. Prices are list prices (snapshot July 2026); structural promo pricing (Myprotein, Bulk, Prozis…) is flagged in the data.

## Known limitations (v1)
Scores rely on label data and public documents, not independent lab work; per-flavour variations exist; prices move (a Phase-1 scraping pipeline will automate refresh); form-quality tiers compress ongoing scientific debate into one number. Corrections and pull requests are welcome — that is the point of being open.
