"""
Profile storage.

In-memory only: enrolled profiles live for as long as the process runs and
are gone on restart. That's enough to demonstrate the enroll -> verify flow.
Swap this module for a persistent one (a file, an HF Dataset, a DB) later
without touching main.py - the three functions below are the whole contract.
"""

from __future__ import annotations

from api.verify import Profile

_PROFILES: dict[str, Profile] = {}


def put(profile: Profile) -> None:
    _PROFILES[profile.name] = profile


def get(name: str) -> Profile | None:
    return _PROFILES.get(name)


def names() -> list[str]:
    return sorted(_PROFILES)
