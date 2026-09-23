# Reproducibility boundary

## What this release reproduces

From a clean clone, a reader can:

1. validate the required ensemble-state columns;
2. aggregate dated states by synthetic transect;
3. compute shoreline change, non-negative retreat, and combined spread;
4. compute DBVR and Gaussian probability of exceedance;
5. apply the documented P0--P3 decision branches;
6. generate a stable numeric CSV contract;
7. load that contract into a reduced GAMA agent visualization;
8. run automated tests covering normal and intervention behavior.

## What this release does not reproduce

It does not reproduce:

- satellite-image acquisition or CoastSat extraction;
- tidal correction and observation-error estimation;
- CoSMoS-COAST calibration or EnKF assimilation;
- any named beach, field survey, climate projection, or management cost;
- manuscript figures, tables, numerical findings, or conclusions;
- the complete research dashboard or production data pipeline.

The supplied values are synthetic and exist only to exercise the software
contract. They must not be presented as observations, forecasts, validation
evidence, or coastal-management recommendations.

## Relationship to the private research archive

The private archive contains the case-study inputs, derived states,
calibration material, validation tables, and manuscript sources. Those files
are governed separately by project and institutional data-sharing decisions.
They are deliberately outside this public package.
