import os
import numpy as np
import pandas as pd
from ai.congestion_prediction.utils import pred_logger
from ai.congestion_prediction.inference import HierarchicalInferenceEngine
from services.synthetic_data.feature_engineering import FeatureEngineering
from services.synthetic_data.train_dataset_generator import TrainDatasetGenerator
from services.synthetic_data.station_dataset_generator import StationDatasetGenerator
from services.synthetic_data.track_dataset_generator import TrackDatasetGenerator
from services.synthetic_data.network_dataset_generator import NetworkDatasetGenerator
from services.graph_builder import GraphBuilder

class PredictionService:
    def __init__(self, models_dir="models/congestion_predictor"):
        self.inference_engine = HierarchicalInferenceEngine(models_dir)
        self.inference_engine.initialize()
        
        # Historical sliding windows for rolling calculations (max length 20)
        self.station_history = []
        self.track_history = []
        self.network_history = []

    def get_predictions_for_tick(self, network, tick: int, time_str: str, running_events: list, delay_preds: list) -> dict:
        """
        Gathers current tick state, runs sliding window rolling aggregates,
        applies neighbor graph operations, merges delay predictions, and evaluates congestion.
        """
        if not self.inference_engine.initialized:
            pred_logger.warning("Hierarchical Congestion Inference engine not initialized. Skipping predictions.")
            return {}

        # 1. Serialize active events
        active_events_serialized = []
        for ev in running_events:
            ev_data = {
                "name": ev.__class__.__name__.replace("Event", ""),
                "active": ev.active,
                "duration": ev.duration
            }
            if hasattr(ev, "intensity"):
                ev_data["intensity"] = ev.intensity
            if hasattr(ev, "station_id"):
                ev_data["station_id"] = ev.station_id
            if hasattr(ev, "track_id"):
                ev_data["track_id"] = ev.track_id
            active_events_serialized.append(ev_data)

        # 2. Get Graph Centralities
        graph = GraphBuilder.build_graph(network)
        graph_metrics = FeatureEngineering.compute_graph_metrics(graph)

        # 3. Serialize Trains
        trains_serialized = []
        for t in network.trains:
            trains_serialized.append({
                "train_no": t.train_no,
                "name": t.name,
                "train_type": t.train_type,
                "is_priority_train": t.is_priority_train,
                "route_id": t.route_id,
                "current_station": t.current_station_id,
                "status": t.status,
                "progress": round(t.progress, 2),
                "speed": t.speed,
                "max_speed": t.max_speed,
                "delay": t.delay,
                "delay_change_last_tick": t.delay_change_last_tick,
                "distance_travelled": t.distance_travelled,
                "remaining_distance": t.remaining_distance,
                "remaining_route_distance": t.remaining_route_distance,
                "scheduled_arrival_time": t.scheduled_arrival_time,
                "expected_arrival_time": t.expected_arrival_time,
                "primary_delay_reason": t.primary_delay_reason,
                "secondary_delay_reason": t.secondary_delay_reason,
                "current_track_id": t.current_track_id
            })

        # 4. Serialize Stations
        stations_serialized = []
        for s in network.stations:
            metrics = graph_metrics.get(s.station_id, {})
            stations_serialized.append({
                "station_id": s.station_id,
                "name": s.name,
                "platforms_total": s.platforms,
                "platforms_occupied": s.platforms_occupied,
                "trains_waiting": s.trains_waiting,
                "incoming_trains": s.incoming_trains,
                "outgoing_trains": s.outgoing_trains,
                "station_congestion_score": s.station_congestion_score,
                "station_utilization_percent": s.station_utilization_percent,
                "average_station_delay": s.average_station_delay,
                "node_degree": metrics.get("node_degree", 0),
                "betweenness_centrality": metrics.get("betweenness_centrality", 0.0),
                "closeness_centrality": metrics.get("closeness_centrality", 0.0),
                "station_connectivity": metrics.get("station_connectivity", 0.0)
            })

        # 5. Serialize Tracks
        tracks_serialized = []
        for tr in network.tracks:
            tracks_serialized.append({
                "track_id": tr.track_id,
                "source": tr.source_station_id,
                "destination": tr.destination_station_id,
                "distance": tr.distance,
                "track_capacity": tr.capacity,
                "max_speed": tr.max_speed,
                "trains_on_track": tr.current_trains,
                "occupancy_percent": tr.occupancy_percent,
                "average_speed": tr.average_speed,
                "travel_time": tr.travel_time,
                "blocked": tr.blocked,
                "maintenance": tr.maintenance
            })

        congested_st = sum(1 for s in network.stations if s.station_utilization_percent >= 80.0)
        congested_tr = sum(1 for tr in network.tracks if tr.occupancy_percent >= 80.0)
        tot_active_trains = sum(1 for t in network.trains if t.status != "ARRIVED")
        avg_delay = sum(t.delay for t in network.trains) / len(network.trains) if network.trains else 0.0
        avg_speed = sum(t.speed for t in network.trains) / len(network.trains) if network.trains else 0.0

        snapshot = {
            "time": time_str,
            "trains": trains_serialized,
            "stations": stations_serialized,
            "tracks": tracks_serialized,
            "active_events": active_events_serialized,
            "congested_stations": congested_st,
            "congested_tracks": congested_tr,
            "active_trains": tot_active_trains,
            "average_delay": round(avg_delay, 2),
            "average_speed": round(avg_speed, 2)
        }

        # Format generators
        history_records = [(tick, snapshot)]
        stations_map = {s.station_id: s.name for s in network.stations}
        tracks_map = {t.track_id: t for t in network.tracks}

        stations_data = StationDatasetGenerator.generate(1, history_records, stations_map)
        tracks_data = TrackDatasetGenerator.generate(1, history_records, stations_map)
        network_data = NetworkDatasetGenerator.generate(1, history_records, "WEEKDAY")
        train_data = TrainDatasetGenerator.generate(1, history_records, network.routes, stations_map, tracks_map, graph)

        df_st_curr = pd.DataFrame(stations_data)
        df_tr_curr = pd.DataFrame(tracks_data)
        df_net_curr = pd.DataFrame(network_data)
        df_tr_train = pd.DataFrame(train_data)

        # -------------------------------------------------------------
        # Feature Engineering v2 additions (calculated live on current tick)
        # -------------------------------------------------------------
        # 1 & 2. ETA demand windows & decay scores
        # Determine next station for each active train
        trains_eta = []
        for t in network.trains:
            if t.status == "ARRIVED":
                eta = 999.0
                next_station_id = None
            else:
                if t.speed > 0:
                    eta = (t.remaining_distance / t.speed) * 60.0
                else:
                    eta = 999.0
                
                # Fetch route stations path to locate next stop
                route_stations = network.routes.get(t.route_id, [])
                if t.route_index + 1 < len(route_stations):
                    next_station_id = route_stations[t.route_index + 1]
                else:
                    next_station_id = None
            
            trains_eta.append({"train_no": t.train_no, "eta": eta, "next_station_id": next_station_id})

        # Calculate counts per station
        eta_counts = {s.station_id: {5: 0, 10: 0, 15: 0, 30: 0, 60: 0, "decay": 0.0} for s in network.stations}
        for entry in trains_eta:
            ns = entry["next_station_id"]
            if ns in eta_counts:
                eta = entry["eta"]
                for h in [5, 10, 15, 30, 60]:
                    if eta <= h:
                        eta_counts[ns][h] += 1
                eta_counts[ns]["decay"] += np.exp(-eta / 15.0)

        # Map to df_st_curr
        for s_id in df_st_curr["station_id"].values:
            counts = eta_counts.get(s_id, {5: 0, 10: 0, 15: 0, 30: 0, 60: 0, "decay": 0.0})
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "incoming_trains_eta_5"] = counts[5]
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "incoming_trains_eta_10"] = counts[10]
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "incoming_trains_eta_15"] = counts[15]
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "incoming_trains_eta_30"] = counts[30]
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "incoming_trains_eta_60"] = counts[60]
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "incoming_demand_score"] = counts["decay"]

        # 3. Downstream backpressure
        # Node status lookup
        station_objs = {s.station_id: s for s in network.stations}
        for s_id in df_st_curr["station_id"].values:
            downstream_ids = []
            for r_id, r_stations in network.routes.items():
                if s_id in r_stations:
                    idx = r_stations.index(s_id)
                    if idx + 1 < len(r_stations):
                        d_id = r_stations[idx + 1]
                        if d_id not in downstream_ids:
                            downstream_ids.append(d_id)
            
            down_congs, down_utils, down_waits, down_delays = [], [], [], []
            for d_id in downstream_ids:
                if d_id in station_objs:
                    down_s = station_objs[d_id]
                    down_congs.append(down_s.station_congestion_score)
                    down_utils.append(down_s.station_utilization_percent)
                    down_waits.append(down_s.trains_waiting)
                    down_delays.append(down_s.average_station_delay)
                    
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "downstream_congestion"] = np.mean(down_congs) if down_congs else 0.0
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "downstream_platform_utilization"] = np.mean(down_utils) if down_utils else 0.0
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "downstream_queue_length"] = np.mean(down_waits) if down_waits else 0.0
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "downstream_average_delay"] = np.mean(down_delays) if down_delays else 0.0

        # 4. Multi-hop aggregates
        import networkx as nx
        G = nx.Graph()
        for s in network.stations:
            G.add_node(s.station_id)
        for t in network.tracks:
            G.add_edge(t.source_station_id, t.destination_station_id)

        for s_id in df_st_curr["station_id"].values:
            try:
                path_lengths = nx.single_source_shortest_path_length(G, s_id)
            except Exception:
                path_lengths = {}
            for h in [1, 2, 3]:
                nodes = [node for node, dist in path_lengths.items() if dist == h]
                nbr_congs, nbr_delays, nbr_utils, nbr_waits = [], [], [], []
                for n in nodes:
                    if n in station_objs:
                        nbr_congs.append(station_objs[n].station_congestion_score)
                        nbr_delays.append(station_objs[n].average_station_delay)
                        nbr_utils.append(station_objs[n].station_utilization_percent)
                        nbr_waits.append(station_objs[n].trains_waiting)
                
                df_st_curr.loc[df_st_curr["station_id"] == s_id, f"neighbor_congestion_mean_h{h}"] = np.mean(nbr_congs) if nbr_congs else 0.0
                df_st_curr.loc[df_st_curr["station_id"] == s_id, f"neighbor_delay_mean_h{h}"] = np.mean(nbr_delays) if nbr_delays else 0.0
                df_st_curr.loc[df_st_curr["station_id"] == s_id, f"neighbor_platform_utilization_h{h}"] = np.mean(nbr_utils) if nbr_utils else 0.0
                df_st_curr.loc[df_st_curr["station_id"] == s_id, f"neighbor_waiting_trains_h{h}"] = np.mean(nbr_waits) if nbr_waits else 0.0

        # 5. Net Flow
        df_st_curr["net_flow"] = df_st_curr["incoming_trains"] - df_st_curr["outgoing_trains"]
        df_st_curr["incoming_rate"] = df_st_curr["incoming_trains"] / np.maximum(1.0, df_st_curr["platforms_total"])
        df_st_curr["outgoing_rate"] = df_st_curr["outgoing_trains"] / np.maximum(1.0, df_st_curr["platforms_total"])
        df_st_curr["flow_balance_ratio"] = df_st_curr["incoming_trains"] / np.maximum(1.0, df_st_curr["outgoing_trains"])

        # 6. Route pressure
        routes_list = list(network.routes.values())
        for s_id in df_st_curr["station_id"].values:
            inc_routes = sum(1 for r in routes_list if s_id in r and r.index(s_id) > 0)
            out_routes = sum(1 for r in routes_list if s_id in r and r.index(s_id) < len(r) - 1)
            comp = float(G.degree(s_id)) if s_id in G else 1.0
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "incoming_routes"] = inc_routes
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "outgoing_routes"] = out_routes
            df_st_curr.loc[df_st_curr["station_id"] == s_id, "route_complexity"] = comp


        # -------------------------------------------------------------
        # sliding histories management
        # -------------------------------------------------------------
        self.station_history.append(df_st_curr)
        self.track_history.append(df_tr_curr)
        self.network_history.append(df_net_curr)

        if len(self.station_history) > 20: self.station_history.pop(0)
        if len(self.track_history) > 20: self.track_history.pop(0)
        if len(self.network_history) > 20: self.network_history.pop(0)

        df_st_hist = pd.concat(self.station_history, ignore_index=True)
        df_tr_hist = pd.concat(self.track_history, ignore_index=True)
        df_net_hist = pd.concat(self.network_history, ignore_index=True)

        # 7. Calculate Rolling average & Max features on current station row
        rolling_cols_st = [
            "platforms_occupied", "waiting_trains", "station_congestion_score", 
            "station_utilization_percent", "average_station_delay"
        ]
        for col in rolling_cols_st:
            for w in [5, 10, 20]:
                for s_id in df_st_curr["station_id"].values:
                    sub = df_st_hist[df_st_hist["station_id"] == s_id].tail(w)
                    df_st_curr.loc[df_st_curr["station_id"] == s_id, f"{col}_roll_mean_{w}"] = sub[col].mean() if not sub.empty else 0.0

        # Rolling Max Congestion
        for w in [5, 10, 20]:
            for s_id in df_st_curr["station_id"].values:
                sub = df_st_hist[df_st_hist["station_id"] == s_id].tail(w)
                df_st_curr.loc[df_st_curr["station_id"] == s_id, f"station_congestion_score_roll_max_{w}"] = sub["station_congestion_score"].max() if not sub.empty else 0.0

        # 8. Calculate Temporal Trend Features
        for col in ["station_congestion_score", "average_station_delay", "waiting_trains", "platforms_occupied"]:
            for s_id in df_st_curr["station_id"].values:
                sub = df_st_hist[df_st_hist["station_id"] == s_id].tail(2)
                val = sub[col].diff().dropna().values[0] if len(sub) == 2 else 0.0
                df_st_curr.loc[df_st_curr["station_id"] == s_id, f"{col}_trend"] = val

        # 9. Feature 9 — Network Pressure Features
        # Merge network statistics (utilization, global average delay)
        df_st_curr["global_congestion_index"] = df_net_curr["network_congestion_score"].values[0]
        df_st_curr["global_platform_utilization"] = df_net_curr["platform_utilization_percent"].values[0]
        df_st_curr["global_track_utilization"] = df_net_curr["track_utilization_percent"].values[0]
        df_st_curr["global_average_delay"] = df_net_curr["average_network_delay"].values[0]
        df_st_curr["global_average_speed"] = df_net_curr["average_train_speed"].values[0]
        df_st_curr["global_resilience_score"] = df_net_curr["network_resilience_score"].values[0]

        # 10. Merge Delay Predictions into station dataframe
        pred_delays_map = {}
        for p in delay_preds:
            pred_delays_map[p["train_id"]] = p["delay_predictions"]

        df_tr_train["future_delay_15"] = df_tr_train["train_no"].map(lambda x: pred_delays_map.get(x, {}).get("15", 0.0))
        df_tr_train["future_delay_30"] = df_tr_train["train_no"].map(lambda x: pred_delays_map.get(x, {}).get("30", 0.0))
        df_tr_train["future_delay_60"] = df_tr_train["train_no"].map(lambda x: pred_delays_map.get(x, {}).get("60", 0.0))

        st_delay_agg = df_tr_train.groupby("current_station_id")[["future_delay_15", "future_delay_30", "future_delay_60"]].mean().reset_index().rename(
            columns={"current_station_id": "station_id"}
        )
        df_st_curr = pd.merge(df_st_curr, st_delay_agg, on="station_id", how="left").fillna(0.0)

        # 11. Calculate Track Rolling Features
        rolling_cols_tr = ["trains_on_track", "occupancy_percent", "average_speed"]
        for col in rolling_cols_tr:
            for w in [5, 10, 20]:
                for tr_id in df_tr_curr["track_id"].values:
                    sub = df_tr_hist[df_tr_hist["track_id"] == tr_id].tail(w)
                    df_tr_curr.loc[df_tr_curr["track_id"] == tr_id, f"{col}_roll_{w}"] = sub[col].mean() if not sub.empty else 0.0

        # Merge Delays into track
        tr_delay_agg = df_tr_train.groupby("current_track_id")[["future_delay_15", "future_delay_30", "future_delay_60"]].mean().reset_index().rename(
            columns={"current_track_id": "track_id"}
        )
        df_tr_curr = pd.merge(df_tr_curr, tr_delay_agg, on="track_id", how="left").fillna(0.0)

        # 12. Calculate Network Rolling Features
        rolling_cols_net = ["network_congestion_score", "platform_utilization_percent", "track_utilization_percent", "average_network_delay"]
        for col in rolling_cols_net:
            for w in [5, 10, 20]:
                sub = df_net_hist.tail(w)
                df_net_curr[f"{col}_roll_{w}"] = sub[col].mean() if not sub.empty else df_net_curr[col].values[0]

        # 13. Execute stacked Hierarchical Predictions
        predicted_futures = self.inference_engine.predict_future_railway_state(
            df_st_curr,
            df_tr_curr,
            df_net_curr
        )

        return predicted_futures
