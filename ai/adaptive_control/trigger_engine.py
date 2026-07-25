import json
import os

class TriggerEngine:
    COOLDOWN_TICKS = 5

    @classmethod
    def requires_optimization(cls, current_state: dict, events: list, last_opt_tick: int) -> tuple:
        """
        Evaluates trigger logic to decide if re-optimization is required with severity-aware behavior.
        """
        tick = current_state["timestamp"]
        
        # Check recovery state
        if current_state["active_disruptions"] == 0 and len(current_state["active_interventions"]) == 0:
            return "STOP_CONTROL", "Network stable and no disruptions active"

        cooldown_active = False
        if last_opt_tick is not None:
            cooldown_active = (tick - last_opt_tick) < cls.COOLDOWN_TICKS

        # Default scheduled monitoring (LOW)
        trigger_name = "SCHEDULED_MONITOR"
        severity = "LOW"
        action = "MONITOR"
        reason = "Normal operations monitoring"

        # Check periodic trigger (LOW)
        if tick % 15 == 0:
            trigger_name = "PERIODIC_SCHEDULE"
            severity = "LOW"
            if not cooldown_active:
                action = "REOPTIMIZE"
                reason = "Time-based periodic optimization (15 minutes interval)"

        # Check other events
        for ev in events:
            ev_type = ev.get("event")
            ev_name = ev.get("name", ev_type)
            ev_severity = ev.get("severity", "MEDIUM")

            # Map event severity and action
            if ev_severity == "CRITICAL" or ev_type in ["PLATFORM_FULL", "CONGESTION_SPIKE"]:
                trigger_name = ev_name
                severity = "CRITICAL"
                action = "REOPTIMIZE"
                reason = f"CRITICAL: Emergency re-optimization triggered by {ev_name}"
                break  # CRITICAL overrides everything
            elif ev_severity == "HIGH" or ev_type in ["TRAIN_DELAY_SPIKE", "INTERVENTION_FAILURE"] or "Intervention Deviation" in ev_name:
                trigger_name = ev_name
                severity = "HIGH"
                action = "REOPTIMIZE"
                reason = f"HIGH: Immediate re-optimization triggered by {ev_name} (bypasses cooldown)"
                break  # HIGH overrides MEDIUM
            elif ev_severity == "MEDIUM" or ev_type in ["WEATHER_CHANGE", "NEW_DISRUPTION"]:
                if not cooldown_active:
                    trigger_name = ev_name
                    severity = "MEDIUM"
                    action = "REOPTIMIZE"
                    reason = f"MEDIUM: Event-triggered re-optimization: {ev_name}"

        # If cooldown is active and action was determined to be REOPTIMIZE (but severity is not HIGH/CRITICAL), suppress it!
        if cooldown_active and severity in ["LOW", "MEDIUM"] and action == "REOPTIMIZE":
            action = "MONITOR"
            reason = f"Optimization cooldown active ({cls.COOLDOWN_TICKS - (tick - last_opt_tick)} ticks remaining)"

        # Log trigger outcome
        trigger_log = {
            "trigger": trigger_name,
            "severity": severity,
            "cooldown_active": cooldown_active,
            "action": action
        }
        
        os.makedirs("datasets", exist_ok=True)
        log_path = os.path.join("datasets", "trigger_engine_log.jsonl")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(trigger_log) + "\n")

        # Also print to console for stress test logging
        print(f"[TRIGGER ENGINE] {json.dumps(trigger_log)}")

        return action, reason
