# SIM SOLACE 5: TANK & STEAM — The Pump-Free Cold Side
*Project SOLACE, architecture study, 2026-10-17. Follows SIM SOLACE 4 BREAKER
(sha 6f6675c33a7800cc) and the pump recommendations memo. Deterministic; no LLM
in the decision path.*

## The sponsor's question

*Put it in a tank with a closed loop — heat the water, make steam, run a backup
power plant. Can it? And we need better than 43 minutes.*

## Finding 0 — the tank alone does NOT beat 43 minutes (intuition killed)

A closed water tank, pump dead, any size: breach in **0.6 h** regardless of 1 m³ or
50 m³. Reason: the bottleneck is the shell-to-water heat *transfer coefficient*
(~550 W/K through natural convection), not the water's heat capacity. 48.3 kW of
waste through a 550 W/K coupling needs ΔT ≈ 88 K — the shell hits its limit long
before the tank warms up. A bigger tank is a bigger bucket behind the same small
pipe. **A tank is a product, not a survival sink** (10 m³ stores 1.47 GJ of useful
hot water, 25 °C → 60 °C — good for plant heat, irrelevant to the breach clock).

## Finding 1 — the steam loop DOES beat it: indefinitely

Move the take-off to the **hot side** (600 °C LBE, before waste heat ever reaches
the shell) and arm it on pump-loss detection. Natural-circulation thermosyphon
(gravity-driven, 4 m head — no pump anywhere), 6 bar / Tsat 160 °C class, condenser
immersed in the sea:

| Loop bypass to shell | Steady shell temp | Margin, indefinitely |
|---|---|---|
| 5% | 15.0 °C | +70.0 °C |
| 10% | 20.0 °C | +65.0 °C |
| 20% | 30.0 °C | +55.0 °C |
| 35% (poor isolation) | 44.9 °C | +40.1 °C |

Even a badly-isolated loop holds +40 °C of margin forever. Only a *stuck valve*
(loop fails to arm) returns the 43-minute breach — and that failure is covered by
the R1 derate ladder and the scram backstop. The protection stack becomes:
**derate ladder → steam loop → scram**, three independent layers, all pump-free.

## Finding 2 — the backup power plant closes

While the loop carries the 60 kWth, a micro-Rankine on the steam side produces:

| Cycle efficiency (honest micro-scale) | Output | Mission |
|---|---|---|
| 8% | 4.8 kWe | below 5 kW load |
| 10% | 6.0 kWe | **meets the 5 kW mission** |
| 13% | 7.8 kWe | **meets the 5 kW mission** |

Steam production ~84 kg/h saturated; closed condensing loop loses ~1% make-up
(~20 kg/day of treated water). **On pump seizure: Stirling trips, the steam loop
takes the heat to the sea, and the backup plant carries the mission.** The plant
does not breach and does not even go dark — it degrades from 12 kWe primary to
6-8 kWe backup, which still serves the full mission load.

## The architecture verdict

Yes to the tank — as a **steam generator and hot-water product**, with the
condenser in the sea and the whole loop thermosyphon-driven. The stack in
priority order:

1. **Steam thermosyphon loop (S5):** pump-free cold side, indefinite pump-loss
   survival at +40 to +70 °C margin, plus backup power (6-8 kWe)
2. **Derate ladder (R1, software):** covers the stuck-valve case at 60-70% power
3. **Scram backstop:** catches everything else (verified in BREAKER)
4. Stirling stays the primary converter (20% vs the Rankine's 10-13%)

## Honest caveats (standing doctrine)

- Steam means a **pressure vessel**: ASME BPVC-class design, safety valves,
  welding qualification, water chemistry control, freeze protection. This is the
  real cost of Finding 1 — regulatory and mechanical, not thermal.
- Micro-turbine efficiency at 60 kWth scale is genuinely modest; the Rankine plant
  is a *backup*, not a primary. Sizing it at 10-13% is honest, not generous.
- The condenser must sit in seawater — the sea remains the ultimate sink; the
  loop is the highway, not the destination.
- Thermosyphon driving head (4 m assumed) must be preserved in the final
  physical layout; a shorter loop needs a bigger pipe.

*This software is a prototype and is provided for educational and research
purposes only. It is not intended for production use, commercial deployment, or
safety-critical environments. All systems are experimental and may contain
defects on them.*
