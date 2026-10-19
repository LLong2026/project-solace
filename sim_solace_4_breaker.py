#!/usr/bin/env python3
"""SIM SOLACE 4: BREAKER — find where the gear actually dies.
Amendment v1.2 (disclosed): pump flow is now COUPLED to convective sink
coefficient (it was tracked-but-uncoupled in v2/v3 — a declared model gap,
fixed forward-only here).
Failure modes run minute-stepped with real thermal inertia (C = 1.5e6 J/K),
each twice: UNPROTECTED (does it breach? when?) and PROTECTED (margin < 10 C
trips the reactor; decay heat 7% decaying t^-0.2; can it survive its own gear
breaking?). Deterministic; no LLM in the decision path."""
import json, hashlib

PTH = 60_000.0; EPS, SIG, R = 0.35, 5.67e-8, 0.70
AREA = 4*3.14159*R**2; H0 = 300.0; TS_LIMIT = 85.0
SEA_C = 10.0; C_THERM = 1.5e6   # J/K structural thermal inertia
EFF = 0.196; PE = PTH*EFF

def rejection(ts, foul, pump):
    rad = EPS*SIG*AREA*((ts+273.15)**4 - (SEA_C+273.15)**4)
    conv = H0*(0.3 + 0.7*pump)*AREA*(ts - SEA_C)   # pump-coupled sink
    return foul*(rad + conv)

def run_mode(name, foul, pump, electric_load, protected, hours=720):
    ts = 43.0  # normal operating shell temp
    t = 0.0; dt = 10.0  # seconds
    tripped = False; trip_at = None; breach_at = None
    steps = int(hours*3600/dt)
    for s in range(steps):
        pth = PTH
        if protected and not tripped and (TS_LIMIT - ts) < 10.0:
            tripped = True; trip_at = t
        if tripped:
            th = t - trip_at
            pth = 0.07*PTH*(th*3600+1)**-0.2*3600/ (th*3600+1)**0.0 # decay curve (W)
            pth = 0.07*PTH*(1.0+th)**-0.2
        waste = pth - min(pth*EFF, electric_load) if not tripped else pth
        if tripped: waste = pth  # all decay heat is waste at zero load
        rej = rejection(ts, foul, pump)
        ts += (waste - rej)/C_THERM*dt
        t += dt/3600.0
        if breach_at is None and ts >= TS_LIMIT:
            breach_at = t; break
    return {"mode":name,"foul":foul,"pump":pump,"load_kw":electric_load/1e3,
            "protected":protected,"tripped":tripped,
            "trip_at_h":round(trip_at,2) if trip_at else None,
            "breach_at_h":round(breach_at,2) if breach_at else None,
            "end_ts_c":round(ts,1),"end_margin_c":round(TS_LIMIT-ts,1)}

MODES = [
 ("A_pump_seizure",        0.93, 0.0, 5_000.0),
 ("B_macrofouling_blanket",0.20, 1.0, 5_000.0),
 ("C_full_load_disconnect",0.93, 1.0, 0.0),
 ("D_combined_catastrophe", 0.20, 0.0, 0.0),
 ("E_seawater_warming",    0.93, 1.0, 5_000.0),
]
SEA_C = 28.0  # mode E override below per-mode; handle separately
results = []
for name, foul, pump, load in MODES:
    if name == "E_seawater_warming":
        SEA_C = 28.0
    else:
        SEA_C = 10.0
    results.append(run_mode(name, foul, pump, load, protected=False))
    results.append(run_mode(name, foul, pump, load, protected=True))
SEA_C = 10.0
out = {"amendment":"v1.2 pump-coupled sink","modes":results}
json.dump(out, open("solace4_results.json","w"), indent=1)
sha = hashlib.sha256(open("solace4_results.json","rb").read()).hexdigest()[:16]
print(f"SIM SOLACE 4 BREAKER COMPLETE | sha {sha}")
for r in results:
    tag = "PROTECTED" if r["protected"] else "UNPROTECTED"
    breach = f"BREACH at {r['breach_at_h']} h" if r["breach_at_h"] else "no breach in 720 h"
    trip = f"tripped at {r['trip_at_h']} h" if r["tripped"] else "no trip"
    print(f"  {r['mode']:24s} {tag:11s} {trip:16s} {breach:26s} end {r['end_ts_c']}C (margin {r['end_margin_c']:+.1f}C)")
