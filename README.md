# market-bars-data

Public archive of **five-minute (and related) OHLCV bar sqlite databases** used in Harikiran’s US (IBKR) and India (Kotak) systematic work. Each dataset appears **once** in this repo (no mirrored copies of the same file).

You can switch visibility on GitHub anytime: **Settings → General → Danger zone → Change repository visibility** (public ↔ private).

## Contents

| File | Region | Purpose |
|------|--------|---------|
| [data/us-etfs-futures/spy_qqq_5min.sqlite](data/us-etfs-futures/spy_qqq_5min.sqlite) | US | SPY, QQQ, NDX, VIX — 5m RTH bars (~Sep 2021 → Nov 2026) |
| [data/us-etfs-futures/es_nq_5min.sqlite](data/us-etfs-futures/es_nq_5min.sqlite) | US | MES, MNQ, ES, NQ stitched 5m (~Sep 2023 → Nov 2026 on micros) |
| [data/india/mock92_bars.sqlite](data/india/mock92_bars.sqlite) | India | NIFTY, BANKNIFTY (+ short FUT windows) |
| [data/india/nifty_bars.sqlite](data/india/nifty_bars.sqlite) | India | NIFTY + INDIAVIX (slightly older cutoff than mock92) |

Symbol-level bar counts, date ranges, and **SHA-256** checksums are in [MANIFEST.json](MANIFEST.json).

## Clone and LFS

Binaries are stored with **Git LFS** (files are ~23–95 MB each).

```bash
git lfs install
git clone https://github.com/harikiransathi/market-bars-data.git
cd market-bars-data
git lfs pull
```

## Local source of truth (this machine)

On the author’s laptop these files are **hard-linked** from:

- `IBKR-expiry-monitor/data/spy_qqq_5min.sqlite`
- `IBKR-expiry-monitor/data/es_nq_5min.sqlite`
- `kotak-option-spreads/data/mock92_bars.sqlite`
- `kotak-option-spreads/data/nifty_bars.sqlite`

Refreshing data locally and pushing updates does not duplicate disk usage until you replace the underlying sqlite.

## Regenerate manifest

```bash
python scripts/build_manifest.py
```

## License

Market data may be subject to exchange/vendor redistribution terms. This repo is for personal research backup; use at your own risk.