#!/usr/bin/env python3
"""
SOLACE-SIM v0.1 — Deterministic design-logic screening machine
===============================================================
Purpose: adversarial physics screening for compact micro-reactor concepts.
         Takes a JSON design spec, runs six deterministic gates, prints receipts.
Doctrine:
  - NO LLM in any decision path. Every verdict is arithmetic on physical constants.
  - Every gate prints its math so any reviewer can reproduce it by hand.
  - Screening = order-of-magnitude bounding, NOT a substitute for neutronics
    (OpenMC/MCNP) or thermal-hydraulics (ANSYS/COMSOL) when a design advances.
Gates:
  G1 HEAT REJECTION  — First Law: can the shell reject the residual load?
  G2 DIRECT CONV     — First Law: is any claimed direct-conversion power <= ceiling?
  G3 COOLANT PHASE   — does the coolant stay liquid at the hot-side temperature?
  G4 TEG GRADIENT    — Second Law + practical efficiency bounds (<=25% of Carnot)
  G5 CRITICALITY     — is fissile mass in the geometry even in the critical ballpark?
  G6 ARITHMETIC      — internal consistency of the spec's own numbers
"""
import json, math, sys

SIG = 5.67e-8           # Stefan-Boltzmann
SIGMA_SB = SIG
MU_RHO_W = 0.06         # tungsten mass atten. coeff ~1 MeV gamma (cm^2/g)
RHO_W = 19.3            # g/cm^3
GAMMA_FRAC = 0.07       # prompt+decay gamma fraction of fission power
EPS_W = 0.35            # tungsten emissivity (conservative)
H_AIR = 8.0             # natural convection W/m^2K
H_SEA = 300.0           # natural convection in water W/m^2K
BARE_HEU_KG = 52.0      # bare U-235 metal critical mass (kg)
REFLECT_SAVING = 0.6    # thick reflector reduces requirement to ~60%
CARNOT_FRAC_OK = 0.25   # practical solid-state conversion as fraction of Carnot

def gate1(spec):
    P_th = spec["thermal_power_kw"]*1e3
    P_e  = spec["claimed_electric_kw"]*1e3
    r    = spec["outer_shell_radius_m"]
    env  = spec["environment"]
    Ts   = spec["shell_surface_c"]+273.15
    Tamb = spec["ambient_c"]+273.15
    A = 4*math.pi*r*r
    load = P_th - P_e
    q_rad = EPS_W*SIG*A*(Ts**4-Tamb**4)
    h = H_SEA if env=="seawater" else H_AIR
    q_conv = h*A*(Ts-Tamb)
    reject = q_rad+q_conv
    ok = load <= reject
    print(f"  shell area {A:.3f} m^2; residual load {load/1e3:.2f} kW; rejectable {reject/1e3:.2f} kW ({env})")
    print(f"  rad {q_rad:.0f} W + conv {q_conv:.0f} W" + ("  -> PASS" if ok else "  -> FAIL (shortfall %.1fx)" % (load/reject)))
    return ok

def gate2(spec):
    P_th = spec["thermal_power_kw"]*1e3
    claim = spec.get("claimed_direct_conv_kw",0)*1e3
    shield_mm = spec["inner_shield_mm"]
    core_r_cm = spec["core_radius_mm"]/10
    mu_core = 0.07*spec.get("core_eff_density",6.0)   # 1 MeV gamma in core mix
    escape = min(0.75/(mu_core*core_r_cm), 1.0)
    att = math.exp(-(MU_RHO_W*RHO_W)*shield_mm/10)
    P_gamma = P_th*GAMMA_FRAC
    ceiling = P_gamma*escape*att
    print(f"  gamma power {P_gamma:.0f} W; core escape {escape*100:.0f}%; shield survival {att*100:.2f}%")
    print(f"  incident-on-converter ceiling: {ceiling:.1f} W; claimed: {claim:.0f} W")
    if claim == 0:
        print("  -> PASS (no direct-conversion claim)"); return True
    ok = claim <= ceiling
    print(("  -> PASS" if ok else "  -> FAIL (claim exceeds incident power by %.0fx)" % (claim/max(ceiling,0.1))))
    return ok

