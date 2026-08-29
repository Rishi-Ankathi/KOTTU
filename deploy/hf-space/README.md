---
title: KOTTU API
emoji: ⌨️
colorFrom: gray
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# KOTTU API

FastAPI service behind the [KOTTU](https://github.com/Rishi-Ankathi/KOTTU) site.

- `POST /identify` — the trained 51-way LSTM: whose CMU typing rhythm is closest.
- `POST /enroll` / `POST /verify` — per-person enrolment and a distance-threshold
  check on the 31 keystroke-timing features (no model).
- `GET /health` — liveness.

Interactive docs at `/docs`.

This Space is generated from `deploy/hf-space/` in the source repo — do not edit
here by hand.
