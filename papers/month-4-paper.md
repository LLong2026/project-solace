# SIM SOLACE 4: Maintenance Recovery and the End-of-Trial Gate Re-Run
*Project SOLACE endurance trial, month 4 of 4 — deterministic simulation, no LLM in any decision path.*

## Abstract
Month 4 proves recovery is real: hull cleaning restores rejection to 99%, pump maintenance restores flow to 98%, the sea cools, and the aged plant is re-run through all six design gates. Question: after four months of wear, does the system still CLOSE?

## Plant (unchanged)
60 kWth Stirling+TEG brick; HALEU 16%, 420 mm core; LBE primary; subsea immersion;
48 V DC bus; 5 kW continuous UUV-dock load.

## Month 4 Results
- **Energy delivered:** 3840 kWh
- **Worst-case thermal margin:** +36.5 C (day 91, vs. 85 C shell limit)
- **Shell temperature envelope:** 37.9-48.5 C

## Injected events and recovery arcs
- **E13 (day 95) hull_cleaning:** recovered in 195 min.

## Daily trace (last 5 days of month)

| day | ambient C | pump flow | fouling eff | conv eff | bus kW | shell C | margin C | kWh |
|---|---|---|---|---|---|---|---|---|
| 118 | 8.0 | 0.980 | 0.99 | 0.194 | 11.64 | 37.9 | +47.1 | 120.0 |
| 119 | 8.0 | 0.980 | 0.99 | 0.194 | 11.64 | 37.9 | +47.1 | 120.0 |
| 120 | 8.0 | 0.980 | 0.99 | 0.194 | 11.64 | 37.9 | +47.1 | 120.0 |
| 121 | 8.0 | 0.980 | 0.99 | 0.194 | 11.64 | 37.9 | +47.1 | 120.0 |
| 122 | 8.0 | 0.980 | 0.99 | 0.194 | 11.64 | 37.9 | +47.1 | 120.0 |

## Verdict
Deterministic simulation, frozen fault schedule (sha cd0f13aa1785eb83). All margins
remained positive; every injected fault completed its recovery arc. No gate was
waived, no number hand-edited.

*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or
safety-critical environments. All systems are experimental and may contain defects
on them.*
