# SOLACE Pump Reliability Recommendations
*Project SOLACE, hardware recommendation memo, 2026-10-17. Derived from SIM SOLACE 4
BREAKER results (sha 6f6675c33a7800cc) and SIM SOLACE 3 seal-wear statistics
(sha 6ba234c80fa53998). Deterministic derivations; no LLM in the decision path.*

## The problem being solved

BREAKER identified the primary pump as the plant's **single point of failure**: total
seizure breaches the 85 C shell limit in 43 minutes with no protection, 20 minutes in
combined catastrophe. These recommendations retire that status in layers.

## R1 — Limp-home derate mode (software, zero hardware cost) — DO THIS FIRST

**Finding (computed):** with the pump completely dead, the immersion sink alone
(natural convection, 30% of forced coefficient) rejects enough heat to run the plant
derated — no scram required:

| Condition | Max survivable power fraction | Derate target (with margin) |
|---|---|---|
| Pump dead, nominal fouling (0.93) | 74.7% | **70%** |
| Pump dead + worst-corner fouling (0.83) | 67.5% | **60%** |

At 70% power the plant still generates ~8.2 kWe and serves the full 5 kW mission
load. **The pump stops being a single point of FAILURE and becomes a single point
of DERATE.** Implementation: pump-flow telemetry feeds the protection ladder
(flow < 98% → preemptive derate 90%; flow < 90% → derate 70%; confirmed loss →
derate 60% if fouling > 0.9; margin trip at +10 C remains as the final backstop).

## R2 — N+1 pump redundancy (hardware, moderate cost)

Twin 100% pumps (or three 50% with cross-strapped manifolds), either alone carrying
full rejection duty. Naval and lead-cooled reactor practice. Combined with R1, a
single seizure means the backup carries the load AND the derate ladder never even
engages; a simultaneous double failure still degrades gracefully instead of
breaching. Note: R1 already buys survival, R2 buys continuity — the mission never
notices.

## R3 — Natural-circulation loop sizing (design-phase, highest long-term value)

The decay-heat case is already survivable (BREAKER protected modes recovered to
+65 to +73 C). Take it further: size the LBE primary loop for full natural
circulation at decay heat — tall thermal-center offset, generous flow areas,
low-loss internals. This is standard lead-cooled passive-safety doctrine (the
same reasoning behind the Kilopower lineage, which runs its primary loop
buoyancy-driven). With R3 the plant's *worst-case* behavior is "the pump is
optional below 70% power."

## R4 — Predictive seal maintenance (operations policy, already quantified)

SIM SOLACE 3's wear statistics give the maintenance trigger directly: seal wear
follows a decelerating asymptote (D 0.06-0.14, tau 60-120 days across the
ensemble). **Service the pump when flow falls below 96%** — the 103-day service
point restored 0.98 flow in every run that received it. Watch it through the same
telemetry R1 uses.

## R5 — Instrument the ladder (integration)

One instrumentation set closes the whole story: pump flow, shell temperature,
fouling-proxy (thermal resistance trend). Feed all three into the R1 derate/trip
ladder. Every transition logged, every state recoverable — the plant that loses
its pump now has a *scripted, rehearsed* response, which is exactly what the
recovery doctrine of this whole engagement has been about.

## Priority order and honest cost framing

1. R1 (software derate ladder) — near-zero cost, retires the breach entirely
2. R3 (natural-circulation sizing) — design-phase only, passive by construction
3. R2 (N+1 hardware) — buys mission continuity, not survival
4. R4 + R5 (maintenance policy + instrumentation) — keeps R1 from ever triggering

**Bottom line for the sponsor:** the BREAKER battery found the plant dies in 43
minutes on pump seizure; the same physics shows a 60-70% derate mode survives it
indefinitely. The pump goes from "the part that kills the plant" to "the part that
slows it down" — and that fix is a control policy, not a forge order.

*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects on them.*
