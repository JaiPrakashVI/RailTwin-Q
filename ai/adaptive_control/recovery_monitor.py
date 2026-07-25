class RecoveryMonitor:
    STABILITY_DELAY_THRESHOLD = 25.0  # minutes average delay
    STABILITY_CONGESTION_THRESHOLD = 0.20  # 20% congestion

    @classmethod
    def is_network_stable(cls, current_state: dict) -> bool:
        """
        Determines if the railway network has stabilized and recovered.
        """
        avg_delay = current_state.get("network_delay", 0.0)
        congestion = current_state.get("congestion", 0.0)
        
        # If no active disruptions and delays/congestion are within baseline parameters
        if current_state["active_disruptions"] == 0:
            if avg_delay <= cls.STABILITY_DELAY_THRESHOLD and congestion <= cls.STABILITY_CONGESTION_THRESHOLD:
                return True
        return False
