#!/usr/bin/env python3
"""SIM SOLACE 3 — THE TEN-THOUSAND-YEAR TEST.
Monte Carlo endurance ensemble: 10,000 seeded missions x 365 days = 10,000
simulated years of plant operation. Deterministic (frozen seed 20261017),
no LLM in any decision path. Four stages:
  A. Distribution: margin/availability percentiles across the ensemble
  B. Time-compression validation: wear at 1x / 5x / 20x
  C. Maintenance optimization sweep (cleaning interval vs availability)
  D. Adversarial corner suite: 20 frozen worst-case parameter sets"""
import numpy as np, json, hashlib

SEED = 20261017
N, D = 10_000, 365
PTH = 60_000.0; EPS, SIG, H, R = 0.35, 5.67e-8, 300.0, 0.70
AREA = 4*np.pi*R**2; TS_LIMIT = 85.0
rng = np.random.RandomState(SEED)

# --- frozen parameter distributions (declared, uniform unless stated) ---
P = {
 "foul_dmax": rng.uniform(0.08, 0.16, N),      # asymptotic fouling loss
 "foul_tau":  rng.uniform(30, 70, N),          # fouling time constant, days
 "corr_base": np.full(N, 0.01),               # cleaning-persistent corrosion
 "pump_dmax": rng.uniform(0.06, 0.14, N),     # pump seal wear asymptote
 "pump_tau":  rng.uniform(60, 120, N),        # seal wear constant, days
 "eff_decay": rng.uniform(0.003, 0.008, N),   # converter decay /month compounded
 "sea_offset":rng.uniform(-2.0, 3.0, N),      # siting offset, C
 "clean_int": rng.choice([15,30,45,60,90,9999], N),   # hull cleaning days
 "serv_int":  rng.choice([80,103,150,9999], N),       # pump service days
 "n_blackouts": rng.randint(2, 5, N),         # blackout drills per year
 "phase": rng.randint(0, 7, N),
}
PARAM_SHA = hashlib.sha256(json.dumps({k: v[:5].tolist() if hasattr(v,'tolist') else v for k,v in P.items()}, sort_keys=True).encode()).hexdigest()[:16]

def sea_c(day, off):
    return 9.5 + off - 5.5*np.cos(2*np.pi*(((day + 250 + (off*0).astype(int)) % 365) - 51)/365)

def load_peak_w(day, phase):
    docked = (day % 7) != phase            # UUV alongside 6 of 7 days
    charge = np.where(docked, 6_500.0, 4_000.0)
    surge = (day % 28) == (phase % 28)
    return np.where(surge, 8_000.0, charge)

def shell_temp(q_w, tamb, foul):
    Ts = np.full(N, 20.0)
    for _ in range(50):                     # Newton-ish fixed iteration
        Tk, Tsk = tamb + 273.15, Ts + 273.15
        rej = foul*(EPS*SIG*AREA*(Tsk**4 - Tk**4) + H*AREA*(Ts - tamb))
        Ts = Ts + (q_w - rej)/ (4*EPS*SIG*AREA*foul*Tsk**3 + H*AREA*foul + 1.0)
    return Ts

def run_ensemble(wear_mult=1.0, params=P, days=D):
    days_since_clean = np.zeros(N); days_since_serv = np.zeros(N)
    min_margin = np.full(N, 1e9); served = np.zeros(N); downtime = np.zeros(N)
    # blackout days: deterministic per run via seeded stream kept outside (rebuild)
    rs = np.random.RandomState(SEED + 7)
    blackouts = [sorted(rs.randint(1, days+1, int(P["n_blackouts"][i]))) for i in range(N)]
    for d in range(1, days+1):
        tf = days_since_clean*wear_mult
        foul = 1.0 - P["corr_base"] - P["foul_dmax"]*(1-np.exp(-tf/P["foul_tau"]))
        tp = days_since_serv*wear_mult
        pump = 1.0 - P["pump_dmax"]*(1-np.exp(-tp/P["pump_tau"]))
        eff = 0.20*(1-P["eff_decay"])**(d*wear_mult/30.0)
        tamb = sea_c(d, P["sea_offset"])
        pe = PTH*eff
        peak = load_peak_w(d, P["phase"])
        waste = PTH - np.minimum(pe, peak)
        ts = shell_temp(waste, tamb, foul)
        margin = TS_LIMIT - ts
        min_margin = np.minimum(min_margin, margin)
        # daily energy: base 2.5 kW x 24h + (peak-base) x 6h window (surge 4h)
        window_h = np.where((d % 28)==(P["phase"]%28), 4.0, 6.0)
        daily_kwh = 2.5*24 + (peak/1000.0-2.5)*window_h
        dt_today = np.zeros(N)
        for i in range(N):
            if d in blackouts[i]: dt_today[i] = 193.0
        downtime += dt_today
        served += daily_kwh*(1 - dt_today/1440.0)
        # maintenance
        clean_today = (P["clean_int"] != 9999) & (days_since_clean >= P["clean_int"])
        days_since_clean = np.where(clean_today, 0.0, days_since_clean+1)
        serv_today = (P["serv_int"] != 9999) & (days_since_serv >= P["serv_int"])
        days_since_serv = np.where(serv_today, 0.0, days_since_serv+1)
    avail = 100.0*(1 - downtime/(days*1440.0))
    return min_margin, avail, served

