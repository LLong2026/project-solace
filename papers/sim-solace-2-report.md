# SIM SOLACE 2: Physics-Based Degradation Trial
*Project SOLACE, v2.0 endurance model, 2026-10-17. Upgrades the frozen step-schedule
trial (SIM SOLACE 1-4) with continuous, literature-informed degradation physics.
Deterministic; no LLM in any decision path. Results sha 01a89013aa8b7fc2.*

## What changed from SIM SOLACE 1-4

| Axis | v1 (frozen schedule) | v2 (physics-based) |
|---|---|---|
| Biofouling | step to fixed levels | asymptotic first-order growth: (1-f) = 0.12(1-e^(-t/45 d)); monthly hull cleaning resets biofilm, corrosion baseline (1%) persists |
| Pump wear | step to fixed flows | decelerating seal-wear curve: deficit 0.10(1-e^(-t/90 d)); day-103 seal replacement restores 0.98 |
| Converter aging | step to 19.4% | compounded -0.5%/month (Stirling free-piston class): 20.0% -> 19.6% over 122 d |
| Seawater | scripted warming 4->16 C | seasonal sinusoid, mean 9.5 C, amp 5.5 C, annual min Feb 20 (trial runs Oct 18 - Feb 17: sea COOLS) |
| Load | flat 5 kW | UUV-dock mission profile: 2.5 kW standby, 6 h daily charge windows (6.5 kW, UUV alongside 6 of 7 days), 8 kW x 4 h surge drills |
| Recovery arcs | 4 scheduled | same doctrine: bus fault (d17), module swap (d24), blackout drill (d75, 193 min), 4 cleanings + pump service |

## Results (122 days, Oct 18 - Feb 17)

| Phase | Demand kWh | Served kWh | Min margin | Shell max | Sea range |
|---|---|---|---|---|---|
| Month 1 | 1,752 | 1,752 | +42.1 C | 42.9 C | 9.9-12.4 C |
| Month 2 | 1,752 | 1,752 | +44.8 C | 40.2 C | 7.1-9.8 C |
| Month 3 | 1,747 | 1,739 | +47.5 C | 37.5 C | 5.0-7.0 C |
| Month 4 | 1,868 | 1,868 | +48.7 C | 36.3 C | 4.0-4.9 C |
| **Total** | **7,119** | **7,111** | **+42.1 C worst** | **never above 42.9 C** | |

**Uptime 99.89%** (single blackout drill window, 193 min, recovered). Eight maintenance
and recovery events, all completed. The 8 kWh shortfall is exactly the blackout drill
window, honestly accounted.

## Findings worth the sponsor's attention

1. **The worst day is early, not late.** Worst margin (+42.1 C, day 6) occurs with a
   clean hull in the warmest water (12.4 C, late October). Degradation accumulates
   fast in autumn, but the cooling sea outpaces it. The v1 "worst month" stress
   (16 C sea + max fouling) is *more* conservative than the realistic season; v1
   bounds the problem, v2 shows the actual operating year.
2. **Monthly hull cleaning is sufficient.** Fouling never drops below 0.932
   efficiency between cleanings, and margins respond visibly to each cleaning arc.
3. **The seasonal load grows and the plant tracks it.** Month 4 demand (1,868 kWh,
   winter surge drills + heaviest dock cycle) is served at the *best* margins of the
   trial (cold sea assists rejection). The design closes with the load, not just the
   datasheet.
4. **Recovery remains the product.** Detect->isolate->heal->verify arcs complete in
   150-360 minutes; the blackout drill recovers in 193 minutes and the missing 8 kWh
   is printed, not hidden.

## Honest limits (unchanged doctrine)

- Degradation constants are literature-informed engineering estimates, now with
  continuous curves instead of steps; they are still declared inputs, not measured
  hardware telemetry.
- G5 criticality remains a screening ballpark; OpenMC-class neutronics is the next rung.
- The blackout arc times are operator-engineered values (the drill is declared, not
  emergent).

*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects on them.*
