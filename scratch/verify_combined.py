import re, os

# Check operations.html
with open('frontend/operations.html', 'r', encoding='utf-8') as f:
    ops = f.read()

# Check judge_demo.html
with open('frontend/judge_demo.html', 'r', encoding='utf-8') as f:
    judge = f.read()

print("=== operations.html VERIFICATION ===")
print(f"File size: {len(ops):,} bytes")

checks = [
    ("Has 6-col KPI grid", "kpi-grid" in ops and "kpi-trains-val" in ops and "kpi-intv-val" in ops),
    ("Has traceability pipeline", "trace-pipeline" in ops and "trace-disruption" in ops),
    ("Has network SVG map", "topology-svg" in ops),
    ("Has AI decision engine", "ai-card" in ops and "ai-issue-val" in ops),
    ("Has counterfactual bars", "bar-baseline-val" in ops and "bar-quantum-val" in ops),
    ("Has solver benchmark", "solver-hybrid-e" in ops),
    ("Has candidate actions list", "top-candidate-actions-list" in ops),
    ("Has passenger impact panel", "pass-delayed-val" in ops),
    ("Has QUBO metrics panel", "qubo-energy-val" in ops and "refined-energy-val" in ops),
    ("Has congestion metrics", "cong-baseline-val" in ops),
    ("Has event timeline", "timeline-bar" in ops),
    ("Has 5-col bottom grid", "bottom-grid" in ops),
    ("Has dark sidebar", "--sidebar-bg: #0b0f19" in ops),
    ("Has mode-badge from simulation", "id=\"mode-badge\"" in ops),
    ("No 18320 hardcoded", "18,320" not in ops),
    ("No 33.6% hardcoded", "33.6%" not in ops),
    ("No 12 min recovery hardcoded", ">12 min<" not in ops),
    ("No CSI 68 hardcoded", ">68 /100<" not in ops),
    ("Has EMBEDDED_STATE", "const EMBEDDED_STATE" in ops),
    ("Has updateDashboard called", "updateDashboard(EMBEDDED_STATE)" in ops),
    ("Has Pareto Frontier + Solver combined", "pareto-frontier-svg" in ops and "solver-hybrid-e" in ops),
]

all_ok = True
for name, result in checks:
    status = "PASS" if result else "FAIL"
    if not result:
        all_ok = False
    print(f"  [{status}] {name}")

print()
if all_ok:
    print("ALL CHECKS PASSED!")
else:
    print("SOME CHECKS FAILED!")

print()
print("=== judge_demo.html ===")
print(f"File size: {len(judge)} bytes")
print(f"  [{'PASS' if 'url=operations.html' in judge else 'FAIL'}] Has redirect to operations.html")
print(f"  [{'PASS' if 'updateJudgeDemo' not in judge else 'FAIL'}] No old JS code")
print(f"  [{'PASS' if len(judge) < 500 else 'FAIL'}] Is lightweight redirect (< 500 bytes)")
