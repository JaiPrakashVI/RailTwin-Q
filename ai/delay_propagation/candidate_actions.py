import networkx as nx
from models.action import create_action

class CandidateActionGenerator:
    @staticmethod
    def generate_candidate_actions(G: nx.DiGraph, network) -> list:
        """
        Generates candidate operational actions based on active disruptions and bottleneck nodes.
        These actions conform to the unified Action Contract.
        """
        actions = []
        action_counter = 1

        # 1. Platform Swaps (triggered by station platform saturation)
        for s in network.stations:
            if s.station_congestion_score >= 40.0:
                # Find trains at this station or heading to it
                trains_at_station = [t for t in network.trains if t.current_station_id == s.station_id and t.status in ["WAITING", "ARRIVED"]]
                train_id = trains_at_station[0].name if trains_at_station else "Global"
                
                act = create_action(
                    action_id=action_counter,
                    action_type="PLATFORM_SWAP",
                    train_id=train_id,
                    source_station=s.station_id,
                    target_station=s.station_id,
                    parameters={"station_id": s.station_id, "train_id": train_id},
                    expected_effect={"delay_reduction": 8.5, "congestion_reduction": round(float(s.station_congestion_score * 0.3), 1)},
                    constraints={"platform_capacity": s.platforms},
                    confidence=0.88,
                    passenger_impact="Low",
                    station_id=s.station_id,
                    station_name=s.name
                )
                actions.append(act)
                action_counter += 1

        # 2. Rerouting (triggered by track saturation/blockages)
        for tr in network.tracks:
            if tr.occupancy_percent >= 50.0 or tr.blocked:
                # Find trains heading to or moving on this track (look for moving trains, or trains at stations whose next track is this track)
                moving_trains = [t for t in network.trains if t.current_track_id == tr.track_id and t.status == "MOVING"]
                
                # Also include trains at the source station of the track that want to traverse it
                source_station_trains = [
                    t for t in network.trains 
                    if t.current_station_id == tr.source_station_id 
                    and t.status in ["WAITING", "ARRIVED", "DELAYED"]
                ]
                
                candidate_trains = moving_trains + source_station_trains
                
                for mt in candidate_trains:
                    # Determine new route stations list based on train identifier and location
                    train_id = mt.name
                    source_station = mt.current_station_id
                    
                    route_stations = network.routes.get(mt.route_id, [])
                    target_station = route_stations[-1] if route_stations else source_station
                    
                    # Connected alternative route calculation
                    if mt.route_id in [1, 12623, 12625, 12007, 12607]: # Route 1 trains
                        if source_station == 1:
                            new_route_stations = [1, 2, 5, 4, 8, 10]
                        elif source_station == 4:
                            new_route_stations = [1, 4, 5, 2, 3]
                        else:
                            new_route_stations = [1, 4, 8, 10]
                    elif mt.route_id in [3, 22625]: # Route 3 trains
                        new_route_stations = [1, 4, 8, 10]
                    else:
                        new_route_stations = [1, 4, 8, 10]
                    
                    act = create_action(
                        action_id=action_counter,
                        action_type="REROUTE",
                        train_id=train_id,
                        source_station=source_station,
                        target_station=target_station,
                        parameters={
                            "new_route_stations": new_route_stations,
                            "original_route_stations": route_stations
                        },
                        expected_effect={"delay_reduction": 14.2, "congestion_reduction": 0.0},
                        constraints={},
                        confidence=0.91,
                        passenger_impact="Medium",
                        track_id=tr.track_id,
                        train_name=mt.name
                    )
                    actions.append(act)
                    action_counter += 1

        # 3. Hold Upstream (triggered by leading delays)
        delayed_trains = [t for t in network.trains if t.delay > 10.0]
        for dt in delayed_trains:
            route_stations = network.routes.get(dt.route_id, [])
            target_station = route_stations[-1] if route_stations else dt.current_station_id
            
            act = create_action(
                action_id=action_counter,
                action_type="HOLD",
                train_id=dt.name,
                source_station=dt.current_station_id,
                target_station=target_station,
                parameters={"duration_mins": 5},
                expected_effect={"delay_reduction": 6.0, "congestion_reduction": 0.0},
                constraints={},
                confidence=0.85,
                passenger_impact="Low",
                duration_mins=5,
                train_name=dt.name
            )
            actions.append(act)
            action_counter += 1

        # 4. Speed Adjustment
        for t in network.trains:
            if t.status == "MOVING" and t.delay > 5.0:
                route_stations = network.routes.get(t.route_id, [])
                target_station = route_stations[-1] if route_stations else t.current_station_id
                
                act = create_action(
                    action_id=action_counter,
                    action_type="SPEED_ADJUST",
                    train_id=t.name,
                    source_station=t.current_station_id,
                    target_station=target_station,
                    parameters={"speed_multiplier": 1.10}, # 10% physical speed adjustment
                    expected_effect={"delay_reduction": 4.5, "congestion_reduction": 0.0},
                    constraints={},
                    confidence=0.93,
                    passenger_impact="None",
                    new_speed_kmp=75 if t.speed > 80 else 90,
                    train_name=t.name
                )
                actions.append(act)
                action_counter += 1

        # Fallback default actions if network is completely stable
        if not actions:
            act = create_action(
                action_id=action_counter,
                action_type="SCHEDULE_MAINTENANCE",
                train_id="Global",
                source_station=1,
                target_station=1,
                parameters={},
                expected_effect={"delay_reduction": 0.0, "congestion_reduction": 0.0},
                constraints={},
                confidence=0.99,
                passenger_impact="None"
            )
            actions.append(act)
            action_counter += 1

        return actions


    @staticmethod
    def compare_scenarios(actions: list, baseline_recovery_time: int) -> list:
        """
        Simulates multiple intervention scenarios and estimates the expected recovery time for each.
        """
        scenarios = [
            {
                "scenario_id": "Scenario A",
                "name": "No Action (Baseline)",
                "expected_recovery_time_mins": baseline_recovery_time,
                "remaining_disruption_mins": baseline_recovery_time,
                "expected_global_delay_reduction": 0.0,
                "confidence": 0.95
            }
        ]

        # Scenario B (Platform Swap actions applied)
        swap_reduction = sum([a["expected_delay_reduction"] for a in actions if a["action"] == "PLATFORM_SWAP"])
        rec_time_b = max(10, baseline_recovery_time - int(swap_reduction))
        scenarios.append({
            "scenario_id": "Scenario B",
            "name": "Junction Platform Swaps",
            "expected_recovery_time_mins": rec_time_b,
            "remaining_disruption_mins": rec_time_b,
            "expected_global_delay_reduction": round(swap_reduction, 1),
            "confidence": 0.88
        })

        # Scenario C (Reroute / Speed limit actions applied)
        reroute_reduction = sum([a["expected_delay_reduction"] for a in actions if a["action"] in ["REROUTE", "SPEED_ADJUST"]])
        rec_time_c = max(10, baseline_recovery_time - int(reroute_reduction))
        scenarios.append({
            "scenario_id": "Scenario C",
            "name": "Dynamic Reroutes & Speed Limits",
            "expected_recovery_time_mins": rec_time_c,
            "remaining_disruption_mins": rec_time_c,
            "expected_global_delay_reduction": round(reroute_reduction, 1),
            "confidence": 0.91
        })

        return scenarios
