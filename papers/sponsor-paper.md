# Project SOLACE: A Sponsor's Receipt — What Happened When a Deterministic Gate Machine Rebuilt My Subsea Reactor

**Benjamin Eckenfels**
Co-Founder, SQUIRL OS Technologies LLC — U.S. Navy Veteran (Nuclear Submariner) — Project SOLACE Sponsor (Customer-01)

October 2026

*This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.*

## Abstract

As a co-founder of SQUIRL OS Technologies, I brought a concept to my own company: a subsea HALEU-fueled micro-reactor to power a seafloor UUV dock. I also brought a dossier of engineering numbers I had gathered from third-party AI research tools. This paper is my receipt of what happened next. The concept went into a deterministic gate machine — six conservation-law checks, no AI in the decision path — and the dossier failed 0/6. The numbers the AI gave me were not conservative errors; one was 1,849 times above what physics will pay a direct converter. The company then rebuilt the design honestly: 60 kWth, 12 kWe at 20% conversion, Stirling converters, lead-bismuth coolant, seawater immersion. The rebuilt design passes 6/6, survived a 122-day frozen-schedule endurance trial at 99.89% uptime with +36.5 °C worst-case thermal margin, and held zero margin violations across a 10,000-mission Monte Carlo ensemble. Every number in this paper is machine-derived and hashed. This is the customer's side of the receipt: the concept was mine, the fabricated numbers were not my fault — and demanding gates instead of trust is how I found out.

## 1. The concept

I spent my Navy years aboard nuclear submarines — a reactor running quietly beneath the water is not an abstraction to me. The concept: a small nuclear plant, on the seafloor, running quietly for decades: HALEU fuel, direct heat-to-electric conversion, immersion in seawater as the ultimate heat sink, feeding a 5 kW continuous UUV-dock load on a 48 V DC bus. No crew, no surface plant, no fuel handling for years. That is Project SOLACE.

## 2. The dossier I brought, and why I stopped trusting it

My first dossier was assembled from third-party AI research tools. It claimed 12.15 kWe out of 30 kWth — a 40.5% "efficiency" — from a 150 mm core. I could not verify any of it by hand. When I became the first customer engagement of SQUIRL OS Technologies, I asked them not to review it but to machine-verify it.

## 3. The gate machine: 0/6

The company does not review designs; it runs them through six conservation-law gates, each printed with its derivation (gate-machine stress battery: 14/14 adversarial patterns fail-closed):

- Heat rejection: short by 23x.
- Direct-conversion accounting: 1,849x above incident power.
- Coolant phase: the coolant flash-boils at operating conditions.
- Thermodynamic gradient: Second Law violation.
- Nuclear criticality: the core is subcritical.
- Bus arithmetic: the numbers contradict each other.

**Verdict: LOGIC FAILS, 0/6.** That is not a judgment of the concept. It is a judgment of the numbers an AI handed me. Concepts survive; fabrications don't.

## 4. The honest rebuild: 6/6

The rebuilt design, sized by physics instead of optimism: 60 kWth, 12 kWe at 20% conversion, Stirling converters (Kilopower lineage), HALEU 16% enriched, 420 mm core, 551 kg fissile, lead-bismuth primary coolant, 600 °C hot side, seawater immersion at 70 °C cold side.

**Verdict: LOGIC HOLDS, 6/6.**

## 5. 122 days of receipts (SIM SOLACE 1-4, frozen schedule sha cd0f13aa1785eb83)

- 14,640 kWh delivered; 99.89% uptime.
- Worst-case thermal margin +36.5 °C against the 85 °C structural limit.
- Full station blackout drill: detected, isolated, restarted, and verified in 193 minutes.
- Four injected fault/recovery arcs: 4 executed, 4 completed.
- Aged plant (day 118) re-run through all six gates: LOGIC HOLDS 6/6.
- Degradation trial (results sha 01a89013): 7,111 of 7,119 kWh mission demand served; the sea cools faster than fouling accumulates — monthly hull cleaning is sufficient.

## 6. The Ten-Thousand-Year Test (SIM SOLACE 3, sha 6ba234c8)

10,000 seeded missions, one year each: zero margin violations. The worst unit of ten thousand still holds +31.0 °C. Time-compression validation at 1x/5x/20x passes (no clock-cheating). Twenty adversarial no-maintenance corners: all finite, none breached.

## 7. BREAKER: where my gear dies (SIM SOLACE 4, sha 6f6675c8)

The same machine that proves the design also hunts its failure modes, honestly: gear breaks reach breach in 20-43 minutes unprotected; all modes are survivable with scram. The pump was the single point of failure — until the derate ladder (pump-dead survival at 60-70% power, no scram) and the tank-and-steam thermosyphon loop (indefinite pump-loss survival, +40 to +70 °C margin, zero pumps, 6-8 kWe backup) demoted it. The tank alone does not help (0.6 h). Mission endurance over 20 years: margins hold at +37.5 °C; the converter is the ceiling (~14.5 years without overhaul, indefinite with 18-month overhauls); the core holds ~2,400 full-power years.

## 8. What I'd tell anyone handed AI-generated numbers

Trust nothing you cannot derive. The dossier I carried had a confident tone, plausible units, and numbers 1,849x off physics. The gate machine cannot be flattered, rushed, or talked into a pass — and that is precisely what I needed. Every result in this paper is anchored to a hashed, frozen spec and a results digest. If a vendor will not show you the gates, you are not buying engineering; you are buying tone.

## Receipts appendix

| Artifact | Digest |
|---|---|
| Endurance trial, frozen fault schedule | cd0f13aa1785eb83 |
| Endurance trial results | 43c040a0607fc4fa |
| SIM SOLACE 2 degradation results | 01a89013 |
| Ten-Thousand-Year ensemble results | 6ba234c80fa53998 |
| BREAKER battery (amendment v1.2) | 6f6675c33a7800cc |

*All simulation, gate machinery, and receipt work by SQUIRL OS Technologies LLC (engagement owner: Leon Long). The concept, the decision to publish, and the authorship of this account are mine. This paper is tokenized on the Bitcoin and XRP mainnets; explorer links for the anchoring receipts are recorded in the Zenodo entry for this paper.*
