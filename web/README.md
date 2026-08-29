# KOTTU — web

The KOTTU site. Static Astro build. Independent of the Python project:
it only ever **reads** `../output/` (via `scripts/sync-data.mjs`) and never
touches `src/`, `train.py`, `tests/`, `models/` or `data/`.

## Prerequisites

Node 18+ (developed on Node 22).

## Commands

```bash
cd web
npm install

npm run dev      # local dev server
npm run sync     # refresh metrics / report / plots from ../output
npm run build    # -> web/dist  (runs sync first, via prebuild)
npm run preview  # serve the built site
```

`web/dist` is fully static — open it from any host or the filesystem.

## Data

`npm run sync` copies these from `../output` into the site:

| source | destination |
| --- | --- |
| `output/metrics/metrics.json` | `src/data/metrics.json` |
| `output/reports/classification_report.txt` | `src/data/classification_report.txt` |
| `output/plots/*.png` | `public/plots/` |

A current copy of each is committed so the site builds without a training run.
The enrolled identity list (`src/data/enrolled-users.json`) is static.

## The model seam

`src/lib/verify.js` currently returns a deterministic **simulation** for the
Authenticate screen. Its return shape is the contract; swap the body for a
`fetch("/api/verify", …)` call to a service that imports `src/predict` when a
live model is wanted. Nothing else on the page changes.
