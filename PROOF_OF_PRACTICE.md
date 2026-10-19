# PROOF OF PRACTICE — SIM SOLACE 1-4
*Evidence bundle. Every figure below is machine-derived from `endurance_results.json`
(results sha 43c040a0607fc4fa, schedule sha cd0f13aa1785eb83). No number in this
document was hand-written.*

## The plant under trial

60 kWth Stirling+TEG brick, 12 kWe at 20% efficiency, HALEU 16% / 420 mm core,
LBE primary coolant, 600 C hot side, 70 C seawater-cooled sink, subsea immersion,
48 V DC bus, 5 kW continuous UUV-dock load. All six design gates passed at
commissioning (LOGIC HOLDS, 6/6).

## Month-by-month proof

| Phase | Energy | Worst margin | Shell envelope | Recovery arcs |
|---|---|---|---|---|
| SOLACE 1 (commissioning + wear-in) | 3,600 kWh | +50.8 C | 33.6-34.2 C | 1 (bus fault, 150 min) |
| SOLACE 2 (warming + fouling) | 3,600 kWh | +41.9 C | 34.2-43.1 C | 1 (hull cleaning, 195 min) |
| SOLACE 3 (peak stress + blackout) | 3,600 kWh | +36.5 C | 42.2-48.5 C | 1 (blackout drill, 193 min) |
| SOLACE 4 (maintenance recovery) | 3,840 kWh | +36.5 C | 37.9-48.5 C | 1 (hull cleaning, 195 min) |
| **Total** | **14,640 kWh** | **never negative** | **never above 48.5 C** | **4/4 completed** |

## The recovery proof (the point of the trial)

1. **Bus regulator fault (day 17):** sagged to 46.2 V; detected in 10 min,
   repaired in 140 min. Load served through the window on the DC bus buffer.
2. **Hull cleaning arc (day 50):** fouling had reached 0.95 rejection
   efficiency; cleaning restored 0.98, executed in 195 min.
3. **Station blackout drill (day 75):** total load disconnect under peak-stress
   conditions (16 C sea, max fouling, aged converter). Recovery arc:
   detect 12 min → isolate 35 min → restart 98 min → verify 48 min =
   **193 minutes**, four stages, every stage timed.
4. **Maintenance recovery (day 95 and 103):** hull cleaning restores rejection
   0.91 → 0.99; pump maintenance restores flow 0.92 → 0.98. Margins recover
   visibly in the daily trace — the system comes back.

## The end-of-trial verdict (E16, day 118)

The aged plant — converter at 19.4%, post-maintenance fouling, 8 C sea — was
re-run through all six design gates at aged parameters:

- G1 heat rejection: PASS
- G2 direct conversion: PASS
- G3 coolant phase: PASS
- G4 converter gradient (11.64 kWe claimed): PASS
- G5 criticality: PASS
- G6 bus arithmetic (48 V x 242.5 A = 11.64 kW): PASS

**VERDICT: LOGIC HOLDS (6/6) — after 122 days of simulated wear.**

## Honest limits (stated, not buried)

- G5 is a ballpark criticality screen (fissile inventory vs. scaled reflected
  critical mass). Real neutronics (e.g., OpenMC) remains the next rung and is
  required before any hardware decision.
- Recovery times are the frozen schedule's engineered values for a first
  design iteration, not measured hardware.
- The stress battery is adversarial but finite; it proves fail-closed
  behavior on 14 frozen patterns, not on all possible inputs.

## Receipts

- Gate machine: `sim/solace_sim.py` v1.1 (14/14 stress patterns fail-closed)
- Trial driver: `endurance_sim.py`, frozen schedule sha `cd0f13aa1785eb83`
- Full daily trace: `endurance_results.json`, sha `43c040a0607fc4fa`
- Aged-plant gate re-run: `sim/spec_aged.json` → LOGIC HOLDS 6/6

*This software is a prototype and is provided for educational and research
purposes only. It is not intended for production use, commercial deployment, or
safety-critical environments. All systems are experimental and may contain
defects on them.*
