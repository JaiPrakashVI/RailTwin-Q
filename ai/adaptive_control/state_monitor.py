import json
import os

class StateMonitor:
    @staticmethod
    def observe(network, active_events, tick, current_intervention_plan) -> dict:
        """
        Observes the current state of the Digital Twin network.
        Returns a dictionary representing the state snapshot.
        """
        trains_state = []
        total_delay = 0.0
        passenger_impact = 0
        
        for t in network.trains:
            total_delay += t.delay
            # Base passengers impacted
            if t.delay > 5:
                passenger_impact += int(t.delay * 50)
                
            loc_str = "At station" if t.progress == 0.0 else "Moving on track"
            trains_state.append({
                "train_id": t.train_no,
                "name": t.name,
                "speed": t.speed,
                "delay": t.delay,
                "location": loc_str,
                "progress": t.progress
            })
            
        avg_delay = total_delay / max(len(network.trains), 1)
        
        # Platform & track utilizations
        station_slots = 0
        station_occupied = 0
        for s in network.stations:
            station_slots += s.platforms
            station_occupied += s.platforms_occupied
            
        platform_util = float(station_occupied / max(station_slots, 1))
        
        track_capacity = 0
        track_occupied = 0
        for tr in network.tracks:
            track_capacity += tr.capacity
            track_occupied += tr.current_trains
            
        track_util = float(track_occupied / max(track_capacity, 1))
        
        # Network congestion score proxy
        network_congestion = (platform_util * 0.4 + track_util * 0.6)
        
        # Signal status & active events
        active_disruptions = []
        weather = "Clear"
        for ev in active_events:
            if ev.active:
                active_disruptions.append({
                    "name": ev.name,
                    "severity": getattr(ev, "intensity", 1.0)
                })
                if "Rain" in ev.name:
                    weather = f"Heavy Rain (Intensity: {getattr(ev, 'intensity', 0.0)})"
                    
        return {
            "timestamp": tick,
            "active_disruptions": len(active_disruptions),
            "disruptions_list": active_disruptions,
            "network_delay": avg_delay,
            "congestion": network_congestion,
            "platform_utilization": platform_util,
            "track_utilization": track_util,
            "passenger_impact": passenger_impact,
            "weather": weather,
            "trains": trains_state,
            "active_interventions": current_intervention_plan
        }
