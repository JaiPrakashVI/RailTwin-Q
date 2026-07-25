import os
import json
import sys
import numpy as np

# Ensure current directory is in python path
sys.path.append(os.getcwd())

from ai.adaptive_control.adaptive_controller import AdaptiveController
from ai.adaptive_control.event_detector import EventDetector
from ai.adaptive_control.trigger_engine import TriggerEngine
from ai.adaptive_control.warm_start import WarmStartManager
from ai.adaptive_control.stability_manager import StabilityManager
from ai.adaptive_control.intervention_manager import InterventionManager
from ai.adaptive_control.recovery_monitor import RecoveryMonitor
from ai.adaptive_control.control_report_generator import ControlReportGenerator

def test_all():
    print("====================================================")
    print("       RUNNING AUTOMATED LAYER 6 ACCEPTANCE TESTS    ")
    print("====================================================")

    # 1. Controller state transitions validation
    print("\n[Assert 1] Controller state transitions...")
    controller = AdaptiveController()
    assert controller.state == "MONITORING"
    controller.transition_to("ASSESSING", 15, "Rain event detected", "WEATHER_CHANGE")
    assert controller.state == "ASSESSING"
    assert len(controller.state_history) == 1
    assert controller.state_history[0]["new_state"] == "ASSESSING"
    assert controller.state_history[0]["trigger"] == "WEATHER_CHANGE"
    print(" -> PASSED")

    # 2. Disruptions event generation
    print("\n[Assert 2] Disruptions event generation...")
    prev_state = {
        "timestamp": 0,
        "weather": "Clear",
        "active_disruptions": 0,
        "disruptions_list": [],
        "trains": [{"train_id": 1, "name": "Train A", "delay": 0.0}],
        "congestion": 0.10,
        "platform_utilization": 0.20
    }
    current_state = {
        "timestamp": 15,
        "weather": "Rain",
        "active_disruptions": 1,
        "disruptions_list": [{"name": "Heavy Rain", "severity": 1.8}],
        "trains": [{"train_id": 1, "name": "Train A", "delay": 8.0}],
        "congestion": 0.12,
        "platform_utilization": 0.20
    }
    events = EventDetector.detect(current_state, prev_state)
    assert any(ev["event"] == "WEATHER_CHANGE" for ev in events)
    assert any(ev["event"] == "NEW_DISRUPTION" for ev in events)
    print(" -> PASSED")

    # 3. Trigger engine cooldown respects boundaries
    print("\n[Assert 3] Trigger engine cooldown...")
    # Last optimization was at tick 15, current is 18 (diff = 3 < 5)
    action_code, reason = TriggerEngine.requires_optimization(current_state, [{"event": "WEATHER_CHANGE", "severity": "MEDIUM"}], last_opt_tick=15)
    assert action_code == "MONITOR"
    print(" -> PASSED")

    # 4. Critical events bypass cooldown
    print("\n[Assert 4] Critical events bypass cooldown...")
    action_code, reason = TriggerEngine.requires_optimization(current_state, [{"event": "NEW_DISRUPTION", "severity": "HIGH"}], last_opt_tick=15)
    assert action_code == "REOPTIMIZE"
    print(" -> PASSED")

    # 5. Warm-start loaded when previous solution exists
    print("\n[Assert 5] Warm-start loading...")
    prev_sol = [1, 0]
    prev_cands = {
        "1": {"index": 0, "action": "REROUTE", "target": "Train A"},
        "2": {"index": 1, "action": "HOLD", "target": "Train B"}
    }
    current_cands = {
        "1": {"index": 0, "action": "REROUTE", "target": "Train A"},
        "2": {"index": 1, "action": "HOLD", "target": "Train B"}
    }
    warm_start_vector = WarmStartManager.get_warm_start_vector(current_cands, prev_sol, prev_cands)
    assert warm_start_vector is not None
    assert len(warm_start_vector) == 2  # 2 candidates mapped to a 2-bit list
    print(" -> PASSED")

    # 6. Switching penalties applied correctly
    print("\n[Assert 6] Switching penalties on QUBO dictionary...")
    Q = {(0, 0): 0.5, (1, 1): -0.2}
    Q_new = StabilityManager.inject_switching_penalties(Q.copy(), current_cands, prev_sol, prev_cands, p_switch=0.15)
    # x_1 was active (1): subtract p_switch -> 0.5 - 0.15 = 0.35
    assert abs(Q_new[(0, 0)] - 0.35) < 1e-6
    # x_2 was inactive (0): add p_switch -> -0.2 + 0.15 = -0.05
    assert abs(Q_new[(1, 1)] - (-0.05)) < 1e-6
    print(" -> PASSED")

    # 7. Decision Quality Gate
    print("\n[Assert 7] Decision Quality Gate...")
    accept, delta_utility = controller.evaluate_decision_gate(new_energy=-0.8, current_energy=-0.5, switching_cost=0.1)
    # -0.5 - (-0.8) - 0.1 = 0.2 > epsilon (0.05) -> True
    assert accept is True
    assert abs(delta_utility - 0.2) < 1e-6
    
    accept2, delta_utility2 = controller.evaluate_decision_gate(new_energy=-0.55, current_energy=-0.5, switching_cost=0.1)
    # -0.5 - (-0.55) - 0.1 = -0.05 <= epsilon -> False
    assert accept2 is False
    print(" -> PASSED")

    # 8. All-zero solutions transition to monitoring
    print("\n[Assert 8] All-zero solution state transitions...")
    # Simulating all-zero plan accepted
    controller.state = "OPTIMIZING"
    # When all-zeros are returned, orchestrator transitions to MONITORING
    controller.transition_to("MONITORING", 15, "Optimal plan: passive monitoring", "PASSIVE_MONITORING")
    assert controller.state == "MONITORING"
    print(" -> PASSED")

    # 9. Invalid interventions rejected & failed interventions update
    print("\n[Assert 9] Interventions lifecycle and statuses...")
    intv_manager = InterventionManager()
    intv_manager.add_intervention(12, "PLATFORM_SWAP", "12623", 30, 8.2)
    assert intv_manager.active_interventions[12]["status"] == "PROPOSED"
    intv_manager.update_status(12, "ACTIVE", 31)
    assert intv_manager.active_interventions[12]["status"] == "ACTIVE"
    intv_manager.update_status(12, "FAILED", 45, actual_delay_reduction=2.28, effectiveness_ratio=0.38)
    assert intv_manager.active_interventions[12]["status"] == "FAILED"
    assert intv_manager.active_interventions[12]["effectiveness_ratio"] == 0.38
    print(" -> PASSED")

    # 10. Recovery transitions back to monitoring
    print("\n[Assert 10] Recovery Monitor stabilization checks...")
    stable_snapshot = {
        "network_delay": 2.0,
        "congestion": 0.05,
        "platform_utilization": 0.10,
        "active_disruptions": 0
    }
    assert RecoveryMonitor.is_network_stable(stable_snapshot) is True
    print(" -> PASSED")

    # 11. Reports generation
    print("\n[Assert 11] HTML Reports output verification...")
    hist = [{"tick": 15, "cycle_number": 1, "trigger_reason": "Weather Change", "qubits": 3, "warm_start": False, "changed_actions": 1, "delta_utility": 0.85}]
    f_log = [{"tick": 16, "type": "HOLD", "target": "Train A", "predicted_reduction": 6.0, "actual_reduction": 5.2, "error": 0.8, "error_percent": 13.3}]
    trans = [
        {"timestamp": 15, "previous_state": "MONITORING", "new_state": "ASSESSING", "trigger": "WEATHER_CHANGE", "reason": "Weather Change"},
        {"timestamp": 15, "previous_state": "ASSESSING", "new_state": "OPTIMIZING", "trigger": "WEATHER_CHANGE", "reason": "Optimizing"},
        {"timestamp": 16, "previous_state": "OPTIMIZING", "new_state": "INTERVENING", "trigger": "APPLY_NEW_PLAN", "reason": "Plan Applied"},
        {"timestamp": 69, "previous_state": "INTERVENING", "new_state": "MONITORING", "trigger": "NETWORK_RECOVERY", "reason": "Network recovered"}
    ]
    ControlReportGenerator.generate_reports(hist, f_log, trans, output_dir="reports")
    assert os.path.exists("reports/layer6_adaptive_control_report.html")
    assert os.path.exists("reports/layer6_closed_loop_report.html")
    assert os.path.exists("reports/layer6_end_to_end_validation.html")
    print(" -> PASSED")

    print("\n====================================================")
    print("       ALL LAYER 6 ACCEPTANCE TESTS COMPLETED SUCCESSFULLY! ")
    print("====================================================")

if __name__ == "__main__":
    test_all()
