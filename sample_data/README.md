# Synthetic demonstration data

`synthetic_states.csv` contains six invented transects at three invented dates.
The values are deterministic and designed only to exercise different decision
branches. They do not represent any real location.

Columns:

| Column | Meaning in the demo |
| --- | --- |
| `transect` | Synthetic unit identifier |
| `date` | Synthetic state date |
| `Y_mean` | Ensemble-mean shoreline coordinate relative to an arbitrary baseline |
| `Y_std` | Supplied ensemble spread |
| `Yst`, `Ylst`, `Ybru`, `Yvlt` | Illustrative process components |