def gate3(spec):
    fluid = spec["coolant"]
    Thot = spec["hot_side_c"]
    BP = {"mercury":356.7,"LBE":1670,"NaK":785,"FLiNaK":725,"none":1e9}
    bp = BP.get(fluid, 1e9)
    if fluid=="mercury":
        # vapor pressure approx at Thot (Antoine-ish): flag if > 2 atm
        p = math.exp(19.3 - 5800/(Thot+273.15))  # rough atm-scale flag only
        extra = f" (vapor pressure ~{p:.0f} atm at {Thot:.0f}C)"
    else:
        extra = f" (boiling point {bp:.0f}C)"
    ok = Thot < bp - 50
    print(f"  fluid {fluid}{extra}; hot side {Thot:.0f}C vs boiling {bp:.0f}C (50C margin required)")
    print(("  -> PASS" if ok else "  -> FAIL (flash-boil / pressurization risk)"))
    return ok

def gate4(spec):
    Th, Tc = spec["hot_side_c"]+273.15, spec["cold_side_c"]+273.15
    claimed_eff = spec["claimed_electric_kw"]/spec["thermal_power_kw"]
    carnot = 1 - Tc/Th
    conv = spec.get("converter","TEG")
    frac = 0.40 if conv in ("stirling","stirling+TEG") else CARNOT_FRAC_OK
    practical = frac*carnot
    grad_ok = spec["cold_side_c"] >= spec.get("shell_surface_c", spec["cold_side_c"])
    print(f"  converter: {conv}; gradient {spec['hot_side_c']:.0f}C -> {spec['cold_side_c']:.0f}C: Carnot {carnot*100:.1f}%, practical bound {practical*100:.1f}%")
    print(f"  claimed system efficiency {claimed_eff*100:.1f}%")
    print(f"  cold side vs shell equilibrium: {spec['cold_side_c']:.0f}C vs {spec.get('shell_surface_c','n/a')}C")
    ok = (claimed_eff <= practical) and grad_ok and Th > Tc
    print(("  -> PASS" if ok else "  -> FAIL" + ("" if grad_ok else " (Second Law: cold side below shell equilibrium)")))
    return ok

def gate5(spec):
    r_cm = spec["core_radius_mm"]/10
    V = (4/3)*math.pi*r_cm**3
    enr = spec.get("enrichment_frac",0.93)
    packing = spec.get("packing_frac",0.64)
    mass_avail = 19.1*V*packing/1000            # kg U in bed (max fill)
    fissile_avail = mass_avail*enr
    bare = BARE_HEU_KG/max(enr,0.02)**1.5        # crude enrichment scaling
    reflected = bare*REFLECT_SAVING
    ok = fissile_avail >= reflected*0.9
    print(f"  core volume {V:.0f} cm^3; U in bed ~{mass_avail:.1f} kg; fissile ~{fissile_avail:.1f} kg")
    print(f"  rough critical need: bare ~{bare:.0f} kg, reflected ~{reflected:.0f} kg (enrichment {enr*100:.0f}%)")
    print(("  -> PASS (ballpark plausible; real neutronics still required)" if ok else "  -> FAIL (subcritical as specified; scale core or enrichment)"))
    return ok

