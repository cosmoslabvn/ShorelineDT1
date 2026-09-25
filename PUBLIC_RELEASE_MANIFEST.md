# Public

## Purpose

The public package demonstrates the ShorelineDT software interface and
decision logic on synthetic inputs. It is intentionally not the private
research workspace and not a case-study data archive.

## Approved content

| Path | Purpose |
| --- | --- |
| `models/` | Reduced GAMA CSV-contract visualization |
| `scripts/demo/` | Deterministic standard-library demonstration and tests |
| `scripts/numerics/` | Reference nourishment kernel and invariant tests |
| `sample_data/` | Synthetic state records only |
| `docs/` | Reproducibility and disclosure documentation |
| `.github/workflows/` | Automated release audit and tests |
| `output/demo/.gitkeep` | Empty output location |

## Prohibited content

- `paper/`, `manuscript/`, `reviews/`, or editorial correspondence;
- `raw/`, `private/`, `restricted/`, or full `includes/` trees;
- PDFs, Office documents, archives, GIS rasters/vectors, MATLAB workspaces,
  Python pickle files, keys, certificates, or environment-secret files;
- real case-study states or manuscript result tables;
- files larger than 1 MiB without written author approval.

## Release gate

Before publication:

1. obtain approval from all authors and the institutional IP/data owner;
2. confirm that MIT is the intended license, or replace it before publication;
3. confirm the final repository URL and add it to `CITATION.cff`;
4. add the actual release date to `CITATION.cff`;
5. run the unit tests and `scripts/audit_release.py`;
6. review `git diff --cached` manually;
7. create a signed or annotated `v1.0.0` tag;
8. archive that exact tag with Zenodo and record the DOI;
9. add the DOI to `CITATION.cff` and the manuscript code-availability text;
10. enable branch protection, secret scanning, and push protection on GitHub.
