# Authentication feature — implementation plan

Two capabilities, one FastAPI service, deployed on a Hugging Face Space. `src/`
is reused as-is. The API contract (`/identify`, `/enroll`, `/verify`, `/health`)
is already built and tested locally — everything below is the path from there to
live.

---

## A. Containerise the API  *(small)*

1. **`api/Dockerfile`** — base `python:3.11-slim`; install `api/requirements.txt`;
   copy `api/` + `src/` + `models/`; expose `7860`; run
   `uvicorn api.main:app --host 0.0.0.0 --port 7860`.
2. **`.dockerignore`** (repo root) — exclude `web/`, `output/`, `data/`, `.git`,
   `__pycache__`, docs — keep the image small.
3. **Local check (walkthrough):** `docker build -t kottu-api .` →
   `docker run -p 7860:7860 kottu-api` → hit `/health` and `/identify`.
4. **`.gitignore`:** add `api/profiles.json` (for when storage becomes a file).

## B. Browser capture bridge  *(`web/`, the bulk of the work)*

1. **Feature extractor** — extend `web/src/lib/keystroke.js` to emit the 31
   features in exact CMU column order (`H.period, DD.period.t, UD.period.t, H.t,
   …, H.Return`). Care points:
   - map key events to the 11 units: `. t i e 5 [Shift+r → R] o a n l Return`
   - decide how Shift+R is timed to match the dataset's `H.Shift.r` / `DD` / `UD`
     columns
   - `performance.now()` is milliseconds; the dataset is seconds → divide by 1000
2. **Validate against the dataset** — capture a handful of real attempts and
   compare feature ranges to `data/DSL-StrongPasswordData.csv`. Browser timer
   resolution (~1 ms vs the rig's ~0.2 ms) may shift the distribution; note
   whether `THRESHOLD_K` in `api/verify.py` needs re-calibrating for live input.
3. **Rewrite `web/src/lib/verify.js`** — replace the simulation with `fetch`
   calls: `identify(features)`, `enroll(name, samples)`, `verify(name,
   features)`. API base URL as one config value (local vs deployed).
4. **Rewrite `web/src/pages/authenticate.astro`** — two modes:
   - *Identify:* one attempt → `/identify` → "closest to CMU sXX, NN%" + bars.
   - *Verify:* enrol (type the phrase ~15×, with a progress indicator) →
     `/enroll`; then an attempt → `/verify` → Accept / Reject with `distance` /
     `threshold` / `margin` shown.
   - On-page caveats: timer precision, ≈9% error each way, profiles are
     in-memory (wiped when the Space restarts).
5. **Landing capture widget** — leave as the visual teaser, or wire its
   completion to `/identify`. Decide.

## C. Deploy

1. **Hugging Face Space** (Docker SDK). Contents: `Dockerfile`, `api/`, `src/`,
   `models/`, `requirements.txt`. Decide: push a subset of the repo, or the Space
   is its own repo with a copy.
2. Confirm it serves on `7860`; test the live `/docs`.
3. Point `web/`'s API base URL at the Space URL.
4. **Keepalive** — GitHub Actions cron (or UptimeRobot) hitting `/health` every
   ~10 min so visitors never see a cold start.
5. **Tighten CORS** — `allow_origins` from `*` to the real site origin.
6. **Deploy the static site** — `web/dist` to GitHub Pages / Netlify / Vercel
   (separate from HF).

## D. Follow-ups *(not blocking)*

- Persist profiles (an HF Dataset repo, or SQLite) — swap `api/store.py` only.
- Re-tune `THRESHOLD_K` on real browser-captured attempts.
- API loading / failure states in the UI (Space waking, network error).
- Rate limiting on `/enroll` and `/verify`.

---

## Ordering

A and B are independent — the API contract is fixed. Suggested: **A → B → C**.
A is short and proves the deploy path; B is the bulk of the work; C ties them
together.
