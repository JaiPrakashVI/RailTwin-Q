class WarmStartManager:
    @staticmethod
    def get_warm_start_vector(current_candidates: dict, previous_solution: list, previous_candidates: dict) -> list:
        """
        Generates an initial warm start bitstring matching new candidate actions to previously optimal choices.
        Args:
            current_candidates (dict): new reduced_variables mapping index -> details
            previous_solution (list): optimal bitstring of the last run
            previous_candidates (dict): previous reduced_variables mapping index -> details
        Returns:
            warm_start_vector (list): list of 0s and 1s matching current_candidates length
        """
        if not previous_solution or not previous_candidates:
            return [0] * len(current_candidates)
            
        # Map previous optimal active configurations (index where bit was 1)
        active_previous = []
        for details in previous_candidates.values():
            idx = details["index"]
            if idx < len(previous_solution) and previous_solution[idx] == 1:
                active_previous.append((details["action"], details["target"]))
                
        # Build warm start vector
        warm_start_vector = []
        # Sort current candidates by index to match variables array structure
        for details in sorted(current_candidates.values(), key=lambda x: x["index"]):
            match_found = False
            for prev_act, prev_tgt in active_previous:
                if details["action"] == prev_act and details["target"] == prev_tgt:
                    match_found = True
                    break
            warm_start_vector.append(1 if match_found else 0)
            
        return warm_start_vector
