"""Reference implementation of the ShorelineDT nourishment update.

The routine mirrors the corrected GAMA algorithm while remaining executable
with the Python standard library.  Values are nourishment-induced shoreline
advance (m) on an equally spaced alongshore grid.  Reflecting end cells impose
zero alongshore flux, and exponential decay is applied before each explicit
diffusion substep.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable


SECONDS_PER_YEAR = 365.25 * 86400.0


@dataclass(frozen=True)
class StepDiagnostics:
    substeps: int
    diffusion_number: float
    mass_before: float
    mass_after: float
    expected_mass_after_decay: float


def evolve_nourishment(
    advance_m: Iterable[float],
    *,
    diffusivity_m2_s: float,
    dt_years: float,
    spacing_m: float = 100.0,
    half_life_years: float = 7.0,
) -> tuple[list[float], StepDiagnostics]:
    """Advance a nourishment field with stable synchronous sub-stepping.

    ``diffusivity_m2_s`` is shoreline diffusivity, so the dimensionless
    explicit coefficient is ``G * dt / dx**2``.  The outer step is divided
    until this coefficient is at most 0.5.
    """
    values = [float(value) for value in advance_m]
    if not values:
        raise ValueError("advance_m must contain at least one cell")
    if any(value < 0.0 for value in values):
        raise ValueError("advance_m cannot contain negative values")
    if diffusivity_m2_s < 0.0 or dt_years < 0.0:
        raise ValueError("diffusivity and dt_years must be non-negative")
    if spacing_m <= 0.0 or half_life_years <= 0.0:
        raise ValueError("spacing and half-life must be positive")

    mass_before = sum(values)
    if dt_years == 0.0:
        diagnostics = StepDiagnostics(1, 0.0, mass_before, mass_before, mass_before)
        return values, diagnostics

    diffusivity_m2_yr = diffusivity_m2_s * SECONDS_PER_YEAR
    coefficient_total = diffusivity_m2_yr * dt_years / spacing_m**2
    substeps = max(1, math.ceil(coefficient_total / 0.5))
    dt_sub = dt_years / substeps
    coefficient = diffusivity_m2_yr * dt_sub / spacing_m**2
    decay = math.exp(-math.log(2.0) * dt_sub / half_life_years)

    for _ in range(substeps):
        decayed = [value * decay for value in values]
        updated: list[float] = []
        for index, center in enumerate(decayed):
            left = center if index == 0 else decayed[index - 1]
            right = center if index == len(decayed) - 1 else decayed[index + 1]
            value = center + coefficient * (left - 2.0 * center + right)
            updated.append(max(0.0, value))
        values = updated

    expected = mass_before * math.exp(-math.log(2.0) * dt_years / half_life_years)
    diagnostics = StepDiagnostics(
        substeps=substeps,
        diffusion_number=coefficient,
        mass_before=mass_before,
        mass_after=sum(values),
        expected_mass_after_decay=expected,
    )
    return values, diagnostics
