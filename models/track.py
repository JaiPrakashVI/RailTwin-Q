class Track:
    def __init__(
        self,
        track_id,
        source_station_id,
        destination_station_id,
        distance,
        max_speed,
        capacity=5,
        name=None,
        track_type="DOUBLE_TRACK",
        direction="BOTH"
    ):
        self.track_id = track_id
        self.name = name or f"Track {track_id}"
        self.source_station_id = source_station_id
        self.destination_station_id = destination_station_id
        self.distance = distance
        self.max_speed = max_speed
        self.capacity = capacity
        self.track_type = track_type
        self.direction = direction

        # State / occupancy track variables
        self.current_trains = 0
        self.occupancy_percent = 0.0
        self.average_speed = float(max_speed)
        self.travel_time = (distance / max_speed) * 60.0 if max_speed > 0 else 0.0
        
        # Disruption flags
        self.blocked = False
        self.maintenance = False

        # Targets
        self.future_track_congestion = 0.0

    def __str__(self):
        return f"{self.name}: Station {self.source_station_id} -> Station {self.destination_station_id}"
