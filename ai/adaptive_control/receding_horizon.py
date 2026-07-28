class RecedingHorizonManager:
    HORIZON_DURATION = 30       # H = 30 minutes moving horizon
    CONTROL_INTERVAL = 5        # replanning every 5 minutes

    @classmethod
    def get_horizon_window(cls, current_tick: int) -> tuple:
        """
        Calculates the start and end ticks of the moving optimization window.
        """
        start = current_tick
        end = current_tick + cls.HORIZON_DURATION
        return start, end

    @classmethod
    def filter_actions_for_current_horizon(cls, selected_actions: list, current_tick: int) -> tuple:
        """
        Implements receding-horizon control logic:
        1. Predicts the next 30 minutes (horizon window).
        2. From the optimized sequence of actions, selects only the first control actions
           to execute immediately within the current control interval (5 minutes).
        3. Defers subsequent actions to be replanned as new state information arrives.
        """
        if not selected_actions:
            return [], []

        # Sort actions by expected delay reduction (highest impact first) or index
        sorted_actions = sorted(
            selected_actions,
            key=lambda x: (x.get("expected_delay_reduction", 0.0), -x.get("action_id", 999)),
            reverse=True
        )

        # In receding horizon control, we execute the first control action(s) immediately,
        # e.g., the highest priority intervention or actions scheduled for the current tick,
        # and defer the rest for subsequent replanning steps.
        # Let's execute the top 1 or 2 high-impact actions immediately, and defer the rest.
        immediate_actions = sorted_actions[:1] if len(sorted_actions) > 0 else []
        deferred_actions = sorted_actions[1:]

        # Mark statuses
        for act in immediate_actions:
            act["receding_horizon_execution"] = "IMMEDIATE"
        for act in deferred_actions:
            act["receding_horizon_execution"] = "DEFERRED_FOR_REPLANNING"

        print(f"[RECEDING HORIZON] Horizon [{current_tick} - {current_tick + cls.HORIZON_DURATION}] | "
              f"Control Interval: {cls.CONTROL_INTERVAL}m | "
              f"Executing {len(immediate_actions)} immediate action(s), "
              f"deferring {len(deferred_actions)} action(s) for replanning at tick {current_tick + cls.CONTROL_INTERVAL}")

        return immediate_actions, deferred_actions
