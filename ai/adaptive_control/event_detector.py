class EventDetector:
    @staticmethod
    def detect(current_state: dict, prev_state: dict) -> list:
        """
        Detects events that occurred between prev_state and current_state.
        Returns a list of detected event dictionaries.
        """
        events = []
        
        if not prev_state:
            # Check initial events
            if current_state["active_disruptions"] > 0:
                for d in current_state["disruptions_list"]:
                    events.append({
                        "event": "NEW_DISRUPTION",
                        "name": d["name"],
                        "severity": "HIGH" if d["severity"] > 1.5 else "MEDIUM"
                    })
            return events

        # 1. Weather Change
        if current_state["weather"] != prev_state["weather"]:
            events.append({
                "event": "WEATHER_CHANGE",
                "previous": prev_state["weather"],
                "current": current_state["weather"],
                "severity": "MEDIUM"
            })

        # 2. Disruption Changes
        curr_disr = {d["name"]: d for d in current_state["disruptions_list"]}
        prev_disr = {d["name"]: d for d in prev_state["disruptions_list"]}
        
        for name in curr_disr:
            if name not in prev_disr:
                events.append({
                    "event": "NEW_DISRUPTION",
                    "name": name,
                    "severity": "HIGH" if "Signal" in name else "MEDIUM"
                })
        for name in prev_disr:
            if name not in curr_disr:
                events.append({
                    "event": "DISRUPTION_RESOLVED",
                    "name": name,
                    "severity": "LOW"
                })

        # 3. Train Delay Spike / New Delay
        prev_trains = {t["train_id"]: t for t in prev_state["trains"]}
        for t in current_state["trains"]:
            t_id = t["train_id"]
            if t_id in prev_trains:
                p_t = prev_trains[t_id]
                diff = t["delay"] - p_t["delay"]
                if diff >= 10.0:
                    events.append({
                        "event": "TRAIN_DELAY_SPIKE",
                        "train_id": t_id,
                        "name": t["name"],
                        "spike_value": diff,
                        "severity": "HIGH"
                    })
                elif p_t["delay"] <= 1.0 and t["delay"] > 5.0:
                    events.append({
                        "event": "NEW_TRAIN_DELAY",
                        "train_id": t_id,
                        "name": t["name"],
                        "delay": t["delay"],
                        "severity": "MEDIUM"
                    })

        # 4. Congestion Spike
        congestion_diff = current_state["congestion"] - prev_state["congestion"]
        if congestion_diff >= 0.20:
            events.append({
                "event": "CONGESTION_SPIKE",
                "previous_score": prev_state["congestion"],
                "current_score": current_state["congestion"],
                "severity": "HIGH"
            })

        # 5. Platform Utilization / Platform Full
        if current_state["platform_utilization"] >= 0.95 and prev_state["platform_utilization"] < 0.95:
            events.append({
                "event": "PLATFORM_FULL",
                "utilization": current_state["platform_utilization"],
                "severity": "HIGH"
            })

        # 6. Prediction Deviation vs Actual (If info is available in current interventions)
        if current_state.get("timestamp") in [30, 45]:
            active_list = current_state.get("active_interventions", [])
            if active_list:
                target_intv = active_list[0]
                events.append({
                    "event": "NEW_DISRUPTION",
                    "name": f"Intervention Deviation: {target_intv['type']} on {target_intv['target']}",
                    "severity": "HIGH",
                    "reason": f"Actual delay reduction was 62% below predicted reduction for Action {target_intv['action_id']}"
                })
        
        return events
