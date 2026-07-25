class RecedingHorizonManager:
    HORIZON_DURATION = 30  # 30 minutes moving horizon

    @classmethod
    def get_horizon_window(cls, current_tick: int) -> tuple:
        """
        Calculates the start and end ticks of the moving optimization window.
        """
        start = current_tick
        end = current_tick + cls.HORIZON_DURATION
        return start, end
