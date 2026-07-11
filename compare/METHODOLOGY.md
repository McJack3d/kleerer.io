# kleerer. — Health & Compo Score methodology (v1.1)

**Goal.** Give every supplement a transparent, reproducible 0–100 score based only on what is on the label and what the brand publicly proves — never on marketing claims. The score is computed by an open script ([`scripts/build_scores.py`](scripts/build_scores.py)) from open datasets ([`data/products_raw.json`](data/products_raw.json) + [`data/fr/*.json`](data/fr/)). Free-text labels are turned into coded tags by an open auto-tagger ([`scripts/autotag.py`](scripts/autotag.py)) — the **same module the collection pipeline uses**, so a scraped product and a hand-curated one are scored identically. Anyone can audit, criticise or rerun it.

**What the score is not.** It is not medical advice, not a measure of whether *you* need the product, and not a lab test — we score label composition and public transparency, not actual batch content.

**v1.1 scope.** 112 products, 11 categories (whey, creatine, vitamin D3, magnesium, omega-3, multivitamin, zinc, vitamin C, collagen, probiotics, melatonin), EU with a French-market focus. Snapshot July 2026.

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
How bioavailable / well-established is the chemical or physical form of the active? Assigned per category from published absorption and stability evidence (see `autotag.infer_form_tier`):

- **Magnesium** — chelated (bisglycinate, malate, taurate, pidolate) 20 · citrate 16 · algae-sourced 16 · blends where micro-encapsulated **oxide dominates by weight** (e.g. Magshape™) 10 · plain or seawater "marine" oxide 4.
- **Omega-3** — rTG 20 · algae TG 18 · natural TG 16 · ethyl esters 10 · undeclared form 12.
- **Vitamin D** — documented D3 (lichen or lanolin) 20 · undocumented D3 source 16 · D2 14.
- **Creatine** — Creapure® monohydrate 20 · generic monohydrate 16.
- **Whey** — native / native-isolate 20 · isolate-led 18 · concentrate+isolate blend 15 · standard concentrate 14.
- **Zinc** — bisglycinate / picolinate 20 · citrate 16 · gluconate 14 · "liposomal" (undefined salt) 12 · oxide 4.
- **Vitamin C** — liposomal 20 · buffered / whole-food (Ester-C®, acerola) 18 · plain ascorbic acid 16.
- **Collagen** — low-MW tripeptides 20 · branded hydrolysed peptides (Peptan®, Naticol®, Verisol®, Collactive®, Aquacol®) 20 · generic hydrolysed peptides 16 · eggshell-membrane 12.
- **Probiotics** — strain-coded **and** gastro-resistant 20 · strain-coded 17 · gastro-resistant only 14 · neither 10.
- **Melatonin** — prolonged / bi-layer release 20 · immediate release 16.
- **Multivitamins** — bioactive / chelated forms 20 · standard forms 12 · cheap forms (oxides, cyanocobalamin, retinol) 8.

### 1b. Effective dosing (0–20)
Daily dose at label serving vs. published effective ranges and EFSA reference values:

- **Vitamin D3**: 800–2 000 IU/day 20 · 400–799 14 · 200–399 10 · <200 6 · **>4 000 IU (EFSA UL) 8** + flag.
- **Magnesium (elemental)**: 100–250 mg 20 (within EFSA supplemental UL) · 251–400 17 (flagged) · <100 8.
- **Omega-3 (EPA+DHA)**: ≥1 000 mg 20 · 500–999 17 · 250–499 12 · <250 8.
- **Creatine**: 3–5 g/serving 20.
- **Whey (protein/100 g)**: ≥80 g 20 · 75–79 17 · 70–74 14 · <70 10.
- **Zinc (elemental)**: 5–25 mg 20 · **>25 mg (EFSA UL) 12** + flag · <5 mg 12.
- **Vitamin C**: ≥200 mg 20 · 80–199 17 · <80 12.
- **Collagen (peptides)**: ≥5 g 20 · 2.5–5 g 16 · 1–2.5 g 12 · <1 g 8.
- **Probiotics (CFU/day)**: ≥20 bn 20 · 10–19 18 · 5–9 15 · 1–4 12 · <1 8.
- **Melatonin**: 1–1.9 mg 20 (EFSA sleep-onset claim, within the French 1.9 mg supplement ceiling) · <1 mg 12 · **>1.9 mg 14** + flag.
- **Multivitamins**: ~100 % NRV coverage 20 · mixed 15 · B-megadosing 12 · major gaps 10.

