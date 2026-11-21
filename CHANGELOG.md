# Changelog

## 2026.11.21 — 2026-11-21

- Initial public release.
- 2373 brokers, 2056 licence records, 64 regulator/region groups.
- Licence references split out of free text into `licence_kind` / `licence_ref` /
  `licence_note` / `licence_raw`; 2034 records carry a resolvable reference.
- Regulator codes normalised across short codes and full names; shared codes carry a
  region suffix (`FMA`, `FMA-AT`, `FMA-LI`).
