# KOTTU — Development Log

A running record of the project's evolution: what changed, why, and the
decisions behind it. Chronological, oldest first. Not tied to any one feature.

---

## Baseline (before this log)

KOTTU is a keystroke-dynamics authentication project. A class-based training
pipeline in `src/` loads the CMU **DSL-StrongPasswordData** benchmark (51
subjects × 400 typings of `.tie5Roanl`), standardises the 31 timing features,
reshapes each attempt into an 11×3 sequence, and trains a two-layer LSTM with a
51-way softmax. `src/predict.py` loads the saved model / scaler / label-encoder
for single-sample inference. Result: ≈83% weighted accuracy on a 4,080-sample
held-out set. Metrics and plots land in `output/`.

Commits `0916850 … dc1e2d9` cover the pipeline plus an early Streamlit UI. The
README was empty.

---

## Phase 1 — README

Wrote the project README from scratch: overview, a stage-by-stage table of the
pipeline, dataset, model architecture, results, project structure, install /
usage, a configuration map, outputs, tech stack, roadmap.

---

## Phase 2 — Streamlit UI, iterated

Took the existing Streamlit app (`app.py`, `pages/`, `ui/`) through several
passes:

- **Component layer + tokens.** `ui/theme.py` became the single source of design
  tokens, mirrored into CSS variables. `ui/components.py` gained real reusable
  pieces (`page_header`, `hero`, `section`, `metric_cards`); the four pages were
  refactored onto them for consistency.
- **Graceful empty states.** New `ui/artifacts.py` (read-only access to
  `output/`); pages show a friendly panel instead of a traceback when no
  training run has happened.
- **Native-widget theming.** `.streamlit/config.toml` so Streamlit's own widgets
  match the custom look; web fonts; `st.logo` + sidebar branding.
- **Interactive Model Insights.** Altair per-class chart parsed from the
  classification report. Training curves / confusion matrix stayed as PNGs — the
  pipeline doesn't export the raw numbers.
- **Authentication page.** UI only, with a clearly-labelled *simulated* verdict.
- **"Security console" restyle.** Aggressive CSS against Streamlit internals,
  near-black + orange, monospace, an Altair console theme.

---

## Phase 3 — decision: leave Streamlit

The result still read as "a Streamlit app." Decision: rebuild the UI as a real
static site.

- Constraint set here: **do not modify backend code** (`src/`, `train.py`,
  `tests/`) without asking. (Later softened — see Phase 9.)
- Direction references (technical / studio-portfolio, strict two-colour, mono,
  grid): awwwards *px-push*, *portfolio-zxc*, *daoism-systems*.
- Stack: **Astro**, static output, minimal JS. Data baked from `output/` at
  build time behind a swap seam.

---

## Phase 4 — Astro site built (`web/`)

New static site; backend untouched.

- Pages: landing, `authenticate`, `insights`, `about`.
- `web/scripts/sync-data.mjs` — read-only copy of `output/` artifacts into the
  site; a current copy committed so it builds without a training run.
- `web/src/lib/keystroke.js` — real in-browser keystroke-timing capture.
- `web/src/lib/verify.js` — deterministic **simulation** behind a `verify()`
  seam, ready to swap for a real call.
- Design system in `web/src/styles/{tokens,app}.css`: near-black warm neutrals,
  one orange accent, Bricolage Grotesque + JetBrains Mono, an instrument
  "bezel" frame.

---

## Phase 5 — structure + button pass

- Three-tier button system (primary / secondary / tertiary); one hover and focus
  treatment.
- Sticky top nav. Footer trimmed to attribution + a GitHub link (dropped the
  repeated page list).
- Model Insights regrouped: Overview → By class → Artifacts, with capped scroll
  regions.
- Section headings promoted to display scale.

---

## Phase 6 — Streamlit removed

Deleted `app.py`, `pages/`, `ui/`, `.streamlit/`. Rewrote the README for the
Astro site. Added a root `.gitignore` (Python bytecode, Node build output) and
stopped tracking committed `__pycache__/*.pyc`.

