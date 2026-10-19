# THESIS: Simulation-Before-Build as Engineering Due Diligence
*Project SOLACE, SIM SOLACE 1-4, October 17 2026*

## The claim

Any engineering concept — however bold — can be subjected to a deterministic
simulation contract before a single dollar of hardware is committed. The simulation
must have three properties to count:

1. **It cannot be flattered.** The gates are conservation laws (First and Second
   Law, criticality, arithmetic), evaluated by code, with no LLM in the decision
   path. A marketing number and an honest number look different to the machine,
   and only one survives.

2. **It degrades honestly.** A design is not its day-one datasheet. SIM SOLACE 1-4
   ran the plant through 122 days of wear: pump degradation to 92% flow, hull
   fouling to 91% rejection efficiency, converter aging from 20.0% to 19.4%,
   seawater warming from 4 C to 16 C, a bus regulator fault, a converter module
   hot-swap, and a full station blackout drill.

3. **It proves recovery, not just survival.** Every fault executed a timed
   detect → isolate → heal → verify arc (150, 195, 193, and 195 minutes). The
   blackout drill — total load disconnect — was recovered in 193 minutes across
   a four-stage arc, delivering 99.89% uptime for the trial.

## The finding

The sponsor's concept, corrected to physics, **holds**:

- At commissioning and at end-of-trial, all six design gates pass (LOGIC HOLDS,
  6/6, deterministic).
- Worst-case thermal margin in the designed worst month was +36.5 C against an
  85 C structural limit — margin, not luck.
- Maintenance recovery arcs demonstrably restore degraded margins (fouling
  0.91 → 0.99; pump 0.92 → 0.98), which is precisely the claim a customer
  should demand before buying: not "it works," but "it keeps working, and
  when it breaks, it comes back."

## What the original dossier claimed vs. what survived

The original third-party dossier claimed 12.15 kWe from 30 kWth at 40.5%
efficiency with a 150 mm core. All six gates rejected it (0/6): heat rejection
short 23x, direct-conversion claims 1,849x above incident power, coolant
flash-boil, a Second Law violation, a subcritical core, and contradictory
arithmetic. The corrected plant that completes the trial is different and
true: 60 kWth, 12 kWe at 20%, 420 mm HALEU core, Stirling converters,
subsea immersion.

## The practice this implies

This is the company's product, exercised end-to-end on its first customer
engagement: **bring us the project; we build the sim; the sim says whether it
holds.** The sim cost one afternoon. The alternative — discovering a Second
Law violation after machining a pressure vessel — costs years.

*This software is a prototype and is provided for educational and research
purposes only. It is not intended for production use, commercial deployment, or
safety-critical environments. All systems are experimental and may contain
defects on them.*