## 2. Purity & Additives (0–30)
Start at 30, subtract per additive (floor 0). Free-text ingredient strings are classified by `autotag.classify_additive`:

| Tag | Penalty | Examples |
|---|---|---|
| Titanium dioxide (E171, banned in EU food) | −10 | — |
| Hydrogenated fat | −6 | fully hydrogenated rapeseed fat |
| Undisclosed / partial doses | −6 | botanical blends without amounts |
| Added sugar | −4 | sugar, glucose syrup, dextrose |
| Artificial sweetener | −4 | sucralose, acesulfame K, aspartame, saccharin |
| Artificial colour | −3 | azo dyes (E110, E129…) |
| Polyol | −2 | maltitol, sorbitol, xylitol |
| Synthetic carrier | −2 | polyethylene glycol (PEG) |
| Artificial flavour | −2 | "artificial flavour" |
| Emulsifier / thickener | −2 each | lecithin, xanthan, guar |
| Filler / bulking agent | −2 each | maltodextrin, starch, MCC, acacia, di/tricalcium phosphate |
| Anti-caking / flow agent | −2 each | magnesium stearate, silica |
| Cosmetic coating / pigment | −2 each | carnauba/shellac coatings, calcium-carbonate whitener |

Neutral (0): water, glycerine, gelatine and capsule shells (HPMC, pullulan, DRcaps…), carrier oils, natural tocopherol/rosemary antioxidants, natural flavours, plant-based colour concentrates, citric acid, lactase, prebiotic fibres, bioflavonoids. An **unrecognised** ingredient is conservatively treated as a −2 filler so nothing is silently ignored.

## 3. Transparency & Testing (0–30)

| Criterion | Points |
|---|---|
| Batch analyses / COAs published (contaminants, heavy metals, TOTOX…) | +12 |
| Recognised third-party certification (Informed Sport, Cologne List, Sport Protect, IFOS, AFNOR NF, Friend of the Sea, MSC, Labdoor…) | +10 |
| Branded, traceable raw ingredient (Creapure®, EPAX®, TRAACS®, Peptan®, Naticol®, Quali-C®, Quatrefolic®…) | +4 |
| Fully quantified label, no proprietary blend | +4 |

## Value metric (separate from the score)
Price never contaminates a health score, so value is displayed alongside, normalised per category to a **standard daily dose**: whey → € / 25 g protein · creatine → € / 3 g creatine · vitamin D3 → € / 1 000 IU · magnesium → € / 300 mg elemental · omega-3 → € / 500 mg EPA+DHA · zinc → € / 15 mg elemental · vitamin C → € / 1 000 mg · collagen → € / 10 g peptides · multivitamins, probiotics, melatonin → € / day. Prices are list prices (snapshot July 2026); structural promo pricing (Myprotein, Bulk, Prozis…) is flagged in the data.

## Label versioning (pipeline hook)
Every scored product carries a `label_hash` — a stable fingerprint of the facts we score (form, additives, certifications, dosages). The collection pipeline ([`pipeline/`](pipeline/)) recomputes it on each daily snapshot; when it changes, a product has been **silently reformulated** and the change is versioned. This is the asset that compounds over time and can't be regenerated retroactively by anyone.

## Known limitations (v1.1)
Scores rely on label data and public documents, not independent lab work; per-flavour variations exist; prices move (the Phase-1 scraping pipeline automates refresh); form-quality tiers compress ongoing scientific debate into one number; the auto-tagger is keyword-based and can mis-handle an unusual ingredient string (it fails safe to −2 and flags nothing silently). Corrections and pull requests are welcome — that is the point of being open.
