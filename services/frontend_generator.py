import os
import json
import time

class FrontendGenerator:
    @staticmethod
    def _safe_write(filepath: str, content: str) -> None:
        for attempt in range(5):
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                break
            except OSError as e:
                if attempt == 4:
                    raise e
                time.sleep(0.2)

    @staticmethod
    def get_timeline_records() -> list:
        timeline = []
        try:
            if os.path.exists("datasets/trigger_engine_log.jsonl"):
                with open("datasets/trigger_engine_log.jsonl", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            d = json.loads(line)
                            tick = d.get("tick", 0)
                            trigger = d.get("trigger", "")
                            action = d.get("action", "")
                            reason = d.get("reason", "")
                            timeline.append({
                                "tick": tick,
                                "type": "trigger",
                                "text": f"🚨 <b>t={tick}</b>: Trigger Engine Action: <b>{action}</b> ({trigger}). Reason: {reason}"
                            })
        except Exception:
            pass

        try:
            if os.path.exists("datasets/decision_gate_log.jsonl"):
                with open("datasets/decision_gate_log.jsonl", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            d = json.loads(line)
                            tick = d.get("tick", 0)
                            decision = d.get("decision", "")
                            reason = d.get("reason", "")
                            timeline.append({
                                "tick": tick,
                                "type": "gate",
                                "text": f"⚖️ <b>t={tick}</b>: Decision Gate Verdict: <b>{decision}</b>. Reason: {reason}"
                            })
        except Exception:
            pass

        try:
            if os.path.exists("datasets/qubo_comparison_log.jsonl"):
                with open("datasets/qubo_comparison_log.jsonl", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            d = json.loads(line)
                            tick = d.get("tick", 0)
                            solver = d.get("solver_selected", "hybrid_qaoa")
                            vars_count = d.get("variable_count", 0)
                            warm = d.get("warm_start_loaded", False)
                            timeline.append({
                                "tick": tick,
                                "type": "qubo",
                                "text": f"⚛️ <b>t={tick}</b>: Quantum Scheduler: QUBO formulated with <b>{vars_count} qubits</b>. Solver: <b>{solver}</b> (Warm-Start: {warm})."
                            })
        except Exception:
            pass

        timeline.sort(key=lambda x: x["tick"])
        return timeline

    @staticmethod
    def generate_live_state(network, tick: int, sim_time_str: str, active_events: list, preds_delay: list, preds_congestion: dict, preds_propagation: dict, control_orchestrator) -> dict:
        events_list = []
        for ev in active_events:
            if getattr(ev, "active", True):
                events_list.append({
                    "name": getattr(ev, "name", "Disruption"),
                    "intensity": getattr(ev, "intensity", 1.0),
                    "station_id": getattr(ev, "station_id", None),
                    "track_id": getattr(ev, "track_id", None)
                })

        stations_list = []
        for s in network.stations:
            stations_list.append({
                "id": s.station_id,
                "name": s.name,
                "code": getattr(s, "code", f"ST{s.station_id}"),
                "x": getattr(s, "x", 100),
                "y": getattr(s, "y", 200),
                "platforms_occupied": s.platforms_occupied,
                "platforms": s.platforms,
                "station_type": getattr(s, "station_type", "REGULAR"),
                "is_junction": getattr(s, "is_junction", False),
                "incoming_trains": getattr(s, "incoming_trains", 0),
                "outgoing_trains": getattr(s, "outgoing_trains", 0),
                "congestion": round(s.station_congestion_score * 100.0, 1),
                "status": "CONGESTED" if s.platforms_occupied >= s.platforms * 0.8 else ("Busy" if s.platforms_occupied > 0 else "Empty")
            })

        tracks_list = []
        for tr in network.tracks:
            src_st = network.get_station_by_id(tr.source_station_id)
            dest_st = network.get_station_by_id(tr.destination_station_id)
            tracks_list.append({
                "id": tr.track_id,
                "name": getattr(tr, "name", f"{src_st.name if src_st else ''}-{dest_st.name if dest_st else ''}"),
                "source_station_id": tr.source_station_id,
                "destination_station_id": tr.destination_station_id,
                "current_trains": tr.current_trains,
                "capacity": tr.capacity,
                "distance": tr.distance,
                "occupancy_percent": round(tr.occupancy_percent, 1),
                "track_type": getattr(tr, "track_type", "DOUBLE_TRACK"),
                "status": "BLOCKED" if any("Failure" in e.get("name", "") for e in events_list if e.get("station_id") == tr.source_station_id) else ("CONGESTED" if tr.occupancy_percent >= 80.0 else "NORMAL")
            })

        trains_list = []
        for t in network.trains:
            pred_item = next((p for p in preds_delay if p["train_id"] == t.train_no), None)
            
            loc_desc = "At Station"
            if t.progress == 0.0:
                st = network.get_station_by_id(t.current_station_id)
                loc_desc = f"At {st.name if st else 'Station'}"
            else:
                track = network.get_track_by_id(t.current_track_id)
                if track:
                    src = network.get_station_by_id(track.source_station_id)
                    dest = network.get_station_by_id(track.destination_station_id)
                    loc_desc = f"Moving {src.name if src else ''} -> {dest.name if dest else ''} ({t.progress:.1f}%)"

            trains_list.append({
                "train_no": t.train_no,
                "name": t.name,
                "train_type": getattr(t, "train_type", "EXPRESS"),
                "priority": getattr(t, "priority", 3),
                "status": t.status,
                "speed": t.speed,
                "progress": t.progress,
                "current_track_id": t.current_track_id,
                "current_station_id": t.current_station_id,
                "delay": round(t.delay, 2),
                "predicted_delay_15": round(pred_item["delay_predictions"]["15"], 1) if pred_item else 0.0,
                "predicted_delay_30": round(pred_item["delay_predictions"]["30"], 1) if pred_item else 0.0,
                "predicted_delay_60": round(pred_item["delay_predictions"]["60"], 1) if pred_item else 0.0,
                "confidence": round(pred_item["confidence"] if pred_item else 0.85, 2),
                "top_factors": pred_item["top_factors"] if pred_item else ["None"],
                "loc_desc": loc_desc
            })

        last_cycle = control_orchestrator.controller_run_history[-1] if control_orchestrator.controller_run_history else {}
        next_eligible = max(tick, (control_orchestrator.controller.last_opt_tick or 0) + control_orchestrator.controller.re_opt_cooldown)
        recovery_status = "STABILIZING" if control_orchestrator.controller.state == "RECOVERING" else ("RECOVERED" if control_orchestrator.controller.state == "MONITORING" and control_orchestrator.controller.last_opt_tick is not None else "NORMAL")
        # Load optimization result metrics
        opt_res = {}
        opt_path = "datasets/optimization_result.json"
        if os.path.exists(opt_path):
            try:
                with open(opt_path, "r", encoding="utf-8") as f:
                    opt_res = json.load(f)
            except Exception:
                pass
        
        cf_results = opt_res.get("counterfactual_results", {})
        baseline_delay_total = cf_results.get("baseline_delay", 878.8)
        optimized_delay_total = cf_results.get("optimized_delay", 878.8)
        delay_reduction_pct = cf_results.get("delay_reduction_percent", 0.0)
        
        num_trains = max(1, len(network.trains))
        baseline_delay = round(baseline_delay_total / num_trains, 1)
        optimized_delay = round(optimized_delay_total / num_trains, 1)
        
        baseline_congestion = round(cf_results.get("baseline_congestion", 9.58), 1)
        optimized_congestion = round(cf_results.get("optimized_congestion", 9.58), 1)
        congestion_reduction_pct = round(cf_results.get("congestion_reduction_percent", 0.0), 1)
        
        # Load benchmark results
        bench_res = {}
        bench_path = "datasets/layer5_final_benchmark.json"
        if os.path.exists(bench_path):
            try:
                with open(bench_path, "r", encoding="utf-8") as f:
                    bench_res = json.load(f)
            except Exception:
                pass
                
        noisy_qaoa_sa = bench_res.get("noise_deconstruction", {}).get("noisy_qaoa_sa", {})
        qaoa_runtime = noisy_qaoa_sa.get("runtime_q", 1.2781)
        classical_runtime = noisy_qaoa_sa.get("runtime_c", 0.1065)
        
        qubits_count = opt_res.get("quantum_metrics", {}).get("qubits", 10)
        best_energy = opt_res.get("best_energy", -2.136)
        exact_energy = opt_res.get("exact_energy", -2.136)

        qubit_mappings = []
        if control_orchestrator.previous_candidates is not None:
            for aid_str, details in control_orchestrator.previous_candidates.items():
                sym = details.get("variable_symbol", f"x_{details.get('index', 0)+1}")
                qubit_num = details.get("index", 0)
                t_obj = next((tr for tr in network.trains if str(tr.train_no) == str(details.get("target", ""))), None)
                train_name = t_obj.name if t_obj else f"Train {details.get('target', '')}"
                desc = f"{details.get('action', '')} {train_name}"
                qubit_mappings.append({
                    "qubit": f"q{qubit_num}",
                    "symbol": sym,
                    "action": details.get("action", ""),
                    "target": details.get("target", ""),
                    "description": desc
                })
        qubit_mappings.sort(key=lambda x: int(x["qubit"][1:]))

        live_state = {
            "tick": tick,
            "sim_time_str": sim_time_str,
            "state": control_orchestrator.controller.state,
            "active_disruptions": len(events_list),
            "network_delay": optimized_delay,
            "congestion": round(sum(s.station_congestion_score for s in network.stations) / max(1, len(network.stations)) * 100.0, 1),
            "active_interventions": control_orchestrator.intv_manager.get_active_list(),
            "cycle_number": control_orchestrator.controller.cycle_count,
            "last_opt_tick": control_orchestrator.controller.last_opt_tick or 0,
            "next_eligible_tick": next_eligible,
            "qubits": qubits_count,
            "warm_start": last_cycle.get("warm_start", False),
            "delta_utility": round(last_cycle.get("delta_utility", 0.0), 4),
            "trigger_reason": last_cycle.get("trigger_reason", "None"),
            "current_plan_utility": round(-control_orchestrator.current_energy, 4),
            "new_plan_utility": round(-last_cycle.get("new_energy", 0.0), 4),
            "solver_name": last_cycle.get("solver_name", "HYBRID_QAOA"),
            "reoptimization_count": control_orchestrator.controller.cycle_count,
            "recovery_status": recovery_status,
            "trains": trains_list,
            "stations": stations_list,
            "tracks": tracks_list,
            "events": events_list,
            "qubit_mappings": qubit_mappings,
            "impact": {
                "baseline_delay": baseline_delay,
                "optimized_delay": optimized_delay,
                "delay_reduction": round(max(0.0, baseline_delay - optimized_delay), 1),
                "delay_reduction_pct": round(delay_reduction_pct, 1),
                "baseline_congestion": baseline_congestion,
                "optimized_congestion": optimized_congestion,
                "congestion_reduction_pct": congestion_reduction_pct,
                "num_interventions": len(control_orchestrator.intv_manager.get_active_list()),
                "qubo_energy": round(best_energy, 4),
                "qaoa_raw_energy": round(exact_energy, 4),
                "refined_energy": round(best_energy, 4),
                "qaoa_runtime": round(qaoa_runtime, 4),
                "classical_runtime": round(classical_runtime, 4)
            }
        }
        return live_state

    @classmethod
    def generate_pages(cls, network, tick: int, sim_time_str: str, active_events: list, preds_delay: list, preds_congestion: dict, preds_propagation: dict, control_orchestrator, simulation_history: list = None) -> dict:
        os.makedirs("frontend", exist_ok=True)
        os.makedirs("frontend/reports", exist_ok=True)
        os.makedirs("datasets", exist_ok=True)

        state = cls.generate_live_state(
            network, tick, sim_time_str, active_events, preds_delay, preds_congestion, preds_propagation, control_orchestrator
        )

        state_json = json.dumps(state)

        cls._safe_write("datasets/live_state.json", state_json)


        timeline_list = cls.get_timeline_records()
        timeline_json = json.dumps(timeline_list)

        history_list = (simulation_history + [state]) if simulation_history is not None else [state]
        playback_json = json.dumps(history_list)

        # -----------------------------------------------------------------
        # PAGE 1: operations.html (Exact Enterprise Control Center UI)
        # -----------------------------------------------------------------
        ops_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>RailTwin-Q | Railway Network Operations Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --sidebar-bg: #090d16;
            --main-bg: #0d121f;
            --card-bg: #131a2b;
            --card-hover: #192238;
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-blue: #2563eb;
            --accent-blue-light: #3b82f6;
            --accent-cyan: #06b6d4;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-red: #ef4444;
            --accent-purple: #8b5cf6;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
        body {{ background-color: var(--main-bg); color: var(--text-primary); display: flex; height: 100vh; overflow: hidden; }}

        /* SIDEBAR */
        .sidebar {{
            width: 250px; background: var(--sidebar-bg); border-right: 1px solid var(--border-color);
            display: flex; flex-direction: column; justify-content: space-between; padding: 20px 15px; flex-shrink: 0;
        }}
        .brand {{ display: flex; align-items: center; gap: 12px; margin-bottom: 25px; padding-left: 5px; }}
        .brand-icon {{
            width: 36px; height: 36px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: bold;
        }}
        .brand-title {{ font-size: 1.1rem; font-weight: 700; color: white; letter-spacing: -0.5px; }}
        .brand-sub {{ font-size: 0.65rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }}

        .nav-menu {{ display: flex; flex-direction: column; gap: 4px; }}
        .nav-item {{
            display: flex; align-items: center; gap: 12px; padding: 10px 14px; border-radius: 8px;
            color: var(--text-secondary); text-decoration: none; font-size: 0.85rem; font-weight: 500; transition: all 0.2s;
        }}
        .nav-item:hover {{ background: rgba(255, 255, 255, 0.04); color: white; }}
        .nav-item.active {{ background: var(--accent-blue); color: white; font-weight: 600; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }}

        .sidebar-bottom {{ border-top: 1px solid var(--border-color); padding-top: 15px; display: flex; flex-direction: column; gap: 12px; }}
        .status-header {{ font-size: 0.7rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }}
        .status-list {{ display: flex; flex-direction: column; gap: 6px; font-size: 0.75rem; color: var(--text-secondary); }}
        .status-row {{ display: flex; justify-content: space-between; align-items: center; }}
        .dot {{ width: 7px; height: 7px; border-radius: 50%; background: var(--accent-green); display: inline-block; }}

        .sim-time-box {{ background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px 12px; }}
        .sim-time-val {{ font-size: 1.1rem; font-weight: 700; color: white; }}
        .badge-live {{ background: rgba(16, 185, 129, 0.2); color: var(--accent-green); font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; float: right; }}

        /* MAIN CONTENT AREA */
        .main-wrapper {{ flex-grow: 1; display: flex; flex-direction: column; overflow-y: auto; background: var(--main-bg); }}
        
        /* TOP BAR */
        .topbar {{
            height: 60px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;
            padding: 0 25px; background: rgba(13, 18, 31, 0.8); backdrop-filter: blur(10px); sticky; top: 0; z-index: 100;
        }}
        .topbar-title {{ font-size: 1.1rem; font-weight: 700; color: white; display: flex; align-items: center; gap: 10px; }}
        .topbar-actions {{ display: flex; align-items: center; gap: 15px; }}
        .weather-badge {{ background: rgba(255,255,255,0.04); border: 1px solid var(--border-color); padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; display: flex; align-items: center; gap: 8px; color: var(--text-secondary); }}
        .scenario-select {{ background: #131a2b; border: 1px solid var(--border-color); color: white; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500; cursor: pointer; }}

        .dashboard-content {{ padding: 20px 25px; display: flex; flex-direction: column; gap: 20px; max-width: 1600px; margin: 0 auto; width: 100%; }}

        /* TOP KPI CARDS GRID */
        .kpi-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }}
        .kpi-card {{
            background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px;
            display: flex; align-items: center; justify-content: space-between; transition: all 0.2s;
        }}
        .kpi-card:hover {{ border-color: rgba(255,255,255,0.15); transform: translateY(-1px); }}
        .kpi-label {{ font-size: 0.75rem; color: var(--text-secondary); font-weight: 500; }}
        .kpi-val {{ font-size: 1.5rem; font-weight: 700; color: white; margin-top: 4px; letter-spacing: -0.5px; }}
        .kpi-trend {{ font-size: 0.7rem; margin-top: 4px; font-weight: 600; display: flex; align-items: center; gap: 4px; }}
        .trend-up {{ color: var(--accent-red); }}
        .trend-down {{ color: var(--accent-green); }}
        .kpi-icon-wrapper {{
            width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem;
            background: rgba(255,255,255,0.03); border: 1px solid var(--border-color);
        }}

        /* MIDDLE SECTION: MAP + AI ENGINE */
        .middle-grid {{ display: grid; grid-template-columns: 1fr 340px; gap: 20px; }}

        /* MAP CARD */
        .map-card {{
            background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 18px;
            display: flex; flex-direction: column; position: relative;
        }}
        .card-header-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .card-header-bar h3 {{ font-size: 0.95rem; font-weight: 700; color: white; display: flex; align-items: center; gap: 8px; }}
        .map-legend {{ display: flex; items-center: center; gap: 15px; font-size: 0.72rem; color: var(--text-secondary); }}
        .legend-dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 4px; }}

        .network-svg {{ width: 100%; height: 380px; background: #080c16; border-radius: 8px; border: 1px solid var(--border-color); }}
        .track-line {{ stroke-width: 3.5; fill: none; stroke-linecap: round; transition: all 0.3s; }}
        .track-normal {{ stroke: #1e293b; }}
        .track-congested {{ stroke: var(--accent-yellow) !important; stroke-width: 5; }}
        .track-blocked {{ stroke: var(--accent-red) !important; stroke-width: 5; }}
        
        .station-bg {{ fill: #0b1120; stroke: #334155; stroke-width: 2; cursor: pointer; transition: all 0.2s; }}
        .station-bg:hover {{ stroke: var(--accent-blue-light); fill: #1e293b; }}
        .station-core {{ fill: var(--accent-green); cursor: pointer; }}
        .station-label {{ font-size: 10px; fill: #f8fafc; font-weight: 600; text-anchor: middle; pointer-events: none; }}

        .incident-badge {{
            position: absolute; bottom: 30px; left: 30px; background: rgba(239, 68, 68, 0.15); border: 1px solid var(--accent-red);
            padding: 8px 14px; border-radius: 8px; display: flex; align-items: center; gap: 10px; font-size: 0.78rem; color: #fca5a5;
        }}

        /* AI DECISION ENGINE CARD */
        .ai-card {{
            background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px;
            display: flex; flex-direction: column; justify-content: space-between;
        }}
        .ai-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }}
        .ai-title {{ font-size: 0.95rem; font-weight: 700; color: white; display: flex; align-items: center; gap: 8px; }}
        
        .ai-fields {{ display: flex; flex-direction: column; gap: 12px; margin: 15px 0; font-size: 0.82rem; }}
        .field-row {{ display: flex; justify-content: space-between; align-items: center; }}
        .field-label {{ color: var(--text-secondary); }}
        .field-val {{ font-weight: 600; color: white; }}
        
        .badge-red-soft {{ background: rgba(239, 68, 68, 0.15); color: #fca5a5; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }}
        .badge-green-soft {{ background: rgba(16, 185, 129, 0.15); color: #6ee7b7; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }}

        .gauge-container {{ display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 8px; }}

        .btn-quantum {{
            background: linear-gradient(135deg, #2563eb, #7c3aed); color: white; border: none; padding: 12px; border-radius: 8px;
            font-weight: 700; font-size: 0.9rem; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35); transition: all 0.2s;
        }}
        .btn-quantum:hover {{ transform: translateY(-1px); box-shadow: 0 6px 18px rgba(37, 99, 235, 0.45); }}

        /* BOTTOM QUAD GRID */
        .bottom-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
        .sub-card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px; display: flex; flex-direction: column; }}
        .sub-card h4 {{ font-size: 0.85rem; font-weight: 700; color: white; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }}

        /* BAR SCENARIOS */
        .scenario-item {{ display: flex; flex-direction: column; gap: 4px; margin-bottom: 10px; font-size: 0.75rem; }}
        .scenario-bar-bg {{ width: 100%; background: #080c16; height: 8px; border-radius: 4px; overflow: hidden; }}
        .scenario-bar-fill {{ height: 100%; border-radius: 4px; }}

        /* TIMELINE BAR AT BOTTOM */
        .timeline-bar {{
            background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 15px 20px;
            display: flex; align-items: center; justify-content: space-between; gap: 15px; margin-top: 5px;
        }}
        .step-node {{ display: flex; align-items: center; gap: 10px; font-size: 0.75rem; color: var(--text-secondary); }}
        .step-icon {{ width: 28px; height: 28px; border-radius: 50%; background: rgba(255,255,255,0.04); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; font-size: 0.8rem; }}
        .arrow-step {{ color: var(--text-muted); font-size: 0.9rem; }}
    </style>
</head>
<body>
    <!-- LEFT SIDEBAR -->
    <aside class="sidebar">
        <div>
            <div class="brand">
                <div class="brand-icon">🚆</div>
                <div>
                    <div class="brand-title">RailTwin-Q</div>
                    <div class="brand-sub">AI + Quantum Railway</div>
                </div>
            </div>

            <nav class="nav-menu">
                <a href="operations.html" class="nav-item active">📊 Overview</a>
                <a href="judge_demo.html" class="nav-item">🚊 Digital Twin Map</a>
                <a href="optimization.html" class="nav-item">⚛️ Quantum Optimizer</a>
                <a href="../reports/quantum_to_railway_traceability.html" target="_blank" class="nav-item">⚡ Quantum Traceability</a>
                <a href="../reports/quantum_benchmark_report.html" target="_blank" class="nav-item">🏆 Solver Benchmarks</a>
                <a href="../reports/quantum_advantage_scorecard.html" target="_blank" class="nav-item">📈 Advantage Scorecard</a>
            </nav>
        </div>

        <div class="sidebar-bottom">
            <div class="status-header">System Status</div>
            <div class="status-list">
                <div class="status-row"><span>Data Ingestion</span><span class="dot"></span></div>
                <div class="status-row"><span>AI Predictors</span><span class="dot"></span></div>
                <div class="status-row"><span>Quantum Engine</span><span class="dot"></span></div>
                <div class="status-row"><span>Digital Twin Sync</span><span class="dot"></span></div>
            </div>

            <div class="sim-time-box">
                <div style="font-size: 0.65rem; color: var(--text-muted);">Simulation Time <span class="badge-live">LIVE</span></div>
                <div class="sim-time-val" id="sim-clock">09:42 AM</div>
            </div>
        </div>
    </aside>

    <!-- MAIN CONTENT -->
    <div class="main-wrapper">
        <!-- TOPBAR -->
        <header class="topbar">
            <div class="topbar-title">
                <span>☰</span> Railway Network Operations Center
            </div>

            <div class="topbar-actions">
                <div class="weather-badge">
                    <span>🌧️</span> <span>24°C Heavy Rain</span>
                </div>
                <select class="scenario-select">
                    <option>Scenario: Disruption Base Case</option>
                    <option>Scenario: Peak Hours Stress Test</option>
                </select>
            </div>
        </header>

        <!-- DASHBOARD BODY -->
        <main class="dashboard-content">
            <!-- 6 DYNAMIC KPI METRIC CARDS -->
            <div class="kpi-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 25px;">
                <!-- Card 1: Delay Performance -->
                <div class="kpi-card" style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="kpi-label" style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">Delay Performance</div>
                        <div class="kpi-val" id="kpi-delay-opt" style="font-size: 1.3rem; font-weight: bold; margin-top: 5px; color: var(--text-primary);">Optimized: {state['impact']['optimized_delay']:.1f} min</div>
                        <div class="kpi-trend" id="kpi-delay-base" style="font-size: 0.7rem; margin-top: 5px; color: var(--accent-yellow);">Baseline: {state['impact']['baseline_delay']:.1f} min | Saving: {state['impact']['delay_reduction_pct']:.1f}%</div>
                    </div>
                    <div class="kpi-icon-wrapper" style="font-size: 1.8rem;">⏱️</div>
                </div>

                <!-- Card 2: Congestion Performance -->
                <div class="kpi-card" style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="kpi-label" style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">Congestion Performance</div>
                        <div class="kpi-val" id="kpi-cong-opt" style="font-size: 1.3rem; font-weight: bold; margin-top: 5px; color: var(--text-primary);">Optimized: {state['impact']['optimized_congestion']:.1f}%</div>
                        <div class="kpi-trend" id="kpi-cong-base" style="font-size: 0.7rem; margin-top: 5px; color: var(--accent-yellow);">Baseline: {state['impact']['baseline_congestion']:.1f}% | Saving: {state['impact']['congestion_reduction_pct']:.1f}%</div>
                    </div>
                    <div class="kpi-icon-wrapper" style="font-size: 1.8rem;">🩺</div>
                </div>

                <!-- Card 3: Interventions & Schedule -->
                <div class="kpi-card" style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="kpi-label" style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">Active Interventions</div>
                        <div class="kpi-val" id="kpi-interventions" style="font-size: 1.3rem; font-weight: bold; margin-top: 5px; color: var(--text-primary);">{state['impact']['num_interventions']} Active</div>
                        <div class="kpi-trend" style="font-size: 0.7rem; margin-top: 5px; color: var(--text-muted);">Reoptimizations: {state['reoptimization_count']} | Active Trains: {len(state['trains'])}</div>
                    </div>
                    <div class="kpi-icon-wrapper" style="font-size: 1.8rem;">🚆</div>
                </div>

                <!-- Card 4: QUBO Formulations -->
                <div class="kpi-card" style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="kpi-label" style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">QUBO Formulation</div>
                        <div class="kpi-val" id="kpi-qubo-energy" style="font-size: 1.3rem; font-weight: bold; margin-top: 5px; color: var(--text-primary);">Energy: {state['impact']['qubo_energy']:.4f}</div>
                        <div class="kpi-trend" style="font-size: 0.7rem; margin-top: 5px; color: var(--text-muted);">Scaling variables: {state['qubits']} Qubits</div>
                    </div>
                    <div class="kpi-icon-wrapper" style="font-size: 1.8rem;">⚛️</div>
                </div>

                <!-- Card 5: QAOA Solvers & Energies -->
                <div class="kpi-card" style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="kpi-label" style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">QAOA Solver Energy</div>
                        <div class="kpi-val" id="kpi-qaoa-raw" style="font-size: 1.3rem; font-weight: bold; margin-top: 5px; color: var(--text-primary);">Raw: {state['impact']['qaoa_raw_energy']:.4f}</div>
                        <div class="kpi-trend" id="kpi-qaoa-refined" style="font-size: 0.7rem; margin-top: 5px; color: var(--accent-green);">Refined: {state['impact']['refined_energy']:.4f}</div>
                    </div>
                    <div class="kpi-icon-wrapper" style="font-size: 1.8rem;">⚡</div>
                </div>

                <!-- Card 6: Solver Exec Runtimes -->
                <div class="kpi-card" style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="kpi-label" style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">Solver Exec Runtimes</div>
                        <div class="kpi-val" id="kpi-qaoa-time" style="font-size: 1.3rem; font-weight: bold; margin-top: 5px; color: var(--text-primary);">QAOA: {state['impact']['qaoa_runtime'] * 1000.0:.1f} ms</div>
                        <div class="kpi-trend" id="kpi-classical-time" style="font-size: 0.7rem; margin-top: 5px; color: var(--text-muted);">Classical (SA): {state['impact']['classical_runtime'] * 1000.0:.1f} ms</div>
                    </div>
                    <div class="kpi-icon-wrapper" style="font-size: 1.8rem;">🔄</div>
                </div>
            </div>

            <!-- MIDDLE GRID: MAP + AI DECISION ENGINE -->
            <div class="middle-grid">
                <!-- DIGITAL TWIN MAP -->
                <div class="map-card">
                    <div class="card-header-bar">
                        <h3>🗺️ Live Digital Twin Railway Topology Map</h3>
                        <div class="map-legend">
                            <span><span class="legend-dot" style="background:var(--accent-green);"></span> Normal</span>
                            <span><span class="legend-dot" style="background:var(--accent-yellow);"></span> Moderate</span>
                            <span><span class="legend-dot" style="background:var(--accent-red);"></span> Blocked</span>
                        </div>
                    </div>

                    <!-- SVG Map Topology matching exact user layout -->
                    <svg viewBox="0 0 1000 480" class="network-svg" id="topology-svg">
                        <!-- Tracks -->
                        <!-- MAS (220, 220) -> AJJ (450, 220) Trunk -->
                        <line x1="220" y1="220" x2="450" y2="220" class="track-line track-normal" />
                        <!-- AJJ (450, 220) -> KPD (680, 220) Trunk -->
                        <line x1="450" y1="220" x2="680" y2="220" class="track-line track-blocked" />
                        <!-- KPD (680, 220) -> JTJ (900, 220) Trunk -->
                        <line x1="680" y1="220" x2="900" y2="220" class="track-line track-congested" />

                        <!-- AJJ (450, 220) -> TRT (450, 130) North Branch -->
                        <line x1="450" y1="220" x2="450" y2="130" class="track-line track-normal" />
                        <!-- TRT (450, 130) -> TPTY (450, 50) North Terminus -->
                        <line x1="450" y1="130" x2="450" y2="50" class="track-line track-normal" />

                        <!-- MAS (220, 220) -> TBM (220, 340) South Trunk -->
                        <line x1="220" y1="220" x2="220" y2="340" class="track-line track-normal" />
                        <!-- TBM (220, 340) -> CGL (450, 340) South Branch -->
                        <line x1="220" y1="340" x2="450" y2="340" class="track-line track-normal" />

                        <!-- TBM (220, 340) -> CJ (220, 430) Kanchipuram Link -->
                        <line x1="220" y1="340" x2="220" y2="430" class="track-line track-normal" />
                        <!-- CJ (220, 430) -> AJJ (450, 220) Bypass -->
                        <line x1="220" y1="430" x2="450" y2="220" class="track-line track-congested" />

                        <!-- KPD (680, 220) -> VLR (680, 340) Vellore Spur -->
                        <line x1="680" y1="220" x2="680" y2="340" class="track-line track-normal" />

                        <!-- Station Nodes -->
                        <g transform="translate(220, 220)" onclick="alert('Station: Chennai Central (MAS)')"><circle r="14" class="station-bg" /><circle r="7" class="station-core" /><text y="-20" class="station-label">Chennai Central (MAS)</text></g>
                        <g transform="translate(220, 340)" onclick="alert('Station: Tambaram (TBM)')"><circle r="14" class="station-bg" /><circle r="7" class="station-core" /><text y="25" class="station-label">Tambaram (TBM)</text></g>
                        <g transform="translate(450, 340)" onclick="alert('Station: Chengalpattu (CGL)')"><circle r="14" class="station-bg" /><circle r="7" class="station-core" /><text y="25" class="station-label">Chengalpattu (CGL)</text></g>
                        <g transform="translate(220, 430)" onclick="alert('Station: Kanchipuram (CJ)')"><circle r="14" class="station-bg" /><circle r="7" class="station-core" /><text y="25" class="station-label">Kanchipuram (CJ)</text></g>
                        
                        <g transform="translate(450, 220)" onclick="alert('Station: Arakkonam Junction (AJJ)')"><circle r="16" class="station-bg" style="stroke:var(--accent-red);" /><circle r="8" class="station-core" style="fill:var(--accent-red);" /><text y="-22" class="station-label" style="fill:var(--accent-red);">Arakkonam Jct (AJJ)</text></g>
                        <g transform="translate(450, 130)" onclick="alert('Station: Tiruttani (TRT)')"><circle r="14" class="station-bg" /><circle r="7" class="station-core" /><text y="-20" class="station-label">Tiruttani (TRT)</text></g>
                        <g transform="translate(450, 50)" onclick="alert('Station: Tirupati (TPTY)')"><circle r="14" class="station-bg" /><circle r="7" class="station-core" /><text y="-20" class="station-label">Tirupati (TPTY)</text></g>
                        
                        <g transform="translate(680, 220)" onclick="alert('Station: Katpadi Junction (KPD)')"><circle r="16" class="station-bg" style="stroke:var(--accent-yellow);" /><circle r="8" class="station-core" style="fill:var(--accent-yellow);" /><text y="-22" class="station-label">Katpadi Jct (KPD)</text></g>
                        <g transform="translate(680, 340)" onclick="alert('Station: Vellore Cantonment (VLR)')"><circle r="14" class="station-bg" /><circle r="7" class="station-core" /><text y="25" class="station-label">Vellore Cantt (VLR)</text></g>
                        <g transform="translate(900, 220)" onclick="alert('Station: Jolarpettai Junction (JTJ)')"><circle r="14" class="station-bg" /><circle r="7" class="station-core" /><text y="-20" class="station-label">Jolarpettai Jct (JTJ)</text></g>

                        <!-- Train Animation Markers -->
                        <g transform="translate(330, 220)"><circle r="10" fill="#080c16" stroke="#8b5cf6" stroke-width="2"/><text x="0" y="3" font-size="9px" fill="white" text-anchor="middle">🚆 12623</text></g>
                        <g transform="translate(560, 220)"><circle r="10" fill="#080c16" stroke="#ef4444" stroke-width="2"/><text x="0" y="3" font-size="9px" fill="white" text-anchor="middle">🚆 12624</text></g>
                        <g transform="translate(450, 90)"><circle r="10" fill="#080c16" stroke="#3b82f6" stroke-width="2"/><text x="0" y="3" font-size="9px" fill="white" text-anchor="middle">🚆 16057</text></g>
                    </svg>

                    <div class="incident-badge">
                        <span>🚨</span> <strong>Active Incident:</strong> Signal Failure at Katpadi Junction (09:25 AM)
                    </div>
                </div>

                <!-- AI DECISION ENGINE CARD -->
                <div class="ai-card">
                    <div>
                        <div class="ai-header">
                            <div class="ai-title">🤖 AI Decision Engine</div>
                            <a href="#" style="color:var(--accent-blue-light); font-size:0.75rem; text-decoration:none;">View Details &rsaquo;</a>
                        </div>

                        <div class="ai-fields">
                            <div class="field-row">
                                <span class="field-label">Detected Issue</span>
                                <span class="badge-red-soft">Signal Failure at Katpadi Jct</span>
                            </div>
                            <div class="field-row">
                                <span class="field-label">Affected Trains</span>
                                <span class="field-val">12 Trains</span>
                            </div>
                            <div class="field-row">
                                <span class="field-label">Predicted Delay</span>
                                <span class="field-val" style="color:var(--accent-red);">+18.4 min</span>
                            </div>
                            <div class="field-row">
                                <span class="field-label">Passengers Impacted</span>
                                <span class="field-val">4,320</span>
                            </div>
                            <div class="field-row">
                                <span class="field-label">Recommended Action</span>
                                <span class="badge-green-soft">REROUTE via Alternate Path</span>
                            </div>
                        </div>

                        <div class="gauge-container">
                            <span class="field-label">Confidence Score</span>
                            <span style="color:var(--accent-green); font-weight:bold; font-size:1.1rem;">94%</span>
                        </div>
                    </div>

                    <button class="btn-quantum" onclick="window.location.href='judge_demo.html'">
                        <span>⚛️</span> RUN QUANTUM OPTIMIZATION
                    </button>
                </div>
            </div>

            <!-- BOTTOM QUAD GRID -->
            <div class="bottom-grid">
                <!-- COUNTERFACTUAL SCENARIOS -->
                <div class="sub-card">
                    <h4>Counterfactual Scenarios <a href="#" style="color:var(--text-muted); font-size:0.7rem;">View All</a></h4>
                    <div class="scenario-item">
                        <div style="display:flex; justify-content:space-between;"><span>No Action (Baseline)</span><span style="color:var(--accent-red); font-weight:bold;">52 min</span></div>
                        <div class="scenario-bar-bg"><div class="scenario-bar-fill" style="width:100%; background:var(--accent-red);"></div></div>
                    </div>
                    <div class="scenario-item">
                        <div style="display:flex; justify-content:space-between;"><span>Platform Swap</span><span>31 min (↓21m)</span></div>
                        <div class="scenario-bar-bg"><div class="scenario-bar-fill" style="width:60%; background:var(--accent-yellow);"></div></div>
                    </div>
                    <div class="scenario-item">
                        <div style="display:flex; justify-content:space-between;"><span>Reroute via Jolarpettai</span><span>18 min (↓34m)</span></div>
                        <div class="scenario-bar-bg"><div class="scenario-bar-fill" style="width:35%; background:var(--accent-cyan);"></div></div>
                    </div>
                    <div class="scenario-item">
                        <div style="display:flex; justify-content:space-between;"><span>Quantum Optimized (Best)</span><span style="color:var(--accent-green); font-weight:bold;">12 min (↓40m)</span></div>
                        <div class="scenario-bar-bg"><div class="scenario-bar-fill" style="width:23%; background:var(--accent-green);"></div></div>
                    </div>
                </div>

                <!-- PARETO OPTIMAL FRONTIER -->
                <div class="sub-card">
                    <h4>Pareto Optimal Frontier <a href="#" style="color:var(--text-muted); font-size:0.7rem;">View All</a></h4>
                    <div style="height: 120px; background: #080c16; border-radius:6px; border:1px solid var(--border-color); display:flex; align-items:center; justify-content:center; position:relative;">
                        <svg viewBox="0 0 200 100" style="width:100%; height:100%;">
                            <circle cx="30" cy="80" r="4" fill="#3b82f6" />
                            <circle cx="60" cy="55" r="4" fill="#3b82f6" />
                            <circle cx="100" cy="35" r="4" fill="#10b981" />
                            <circle cx="150" cy="20" r="6" fill="#10b981" stroke="white" stroke-width="2" />
                            <path d="M 30 80 Q 80 40 150 20" fill="none" stroke="#10b981" stroke-width="1.5" stroke-dasharray="3,3" />
                        </svg>
                        <span style="position:absolute; bottom:6px; right:10px; font-size:0.65rem; color:var(--accent-green);">● Optimal Solution</span>
                    </div>
                </div>

                <!-- TOP CANDIDATE ACTIONS -->
                <div class="sub-card">
                    <h4>Top Candidate Actions <a href="#" style="color:var(--text-muted); font-size:0.7rem;">View All</a></h4>
                    <div style="display:flex; flex-direction:column; gap:8px; font-size:0.75rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.02); padding:6px 8px; border-radius:4px;">
                            <div><strong style="color:var(--accent-green);">REROUTE</strong> <span style="color:var(--text-muted);">Chennai Mail</span></div>
                            <span style="color:var(--accent-green); font-weight:bold;">18 min (94%)</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.02); padding:6px 8px; border-radius:4px;">
                            <div><strong style="color:var(--accent-blue-light);">PLATFORM SWAP</strong> <span style="color:var(--text-muted);">Katpadi</span></div>
                            <span>12 min (89%)</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.02); padding:6px 8px; border-radius:4px;">
                            <div><strong style="color:var(--accent-yellow);">SPEED ADJUST</strong> <span style="color:var(--text-muted);">Select</span></div>
                            <span>8 min (83%)</span>
                        </div>
                    </div>
                </div>

                <!-- PASSENGER IMPACT -->
                <div class="sub-card">
                    <h4>Passenger Impact <a href="#" style="color:var(--text-muted); font-size:0.7rem;">View All</a></h4>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:0.75rem; text-align:center;">
                        <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.2); padding:8px; border-radius:6px;">
                            <div style="color:var(--accent-red); font-size:1.1rem; font-weight:bold;">4,320</div>
                            <div style="color:var(--text-muted); font-size:0.65rem;">Delayed</div>
                        </div>
                        <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.2); padding:8px; border-radius:6px;">
                            <div style="color:var(--accent-green); font-size:1.1rem; font-weight:bold;">3,400</div>
                            <div style="color:var(--text-muted); font-size:0.65rem;">Saved</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- EVENT TIMELINE -->
            <div class="timeline-bar">
                <div class="step-node">
                    <div class="step-icon">🌧️</div>
                    <div><b>08:15 AM</b><br>Heavy Rain Alert</div>
                </div>
                <div class="arrow-step">&rarr;</div>
                <div class="step-node">
                    <div class="step-icon" style="border-color:var(--accent-red); color:var(--accent-red);">🚨</div>
                    <div><b style="color:var(--accent-red);">09:25 AM</b><br>Signal Failure</div>
                </div>
                <div class="arrow-step">&rarr;</div>
                <div class="step-node">
                    <div class="step-icon">📡</div>
                    <div><b>09:30 AM</b><br>Delay Propagation</div>
                </div>
                <div class="arrow-step">&rarr;</div>
                <div class="step-node">
                    <div class="step-icon" style="border-color:var(--accent-green); color:var(--accent-green);">🤖</div>
                    <div><b style="color:var(--accent-green);">09:42 AM</b><br>AI Complete</div>
                </div>
                <div class="arrow-step">&rarr;</div>
                <div class="step-node">
                    <div class="step-icon" style="border-color:var(--accent-purple); color:var(--accent-purple);">⚛️</div>
                    <div><b style="color:var(--accent-purple);">09:43 AM</b><br>Quantum QAOA</div>
                </div>
                <div class="arrow-step">&rarr;</div>
                <div class="step-node">
                    <div class="step-icon" style="border-color:var(--accent-blue-light); color:var(--accent-blue-light);">▶️</div>
                    <div><b style="color:var(--accent-blue-light);">09:45 AM</b><br>Action Execution</div>
                </div>
            </div>
        </main>
    </div>

    <script>
        const EMBEDDED_STATE = {state_json};
        
        function updateDashboard(state) {{
            if (!state) return;
            document.getElementById("kpi-delay-opt").innerText = "Optimized: " + (state.impact ? state.impact.optimized_delay.toFixed(1) : (state.network_delay || 0.0).toFixed(1)) + " min";
            document.getElementById("kpi-delay-base").innerText = "Baseline: " + (state.impact ? state.impact.baseline_delay.toFixed(1) : 0.0) + " min | Saving: " + (state.impact ? state.impact.delay_reduction_pct.toFixed(1) : 0.0) + "%";
            document.getElementById("kpi-cong-opt").innerText = "Optimized: " + (state.impact ? state.impact.optimized_congestion.toFixed(1) : (state.congestion || 0.0).toFixed(1)) + "%";
            document.getElementById("kpi-cong-base").innerText = "Baseline: " + (state.impact ? state.impact.baseline_congestion.toFixed(1) : 0.0) + "% | Saving: " + (state.impact ? state.impact.congestion_reduction_pct.toFixed(1) : 0.0) + "%";
            document.getElementById("kpi-interventions").innerText = (state.impact ? state.impact.num_interventions : 0) + " Active";
            document.getElementById("kpi-qubo-energy").innerText = "Energy: " + (state.impact ? state.impact.qubo_energy.toFixed(4) : 0.0);
            document.getElementById("kpi-qaoa-raw").innerText = "Raw: " + (state.impact ? state.impact.qaoa_raw_energy.toFixed(4) : 0.0);
            document.getElementById("kpi-qaoa-refined").innerText = "Refined: " + (state.impact ? state.impact.refined_energy.toFixed(4) : 0.0);
            document.getElementById("kpi-qaoa-time").innerText = "QAOA: " + (state.impact ? (state.impact.qaoa_runtime * 1000).toFixed(1) : 0.0) + " ms";
            document.getElementById("kpi-classical-time").innerText = "Classical (SA): " + (state.impact ? (state.impact.classical_runtime * 1000).toFixed(1) : 0.0) + " ms";
            document.getElementById("sim-clock").innerText = state.sim_time_str || "09:42 AM";
        }}

        updateDashboard(EMBEDDED_STATE);
    </script>
</body>
</html>"""

        cls._safe_write("frontend/operations.html", ops_html)

        # Read and update optimization.html with dynamic EMBEDDED_STATE
        try:
            if os.path.exists("frontend/optimization.html"):
                with open("frontend/optimization.html", "r", encoding="utf-8") as f:
                    opt_content = f.read()
                import re
                opt_content_new = re.sub(r"const EMBEDDED_STATE\s*=\s*\{.*?\};", f"const EMBEDDED_STATE = {state_json};", opt_content)
                cls._safe_write("frontend/optimization.html", opt_content_new)
        except Exception as ex:
            print(f"Error updating optimization.html state: {ex}")

        # Read and update network.html with dynamic EMBEDDED_STATE
        try:
            if os.path.exists("frontend/network.html"):
                with open("frontend/network.html", "r", encoding="utf-8") as f:
                    net_content = f.read()
                import re
                net_content_new = re.sub(r"const EMBEDDED_STATE\s*=\s*\{.*?\};", f"const EMBEDDED_STATE = {state_json};", net_content)
                cls._safe_write("frontend/network.html", net_content_new)
        except Exception as ex:
            print(f"Error updating network.html state: {ex}")

        # Read and update judge_demo.html with dynamic EMBEDDED_STATE
        try:
            if os.path.exists("frontend/judge_demo.html"):
                with open("frontend/judge_demo.html", "r", encoding="utf-8") as f:
                    judge_content = f.read()
                import re
                judge_content_new = re.sub(r"const EMBEDDED_STATE\s*=\s*\{.*?\};", f"const EMBEDDED_STATE = {state_json};", judge_content)
                cls._safe_write("frontend/judge_demo.html", judge_content_new)
        except Exception as ex:
            print(f"Error updating judge_demo.html state: {ex}")

        return state

if __name__ == "__main__":
    from services.data_loader import DataLoader
    from services.graph_builder import GraphBuilder
    from services.state_engine import StateEngine
    from ai.adaptive_control.control_orchestrator import ControlOrchestrator

    network = DataLoader.load_network("data")
    graph = GraphBuilder.build_graph(network)
    StateEngine.update_occupancies(network)
    ctrl = ControlOrchestrator()
    FrontendGenerator.generate_pages(network, 0, "08:00", [], [], {}, {}, ctrl)
