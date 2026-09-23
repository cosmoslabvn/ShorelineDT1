# ShorelineDT — Minimal Public Research Release

This repository is a deliberately reduced, reviewable release of the
ShorelineDT uncertainty-to-decision interface. It demonstrates how an ensemble
shoreline state is validated, converted to DBVR and probability-of-exceedance
(PoE) metrics, classified into P0--P3 priorities, and passed to GAMA through a
numeric CSV contract.

The release uses a small **synthetic** dataset. It does not contain manuscript
sources, case-study results, raw imagery, production calibration code, the full
EnKF archive, or unpublished research material.

## Disclosure boundary

Included:

- the reduced Python uncertainty-to-decision implementation;
- a deterministic synthetic input with six transects;
- automated tests for the normal and intervention branches;
- a minimal GAMA model that consumes the generated CSV contract;
- documentation of the interface and reproducibility boundary.

Excluded:

- manuscript PDF, LaTeX, cover letter, reviews, and correspondence;
- named case-study observations and projected states;
- raw satellite imagery, GIS layers, and environmental forcing;
- production CoastSat and CoSMoS-COAST calibration workflows;
- full dashboard assets, numerical results, and research scripts;
- credentials, private paths, unpublished analyses, and future-work code.

This compact release verifies the software contract and decision logic. It is
not an end-to-end reproduction of the case study.

## Repository layout

```text
ShorelineDT/
|-- README.md
|-- LICENSE
|-- CITATION.cff
|-- SECURITY.md
|-- PUBLIC_RELEASE_MANIFEST.md
|-- .project
|-- .github/workflows/ci.yml
|-- docs/REPRODUCIBILITY.md
|-- models/Model_ShorelineDT_ContractDemo.gaml
|-- sample_data/synthetic_states.csv
|-- scripts/audit_release.py
|-- scripts/demo/run_demo.py
`-- scripts/demo/test_demo.py
```

## Requirements

- Python 3.9 or newer for the contract demonstration and tests;
- GAMA Platform 1.9.3 or newer for the optional visualization.

The Python demonstration uses only the standard library.

## Run the demonstration

From the repository root:

```bash
python scripts/demo/run_demo.py
```

This writes three ignored files under `output/demo/`:

- `decisions.csv` — human-readable calculations;
- `gama_contract.csv` — headerless numeric GAMA interface;
- `run_metadata.json` — parameters and provenance.

To exercise a stronger retreat scenario explicitly:

```bash
python scripts/demo/run_demo.py --stress-retreat-m 20
```

The stress offset is recorded in the metadata and must not be interpreted as
an observation or forecast.

## Run the checks

```bash
python -m unittest discover -s scripts/demo -p "test_*.py"
python scripts/audit_release.py
```

The release audit rejects common credential patterns, private absolute paths,
manuscript/archive formats, unexpected top-level content, and files larger than
the configured public-release limit.

## Open in GAMA

1. Run `python scripts/demo/run_demo.py`.
2. Import this directory as a GAMA project.
3. Open `models/Model_ShorelineDT_ContractDemo.gaml`.
4. Run `ShorelineDT_Public_Demo`.

The colors represent the synthetic P0--P3 decision classes. They are a software
demonstration, not a management recommendation.

## Reproducibility and scientific interpretation

See [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md). The public interface
is intentionally narrower than the private research archive. Any manuscript
using this release must describe that boundary accurately.

## Citation and license

Author and software metadata are provided in [`CITATION.cff`](CITATION.cff).
The distributed code and documentation are licensed under the MIT License.
Synthetic demonstration data are provided solely as part of this software
example and contain no field observations.
