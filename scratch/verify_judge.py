import json, re

with open('frontend/judge_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find EMBEDDED_STATE
m = re.search(r'const EMBEDDED_STATE = (\{.*?\});', content, re.DOTALL)
if m:
    state = json.loads(m.group(1))
    imp = state.get('impact', {})
    stations = state["stations"]
    trains = state["trains"]
    tracks = state["tracks"]
    print('== VERIFICATION ==')
    print(f'Stations: {len(stations)}')
    print(f'Trains: {len(trains)}')
    print(f'Tracks: {len(tracks)}')
    print(f'Baseline Delay: {imp.get("baseline_delay")} min')
    print(f'Optimized Delay: {imp.get("optimized_delay")} min')
    print(f'Delay Reduction: {imp.get("delay_reduction_pct")}%')
    print(f'QUBO Energy: {imp.get("qubo_energy")}')
    print(f'Refined Energy: {imp.get("refined_energy")}')
    print(f'QAOA Runtime: {imp.get("qaoa_runtime")} s')
    print(f'Classical Runtime: {imp.get("classical_runtime")} s')
    print(f'File size: {len(content)} bytes')
    print(f'Has sidebar: {"sidebar" in content}')
    print(f'Has KPI grid: {"kpi-grid" in content}')
    print(f'Has traceability pipeline: {"trace-pipeline" in content}')
    print(f'No hardcoded 18320: {"18320" not in content}')
    print(f'No hardcoded 33.6%: {"33.6%" not in content}')
else:
    print('ERROR: EMBEDDED_STATE not found')
