import re, json, os

def check_file(path, expected_ids, forbidden_strings):
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist!")
        return False
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    m = re.search(r"const EMBEDDED_STATE\s*=\s*(\{.*?\});", content, re.DOTALL)
    if not m:
        print(f"FAIL: EMBEDDED_STATE block not found in {path}!")
        return False
        
    try:
        state = json.loads(m.group(1))
    except Exception as e:
        print(f"FAIL: EMBEDDED_STATE JSON parse failed in {path}: {e}")
        return False
        
    all_ok = True
    print(f"=== Verification of {path} (Size: {len(content):,} bytes) ===")
    
    # Check expected dynamic IDs exist in markup
    for eid in expected_ids:
        if eid not in content:
            print(f"  [FAIL] ID '{eid}' not found in file markup!")
            all_ok = False
        else:
            print(f"  [PASS] Found ID '{eid}'")
            
    # Check forbidden static placeholders/numbers do not exist or are properly handled
    for fs in forbidden_strings:
        if fs in content:
            # Check if it is inside the EMBEDDED_STATE JSON (which is allowed) or if it's in the static HTML markup
            # We can strip out the EMBEDDED_STATE block to check the rest of the content
            content_no_state = content.replace(m.group(0), "")
            if fs in content_no_state:
                print(f"  [FAIL] Forbidden static string '{fs}' found in HTML markup!")
                all_ok = False
            else:
                print(f"  [PASS] Forbidden string '{fs}' only found in EMBEDDED_STATE JSON.")
        else:
            print(f"  [PASS] No forbidden string '{fs}' found.")
            
    return all_ok

print("Running dynamic frontend verifications...")
ops_ok = check_file(
    "frontend/operations.html",
    ["kpi-trains-val", "kpi-baseline-val", "kpi-opt-val", "kpi-reduction-val", "kpi-qubo-val", "kpi-intv-val",
     "trace-disruption-val", "trace-ai-val", "trace-qubo-val", "trace-qaoa-val", "trace-refine-val", "trace-impact-val",
     "topology-svg", "ai-issue-val", "ai-trains-val", "ai-delay-val", "ai-action-val", "ai-conf-val",
     "bar-baseline-val", "bar-quantum-val",
     "solver-hybrid-e", "solver-raw-e", "solver-sa-e", "top-candidate-actions-list",
     "pass-delayed-val", "pass-saved-val", "qubo-energy-val", "refined-energy-val",
     "qaoa-runtime-val", "classical-runtime-val", "timeline-container", "map-station-1", "map-station-10"],
    ["18,320", "33.6%"]
)

opt_ok = check_file(
    "frontend/optimization.html",
    ["opt-framework-val", "opt-backend-val", "opt-hardware-val", "opt-depth-val", "opt-circuit-depth-val",
     "opt-gates-val", "opt-shots-val", "opt-status-val", "qubo-mappings-list", "offset-label",
     "measured-bitstrings-container", "refine-raw-energy", "refine-raw-bitstring", "refine-final-energy", "refine-gap"],
    ["Qubits: 6", "10110 (Optimum)", "48.5 ms", "45.2 ms", "4.1 ms", "1.2 ms", "Energy: -2.10", "Energy: -2.50"]
)

net_ok = check_file(
    "frontend/network.html",
    ["topology-svg", "map-station-1", "map-station-10", "map-track-1", "map-track-10", "sim-clock", "mode-badge", "weather-badge-text"],
    []
)

if ops_ok and opt_ok and net_ok:
    print("\nALL FRONTEND PAGES PASSED VERIFICATION!")
else:
    print("\nSOME FRONTEND PAGES FAILED VERIFICATION!")
