# In-store products — schema

Brick-and-mortar-only products (guidelines §5.1, item 3). Products with no online
listing, whose price was observed on a shelf by a human.

**Add one with `python3 scripts/instore.py --new`** rather than by hand — the CLI
gets the provenance block right, which is the part that matters.

These are scored on exactly the same code path as online products: same
auto-tagger, same red-card registry, same §5.2 review gate. Being hard to collect
earns a product no leniency.

## Format

One JSON array per store, filename `<store-slug>.json`:

```json
[
  {
    "id": "brand-product-name",
    "brand": "Brand",
    "name": "Product name",
    "category": "magnesium",
    "price_eur": 12.90,
    "url": null,
    "confidence": "medium",
    "form": "magnesium bisglycinate",
    "additives": ["stéarate de magnésium", "hypromellose"],
    "active_per_unit": 100,
    "units_per_day": 2,
    "units_pack": 60,
    "price_provenance": {
      "store": "Pharmacie Lafayette",
      "city": "Bordeaux",
      "observed_on": "2026-08-07",
      "method": "in_store_observation"
    }
  }
]
```

## Rules

- **`url` is `null`.** There is no listing. The card shows the observation
  instead of a buy button.
- **`price_provenance` is mandatory.** A shelf price is one shop on one day. The
  site says so explicitly rather than letting it read as a national price.
- **`confidence` defaults to `medium`.** A label read once is weaker evidence
  than a page re-read daily. Use `low` if the label was partly illegible.
- **`additives` is transcribed exactly as printed**, in the label's own language.
  Do not tidy, translate, or summarise it — the tagger and the review ledger both
  key on the literal string, and a "helpful" edit silently changes the score.
- **Photograph the label.** Not stored in git (it would be archive data), but it
  is the evidence behind the record and belongs in the offline archive.

## Staleness

Online prices are re-observed daily; these are frozen when typed.

```bash
python3 scripts/instore.py --stale 90
```

Re-visit or withdraw. A year-old shelf price displayed as current is the same
class of failure as publishing a label nobody could read.
