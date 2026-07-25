import os
import json
from ai.adaptive_control.state_monitor import StateMonitor
from ai.adaptive_control.event_detector import EventDetector
from ai.adaptive_control.intervention_manager import InterventionManager
from ai.adaptive_control.trigger_engine import TriggerEngine
from ai.adaptive_control.receding_horizon import RecedingHorizonManager
from ai.adaptive_control.warm_start import WarmStartManager
from ai.adaptive_control.stability_manager import StabilityManager
from ai.adaptive_control.action_executor import ActionExecutor
from ai.adaptive_control.feedback_engine import FeedbackEngine
from ai.adaptive_control.recovery_monitor import RecoveryMonitor
from ai.adaptive_control.adaptive_controller import AdaptiveController
from ai.adaptive_control.control_report_generator import ControlReportGenerator
from ai.quantum_optimization.classical_baselines import ClassicalBaselines

class ControlOrchestrator:
    def __init__(self):
        self.controller = AdaptiveController()
        self.intv_manager = InterventionManager()
        self.feedback_eng = FeedbackEngine()
        self.prev_snapshot = None
        self.previous_solution = None
        self.previous_candidates = None
        self.current_energy = 0.0
        self.controller_run_history = []
        
        # Initial active states
        self.current_active_actions = []

    def orchestrate_tick(self, network, active_events, tick, baseline_rec_time, orchestrator_l5) -> dict:
        """
        Coordinates the Layer 6 closed-loop control tick state evaluations.
        """
        # 1. Observe state
        current_snapshot = StateMonitor.observe(network, active_events, tick, self.intv_manager.get_active_list())
        
        # 2. Detect events
        events = EventDetector.detect(current_snapshot, self.prev_snapshot)
        
        # 3. Check Triggers
        action_code, reason = TriggerEngine.requires_optimization(current_snapshot, events, self.controller.last_opt_tick)
        
        # Determine trigger type
        trigger = "SCHEDULED_MONITOR"
        for ev in events:
            if "Intervention Deviation" in ev.get("name", ""):
                trigger = "INTERVENTION_FAILURE"
                reason = ev.get("reason", reason)
                for intv in self.intv_manager.get_active_list():
                    self.intv_manager.update_status(
                        intv["action_id"], "FAILED", tick,
                        actual_delay_reduction=round(intv["expected_delay_reduction"] * 0.38, 2),
                        effectiveness_ratio=0.38
                    )
                break
            elif ev.get("event") in ["NEW_DISRUPTION", "WEATHER_CHANGE", "TRAIN_DELAY_SPIKE", "CONGESTION_SPIKE", "PLATFORM_FULL"]:
                trigger = ev.get("event")

        # 4. State transitions
        if action_code == "REOPTIMIZE":
            if self.controller.state == "INTERVENING":
                self.controller.transition_to("REOPTIMIZING", tick, reason, trigger=trigger)
            else:
                self.controller.transition_to("ASSESSING", tick, reason, trigger=trigger)
            self.controller.transition_to("OPTIMIZING", tick, "Trigger confirmed, building dynamic decision space", trigger=trigger)
        elif action_code == "STOP_CONTROL":
            if self.controller.state != "MONITORING":
                self.controller.transition_to("RECOVERING", tick, "Disruptions cleared and system stable", trigger="NETWORK_RECOVERY")
                self.controller.transition_to("MONITORING", tick, "Passive network monitoring", trigger="NETWORK_RECOVERY")
        elif action_code == "MONITOR" and self.controller.state == "INTERVENING":
            if RecoveryMonitor.is_network_stable(current_snapshot):
                self.controller.transition_to("RECOVERING", tick, "Disruptions cleared and system stable", trigger="NETWORK_RECOVERY")
                self.controller.transition_to("MONITORING", tick, "Passive network monitoring", trigger="NETWORK_RECOVERY")

        # Clear expired status
        self.intv_manager.clear_expired_interventions(tick, network)
        
        # Log outcomes
        active_list = self.intv_manager.get_active_list()
        for intv in active_list:
            actual_save = max(0.5, intv["expected_delay_reduction"] * (1.0 - (current_snapshot["network_delay"] / 120.0)))
            self.feedback_eng.record_outcome(tick, intv["action_id"], intv["type"], intv["target"], intv["expected_delay_reduction"], actual_save)

        # 5. Optimize
        payload = {}
        if self.controller.state == "OPTIMIZING":
            # Run dynamic re-optimization
            res = orchestrator_l5.optimize_network(
                network, active_events, tick, baseline_rec_time,
                previous_solution=self.previous_solution,
                previous_candidates=self.previous_candidates,
                p_switch=0.15
            )
            
            if res and res.get("selected_solver") != "NONE":
                new_solution = res["selected_bitstring"]
                new_candidates = res["reduced_variables"]
                new_energy = res["best_energy"]
                
                # Evaluate current plan energy under the new QUBO matrix Q
                warm_start_vector = res.get("initial_state_vector")
                if warm_start_vector is not None:
                    current_energy = res.get("exact_energy", 0.0)
                else:
                    current_energy = 0.0
                    
                switching_cost = StabilityManager.calculate_switching_cost(
                    new_solution, new_candidates,
                    self.previous_solution, self.previous_candidates,
                    p_switch=0.15
                )
                
                # Decision Quality Gate check
                accept, delta_utility = self.controller.evaluate_decision_gate(new_energy, current_energy, switching_cost)
                
                # Formulate decision logging
                gate_decision = "KEEP_CURRENT_PLAN"
                gate_reason = f"Reject new plan (Delta utility {delta_utility:.4f} <= epsilon {self.controller.epsilon})"
                if accept or self.previous_solution is None:
                    if any(new_solution):
                        gate_decision = "APPLY_NEW_PLAN"
                        gate_reason = "New plan provides meaningful improvement after switching cost"
                    else:
                        gate_decision = "PASSIVE_MONITORING"
                        gate_reason = "No intervention provides sufficient positive utility after constraints and switching costs"
                
                gate_log_entry = {
                    "timestamp": tick,
                    "current_plan_utility": -current_energy,
                    "new_plan_utility": -new_energy,
                    "switching_cost": switching_cost,
                    "delta_utility": delta_utility,
                    "epsilon": self.controller.epsilon,
                    "decision": gate_decision,
                    "reason": gate_reason
                }
                print(f"[DECISION GATE] {json.dumps(gate_log_entry, indent=2)}")
                gate_log_path = os.path.join("datasets", "decision_gate_log.jsonl")
                with open(gate_log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(gate_log_entry) + "\n")
                
                if accept or self.previous_solution is None:
                    if any(new_solution):
                        # Execute new actions
                        executed = ActionExecutor.execute_plan(res["selected_actions"], network, active_events, tick)
                        
                        # Update intervention manager
                        for act in executed:
                            self.intv_manager.add_intervention(act["action_id"], act["action"], act["target"], tick, act.get("expected_delay_reduction", 5.0))
                            self.intv_manager.update_status(act["action_id"], "ACTIVE", tick)
                            
                        self.controller.cycle_count += 1
                        self.controller.last_opt_tick = tick
                        self.previous_solution = new_solution
                        self.previous_candidates = new_candidates
                        self.current_energy = new_energy
                        
                        self.controller_run_history.append({
                            "tick": tick,
                            "cycle_number": self.controller.cycle_count,
                            "trigger_reason": reason,
                            "qubits": len(new_solution),
                            "warm_start": warm_start_vector is not None,
                            "changed_actions": len(executed),
                            "delta_utility": delta_utility if self.previous_solution is not None else 0.0,
                            "new_energy": new_energy,
                            "solver_name": res.get("selected_solver", "HYBRID_QAOA")
                        })
                        
                        self.controller.transition_to("INTERVENING", tick, f"New schedule applied successfully: {len(executed)} actions active", trigger="APPLY_NEW_PLAN")
                    else:
                        self.controller.cycle_count += 1
                        self.controller.last_opt_tick = tick
                        self.previous_solution = new_solution
                        self.previous_candidates = new_candidates
                        self.current_energy = new_energy
                        
                        self.controller_run_history.append({
                            "tick": tick,
                            "cycle_number": self.controller.cycle_count,
                            "trigger_reason": reason,
                            "qubits": len(new_solution),
                            "warm_start": warm_start_vector is not None,
                            "changed_actions": 0,
                            "delta_utility": delta_utility if self.previous_solution is not None else 0.0,
                            "new_energy": new_energy,
                            "solver_name": res.get("selected_solver", "HYBRID_QAOA")
                        })
                        
                        self.controller.transition_to("MONITORING", tick, "Optimal plan: passive monitoring (no interventions needed)", trigger="PASSIVE_MONITORING")
                else:
                    self.controller.transition_to("INTERVENING", tick, f"Reject new plan (Delta utility {delta_utility:.4f} <= epsilon)", trigger="KEEP_CURRENT_PLAN")
            else:
                self.controller.transition_to("MONITORING", tick, "Empty decision space returned", trigger="EMPTY_DECISION_SPACE")
                
            payload = res
            
        self.prev_snapshot = current_snapshot
        
        # Save Layer 6 state for web dashboard
        os.makedirs("datasets", exist_ok=True)
        last_cycle = self.controller_run_history[-1] if self.controller_run_history else {}
        next_eligible = max(tick, (self.controller.last_opt_tick or 0) + self.controller.re_opt_cooldown)
        recovery_status = "STABILIZING" if self.controller.state == "RECOVERING" else ("RECOVERED" if self.controller.state == "MONITORING" and self.controller.last_opt_tick is not None else "NORMAL")
        
        dashboard_state = {
            "state": self.controller.state,
            "active_disruptions": current_snapshot["active_disruptions"],
            "network_delay": round(current_snapshot["network_delay"], 2),
            "congestion": round(current_snapshot["congestion"] * 100.0, 1),
            "active_interventions": self.intv_manager.get_active_list(),
            "cycle_number": self.controller.cycle_count,
            "tick": tick,
            "last_opt_tick": self.controller.last_opt_tick or 0,
            "next_eligible_tick": next_eligible,
            "qubits": last_cycle.get("qubits", 0),
            "warm_start": last_cycle.get("warm_start", False),
            "delta_utility": round(last_cycle.get("delta_utility", 0.0), 4),
            "trigger_reason": last_cycle.get("trigger_reason", "None"),
            "current_plan_utility": round(-self.current_energy, 4),
            "new_plan_utility": round(-last_cycle.get("new_energy", 0.0), 4),
            "solver_name": last_cycle.get("solver_name", "HYBRID_QAOA"),
            "reoptimization_count": self.controller.cycle_count,
            "recovery_status": recovery_status
        }
        with open("datasets/layer6_state.json", "w", encoding="utf-8") as f:
            json.dump(dashboard_state, f, indent=4)
            
        return payload

    def finalize_simulation(self):
        """
        Generates the Layer 6 HTML reports.
        """
        ControlReportGenerator.generate_reports(
            self.controller_run_history,
            self.feedback_eng.feedback_log,
            self.controller.state_history
        )
