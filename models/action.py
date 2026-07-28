class Action(dict):
    def __init__(
        self,
        action_id: int,
        action_type: str,
        train_id: str,
        source_station: int,
        target_station: int,
        parameters: dict,
        expected_effect: dict,
        constraints: dict,
        execution_function,
        **kwargs
    ):
        """
        Action Contract representing a single dispatch intervention.
        Inherits from dict to ensure full backward compatibility across Layer 4, 5, and 6.
        """
        super().__init__()
        self["action_id"] = action_id
        self["action"] = action_type          # For legacy compatibility with act.get("action")
        self["action_type"] = action_type
        self["train_id"] = train_id
        self["target"] = train_id             # For legacy compatibility with act.get("target")
        self["source_station"] = source_station
        self["target_station"] = target_station
        self["parameters"] = parameters
        self["expected_effect"] = expected_effect
        self["constraints"] = constraints
        self.execution_function = execution_function
        
        # Populate legacy keys for backward compatibility
        self["expected_delay_reduction"] = expected_effect.get("delay_reduction", 0.0)
        self["expected_congestion_reduction"] = expected_effect.get("congestion_reduction", 0.0)
        self["confidence"] = kwargs.get("confidence", 0.90)
        self["passenger_impact"] = kwargs.get("passenger_impact", "None")
        
        self.update(kwargs)                   # Copy all extra legacy/helper keys into the dict


    def execute(self, network, active_events, tick) -> bool:
        """
        Invokes the encapsulated execution function to apply changes directly to the Digital Twin.
        """
        if self.execution_function:
            return self.execution_function(self, network, active_events, tick)
        return False

    def __repr__(self):
        return (
            f"Action(id={self['action_id']}, type={self['action_type']}, "
            f"train={self['train_id']}, source={self['source_station']}, target={self['target_station']})"
        )


# Unified Execution Functions

def execute_speed_adjust(action, network, active_events, tick) -> bool:
    train_id = action["train_id"]
    mult = action["parameters"].get("speed_multiplier", 1.05)
    train_obj = network.get_train_by_no(train_id)
    if not train_obj:
        train_obj = next((t for t in network.trains if t.name == train_id), None)
    
    if train_obj:
        # Physical speed modification
        train_obj.base_speed = min(train_obj.base_speed * mult, train_obj.max_speed)
        train_obj.speed = min(train_obj.speed * mult, train_obj.max_speed)
        return True
    return False

def execute_platform_swap(action, network, active_events, tick) -> bool:
    train_id = action["train_id"]
    train_obj = network.get_train_by_no(train_id)
    if not train_obj:
        train_obj = next((t for t in network.trains if t.name == train_id), None)
    
    if train_obj:
        # Mark as priority to bypass departure platform waits
        train_obj.is_priority_train = True
        return True
    return False

def execute_hold(action, network, active_events, tick) -> bool:
    train_id = action["train_id"]
    duration = action["parameters"].get("duration_mins", 5)
    train_obj = network.get_train_by_no(train_id)
    if not train_obj:
        train_obj = next((t for t in network.trains if t.name == train_id), None)
    
    if train_obj:
        # Force dwell countdown time
        train_obj.dwell_time_remaining = max(train_obj.dwell_time_remaining, duration)
        train_obj.status = "DELAYED"
        train_obj.speed = 0.0
        return True
    return False

def execute_reroute(action, network, active_events, tick) -> bool:
    train_id = action["train_id"]
    new_route_stations = action["parameters"].get("new_route_stations", [])
    train_obj = network.get_train_by_no(train_id)
    if not train_obj:
        train_obj = next((t for t in network.trains if t.name == train_id), None)
    
    if train_obj and new_route_stations:
        # Dynamically register the new route in the network
        new_route_id = f"dynamic_reroute_{train_obj.train_no}_{tick}"
        network.add_route(new_route_id, new_route_stations)
        train_obj.route_id = new_route_id
        
        # Reset route_index to the index of current station in the new route
        if train_obj.current_station_id in new_route_stations:
            train_obj.route_index = new_route_stations.index(train_obj.current_station_id)
        else:
            # Fallback: align to the first station in the new route list
            train_obj.route_index = 0
            train_obj.current_station_id = new_route_stations[0]
        return True
    return False

def execute_maintenance(action, network, active_events, tick) -> bool:
    return True

# Helper registry maps action types to execution handlers
EXECUTION_REGISTRY = {
    "SPEED_ADJUST": execute_speed_adjust,
    "PLATFORM_SWAP": execute_platform_swap,
    "HOLD": execute_hold,
    "REROUTE": execute_reroute,
    "SCHEDULE_MAINTENANCE": execute_maintenance
}

def create_action(
    action_id: int,
    action_type: str,
    train_id: str,
    source_station: int,
    target_station: int,
    parameters: dict = None,
    expected_effect: dict = None,
    constraints: dict = None,
    **kwargs
) -> Action:
    """
    Action Builder that automatically links the correct execution function from registry.
    """
    if parameters is None:
        parameters = {}
    if expected_effect is None:
        expected_effect = {}
    if constraints is None:
        constraints = {}

    exec_fn = EXECUTION_REGISTRY.get(action_type, execute_maintenance)
    
    return Action(
        action_id=action_id,
        action_type=action_type,
        train_id=train_id,
        source_station=source_station,
        target_station=target_station,
        parameters=parameters,
        expected_effect=expected_effect,
        constraints=constraints,
        execution_function=exec_fn,
        **kwargs
    )

