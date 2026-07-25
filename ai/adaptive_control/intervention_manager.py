class InterventionManager:
    def __init__(self):
        self.active_interventions = {}  # action_id -> dict

    def add_intervention(self, action_id: int, action_type: str, target: str, tick: int, expected_delay_reduction: float):
        """
        Adds a new intervention with the 'PROPOSED' lifecycle status.
        """
        self.active_interventions[action_id] = {
            "action_id": action_id,
            "action_type": action_type,
            "type": action_type, # compatibility
            "target_train": target,
            "target": target, # compatibility
            "status": "PROPOSED",
            "proposed_at": tick,
            "validated_at": tick,
            "applied_at": tick + 1,
            "expected_delay_reduction": expected_delay_reduction,
            "actual_delay_reduction": 0.0,
            "effectiveness_ratio": 1.0,
            "history": [{"status": "PROPOSED", "tick": tick}]
        }

    def update_status(self, action_id: int, new_status: str, tick: int, **kwargs):
        """
        Updates the lifecycle status of an active intervention.
        """
        if action_id in self.active_interventions:
            self.active_interventions[action_id]["status"] = new_status
            self.active_interventions[action_id]["history"].append({
                "status": new_status,
                "tick": tick
            })
            for key, val in kwargs.items():
                self.active_interventions[action_id][key] = val

    def get_active_list(self) -> list:
        """
        Returns a list of interventions that are currently active or applied.
        """
        return [
            intv for intv in self.active_interventions.values()
            if intv["status"] in ["VALIDATED", "APPLIED", "ACTIVE", "PARTIALLY_EFFECTIVE"]
        ]

    def clear_expired_interventions(self, current_tick: int, network):
        """
        Marks completed, expired, or failed interventions based on network conditions.
        """
        for action_id, intv in list(self.active_interventions.items()):
            if intv["status"] in ["ACTIVE", "PARTIALLY_EFFECTIVE", "APPLIED"]:
                train_name = intv["target"]
                train_obj = None
                for t in network.trains:
                    if t.name == train_name:
                        train_obj = t
                        break
                
                # If train has completed or progress is 100%, set status to COMPLETED
                if not train_obj or (train_obj.progress >= 100.0 and train_obj.status == "COMPLETED"):
                    self.update_status(action_id, "COMPLETED", current_tick, actual_delay_reduction=intv["expected_delay_reduction"])
                # Check if applied for more than 40 minutes, set as EXPIRED
                elif current_tick - intv["applied_at"] > 40:
                    self.update_status(action_id, "EXPIRED", current_tick)
