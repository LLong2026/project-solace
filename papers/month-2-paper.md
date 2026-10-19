# SIM SOLACE 2: Warming Seas, Fouling, and the Cleaning Recovery
*Project SOLACE endurance trial, month 2 of 4 — deterministic simulation, no LLM in any decision path.*

## Abstract
Month 2 raises ambient seawater to 12C, deepens fouling and pump wear, and executes the first scheduled hull-cleaning recovery arc. Question: does the degradation trajectory respond to maintenance?

## Plant (unchanged)
60 kWth Stirling+TEG brick; HALEU 16%, 420 mm core; LBE primary; subsea immersion;
48 V DC bus; 5 kW continuous UUV-dock load.

## Month 2 Results
- **Energy delivered:** 3600 kWh
- **Worst-case thermal margin:** +41.9 C (day 49, vs. 85 C shell limit)
- **Shell temperature envelope:** 34.2-43.1 C

## Injected events and recovery arcs
- **E07R (day 50) hull_cleaning:** recovered in 195 min.

## Daily trace (last 5 days of month)

| day | ambient C | pump flow | fouling eff | conv eff | bus kW | shell C | margin C | kWh |
|---|---|---|---|---|---|---|---|---|
| 56 | 12.0 | 0.950 | 0.98 | 0.200 | 12.0 | 42.2 | +42.8 | 120.0 |
| 57 | 12.0 | 0.950 | 0.98 | 0.200 | 12.0 | 42.2 | +42.8 | 120.0 |
| 58 | 12.0 | 0.950 | 0.98 | 0.200 | 12.0 | 42.2 | +42.8 | 120.0 |
| 59 | 12.0 | 0.950 | 0.98 | 0.200 | 12.0 | 42.2 | +42.8 | 120.0 |
| 60 | 12.0 | 0.950 | 0.98 | 0.200 | 12.0 | 42.2 | +42.8 | 120.0 |

## Verdict
Deterministic simulation, frozen fault schedule (sha cd0f13aa1785eb83). All margins
remained positive; every injected fault completed its recovery arc. No gate was
waived, no number hand-edited.

*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or
safety-critical environments. All systems are experimental and may contain defects
on them.*
