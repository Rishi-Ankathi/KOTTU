"""
KOTTU authentication API.

  /identify  - the trained 51-way LSTM, via the TF-Lite runtime (api.infer).
  /enroll    - build a personal profile from several passphrase attempts.
  /verify    - accept / reject one attempt against a named profile (no model).
  /health    - liveness check for the keepalive ping.

Run from the repo root:  uvicorn api.main:app --reload
"""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from api import infer
from api import store
from api import verify as verifier

N_FEATURES = 31

app = FastAPI(title="KOTTU API", version="1.0")

# The static site calls this API from another origin, so its URL must be listed
# here. Default: the deployed site plus the local Astro dev server. Override with
# KOTTU_ALLOWED_ORIGINS (comma-separated) at deploy time if the domain changes.
ALLOWED_ORIGINS = os.environ.get(
    "KOTTU_ALLOWED_ORIGINS",
    "https://kottu-lstm.netlify.app,http://localhost:4321,http://127.0.0.1:4321",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------
# request bodies
# --------------------------------------------------------------------------

class Attempt(BaseModel):
    features: list[float] = Field(min_length=N_FEATURES, max_length=N_FEATURES)


class Enrollment(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    samples: list[list[float]]


class VerifyRequest(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    features: list[float] = Field(min_length=N_FEATURES, max_length=N_FEATURES)


# --------------------------------------------------------------------------
# routes
# --------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"ok": True}


@app.post("/identify")
def identify(attempt: Attempt):
    """Which of the 51 enrolled CMU typists does this rhythm look most like?"""
    try:
        return infer.identify(attempt.features)
    except infer.ModelUnavailable:
        raise HTTPException(503, "model artifacts are not available")


@app.post("/enroll")
def enroll(body: Enrollment):
    """Register a person from several attempts at the passphrase."""
    try:
        profile = verifier.enroll(body.name, body.samples)
    except ValueError as exc:
        raise HTTPException(422, str(exc))

    store.put(profile)
    return {
        "name": profile.name,
        "samples": profile.n_samples,
        "threshold": round(profile.threshold, 4),
    }


@app.post("/verify")
def verify(body: VerifyRequest):
    """Is this attempt close enough to the named person's profile?"""
    profile = store.get(body.name)
    if profile is None:
        raise HTTPException(404, f"no enrolled profile for '{body.name}'")

    try:
        return verifier.verify(profile, body.features)
    except ValueError as exc:
        raise HTTPException(422, str(exc))


@app.get("/profiles")
def profiles():
    return {"names": store.names()}
