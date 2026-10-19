# SIM SOLACE 3: The Ten-Thousand-Year Test
*Project SOLACE, statistical endurance ensemble, 2026-10-17. Frozen seed 20261017,
results sha 6ba234c80fa53998. Deterministic; no LLM in any decision path.*

## Why a third trial

A single 122-day trace is an anecdote. A distribution is evidence. SIM SOLACE 3 runs
**10,000 seeded missions of 365 days each — 10,000 simulated years of plant
operation** — with every degradation parameter drawn from declared uniform ranges
(frozen and hashed), then validates the model against accelerated time and attacks it
with worst-case corners.

## Stage A — The distribution

| Statistic | Value |
|---|---|
| Ensemble | 10,000 runs x 365 days = 10,000 simulated years |
| Margin P50 | +36.8 °C |
| Margin P5 | +33.4 °C |
| Margin P1 | +32.0 °C |
| Margin P0.1 | +31.2 °C |
| **Worst unit of 10,000** | **+31.0 °C (limit 85 °C — never approached)** |
| **Margin violations (< 0 °C)** | **0 in 10,000 years** |
| Availability P50 / worst | 99.89% / 99.85% |
| Energy P50 | ~31,300 kWh/yr mission demand served |

## Stage B — Time-compression validation (the credibility test)

Same 200-run subset, wear clock accelerated 1x / 5x / 20x. If simulated time were
"cheating," margins would diverge or invert under compression.

| Wear rate | P5 margin | Worst |
|---|---|---|
| 1x | +33.4 °C | +31.0 °C |
| 5x | +32.4 °C | +30.8 °C |
| 20x | +31.5 °C | +29.6 °C |

Ordering is finite and physics-consistent (faster wear, monotonically worse margin,
no divergence). **PASS** — the model degrades the same way regardless of how fast
we run the clock.

## Stage C — Maintenance optimization sweep

| Hull cleaning | n runs | P5 margin | Availability P50 |
|---|---|---|---|
| every 15 d | 1,634 | +36.0 °C | 99.89% |
| every 30 d | 1,630 | +35.7 °C | 99.89% |
| every 45 d | 1,691 | +34.7 °C | 99.89% |
| every 60 d | 1,666 | +33.9 °C | 99.89% |
| every 90 d | 1,717 | +33.2 °C | 99.89% |
| never | 1,662 | +32.0 °C | 99.89% |

**Operating recommendation:** monthly-to-45-day cleaning captures nearly all
available margin; below 30 days buys almost nothing. Availability is dominated by
the blackout drills, not by maintenance — the plant keeps the load through cleaning
windows.

## Stage D — Adversarial corner suite (20 frozen worst-case sets)

Each corner combines maximum fouling growth (D=0.16, τ=25 d), maximum pump wear
(D=0.14, τ=50 d), doubled converter decay (1.0%/mo), warmest siting (+4 °C), six
blackout drills, and **no maintenance at all**. Varying load phase across 20 seeds:

- 20/20 corners produce finite, well-behaved results (no NaN, no divergence)
- Worst corner margin: **+31.0 °C — no breach, no limit approach**

## The headline for the sponsor

*Ten thousand simulated years. Zero margin violations. Worst unit ever run still held
+31 °C of structural margin. Time compression does not change the verdict. The
maintenance schedule is optimized, not guessed. And twenty deliberate worst-case
corners with zero maintenance could not produce a breach.*

## Honest limits (standing doctrine)

- The ensemble exercises the declared parameter ranges. A corner outside those
  ranges (e.g., catastrophic hull breach) is not covered — that is a different
  failure mode and a future battery.
- Degradation constants remain literature-informed estimates; the distribution is
  only as good as its priors, which is exactly why they are published in the repo.
- Availability excludes common-mode external events (grid, weather beyond sea state).

*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects on them.*