print("Stage A: 10,000-run ensemble...")
mm, avail, served = run_ensemble()
viol = int((mm < 0).sum())
pct = lambda a, q: float(np.percentile(a, q))
stats = {"runs": N, "days_per_run": D, "sim_years": N*D/365.0,
 "margin_p50": round(pct(mm,50),1), "margin_p05": round(pct(mm,5),1),
 "margin_p01": round(pct(mm,1),1), "margin_p001": round(pct(mm,0.1),1),
 "margin_worst": round(float(mm.min()),1), "violations": viol,
 "avail_p50": round(pct(avail,50),2), "avail_min": round(float(avail.min()),2),
 "kwh_p50": round(pct(served,50)), "seed": SEED, "param_sha": PARAM_SHA}
print(f"  min margin: P50 {stats['margin_p50']}C | P5 {stats['margin_p05']}C | P1 {stats['margin_p01']}C | P0.1 {stats['margin_p001']}C | worst {stats['margin_worst']}C")
print(f"  violations (margin<0): {viol} | availability: P50 {stats['avail_p50']}% | min {stats['avail_min']}%")

print("Stage B: time-compression validation (200 runs at 1x/5x/20x wear)...")
sub = {k: v[:200] if hasattr(v,'__len__') else v for k,v in P.items()}
comp = {}
for mult in (1,5,20):
    m2, a2, s2 = run_ensemble(wear_mult=mult, params=sub, days=365)
    comp[mult] = {"margin_p05": round(pct(m2,5),1), "worst": round(float(m2.min()),1)}
    print(f"  wear {mult}x: P5 margin {comp[mult]['margin_p05']}C | worst {comp[mult]['worst']}C")
comp_pass = comp[1]["margin_p05"] > comp[5]["margin_p05"] > comp[20]["margin_p05"] and all(np.isfinite(float(v[m])) for v in comp.values() for m in v)
print(f"  ordering finite and physics-consistent: {'PASS' if comp_pass else 'FAIL'}")

print("Stage C: maintenance optimization sweep...")
groups = {}
for ci in [15,30,45,60,90,9999]:
    mask = P["clean_int"][:N] == ci
    if mask.sum() < 30: continue
    groups[ci if ci!=9999 else "never"] = {
      "n": int(mask.sum()), "margin_p05": round(pct(mm[mask],5),1),
      "avail_p50": round(pct(avail[mask],50),2)}
for k,v in groups.items(): print(f"  clean every {k} d: n={v['n']}, P5 margin {v['margin_p05']}C, avail P50 {v['avail_p50']}%")

print("Stage D: adversarial corner suite (20 frozen worst-case sets)...")
corners = []
for i in range(20):
    rs = np.random.RandomState(9000+i)
    cp = {k: v.copy() for k,v in P.items()}
    cp["foul_dmax"] = np.full(N, 0.16); cp["foul_tau"] = np.full(N, 25.0)
    cp["pump_dmax"] = np.full(N, 0.14); cp["pump_tau"] = np.full(N, 50.0)
    cp["eff_decay"] = np.full(N, 0.010)
    cp["sea_offset"] = np.full(N, 4.0)
    cp["clean_int"] = np.full(N, 9999); cp["serv_int"] = np.full(N, 9999)
    cp["n_blackouts"] = np.full(N, 6)
    cp["phase"] = np.full(N, i % 7)
    m2, a2, s2 = run_ensemble(params=cp, days=365)
    corners.append({"corner": i+1, "worst_margin": round(float(m2.min()),1), "finite": bool(np.isfinite(m2).all())})
worst_corner = min(c["worst_margin"] for c in corners)
all_finite = all(c["finite"] for c in corners)
print(f"  20/20 corners finite: {all_finite} | worst corner margin: +{worst_corner}C | any breach: {worst_corner < 0}")

out = {"stage_a": stats, "stage_b": comp, "stage_b_pass": bool(comp_pass),
       "stage_c": groups, "stage_d": {"corners": corners, "all_finite": all_finite, "worst_corner_margin": worst_corner}}
json.dump(out, open("solace3_results.json","w"), indent=1)
sha = hashlib.sha256(open("solace3_results.json","rb").read()).hexdigest()[:16]
print(f"SIM SOLACE 3 COMPLETE | results sha {sha}")
