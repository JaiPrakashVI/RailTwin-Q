class ActionExecutor:
    @staticmethod
    def apply_action(act, network, active_events, tick) -> bool:
        """
        Executes a single action contract on the given network, translating
        it to physical track mutations (rerouting, holds, platform swaps, speed changes).
        Supports both Action objects and plain dictionaries.
        """
        if hasattr(act, "execute"):
            return act.execute(network, active_events, tick)
            
        action_type = act.get("action", "")
        train_name = act.get("target", "")
        
        train_obj = network.get_train_by_no(train_name)
        if not train_obj:
            for t_obj in network.trains:
                if t_obj.name == train_name:
                    train_obj = t_obj
                    break
        if not train_obj:
            return False
            
        if action_type == "SPEED_ADJUST":
            train_obj.base_speed = min(train_obj.base_speed * 1.02, train_obj.max_speed)
            return True
        elif action_type == "PLATFORM_SWAP":
            train_obj.is_priority_train = True
            return True
        elif action_type == "HOLD":
            train_obj.dwell_time_remaining = max(train_obj.dwell_time_remaining, 1)
            return True
        elif action_type == "REROUTE":
            new_route_stations = act.get("parameters", {}).get("new_route_stations", [])
            if new_route_stations:
                new_route_id = f"fallback_reroute_{train_obj.train_no}_{tick}"
                network.add_route(new_route_id, new_route_stations)
                train_obj.route_id = new_route_id
                if train_obj.current_station_id in new_route_stations:
                    train_obj.route_index = new_route_stations.index(train_obj.current_station_id)
                else:
                    train_obj.route_index = 0
                    train_obj.current_station_id = new_route_stations[0]
                return True
        return False

    @staticmethod
    def execute_plan(selected_actions: list, network, active_events, tick) -> list:
        """
        Verifies the lifecycle validity of optimal plan actions and executes them.
        Returns:
            executed_list (list): list of actions that were successfully applied.
        """
        executed_list = []
        train_map = {t.name: t for t in network.trains}
        
        # Check active disruptions
        active_disruptions = [e for e in active_events if e.active]
        
        for act in selected_actions:
            train_name = act.get("target", "")
            action_type = act.get("action", "")
            action_id = act.get("action_id", 0)
            
            # Validation checks:
            # 1. Check if disruption is resolved
            if not active_disruptions:
                # Disruption resolved, revoke proposed action
                act["status"] = "REVOKED"
                act["reason"] = "Disruption resolved"
                continue
                
            # 2. Check if train exists and has not completed its journey
            train_obj = train_map.get(train_name)
            if not train_obj:
                for t in network.trains:
                    if t.name == train_name:
                        train_obj = t
                        break
            
            if not train_obj:
                act["status"] = "REVOKED"
                act["reason"] = f"Train {train_name} not found in active network"
                continue
                
            if train_obj.progress >= 100.0 or train_obj.status == "COMPLETED":
                act["status"] = "REVOKED"
                act["reason"] = f"Train {train_name} has already completed journey"
                continue
                
            # 3. Platform Capacity validation for Platform Swaps
            if action_type == "PLATFORM_SWAP":
                # Verify station has available platform slots (e.g. Katpadi Station ID 3)
                station_id = train_obj.current_station_id
                station = network.get_station_by_id(station_id)
                if station and station.platforms_occupied >= station.platforms:
                    act["status"] = "FAILED"
                    act["reason"] = f"No available platforms at station {station.name}"
                    continue
                    
            # 4. Apply physical changes to the Digital Twin
            success = ActionExecutor.apply_action(act, network, active_events, tick)
                
            if success:
                act["status"] = "ACTIVE"
                act["applied_at"] = tick
                executed_list.append(act)
            else:
                act["status"] = "FAILED"
                act["reason"] = "Physical execution failed"
                
        return executed_list


