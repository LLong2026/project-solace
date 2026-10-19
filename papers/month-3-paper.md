# SIM SOLACE 3: Peak Stress: Maximum Fouling, Converter Aging, Blackout Drill
*Project SOLACE endurance trial, month 3 of 4 — deterministic simulation, no LLM in any decision path.*

## Abstract
Month 3 is the designed worst month: peak ambient (16C), maximum fouling (91% rejection efficiency), converter aging to 19.4%, pump flow at 92%, and a deliberate full station blackout with a timed four-stage recovery. Question: does the plant survive its designed worst case with margin to spare?

## Plant (unchanged)
60 kWth Stirling+TEG brick; HALEU 16%, 420 mm core; LBE primary; subsea immersion;
48 V DC bus; 5 kW continuous UUV-dock load.

## Month 3 Results
- **Energy delivered:** 3600 kWh
- **Worst-case thermal margin:** +36.5 C (day 82, vs. 85 C shell limit)
- **Shell temperature envelope:** 42.2-48.5 C

## Injected events and recovery arcs
- **E11 (day 75) blackout_drill:** recovered in 193 min. Arc: detect 12 -> isolate 35 -> restart 98 -> verify 48

## Daily trace (last 5 days of month)

| day | ambient C | pump flow | fouling eff | conv eff | bus kW | shell C | margin C | kWh |
|---|---|---|---|---|---|---|---|---|
| 86 | 16.0 | 0.920 | 0.91 | 0.194 | 11.64 | 48.5 | +36.5 | 120.0 |
| 87 | 16.0 | 0.920 | 0.91 | 0.194 | 11.64 | 48.5 | +36.5 | 120.0 |
| 88 | 16.0 | 0.920 | 0.91 | 0.194 | 11.64 | 48.5 | +36.5 | 120.0 |
| 89 | 16.0 | 0.920 | 0.91 | 0.194 | 11.64 | 48.5 | +36.5 | 120.0 |
| 90 | 16.0 | 0.920 | 0.91 | 0.194 | 11.64 | 48.5 | +36.5 | 120.0 |

## Verdict
Deterministic simulation, frozen fault schedule (sha cd0f13aa1785eb83). All margins
remained positive; every injected fault completed its recovery arc. No gate was
waived, no number hand-edited.

*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or
safety-critical environments. All systems are experimental and may contain defects
on them.*
