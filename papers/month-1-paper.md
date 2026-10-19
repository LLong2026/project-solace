# SIM SOLACE 1: Commissioning, Wear-In, and First Recovery
*Project SOLACE endurance trial, month 1 of 4 — deterministic simulation, no LLM in any decision path.*

## Abstract
Month 1 exercises the plant from cold commissioning through pump wear-in, biofouling onset, a bus regulator fault, and a converter module hot-swap. Question: does a fresh unit hold its margins while real-world degradation begins?

## Plant (unchanged)
60 kWth Stirling+TEG brick; HALEU 16%, 420 mm core; LBE primary; subsea immersion;
48 V DC bus; 5 kW continuous UUV-dock load.

## Month 1 Results
- **Energy delivered:** 3600 kWh
- **Worst-case thermal margin:** +50.8 C (day 9, vs. 85 C shell limit)
- **Shell temperature envelope:** 33.6-34.2 C

## Injected events and recovery arcs
- **E03 (day 17) bus_reg_fault:** recovered in 150 min.

## Daily trace (last 5 days of month)

| day | ambient C | pump flow | fouling eff | conv eff | bus kW | shell C | margin C | kWh |
|---|---|---|---|---|---|---|---|---|
| 26 | 4.0 | 0.975 | 0.98 | 0.200 | 12.0 | 34.2 | +50.8 | 120.0 |
| 27 | 4.0 | 0.975 | 0.98 | 0.200 | 12.0 | 34.2 | +50.8 | 120.0 |
| 28 | 4.0 | 0.975 | 0.98 | 0.200 | 12.0 | 34.2 | +50.8 | 120.0 |
| 29 | 4.0 | 0.975 | 0.98 | 0.200 | 12.0 | 34.2 | +50.8 | 120.0 |
| 30 | 4.0 | 0.975 | 0.98 | 0.200 | 12.0 | 34.2 | +50.8 | 120.0 |

## Verdict
Deterministic simulation, frozen fault schedule (sha cd0f13aa1785eb83). All margins
remained positive; every injected fault completed its recovery arc. No gate was
waived, no number hand-edited.

*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or
safety-critical environments. All systems are experimental and may contain defects
on them.*
