"""Offline tests for the synthetic ShorelineDT public demonstration."""

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class DemoTest(unittest.TestCase):
    def run_demo(self, *extra: str) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        output = Path(temporary.name)
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "demo" / "run_demo.py"),
                "--output-dir",
                str(output),
                *extra,
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return output

    def test_default_pipeline_outputs(self) -> None:
        output = self.run_demo()
        with (output / "decisions.csv").open(newline="", encoding="utf-8") as handle:
            decisions = list(csv.DictReader(handle))
        with (output / "gama_contract.csv").open(newline="", encoding="utf-8") as handle:
            contract = list(csv.reader(handle))
        metadata = json.loads((output / "run_metadata.json").read_text(encoding="utf-8"))

        self.assertEqual(len(decisions), 6)
        self.assertEqual(len(contract), 6)
        self.assertTrue(all(len(row) == 8 for row in contract))
        self.assertTrue(all(row["priority"] in {"P0", "P1", "P2", "P3"} for row in decisions))
        self.assertEqual(metadata["data_classification"], "synthetic; no field observations or forecasts")

    def test_intervention_branch_is_exercised(self) -> None:
        output = self.run_demo("--stress-retreat-m", "20")
        with (output / "decisions.csv").open(newline="", encoding="utf-8") as handle:
            decisions = list(csv.DictReader(handle))
        self.assertTrue(any(row["action"] == "nourish" for row in decisions))

    def test_invalid_buffer_is_rejected(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "demo" / "run_demo.py"),
                "--buffer-m",
                "0",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
