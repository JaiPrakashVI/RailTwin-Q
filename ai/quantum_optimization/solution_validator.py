class SolutionValidator:
    @staticmethod
    def validate_plan(selected_actions: list, constraints: dict, dependencies: dict) -> dict:
        """
        Validates the selected action plan against platform capacity, track capacity, and dependency conflicts.
        """
        violations = 0
        details = []

        # 1. Action Conflict Checks (Mutual Exclusions)
        selected_ids = {act["action_id"] for act in selected_actions}
        edges = dependencies.get("edges", [])
        
        for edge in edges:
            src = int(edge.get("source", 0))
            tgt = int(edge.get("target", 0))
            rel = edge.get("relationship", "")

            if src in selected_ids and tgt in selected_ids:
                if rel in ["CONFLICTS_WITH", "INCOMPATIBLE"]:
                    violations += 1
                    details.append(f"Conflict: Action {src} and Action {tgt} are incompatible but both selected.")

            # Prerequisite check: if B is selected, it requires A. So if B is in selected_ids, A must be too.
            if rel == "REQUIRES":
                if tgt in selected_ids and src not in selected_ids:
                    violations += 1
                    details.append(f"Prerequisite failure: Action {tgt} requires Action {src} which was not selected.")

        # 2. Platform Capacity Checks
        nodes = dependencies.get("nodes", {})
        platform_caps = constraints.get("platform_capacities", {})
        swaps_per_station = {}
        for act in selected_actions:
            action_id = act["action_id"]
            node_detail = nodes.get(str(action_id), {})
            if node_detail.get("action") == "PLATFORM_SWAP":
                station_id = node_detail.get("station_id")
                if station_id:
                    stat_key = f"station_{station_id}"
                    swaps_per_station[stat_key] = swaps_per_station.get(stat_key, 0) + 1

        for stat_key, num_swaps in swaps_per_station.items():
            cap_info = platform_caps.get(stat_key, {})
            avail = cap_info.get("available_slots", 1)
            if num_swaps > avail:
                violations += 1
                details.append(f"Capacity failure: Station {stat_key} has {avail} platform swap slot(s) available, but {num_swaps} selected.")

        # 3. Track capacity & headway checks
        track_caps = constraints.get("track_capacities", {})
        reroutes_per_track = {}
        for act in selected_actions:
            action_id = act["action_id"]
            node_detail = nodes.get(str(action_id), {})
            if node_detail.get("action") == "REROUTE":
                track_id = node_detail.get("track_id")
                if track_id:
                    track_key = f"track_{track_id}"
                    reroutes_per_track[track_key] = reroutes_per_track.get(track_key, 0) + 1

        for track_key, num_reroutes in reroutes_per_track.items():
            cap_info = track_caps.get(track_key, {})
            capacity = cap_info.get("capacity", 2)
            current = cap_info.get("current_trains", 0)
            if current + num_reroutes > capacity:
                violations += 1
                details.append(f"Capacity failure: Track {track_key} has capacity {capacity} ({current} current), but adding {num_reroutes} rerouted trains exceeds it.")

        valid = violations == 0
        return {
            "valid": valid,
            "violations": violations,
            "details": details
        }

    @staticmethod
    def audit_pipeline(qubo_matrix: dict, linear_costs: dict, selected_bitstring: list, 
                       reduced_variables: dict, cost_vectors: list, constraints: dict, 
                       dependencies: dict, penalty_strength: float) -> None:
        """
        Runs automated safety and formulation audits on the QUBO matrix and solver decisions.
        Raises AssertionError if any anomaly is detected.
        """
        # 1. Mixed normalized and raw metrics:
        for idx, cost in linear_costs.items():
            assert -1.0 - 1e-5 <= cost <= 1.0 + 1e-5, f"Anomaly: mixed normalized and raw metrics detected at index {idx} with cost {cost}"

        # 2. All candidate actions having positive net cost during active disruption:
        has_active_disruption = any(cv.get("cost_vector", {}).get("delay", 0.0) < -15.0 for cv in cost_vectors)
        if has_active_disruption and len(linear_costs) > 0:
            any_beneficial = any(cost < 0.0 for cost in linear_costs.values())
            assert any_beneficial, "Anomaly: All candidate actions have positive net cost during an active disruption (coefficient scaling error)."

        # 3. Zero-action solution being selected despite significant predicted delay reduction:
        is_zero_action = all(b == 0 for b in selected_bitstring)
        if is_zero_action and len(selected_bitstring) > 0:
            for idx, cost in linear_costs.items():
                if cost < -0.05:
                    # Check if this beneficial action is conflict-free and feasible on its own
                    idx_map = {details["index"]: details for details in reduced_variables.values()}
                    if idx in idx_map:
                        details = idx_map[idx]
                        single_action = [{
                            "action_id": details["action_id"],
                            "action": details["action"],
                            "target": details["target"]
                        }]
                        val_status = SolutionValidator.validate_plan(single_action, constraints, dependencies)
                        if val_status["valid"]:
                            raise AssertionError(
                                f"Anomaly: Zero-action solution was selected despite action {details['action_id']} having "
                                f"significant predicted delay reduction ({cost}) and being fully feasible on its own."
                            )

        # 4. Constraint penalties being smaller than objective benefits:
        max_possible_benefit = sum(abs(c) for c in linear_costs.values() if c < 0)
        assert penalty_strength > max_possible_benefit, f"Anomaly: Constraint penalty strength ({penalty_strength}) is smaller than max objective benefit ({max_possible_benefit})."

        # 5. Invalid or infeasible decoded action plans:
        idx_map = {details["index"]: details for details in reduced_variables.values()}
        decoded_actions = []
        for idx, val in enumerate(selected_bitstring):
            if val == 1 and idx in idx_map:
                details = idx_map[idx]
                decoded_actions.append({
                    "action_id": details["action_id"],
                    "action": details["action"],
                    "target": details["target"]
                })
        val_status = SolutionValidator.validate_plan(decoded_actions, constraints, dependencies)
        if not val_status["valid"]:
            raise AssertionError(f"Anomaly: Decoded action plan is invalid or infeasible: {val_status['details']}")

