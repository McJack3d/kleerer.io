# p1 · compare

**The independent supplement comparator — score the label, price the active.**

First product of the kleerer. roadmap. Every supplement gets a transparent **Health & Compo Score** (0–100, grades A–E) computed from its label and public proofs, plus a price per gram of *actual* active — € per 25 g protein, per 3 g creatine, per 1000 IU vitamin D3, per 300 mg elemental magnesium, per 500 mg EPA+DHA. No sponsors, no affiliate links, no paid placements.

## Run it

No build step, no server needed — open `compare/index.html` in any browser, or visit `/compare/` on the hosted site (GitHub Pages serves it automatically from this folder).

## What's inside

```
index.html               the app (single file, vanilla JS, zero runtime deps)
data.js                  generated dataset with scores — do not edit by hand
data/products_raw.json   source of truth: 37 real EU products, July 2026 snapshot
scripts/build_scores.py  scoring engine — regenerates data.js
METHODOLOGY.md           full Health & Compo Score methodology (v1.0)
```

## Edit or extend the data

1. Edit `data/products_raw.json` (add a product, fix a price, correct a label).
2. Rebuild: `python3 scripts/build_scores.py` (stdlib only, Python ≥ 3.8).
3. Reload `index.html`.

The script validates score ranges and prints the full ranking so regressions are visible at a glance.

## Scoring in one paragraph

`Score = Composition & Efficacy (40) + Purity & Additives (30) + Transparency & Testing (30)`. Form quality (chelate vs oxide, rTG vs ethyl ester, Creapure® vs generic…) and effective dosing vs EFSA references make up composition; additives subtract from a 30-point purity base; published COAs (+12), third-party certifications (+10), branded traceable ingredients (+4) and fully quantified labels (+4) make up transparency. Price never touches the health score — value is shown separately. Full rules and known limitations: [METHODOLOGY.md](METHODOLOGY.md).

## Data honesty

Prices are EU list prices snapshotted **July 2026**; promo-heavy brands (Myprotein, Bulk, Prozis) sell 30–45 % below list most of the year, and this is flagged per product. Each product carries a data-confidence level (high / medium / low). Scores are computed from labels and public documents — **not** from independent lab testing. A scraping pipeline (roadmap Phase 1) will automate refresh.

## Disclaimer

kleerer. does not provide medical advice. Supplements are not a substitute for a varied diet. Consult a healthcare professional before supplementing, especially if pregnant, on medication, or managing a condition.

## License

MIT — see [LICENSE](../LICENSE) at the repository root. Corrections and pull requests welcome: if a brand disagrees with a score, the fix is the same for everyone — publish better proof.