def gate6(spec):
    ok = True
    Pe = spec["claimed_electric_kw"]; Pth = spec["thermal_power_kw"]
    V, I = spec.get("bus_v",0), spec.get("bus_a",0)
    if V and I:
        m = abs(V*I/1e3 - Pe) <= 0.05*Pe+0.05
        print(f"  bus check: {V} V x {I} A = {V*I/1e3:.2f} kW vs claimed {Pe} kW -> " + ("PASS" if m else "FAIL")); ok &= m
    if spec.get("cluster_modules") and spec.get("cluster_module_kw"):
        tot = spec["cluster_modules"]*spec["cluster_module_kw"]
        m = abs(tot - spec.get("cluster_total_kw",tot)) <= 1
        print(f"  cluster check: {spec['cluster_modules']} x {spec['cluster_module_kw']} kW = {tot} kW vs stated {spec.get('cluster_total_kw','n/a')} kW -> " + ("PASS" if m else "FAIL")); ok &= m
        m2 = spec["cluster_module_kw"] == Pth
        print(f"  cluster module rating ({spec['cluster_module_kw']} kW) vs core spec ({Pth} kW) -> " + ("PASS" if m2 else "FAIL")); ok &= m2
    if not (V and I) and not spec.get("cluster_modules"): print("  (no bus/cluster claims to check)")
    return ok

def validate(spec):
    """Fail-closed input validation. Invalid specs get LOGIC FAILS with a receipt, never a crash."""
    required = ["thermal_power_kw","claimed_electric_kw","core_radius_mm","inner_shield_mm",
                "coolant","hot_side_c","cold_side_c","shell_surface_c","environment",
                "outer_shell_radius_m","ambient_c"]
    numeric = ["thermal_power_kw","claimed_electric_kw","core_radius_mm","inner_shield_mm",
               "hot_side_c","cold_side_c","shell_surface_c","outer_shell_radius_m","ambient_c"]
    for k in required:
        if k not in spec:
            print(f"  INPUT INVALID: required field '{k}' missing"); return False
    for k in numeric:
        v = spec[k]
        if isinstance(v,(int,float)) and not math.isfinite(v):
            print(f"  INPUT INVALID: field '{k}' is non-finite ({v})"); return False
        if not isinstance(v,(int,float)) or isinstance(v,bool):
            print(f"  INPUT INVALID: field '{k}' is not a finite number ({v!r})"); return False
    if spec["thermal_power_kw"] <= 0:
        print(f"  INPUT INVALID: thermal power must be > 0 (got {spec['thermal_power_kw']})"); return False
    if spec["outer_shell_radius_m"] <= 0 or spec["core_radius_mm"] <= 0:
        print("  INPUT INVALID: radii must be > 0"); return False
    # Declared screening scope: compact micro-reactors only (0.05-10 m shell, <=2 m core)
    if not (0.05 <= spec["outer_shell_radius_m"] <= 10):
        print(f"  INPUT INVALID: outer radius {spec['outer_shell_radius_m']} m outside screening scope (0.05-10 m)"); return False
    if spec["core_radius_mm"] > 2000:
        print(f"  INPUT INVALID: core radius {spec['core_radius_mm']} mm outside screening scope (<=2000 mm)"); return False
    if spec["claimed_electric_kw"] > spec["thermal_power_kw"]:
        print(f"  INPUT INVALID: overunity — claimed electric {spec['claimed_electric_kw']} kW > thermal {spec['thermal_power_kw']} kW")
        print("  -> FAIL (First Law: output cannot exceed thermal input)"); return False
    return True

def run(spec_file):
    spec = json.load(open(spec_file))
    name = spec.get("name", spec_file)
    print("="*76)
    print(f"SOLACE-SIM v1.1 | {name}")
    print("="*76)
    if not validate(spec):
        print("\n" + "="*76)
        print("VERDICT: LOGIC FAILS (input rejected, fail-closed)   (deterministic)")
        print("="*76)
        return {"INPUT": False}
    gates = {"G1 heat rejection":gate1,"G2 direct conversion":gate2,"G3 coolant phase":gate3,
             "G4 TEG gradient":gate4,"G5 criticality":gate5,"G6 arithmetic":gate6}
    results = {}
    for g, fn in gates.items():
        print(f"\n[{g}]")
        results[g] = fn(spec)
    npass = sum(results.values())
    print("\n" + "="*76)
    verdict = "LOGIC HOLDS" if npass==6 else f"LOGIC FAILS ({npass}/6 gates)"
    print(f"VERDICT: {verdict}   (deterministic; no LLM in any decision path)")
    print("="*76)
    return results

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv)>1 else "spec_original.json")
