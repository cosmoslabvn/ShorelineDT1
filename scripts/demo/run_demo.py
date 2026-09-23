"""Run the minimal ShorelineDT uncertainty-to-decision demonstration.

The default input is synthetic. It contains no observations or forecasts from
the private ShorelineDT research archive.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "sample_data" / "synthetic_states.csv"
DEFAULT_OUTPUT = ROOT / "output" / "demo"
REQUIRED_COLUMNS = {
    "transect", "date", "Y_mean", "Y_std", "Yst", "Ylst", "Ybru", "Yvlt"
}


def normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def classify(dbvr: float, poe: float) -> str:
    if dbvr > 1.0:
        return "P1"
    if dbvr >= 0.5:
        return "P2"
    if dbvr >= 0.2 and poe >= 0.30:
        return "P3"
    return "P0"


def unit_number(unit: str) -> int:
    digits = "".join(character for character in unit if character.isdigit())
    if not digits:
        raise SystemExit(f"Unit identifier has no numeric component: {unit!r}")
    return int(digits)


def load_states(path: Path) -> dict[str, list[dict[str, str]]]:
    if not path.is_file():
        raise SystemExit(f"Synthetic state file not found: {path}")

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Input contract missing columns: {sorted(missing)}")
        for row in reader:
            grouped[row["transect"]].append(row)

    if not grouped:
        raise SystemExit("Input contract contains no state rows")
    for rows in grouped.values():
        rows.sort(key=lambda row: row["date"])
        if len(rows) < 2:
            raise SystemExit("Every synthetic unit must contain at least two dated states")
    return dict(sorted(grouped.items(), key=lambda item: unit_number(item[0])))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_gama_contract(path: Path, rows: list[dict[str, object]]) -> None:
    columns = [
        "unit_id", "retreat_m", "sigma_m", "dbvr", "poe",
        "priority_code", "action_code", "volume_m3",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerows([[row[column] for column in columns] for row in rows])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--buffer-m", type=float, default=40.0)
    parser.add_argument("--stress-retreat-m", type=float, default=0.0)
    parser.add_argument("--unit-spacing-m", type=float, default=100.0)
    parser.add_argument("--active-profile-height-m", type=float, default=6.5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if min(args.buffer_m, args.unit_spacing_m, args.active_profile_height_m) <= 0:
        raise SystemExit("Buffer, spacing, and active-profile height must be positive")
    if args.stress_retreat_m < 0:
        raise SystemExit("--stress-retreat-m cannot be negative")

    states = load_states(args.input)
    decisions: list[dict[str, object]] = []
    contract_rows: list[dict[str, object]] = []

    for unit, rows in states.items():
        first, latest = rows[0], rows[-1]
        change = float(latest["Y_mean"]) - float(first["Y_mean"])
        change -= args.stress_retreat_m
        retreat = max(-change, 0.0)
        sigma_change = math.hypot(float(first["Y_std"]), float(latest["Y_std"]))
        dbvr = retreat / args.buffer_m
        poe = 1.0 - normal_cdf((args.buffer_m - retreat) / max(sigma_change, 1.0))
        priority = classify(dbvr, poe)
        deficit = max(retreat - args.buffer_m, 0.0)
        volume = deficit * args.unit_spacing_m * args.active_profile_height_m
        action = "nourish" if priority == "P1" else ("monitor" if priority == "P3" else "none")
        components = {name: float(latest[name]) for name in ("Yst", "Ylst", "Ybru", "Yvlt")}
        dominant = max(components, key=lambda name: abs(components[name]))
        numeric_id = unit_number(unit)

        decisions.append({
            "unit": unit,
            "baseline_date": first["date"],
            "latest_date": latest["date"],
            "change_m": f"{change:.4f}",
            "retreat_m": f"{retreat:.4f}",
            "sigma_change_m": f"{sigma_change:.4f}",
            "buffer_m": f"{args.buffer_m:.2f}",
            "dbvr": f"{dbvr:.6f}",
            "poe": f"{poe:.6f}",
            "dominant_component": dominant,
            "priority": priority,
            "action": action,
            "illustrative_volume_m3": f"{volume:.2f}",
        })
        contract_rows.append({
            "unit_id": numeric_id,
            "retreat_m": f"{retreat:.4f}",
            "sigma_m": f"{sigma_change:.4f}",
            "dbvr": f"{dbvr:.6f}",
            "poe": f"{poe:.6f}",
            "priority_code": int(priority[1]),
            "action_code": 1 if action == "nourish" else (2 if action == "monitor" else 0),
            "volume_m3": f"{volume:.2f}",
        })

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "decisions.csv", decisions)
    write_gama_contract(args.output_dir / "gama_contract.csv", contract_rows)
    metadata = {
        "scope": "synthetic ShorelineDT contract demonstration",
        "data_classification": "synthetic; no field observations or forecasts",
        "input_state_rows": sum(len(rows) for rows in states.values()),
        "units_processed": len(decisions),
        "buffer_m": args.buffer_m,
        "stress_retreat_m": args.stress_retreat_m,
        "outputs": ["decisions.csv", "gama_contract.csv"],
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Processed {len(decisions)} synthetic units from {metadata['input_state_rows']} rows.")
    print(f"GAMA contract written to: {args.output_dir / 'gama_contract.csv'}")


if __name__ == "__main__":
    main()
