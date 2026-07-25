import numpy as np

class StabilityManager:
    @staticmethod
    def inject_switching_penalties(Q: dict, current_candidates: dict, previous_solution: list, previous_candidates: dict, p_switch: float = 0.15) -> dict:
        """
        Modifies the diagonal of the QUBO matrix dictionary Q to inject switching costs.
        For each variable x_i:
          - If x_i was previously active (bit = 1), subtract p_switch from Q[(i, i)].
          - If x_i was previously inactive (bit = 0 or new action), add p_switch to Q[(i, i)].
        """
        # Map previous optimal active configurations
        active_previous = []
        if previous_solution and previous_candidates:
            for details in previous_candidates.values():
                idx = details["index"]
                if idx < len(previous_solution) and previous_solution[idx] == 1:
                    active_previous.append((details["action"], details["target"]))
                    
        # Update diagonal of Q
        for details in current_candidates.values():
            idx = details["index"]
            match_found = False
            for prev_act, prev_tgt in active_previous:
                if details["action"] == prev_act and details["target"] == prev_tgt:
                    match_found = True
                    break
            
            if match_found:
                # Previously active: penalize turning off. Subtract p_switch from Q[(idx, idx)]
                Q[(idx, idx)] = Q.get((idx, idx), 0.0) - p_switch
            else:
                # Previously inactive or new action: penalize turning on. Add p_switch to Q[(idx, idx)]
                Q[(idx, idx)] = Q.get((idx, idx), 0.0) + p_switch
                
        return Q

    @staticmethod
    def calculate_switching_cost(new_solution: list, current_candidates: dict, previous_solution: list, previous_candidates: dict, p_switch: float = 0.15) -> float:
        """
        Calculates the explicit total switching cost between the previous and new solution.
        """
        if not previous_solution or not previous_candidates:
            return 0.0
            
        active_prev = set()
        for details in previous_candidates.values():
            idx = details["index"]
            if idx < len(previous_solution) and previous_solution[idx] == 1:
                active_prev.add((details["action"], details["target"]))
                
        active_new = set()
        if new_solution and current_candidates:
            for details in current_candidates.values():
                idx = details["index"]
                if idx < len(new_solution) and new_solution[idx] == 1:
                    active_new.add((details["action"], details["target"]))
                
        # Total switching cost is p_switch * symmetric_difference(active_prev, active_new)
        diff_count = len(active_prev.symmetric_difference(active_new))
        return float(diff_count * p_switch)