---

## Phase 7 — landing redesign

The landing was doing four kinds of navigation and little else. Two directions
were prototyped as standalone artifacts — **A** (lean showcase) and **C**
(scrollable explainer) — then a hybrid of A was chosen: keep the oversized hero,
add display-scale section headings and one big headline result number so it
holds up on scroll, keep the simple three-step "how it works", and put the
interactive keystroke capture on the landing itself. Ported into
`web/src/pages/index.astro`. GitHub repo linked; footer to attribution only.

---

## Phase 8 — git recovery

A stray nested repo at `web/.git` had been created at some point. A
`git push --force` run from inside `web/` used *that* repo — dumping the `web/`
folder (with `node_modules`, `dist`) at the GitHub repo root and **overwriting
the real project history**. The local outer repo was never affected.

Recovery: removed `web/.git`, committed correctly in the outer repo on top of
`dc1e2d9` (commit `e01bbb2`), force-pushed to restore
`0916850 … dc1e2d9 → e01bbb2` with `web/` as a clean subfolder.

Rule set afterward: **the user does all committing and pushing; the agent runs
read-only git only, and never adds a Claude co-author trailer.**

---

## Phase 9 — authentication feature: planning

"Authenticate" is really two features:

- **Identify** — "whose rhythm is this closest to?" — uses the trained 51-way
  LSTM. Honest as a demo, not authentication of a visitor.
- **Verify** — "is this the enrolled person?" — a distance threshold on the 31
  features; no model needed.

Decision: build both.

- **Scoring runs in a thin FastAPI service**, not in-browser TensorFlow.js —
  chosen because the maintainer wants to work in Python.
- **Host: a Hugging Face Space** (Docker SDK; 16 GB RAM, 48 h idle sleep,
  keepalive within ToS).
- `src/` reused as-is; edits to `src/` are allowed but only with authorization.

---

## Phase 10 — API built (`api/`)

- `api/main.py` — FastAPI: `/identify` (reuses `src.predict.Predictor`
  unchanged), `/enroll`, `/verify`, `/profiles`, `/health`. CORS open for now.
- `api/verify.py` — the verifier. Standardise with the global `scaler.pkl`,
  per-person mean + std, clipped RMS z-score distance, leave-one-out threshold.
  Calibrated on the benchmark (~15 enrollment attempts): ≈9% false-reject /
  ≈9% false-accept.
- `api/store.py` — in-memory profile store; a swap seam for persistence later.
- `api/requirements.txt` — runtime deps only; TensorFlow pinned to 2.15.1 (the
  version the model was saved with).

Tested locally with uvicorn: all endpoints behave; `src/` untouched.

---

## Phase 11 — browser capture bridge

The Authenticate page wired to the real API.

- `web/src/lib/features.js` — `extractFeatures` builds the 31 CMU features in the
  exact column order (ms → s, `UD` keeps its sign, Shift+R timed as the `r` key);
  `PhraseCapture` wraps the input and fires one attempt per clean run of the
  passphrase, resetting on any typo or Backspace.
- `web/src/lib/verify.js` — the simulation removed; now a `fetch` client for
  `/identify`, `/enroll`, `/verify`, `/health`. API base from `PUBLIC_KOTTU_API`
  with a localhost fallback. Typed `ApiError`.
- `web/src/pages/authenticate.astro` — rebuilt with two modes: **Identify** (one
  attempt → the LSTM names the closest of 51 CMU typists) and **Verify** (name +
  ~10 enrolment attempts → then accept / reject against the profile, with
  distance / threshold / margin shown). API status indicator; on-page caveats
  about timer resolution, ≈9% error, in-memory profiles, and cold starts.
- Verified: `extractFeatures` on synthetic keystrokes → dataset-range features;
  the full chain through `verify.js` against a running API. **Not yet exercised
  in a real browser** — capture with real timer resolution / a real keyboard is
  the open validation item (AUTH_PLAN step B2).

