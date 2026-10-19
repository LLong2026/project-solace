# RECEIPTS — Project SOLACE

| Artifact | Hash / verdict | Date |
|---|---|---|
| Original dossier spec (Google-sourced) | LOGIC FAILS 0/6 | 2026-10-17 |
| Honest TEG brick spec v2 | LOGIC HOLDS 6/6 | 2026-10-17 |
| Stirling brick spec (12 kWe) | LOGIC HOLDS 6/6 | 2026-10-17 |
| Machine stress battery (14 frozen patterns) | 14/14 fail-closed | 2026-10-17 |
| Forward-only amendments (disclosed) | vacuum convection fix; input validation; screening scope; converter-aware G4 | 2026-10-17 |
| SIM SOLACE 1-4 frozen fault schedule | sha cd0f13aa1785eb83 | 2026-10-17 |
| SIM SOLACE 1-4 results (122-day daily trace) | sha 43c040a0607fc4fa | 2026-10-17 |
| Aged-plant gate re-run (E16) | LOGIC HOLDS 6/6 | 2026-10-17 |
| Trial totals | 14,640 kWh, 99.89% uptime, 4/4 recovery arcs | 2026-10-17 |

Doctrine: forward-only, append-only. Any correction to a frozen artifact is a new
version with a disclosed reason; prior versions remain in git history.
| SIM SOLACE 3 ensemble (10,000 runs x 365 d, seed 20261017) | sha 6ba234c80fa53998 — 0 violations, worst +31.0 C, compression PASS, corners 20/20 | 2026-10-17 |
| SIM SOLACE 4 BREAKER failure battery + amendment v1.2 (pump-coupled sink) | sha 6f6675c33a7800cc — breach times found (20-43 min unprotected), all modes survivable with scram | 2026-10-17 |
| SIM SOLACE 5 TANK & STEAM study | tank-alone: no help (0.6 h, coupling-limited); hot-side thermosyphon loop: indefinite survival +40/+70 C, backup 6-8 kWe | 2026-10-17 |
