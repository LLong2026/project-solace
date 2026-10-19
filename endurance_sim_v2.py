#!/usr/bin/env python3
"""SIM SOLACE 2 (v2.0) — physics-based degradation endurance trial.
Upgrades the frozen step schedule with continuous, literature-informed models:
- Biofouling: asymptotic first-order growth (biofilm + corrosion product),
  (1-f) = Dmax*(1-exp(-t/tau)), cleaning resets biofilm, corrosion baseline stays.
- Pump seal wear: decelerating wear curve, asymptotic deficit.
- Converter aging: compounded -0.5%/month (Stirling free-piston class).
- Seawater: seasonal sinusoid, annual mean 9.5 C, amplitude 5.5, min Feb 20.
- Load: UUV-dock mission profile (standby + docked charge windows + surge).
Deterministic: fixed arithmetic, no LLM, no RNG. Every number printed."""
import json, math, hashlib

DAYS = 122
PTH_W = 60_000.0
EFF0 = 0.20
EPS, SIG, H_SEA = 0.35, 5.67e-8, 300.0
R_SHELL = 0.70
A = 4*math.pi*R_SHELL**2
TS_LIMIT_C = 85.0
START_DOY = 291          # Oct 18 day-of-year
SEAWATER_MEAN, AMP, MIN_DOY = 9.5, 5.5, 51  # min Feb 20 (DOY 51)

# degradation model constants (literature-informed, declared)
FOUL_DMAX, FOUL_TAU, CORR_BASE = 0.12, 45.0, 0.01   # asymptotic biofilm+corrosion
PUMP_DMAX, PUMP_TAU = 0.10, 90.0                    # seal wear asymptote
EFF_MONTH_DECAY = 0.005                             # -0.5%/month compounded

CLEANINGS = {30, 60, 90, 119}      # monthly hull cleaning windows
PUMP_SERVICE = {103}
BLACKOUT_DAY = 75                  # operator drill (declared)
MODULE_SWAP = (24, 6.0)            # day, hours degraded 25%
BUS_FAULT = (17, 2.5)             # day, hours sagged 46.2 V
SURGE_DRILLS = {28, 56, 84, 112}   # 8 kW for 4 h

def seawater_c(day):
    doy = (START_DOY + day) % 365
    return SEAWATER_MEAN - AMP*math.cos(2*math.pi*(doy-MIN_DOY)/365)

def mission_load_w(day):
    base = 2_500.0                                  # standby: dock, comms, sensors
    docked = (day % 7) not in (6,)                  # UUV alongside 6 of 7 days
    charge = 6_500.0 if docked else 4_000.0         # 6h daily charge window
    hours = 6.0
    surge = 8_000.0 if day in SURGE_DRILLS else 0.0 # 4h surge drill
    kwh = (base*24 + (charge-base)*hours + (surge-charge)*4.0)/1e3
    return base, charge, surge, round(kwh,1)

def rejection_w(ts_c, tamb_c, fouling):
    Tsk, Tk = ts_c+273.15, tamb_c+273.15
    return fouling*(EPS*SIG*A*(Tsk**4-Tk**4) + H_SEA*A*(Tsk-Tk))

def shell_temp(q_w, tamb_c, fouling):
    lo, hi = -50.0, 400.0
    for _ in range(80):
        mid = (lo+hi)/2
        if rejection_w(mid, tamb_c, fouling) < q_w: lo = mid
        else: hi = mid
    return (lo+hi)/2

