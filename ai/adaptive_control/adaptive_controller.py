class AdaptiveController:
    def __init__(self):
        self.state = "MONITORING"
        self.last_opt_tick = None
        self.cycle_count = 0
        self.state_history = []
        self.re_opt_cooldown = 5
        self.epsilon = 0.05  # Delta utility threshold

    def transition_to(self, new_state: str, tick: int, reason: str = "", trigger: str = "SCHEDULED_MONITOR"):
        """
        Transitions the controller state machine to a new state and logs it with strict schema.
        """
        old_state = self.state
        if old_state != new_state:
            self.state = new_state
            entry = {
                "timestamp": tick,
                "previous_state": old_state,
                "new_state": new_state,
                "trigger": trigger,
                "reason": reason
            }
            self.state_history.append(entry)
            print(f"[LAYER 6 STATE] Tick {tick} | State Shift: {old_state} -> {new_state} | Trigger: {trigger} | Reason: {reason}")

    def evaluate_decision_gate(self, new_energy: float, current_energy: float, switching_cost: float) -> tuple:
        """
        Evaluates the Decision Quality Gate:
          delta_utility = Utility_new - Utility_current - SwitchingCost
          Since minimizing energy maximizes utility:
          delta_utility = Energy_current - Energy_new - SwitchingCost
        Returns:
          (accept_bool, delta_utility)
        """
        delta_utility = current_energy - new_energy - switching_cost
        accept = delta_utility > self.epsilon
        return accept, delta_utility
