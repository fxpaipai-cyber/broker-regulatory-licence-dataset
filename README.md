# Global Broker Regulatory Licences Dataset

Public dataset of **regulatory authorisations and licence records** for forex/CFD,
precious-metals, securities & futures, and crypto-asset brokers worldwide. Every
licence row is a four-tuple — *regulator + legal entity + licence reference + tier* —
each of which can be checked against the official public register it came from.

- **Snapshot**: 2026-11-21
- **Homepage**: https://paipaifx.com/open-data.html
- **Licence**: CC BY 4.0 (attribution + link back, commercial use allowed)
- **Scale**: 2,373 brokers · 2,056 licence records · 64 regulator/region groups
- **DOI**: [10.5281/zenodo.24415043](https://doi.org/10.5281/zenodo.24415043)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24415043.svg)](https://doi.org/10.5281/zenodo.24415043)

## Why this dataset

Most "broker lists" are marketing copy. This one is built from register lookups: for
each broker we record which entity is licensed, by which regulator, in which
jurisdiction, under which reference number, and at what tier. Licence references are
normalised into a dedicated column instead of being buried in free text, so you can
join against register exports or de-duplicate group structures.

## Files

| File | Rows | Description |
|---|---|---|
| `data/brokers.csv` | 2,373 | Broker master table: name, legal entity, HQ, category, tier, six dimension scores, licence counts |
| `data/licences.csv` | 2,056 | Licence records: broker × regulator × jurisdiction × identifier kind × reference (subset of the 2,490 authorisations below) |
| `data/regulators.csv` | 64 | Regulator aggregates: brokers and tier distribution per (regulator, region); tier columns sum to 2,490 authorisations |
| `data/brokers.json` | 2,373 | Same content as JSON, with a `meta` block |
| `FIELD_DICT.md` | — | Full field dictionary (EN/中文) |
| `datapackage.json` | — | [Frictionless Data Package](https://specs.frictionlessdata.io/data-package/) descriptor |
| `scripts/recompute_score.py` | — | Reference implementation of the composite score, incl. missing-dimension handling |

## Quick start

```python
import pandas as pd

base = "https://raw.githubusercontent.com/fxpaipai-cyber/broker-regulatory-licence-dataset/main/data/"
brokers = pd.read_csv(base + "brokers.csv", encoding="utf-8-sig")
licences = pd.read_csv(base + "licences.csv", encoding="utf-8-sig")

# UK FCA-authorised brokers, by legal entity
fca = licences[(licences.regulator_code == "FCA") & licences.licence_ref.notna()]
print(fca[["broker_name", "legal_entity", "licence_kind", "licence_ref"]].head())
```

```sql
-- after loading into SQLite / DuckDB
SELECT regulator_code, region, SUM(brokers_count) AS brokers
FROM regulators
GROUP BY 1, 2
ORDER BY brokers DESC
LIMIT 10;
```

> **Encoding note**: CSVs are UTF-8 **with BOM** so that double-clicking them in
> Excel does not mangle non-ASCII names. Programmatic readers should pass
> `encoding="utf-8-sig"` (Python) or `encoding: "utf-8-sig"` (pandas). With plain
> `utf-8` the first column name keeps a leading `\ufeff`.

## Caveats — please read before drawing conclusions

1. **`licence_count = 0` does not mean "unlicensed".** It means this dataset has not
   collected a verifiable authorisation for that broker: 372 of 2,373 brokers
   are in that state. Do not publish "X is unlicensed" based on this file.
2. **Two different `verified` columns.** In `licences.csv` it marks an individual licence
   record (1 not yet line-checked against the register); in `brokers.csv` it
   marks the whole broker record (134 brokers not yet fully checked). It is a
   snapshot, not a legal opinion.
3. **`skipped_dims`** lists dimensions that were *not collected* (e.g. `prod|plat`).
   Those dimensions are excluded from the weighting and their weight is redistributed
   proportionally — they are **not** scored 0. Recomputing `score_total` without
   honouring this will give wrong numbers.
4. **`licence_kind = LEI` is not a licence.** An LEI is a legal entity identifier
   issued by GLEIF; it identifies the entity, not its authorisation. Keep it out of
   licence-number statistics.
5. **Tier is our editorial label**, not a statutory category. `T3` does not mean the
   broker is unregulated — it means the authorisation sits in a jurisdiction with
   weaker retail-investor protection rules.
6. **Regulator codes are normalised.** Short codes and full names coexist in the
   source (`CySEC` and `Cyprus Securities and Exchange Commission`, `BaFin` and
   `Bundesanstalt für Finanzdienstleistungsaufsicht`). `regulator_code` merges them;
   codes shared across jurisdictions carry a region suffix (`FMA` = New Zealand,
   `FMA-AT` = Austria, `FMA-LI` = Liechtenstein). `regulator_code_raw` preserves the
   original spelling for traceability.
7. **`licences.csv` rows ≠ authorisation counts in `regulators.csv`.** The tier columns
   in `regulators.csv` sum to **2,490 authorisations** (broker × regulator pairs),
   while `licences.csv` holds **2,056 rows**. The 434 pair difference is
   authorisations where the register confirms the licence but does not expose a discrete
   reference number, so there is no per-licence row to emit. The two files are not
   expected to reconcile row-for-row; use `regulators.csv` for counts and
   `licences.csv` for identifiers.

## Licensing and attribution

Released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You may use it commercially, including in
products, provided you attribute and link back. The required attribution string:

> Data source: 交易商排排网 (PAIPAI RANKING), https://paipaifx.com/open-data.html, licensed under CC BY 4.0.

A visible hyperlink to the homepage from any public use satisfies the attribution
requirement. Please do not re-publish the dataset as a competing download without
noting that this repository is the canonical source.

## Citation

`CITATION.cff` is included with the minted DOI, so GitHub's "Cite this repository"
button works out of the box.

- **Zenodo (concept DOI)**: [10.5281/zenodo.24415043](https://doi.org/10.5281/zenodo.24415043) — always points to the latest version
- **Zenodo (this version)**: [10.5281/zenodo.24415044](https://doi.org/10.5281/zenodo.24415044) — snapshot 2026-11-21

```
PAIPAI RANKING (交易商排排网). Global Broker Regulatory Licences Dataset. Snapshot 2026-11-21. Zenodo. https://doi.org/10.5281/zenodo.24415043. CC BY 4.0.
```

## Updates

The snapshot is regenerated when the underlying register data changes; the version
scheme is `YYYY.MM.DD`. Breaking schema changes bump a major segment and are described
in `CHANGELOG.md`.

## Contact

Corrections are genuinely welcome — a wrong licence number is worse than no number.
Open an issue, or email fxpaipai@gmail.com with the broker, regulator and the register URL you
are looking at.
