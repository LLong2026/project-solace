# Project SOLACE — Subsea HALEU Micro-Reactor Concept, Machine-Verified

Author: **Benjamin Eckenfels** — Co-Founder, SQUIRL OS Technologies LLC, U.S. Navy
Veterunteer (Nuclear Submariner), Project SOLACE Sponsor.
Engineering and receipt machinery: SQUIRL OS Technologies LLC.

Project SOLACE is a concept for a seafloor HALEU-fueled micro-reactor quietly powering
an unmanned-underwater-vehicle dock for decades: Stirling conversion, lead-bismuth
primary coolant, seawater immersion as the ultimate heat sink, 5 kW continuous load
on a 48 V DC bus.

This repository is the open engineering record of what happened when the concept was
run through a deterministic gate machine: six conservation-law gates with no LLM in
the decision path.

## The arc

1. **The original dossier failed 0/6.** Numbers gathered from third-party AI research
   tools were tested against conservation laws. One figure was 1,849x above what
   physics will pay a direct converter. `sim/spec_original.json` is the failed spec,
   preserved exactly as received.
2. **The honest rebuild passed 6/6.** 60 kWth, 12 kWe at 20% conversion, Stirling
   converters, 420 mm core, LBE coolant. `sim/spec_stirling.json`.
3. **122-day frozen-schedule endurance trial** (`endurance_sim.py`, results
   sha 43c040a0607fc4fa, schedule sha cd0f13aa1785eb83): 14,640 kWh delivered,
   99.89% uptime, +36.5 C worst-case thermal margin, station-blackout drill recovered
   in 193 minutes, aged plant re-passing all six gates.
4. **The Ten-Thousand-Year Test** (`sim_solace_3.py`, sha 6ba234c8): 10,000 seeded
   one-year missions, zero margin violations, worst unit +31.0 C, time-compression
   validated at 1x/5x/20x.
5. **BREAKER** (`sim_solace_4_breaker.py`, sha 6f6675c3): the failure-mode battery.
   Gear breach in 20-43 minutes unprotected; all modes survivable with scram; the
   derate ladder and tank-and-steam loop demote the pump from killer to derate.
   Published on purpose: a receipt system that hides bad news is a marketing system.

## Contents

| Path | What it is |
|---|---|
| `sim/` | Gate machine + the four frozen specs (failed original and honest rebuilds) |
| `endurance_sim*.py`, `endurance_results*.json` | SIM SOLACE 1-4 endurance trial |
| `sim_solace_3.py`, `solace3_results.json` | Ten-Thousand-Year Monte Carlo ensemble |
| `sim_solace_4_breaker.py`, `solace4_results.json` | BREAKER failure-mode battery |
| `papers/` | The sponsor paper (published) and the per-simulation reports |
| `THESIS.md` | Simulation-before-build as engineering due diligence |
| `RECEIPTS.md` | Every hash and verdict in one table |
| `PROOF_OF_PRACTICE.md` | The evidence bundle for SIM SOLACE 1-4 |

## Published record

- Sponsor paper (published under the author's name):
  https://doi.org/10.5281/zenodo.23463568
- The paper's 32-byte hash is anchored on Bitcoin mainnet, block 972104, tx
  [54764b6d...8dded](https://mempool.space/tx/54764b6ddfaacdf4c96de28d8bf8bc44c8fcb2f3ece7669a899bc1d60618dded)
  (hash-only OP_RETURN, no monetary output), and walked a custody round trip on the
  XRP ledger:
  [hop 1](https://xrpscan.com/tx/8DD65725C9BB91BBB789133705BCDF292E6DE55015537CEC46585586AE3FBB1A),
  [hop 2](https://xrpscan.com/tx/8A56FAC6E0D541B3E34A01A7638831FFA8D06761F47B7BDFC78B27379CDA502C).
- Company ledger: https://github.com/LLong2026/four-horsemen

Dual Mesh Benchmark status: MEASURED (scoped) — no neural-mesh inference in the
decision path of any result in this repository. Program benchmark:
https://doi.org/10.5281/zenodo.23321637

## Disclaimer

This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects on them.

Nothing in this repository is a nuclear design, a licensed reactor design, or
engineering advice. The simulations are deterministic arithmetic models of a concept,
published as receipts of method, not as hardware claims.
