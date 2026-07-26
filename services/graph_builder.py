import networkx as nx
from models.railway_network import RailwayNetwork

class GraphBuilder:
    @staticmethod
    def build_graph(network: RailwayNetwork) -> nx.Graph:
        """
        Builds a NetworkX undirected graph representing the railway network.
        Stations are nodes, and Tracks are edges.
        """
        G = nx.Graph()

        # Add stations as nodes
        for station in network.stations:
            G.add_node(
                station.station_id,
                name=station.name,
                code=getattr(station, "code", f"ST{station.station_id}"),
                x=getattr(station, "x", 100),
                y=getattr(station, "y", 200),
                latitude=station.latitude,
                longitude=station.longitude,
                platforms=station.platforms,
                station_type=getattr(station, "station_type", "REGULAR"),
                is_junction=getattr(station, "is_junction", False),
                station_obj=station
            )

        # Add tracks as edges
        for track in network.tracks:
            travel_time_hours = track.distance / track.max_speed if track.max_speed > 0 else float('inf')
            G.add_edge(
                track.source_station_id,
                track.destination_station_id,
                track_id=track.track_id,
                name=getattr(track, "name", f"Track {track.track_id}"),
                distance=track.distance,
                max_speed=track.max_speed,
                capacity=track.capacity,
                track_type=getattr(track, "track_type", "DOUBLE_TRACK"),
                direction=getattr(track, "direction", "BOTH"),
                weight=travel_time_hours,
                track_obj=track
            )

        return G
