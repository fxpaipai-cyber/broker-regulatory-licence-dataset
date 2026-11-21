---
license: cc-by-4.0
language:
  - en
  - zh
pretty_name: Global Broker Regulatory Licences
size_categories:
  - 1K<n<10K
task_categories:
  - tabular-classification
tags:
  - finance
  - regulation
  - forex
  - cfd
  - licence
configs:
  - config_name: brokers
    data_files: data/brokers.csv
  - config_name: licences
    data_files: data/licences.csv
  - config_name: regulators
    data_files: data/regulators.csv
---

# Global Broker Regulatory Licences Dataset

Regulatory authorisations and licence records for FX/CFD, precious-metals,
securities & futures and crypto-asset brokers worldwide — 2373 brokers,
2056 licence records, 64 regulator/region groups.

Each licence record is a four-tuple: **regulator + licensed legal entity + licence
reference + tier**. The reference column holds numbers resolvable in the issuing
register (FCA FRN, ASIC AFSL, SFC CE number, CySEC CIF, FSCA FSP), which is why this
dataset can be joined against register exports and used to de-duplicate group
structures.

## Load

```python
from datasets import load_dataset

brokers = load_dataset("paipaifx/broker-regulatory-licence-dataset", "brokers", split="train")
licences = load_dataset("paipaifx/broker-regulatory-licence-dataset", "licences", split="train")
```

Or read the raw CSVs with `encoding="utf-8-sig"` (they carry a BOM for Excel).

## Field notes (read before use)

- `licence_count = 0` means **not collected**, not "unlicensed" (372 brokers).
- `verified` differs per file: per-licence in `licences.csv`, per-broker in `brokers.csv`.
- `skipped_dims` lists dimensions excluded from weighting — **not scored 0**.
- `licence_kind = LEI` is a GLEIF entity identifier, **not a licence number**.
- `regulator_code` is normalised; shared codes carry a region suffix
  (`FMA` = NZ, `FMA-AT` = Austria, `FMA-LI` = Liechtenstein).
- `licences.csv` (2056 rows) is **not** meant to reconcile with the
  2490 authorisations counted in `regulators.csv`: 434 authorisations
  have no discrete reference number in the register, so they emit no row.

## Citation

Zenodo (concept DOI): https://doi.org/10.5281/zenodo.24415043 — always points to the latest version.

```
PAIPAI RANKING (交易商排排网). Global Broker Regulatory Licences Dataset.
Snapshot 2026-11-21. Zenodo. https://doi.org/10.5281/zenodo.24415043. CC BY 4.0.
```

Full documentation: https://paipaifx.com/open-data.html
