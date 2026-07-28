from models.action import create_action

class SolutionDecoder:
    @staticmethod
    def decode_solution(bitstring: list, reduced_variables: dict) -> list:
        """
        Decodes the binary bitstring back into a list of selected operational Action Contract objects.
        """
        selected_actions = []
        
        # Invert reduced_variables mapping to index -> action details
        idx_map = {details["index"]: details for details in reduced_variables.values()}

        for idx, val in enumerate(bitstring):
            if val == 1 and idx in idx_map:
                details = idx_map[idx]
                # Reconstruct Action Contract Object
                act = create_action(
                    action_id=details["action_id"],
                    action_type=details.get("action_type", details.get("action", "SCHEDULE_MAINTENANCE")),
                    train_id=details.get("train_id", details.get("target", "Global")),
                    source_station=details.get("source_station", 1),
                    target_station=details.get("target_station", 1),
                    parameters=details.get("parameters", {}),
                    expected_effect=details.get("expected_effect", {}),
                    constraints=details.get("constraints", {}),
                    # Copy other legacy/helper keys
                    **{k: v for k, v in details.items() if k not in ["action_id", "action_type", "action", "train_id", "target", "source_station", "target_station", "parameters", "expected_effect", "constraints", "index", "variable_symbol"]}
                )
                selected_actions.append(act)

        return selected_actions