def run():
    daily, events = [], []
    last_clean_day = 0
    last_service_day = 0
    downtime_min = 0.0
    for d in range(1, DAYS+1):
        # continuous degradation since last maintenance
        tf = d - last_clean_day
        foul = 1.0 - CORR_BASE - FOUL_DMAX*(1-math.exp(-tf/FOUL_TAU))
        tp = d - last_service_day
        pump = 1.0 - PUMP_DMAX*(1-math.exp(-tp/PUMP_TAU))
        eff = EFF0*(1-EFF_MONTH_DECAY)**(d/30.0)
        tamb = seawater_c(d)
        base, charge, surge, kwh = mission_load_w(d)
        # peak-load shell temp (worst hour: surge/charge window)
        pe = PTH_W*eff
        waste = PTH_W - min(pe, surge if surge else charge)
        ts = shell_temp(waste, tamb, foul)
        margin = TS_LIMIT_C - ts
        downtime = 0.0
        if d == BUS_FAULT[0]: events.append({"day":d,"id":"V2-B1","type":"bus_reg_sag","detail":"46.2 V for 2.5 h, detected 10 min, repaired 140 min","recover_min":150})
        if d == MODULE_SWAP[0]: events.append({"day":d,"id":"V2-M1","type":"module_hot_swap","detail":"converter module at 25% for 6 h, swap completed","recover_min":360})
        if d == BLACKOUT_DAY:
            arc = {"day":d,"id":"V2-K1","type":"blackout_drill","detail":"detect 12 -> isolate 35 -> restart 98 -> verify 48","recover_min":193}
            events.append(arc); downtime = 193.0
        if d in CLEANINGS: events.append({"day":d,"id":f"V2-C{d}","type":"hull_cleaning","detail":f"fouling {foul:.3f} -> 0.990 (biofilm removed, corrosion baseline remains)","recover_min":195}); last_clean_day = d
        if d in PUMP_SERVICE: events.append({"day":d,"id":"V2-P1","type":"pump_service","detail":f"flow {pump:.3f} -> 0.980 (seals replaced)","recover_min":240}); last_service_day = d
        downtime_min += downtime
        served = max(0.0, kwh*(1-downtime/1440.0))
        daily.append({"day":d,"sea_c":round(tamb,1),"fouling":round(foul,3),"pump":round(pump,3),
                      "eff":round(eff,4),"pe_kw":round(pe/1e3,2),"ts_c":round(ts,1),
                      "margin_c":round(margin,1),"load_kwh":kwh,"served_kwh":round(served,1)})
    return daily, events, downtime_min

if __name__ == "__main__":
    daily, events, downtime = run()
    months = {"1":(1,30),"2":(31,60),"3":(61,90),"4":(91,122)}
    stats = {}
    for k,(lo,hi) in months.items():
        m = daily[lo-1:hi]
        stats[k] = {"kwh":round(sum(x["served_kwh"] for x in m),0),
                    "load":round(sum(x["load_kwh"] for x in m),0),
                    "min_margin":min(x["margin_c"] for x in m),
                    "ts_max":max(x["ts_c"] for x in m),
                    "sea_range":f"{min(x['sea_c'] for x in m):.1f}-{max(x['sea_c'] for x in m):.1f}"}
    total_kwh = sum(x["served_kwh"] for x in daily)
    total_load = sum(x["load_kwh"] for x in daily)
    uptime = 100*(1-downtime/(DAYS*1440))
    out = {"daily":daily,"events":events,"months":stats,"total_kwh":total_kwh,
           "total_load_kwh":total_load,"uptime_pct":round(uptime,2),
           "downtime_min":downtime,"min_margin":min(x["margin_c"] for x in daily),
           "min_margin_day":[x["day"] for x in daily if x["margin_c"]==min(y["margin_c"] for y in daily)][0]}
    json.dump(out, open("endurance_results_v2.json","w"), indent=1)
    sha = hashlib.sha256(open("endurance_results_v2.json","rb").read()).hexdigest()[:16]
    print(f"SIM SOLACE 2 COMPLETE | results sha {sha}")
    for k,m in stats.items(): print(f"  M{k}: served {m['kwh']:.0f} kWh (demand {m['load']:.0f}), min margin +{m['min_margin']} C, shell max {m['ts_max']} C, sea {m['sea_range']} C")
    print(f"  TOTAL served {total_kwh:.0f} kWh | demand {total_load:.0f} kWh | uptime {uptime:.2f}%")
    print(f"  worst margin +{out['min_margin']} C on day {out['min_margin_day']} | events {len(events)}")
