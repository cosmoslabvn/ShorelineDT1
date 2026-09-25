"""Numerical invariants for the corrected nourishment update."""

import math
import unittest

from nourishment import evolve_nourishment


class NourishmentNumericsTest(unittest.TestCase):
    def test_isolated_placement_spreads_without_disappearing(self) -> None:
        result, diagnostics = evolve_nourishment(
            [0.0, 10.0, 0.0], diffusivity_m2_s=0.005, dt_years=0.5
        )
        self.assertGreater(result[0], 0.0)
        self.assertGreater(result[1], 0.0)
        self.assertGreater(result[2], 0.0)
        self.assertLessEqual(diagnostics.diffusion_number, 0.5)

    def test_no_flux_mass_balance_equals_decay(self) -> None:
        result, diagnostics = evolve_nourishment(
            [0.0, 4.0, 12.0, 4.0, 0.0],
            diffusivity_m2_s=0.005,
            dt_years=5.0,
        )
        self.assertTrue(all(value >= 0.0 for value in result))
        self.assertAlmostEqual(
            diagnostics.mass_after,
            diagnostics.expected_mass_after_decay,
            places=10,
        )

    def test_zero_diffusion_is_exact_exponential_decay(self) -> None:
        initial = [1.0, 2.0, 3.0]
        result, _ = evolve_nourishment(
            initial, diffusivity_m2_s=0.0, dt_years=7.0
        )
        for actual, expected in zip(result, [0.5, 1.0, 1.5]):
            self.assertAlmostEqual(actual, expected, places=12)

    def test_two_half_steps_match_one_full_step(self) -> None:
        initial = [0.0, 0.0, 10.0, 0.0, 0.0]
        full, _ = evolve_nourishment(
            initial, diffusivity_m2_s=0.005, dt_years=0.5
        )
        half, _ = evolve_nourishment(
            initial, diffusivity_m2_s=0.005, dt_years=0.25
        )
        half_twice, _ = evolve_nourishment(
            half, diffusivity_m2_s=0.005, dt_years=0.25
        )
        error = math.sqrt(sum((a - b) ** 2 for a, b in zip(full, half_twice)))
        self.assertLess(error, 1e-12)


if __name__ == "__main__":
    unittest.main()