## Phase 12 — deployment config

Files so deploying is copy-paste; the account actions are still manual.

- `deploy/hf-space/` — root `Dockerfile`, HF-frontmatter `README.md`, and
  `populate.mjs`, which vendors `api/ src/ models/` + `requirements.txt` into a
  Hugging Face Space checkout (plain file copy, no nested git).
- `web/netlify.toml`, `web/.env.example`.
- `.github/workflows/keepalive.yml` — pings `/health` every 10 min so the free
  Space never sleeps.
- `.gitignore` — `web/.env*`.

Pending: a proposed env-driven CORS change in `api/main.py` (lock `allow_origins`
to the real site in production) — awaiting approval.

## Phase 13 — API slimmed to the TF-Lite runtime

The site deployed on Netlify. Hugging Face's Docker SDK turned out not to be
free, and the alternatives that are (Render, Koyeb, …) cap RAM at ~512 MB —
where `tensorflow-cpu` (≈600 MB installed, ≈400 MB just to import) does not fit.
The model itself is tiny (35k params, a 456 KB `.keras` file); the whole
hosting problem was the TensorFlow runtime.

Fix: run the model through the **standalone TF-Lite runtime** (~5 MB) instead of
full TensorFlow. FastAPI, every endpoint, and the request/response shapes are
unchanged.

- `scripts/export_serving.py` — one-time, run on a training machine: converts
  `kottu_model.keras` → `kottu_model.tflite` (float32, built-in ops only, pinned
  to a `(1, 11, 3)` input so the LSTM unrolls statically and needs no Flex ops),
  and lifts the scaler mean/std + label classes into `serving_params.json`. Both
  files are committed so the API builds without a training run. Imports TF but
  never runs in production.
- `scripts/check_parity.py` — throwaway gate: 40 real dataset samples through
  both `src/predict.py` (full TF) and the TF-Lite path; requires the same
  predicted user and class probabilities within 1e-4. Passes at ~6e-7 after one
  fix — the converted LSTM is a fused op whose state persists between
  `invoke()`s, so `api/infer.py` calls `reset_all_variables()` before each run.
- `api/infer.py` *(new)* — `identify()` / `probabilities()` over the `.tflite`
  file; only `numpy` + a TF-Lite interpreter at runtime (`tflite_runtime` in
  prod, falls back to `tensorflow.lite` on a dev box).
- `api/main.py` — `/identify` calls `api.infer` instead of
  `src.predict.Predictor`. `api/verify.py` — reads the scaler stats from
  `serving_params.json`; no more `joblib` / `scikit-learn`.
- `api/requirements.txt` — `fastapi`, `uvicorn`, `tflite-runtime`, `numpy`.
- `api/Dockerfile`, `deploy/hf-space/` — no TensorFlow, no `libgomp1`, `src/` no
  longer vendored (the API only reads `models/`).
- `src/`, `train.py`, `tests/` untouched; `src/predict.py` stays as the
  training-side reference. Test suite green.

Target host: Koyeb free tier (no card, always-on) — pending. On an always-on
host the keepalive workflow is unnecessary and should be disabled/removed.

## Current state

- `web/` — Astro static site, four pages, deployed on Netlify. Authenticate
  calls the real API; needs a live browser + running API end to end.
- `api/` — FastAPI service, TF-Lite serving path, works locally (all endpoints
  smoke-tested, parity verified). Not yet deployed to a host.
- Backend pipeline (`src/`, `train.py`, `tests/`) unchanged throughout.
- Committed through `40a37a0`. Uncommitted: Phase 13 (TF-Lite slim).

## Next

Pick a host (Koyeb, else Render) and deploy `api/`; point the Netlify site's
`PUBLIC_KOTTU_API` at it; disable the keepalive workflow if the host is
always-on. Then the CORS change and the Part D follow-ups in
[`docs/AUTH_PLAN.md`](AUTH_PLAN.md).
