# SIM SOLACE 4: BREAKER — Where the Gear Actually Dies
*Project SOLACE failure-mode battery, 2026-10-17. Results sha 6f6675c33a7800cc.
Deterministic; no LLM in the decision path.*

## Amendment v1.2 (disclosed, forward-only)

This battery exposed a model gap: in SIM SOLACE 2 and 3, pump flow degradation was
*tracked* but never *coupled* into the heat-rejection physics — the sink ignored it.
BREAKER fixes this forward-only: pump flow now scales the convective sink
coefficient (total seizure = natural convection only, 30% of forced). This is the
kind of finding an adversarial customer would catch, so it is printed here rather
than patched silently.

## The question

SIM SOLACE 3 proved 10,000 simulated years without a margin violation. The sponsor's
correct question: *that means the gear never breaks — so when does it?* This battery
kills real components on purpose and times the death.

## Failure modes (minute-stepped, real thermal inertia, 720-hour horizon)

| Mode | What dies | Unprotected verdict | Protected verdict (margin trip at +10 C -> scram) |
|---|---|---|---|
| A — Pump seizure | total forced-convection loss | **BREACH in 43 min** (0.71 h) | trips at 28 min, no breach, settles at +72.9 C margin |
| B — Macrofouling blanket | rejection cut 80% (barnacle/mussel blanket) | **BREACH in 31 min** (0.51 h) | trips at 22 min, no breach, +72.0 C |
| C — Full electrical disconnect | bus dead, all 60 kW becomes waste | **no breach — ever** (steady 44.7 C, +40.3 C) | n/a — never trips |
| D — Combined catastrophe | pump dead + fouling blanket + no load | **BREACH in 20 min** (0.33 h) | trips at 15 min, no breach, +65.0 C |
| E — Seawater warming to 28 C | global siting extreme | no breach (+25.3 C) | n/a |

## The honest findings

1. **Yes — the gear breaks.** Kill the pump and the shell hits the 85 C structural
   limit in 43 minutes. Kill everything at once and it dies in 20 minutes. There is
   no version of this plant that survives total component death without protection.
2. **The single point of failure is the pump.** It is the only component whose loss
   alone kills the plant. This is the design's most actionable finding: redundancy
   or natural-circulation capability on the primary loop is the first hardware
   priority.
3. **The immersion sink is a gift.** Full electrical disconnect — every watt of
   60 kW thermal becoming waste heat — does NOT breach (44.7 C steady). The ocean
   rejects the entire reactor output with 40 C of margin. You cannot overheat this
   plant by breaking its electrical side.
4. **Protection converts death into downtime.** With a margin trip (scram at
   +10 C margin, decay heat decaying t^-0.2), every fatal mode becomes survivable:
   trips in 15-28 minutes, margins recover to +65 to +73 C. The plant that loses its
   pump does not die — it shuts down, and shutdown is a known, recoverable state.

## The vendor statement this earns

*The gear breaks: 20 to 43 minutes from total component failure to structural limit,
unprotected. The design's response is the trip, not the tank: with the margin-based
scram armed, all five failure modes are survived with margin. The pump is the single
point of failure — flagged for hardware redundancy — and the electrical side is
demonstrably over-sinked. Breakdown is proven, timed, and survivable.*

*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects on them.*
