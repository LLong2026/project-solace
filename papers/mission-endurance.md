# Mission Endurance & Pump-Loss Survival — The Complete Clocks
*Project SOLACE, 2026-10-17. Extends SIM SOLACE 2/3/5 physics with multi-year runs.
Deterministic; no LLM in the decision path.*

## Clock 1 — Without the pumps

| Configuration | Survival | Mission load |
|---|---|---|
| Full power, no protection (pump dead) | **43 minutes to breach** | until breach |
| Derate ladder (R1): 70% / 60% power | **indefinite**, +13.5 C margin at 70% | 8.2 kWe — 5 kW mission fully served |
| Thermosyphon steam loop (SIM SOLACE 5) | **indefinite**, +40 to +70 C margin | 6-8 kWe backup — mission served |

Without pumps this plant is a 43-minute casualty if you do nothing, a
permanently-derated survivor if you do anything, and a full mission carrier
if you do the tank-and-steam architecture.

## Clock 2 — How long can a mission run? (20-year run, monthly cleaning + 103-day pump service)

| Horizon | Worst margin | Converter eff | 5 kW mission served? |
|---|---|---|---|
| 5 years | +38.3 C | 14.7% (no overhaul) | yes |
| 10 years | +38.3 C | 10.9% | yes |
| 15 years | +38.2 C | 8.0% | **falling short** (4.8 kWe) |
| 20 years | +37.5 C | 5.9% | no (3.5 kWe) |

- **Thermal closure is never the limit**: margins stay above +37 C for 20 years.
- **The ceiling is the converter**: efficiency decays -0.5%/month compounded;
  output crosses below the 5 kW mission load at ~14.5 years without overhaul.
- **With an 18-month converter overhaul** (eff restored to 20%, cycling
  18.3-19.4%): the mission is served indefinitely — the only remaining limit
  is material life.
- **Fuel is a non-issue**: 60 kWth burns ~23 g/yr of U-235; the 551 kg core holds
  ~2,400 full-power years at a 10% FIMA burnup limit.

## Honest limits

The 20-year run extrapolates literature-informed degradation constants (fouling,
seal wear, converter aging). The genuine long-pole for a 600 C LBE system is
coolant/structural corrosion, which this model does not simulate — that is a
materials-qualification question, not a simulation one, and is flagged as the
top physics item before any hardware program.

*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects on them.*
