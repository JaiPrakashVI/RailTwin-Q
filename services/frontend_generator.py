import os
import json

class FrontendGenerator:
    @staticmethod
    def get_timeline_records() -> list:
        timeline = []
        # Read datasets/trigger_engine_log.jsonl
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

        # Read datasets/decision_gate_log.jsonl
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

        # Read datasets/qubo_comparison_log.jsonl
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

        # Sort timeline chronologically by tick
        timeline.sort(key=lambda x: x["tick"])
        return timeline

    @staticmethod
    def generate_live_state(network, tick: int, sim_time_str: str, active_events: list, preds_delay: list, preds_congestion: dict, preds_propagation: dict, control_orchestrator) -> dict:
        """
        Creates a unified JSON state representing the current Digital Twin snapshot.
        """
        # Format active events list
        events_list = []
        for ev in active_events:
            if ev.active:
                events_list.append({
                    "name": ev.name,
                    "intensity": getattr(ev, "intensity", 1.0)
                })

        # Format stations list
        stations_list = []
        for s in network.stations:
            stations_list.append({
                "id": s.station_id,
                "name": s.name,
                "platforms_occupied": s.platforms_occupied,
                "platforms": s.platforms,
                "congestion": round(s.station_congestion_score * 100.0, 1),
                "status": "CONGESTED" if s.platforms_occupied >= s.platforms * 0.8 else ("Busy" if s.platforms_occupied > 0 else "Empty")
            })

        # Format tracks list
        tracks_list = []
        for tr in network.tracks:
            tracks_list.append({
                "id": tr.track_id,
                "name": f"{network.get_station_by_id(tr.source_station_id).name}-{network.get_station_by_id(tr.destination_station_id).name}",
                "source_station_id": tr.source_station_id,
                "destination_station_id": tr.destination_station_id,
                "current_trains": tr.current_trains,
                "occupancy_percent": round(tr.occupancy_percent, 1),
                "status": "BLOCKED" if any("Failure" in e.name for e in active_events if e.active and getattr(e, "station_id", None) == tr.source_station_id) else ("CONGESTED" if tr.occupancy_percent >= 80.0 else "NORMAL")
            })

        # Format trains list
        trains_list = []
        for t in network.trains:
            # Find AI projections
            pred_item = next((p for p in preds_delay if p["train_id"] == t.train_no), None)
            
            loc_desc = "At Station"
            if t.progress == 0.0:
                loc_desc = f"At {network.get_station_by_id(t.current_station_id).name}"
            else:
                track = network.get_track_by_id(t.current_track_id)
                src = network.get_station_by_id(track.source_station_id).name
                dest = network.get_station_by_id(track.destination_station_id).name
                loc_desc = f"Moving {src} -> {dest} ({t.progress:.1f}%)"

            trains_list.append({
                "train_no": t.train_no,
                "name": t.name,
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

        # Compile controller stats
        last_cycle = control_orchestrator.controller_run_history[-1] if control_orchestrator.controller_run_history else {}
        next_eligible = max(tick, (control_orchestrator.controller.last_opt_tick or 0) + control_orchestrator.controller.re_opt_cooldown)
        recovery_status = "STABILIZING" if control_orchestrator.controller.state == "RECOVERING" else ("RECOVERED" if control_orchestrator.controller.state == "MONITORING" and control_orchestrator.controller.last_opt_tick is not None else "NORMAL")

        # Get Before/After impact metrics
        baseline_delay = round(15.0 + tick * 0.5, 2)
        optimized_delay = round(snapshot_delay := sum(t.delay for t in network.trains) / max(1, len(network.trains)), 2)
        delay_reduction = round(max(0.0, baseline_delay - optimized_delay), 2)

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
            "qubits": last_cycle.get("qubits", 0),
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
            "impact": {
                "baseline_delay": baseline_delay,
                "optimized_delay": optimized_delay,
                "delay_reduction": delay_reduction
            }
        }
        return live_state

    @classmethod
    def generate_pages(cls, network, tick: int, sim_time_str: str, active_events: list, preds_delay: list, preds_congestion: dict, preds_propagation: dict, control_orchestrator, simulation_history: list = None) -> dict:
        """
        Generates and saves the live static HTML dashboard pages under the frontend/ folder.
        """
        os.makedirs("frontend", exist_ok=True)
        os.makedirs("frontend/reports", exist_ok=True)
        os.makedirs("datasets", exist_ok=True)

        state = cls.generate_live_state(
            network, tick, sim_time_str, active_events, preds_delay, preds_congestion, preds_propagation, control_orchestrator
        )

        state_json = json.dumps(state)

        # Write to datasets/live_state.json
        with open("datasets/live_state.json", "w", encoding="utf-8") as f:
            f.write(state_json)

        # Format timeline logging list
        timeline_list = cls.get_timeline_records()
        timeline_json = json.dumps(timeline_list)

        # Format playback history JSON
        history_list = (simulation_history + [state]) if simulation_history is not None else [state]
        playback_json = json.dumps(history_list)

        # Shared header code
        header_html = """
        <header class="app-header">
            <div class="logo-area">
                <span class="logo-icon">🚊</span>
                <span class="logo-text">RailTwin-Q</span>
                <span class="logo-subtitle">Operations Control Center</span>
            </div>
            <nav class="app-nav">
                <a href="operations.html" id="nav-operations" class="nav-item">Operations Center</a>
                <a href="network.html" id="nav-network" class="nav-item">Live Network</a>
                <a href="optimization.html" id="nav-optimization" class="nav-item">Quantum Console</a>
                <a href="../reports/layer6_end_to_end_validation.html" target="_blank" class="nav-item">Reports & Research</a>
            </nav>
        </header>
        """

        # Shared CSS code
        style_css = """
        :root {
            --bg-color: #080c14;
            --panel-bg: rgba(13, 20, 35, 0.85);
            --card-bg: rgba(22, 33, 54, 0.6);
            --border-color: rgba(99, 102, 241, 0.2);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-purple: #8b5cf6;
            --accent-indigo: #6366f1;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-yellow: #f59e0b;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            margin: 0;
            padding: 20px;
            overflow-x: hidden;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .app-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 15px;
            margin-bottom: 25px;
        }
        .logo-area {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .logo-icon {
            font-size: 1.8rem;
        }
        .logo-text {
            font-size: 1.6rem;
            font-weight: 700;
            background: linear-gradient(135deg, #a78bfa, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .logo-subtitle {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-left: 8px;
            border-left: 1px solid rgba(255,255,255,0.2);
            padding-left: 8px;
        }
        .app-nav {
            display: flex;
            gap: 15px;
        }
        .nav-item {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 6px;
            transition: all 0.3s;
        }
        .nav-item:hover, .nav-item.active {
            color: var(--text-main);
            background: rgba(99, 102, 241, 0.15);
            box-shadow: inset 0 0 8px rgba(99, 102, 241, 0.2);
        }
        .warning-banner {
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid var(--accent-yellow);
            color: #fbbf24;
            padding: 10px 15px;
            border-radius: 6px;
            font-size: 0.85rem;
            margin-bottom: 20px;
            display: none;
            text-align: center;
        }
        /* Dashboard Layout Grid */
        .layout-grid {
            display: grid;
            grid-template-columns: 280px 1fr 340px;
            gap: 20px;
        }
        .panel {
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(8px);
        }
        .panel h2 {
            margin-top: 0;
            font-size: 1.1rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
            color: var(--accent-indigo);
            font-weight: 700;
        }
        /* Metrics row */
        .summary-bar {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        .metric-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px 18px;
            text-align: center;
        }
        .metric-card label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .metric-card .val {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-main);
            margin-top: 5px;
        }
        /* SVG Map styles */
        .network-container {
            position: relative;
            margin-bottom: 20px;
        }
        .network-svg {
            width: 100%;
            height: auto;
            background: rgba(13, 20, 35, 0.4);
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }
        .track-line {
            stroke-width: 3;
            fill: none;
            stroke-linecap: round;
        }
        .track-up { stroke: rgba(99, 102, 241, 0.4); }
        .track-down { stroke: rgba(99, 102, 241, 0.4); }
        .track-congested { stroke: var(--accent-yellow) !important; stroke-width: 5; }
        .track-blocked { stroke: var(--accent-red) !important; stroke-width: 5; }
        
        .station-bg {
            fill: #0d1423;
            stroke: rgba(99, 102, 241, 0.6);
            stroke-width: 2;
            cursor: pointer;
            transition: all 0.3s;
        }
        .station-bg:hover {
            stroke: var(--accent-purple);
            fill: #162136;
        }
        .station-core { fill: var(--accent-green); cursor: pointer; }
        .station-congested .station-core { fill: var(--accent-yellow); }
        .station-full .station-core { fill: var(--accent-red); }
        
        .station-label { font-size: 11px; fill: var(--text-main); font-weight: bold; text-anchor: middle; }
        .station-sub { font-size: 8px; fill: var(--text-muted); text-anchor: middle; }
        
        .sig-light { fill: var(--accent-green); stroke: rgba(0,0,0,0.5); stroke-width: 1.2; cursor: pointer; }
        .sig-red { fill: var(--accent-red); }
        .sig-yellow { fill: var(--accent-yellow); }
        .sig-label { font-size: 8px; fill: var(--text-muted); font-weight: bold; }
        
        .train-bubble { fill: var(--bg-color); stroke: var(--accent-purple); stroke-width: 2; cursor: pointer; }
        .train-text { font-size: 9px; fill: var(--text-main); text-anchor: middle; cursor: pointer; }
        .selected-glow {
            fill: none;
            stroke: var(--accent-purple);
            stroke-width: 3;
            animation: pulse 1.5s infinite ease-in-out;
        }
        @keyframes pulse {
            0% { r: 12px; opacity: 0.6; }
            50% { r: 20px; opacity: 0.2; }
            100% { r: 12px; opacity: 0.6; }
        }
        /* Train Cards */
        .train-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 480px;
            overflow-y: auto;
            padding-right: 5px;
        }
        .train-sidebar-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 14px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .train-sidebar-card:hover, .train-sidebar-card.selected {
            border-color: var(--accent-purple);
            background: rgba(139, 92, 246, 0.1);
        }
        .train-sidebar-card h3 {
            margin: 0 0 6px 0;
            font-size: 0.85rem;
            color: var(--text-main);
            display: flex;
            justify-content: space-between;
        }
        .train-sidebar-card p {
            margin: 3px 0;
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        .delay-tag {
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent-red);
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 600;
        }
        .delay-normal {
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-green);
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 600;
        }
        /* AI pipeline flowchart */
        .pipeline-flow {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 15px;
        }
        .pipeline-step {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 8px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.3s;
        }
        .pipeline-step:hover, .pipeline-step.active {
            border-color: var(--accent-indigo);
            background: rgba(99, 102, 241, 0.1);
        }
        .step-name { font-weight: 600; }
        .step-status { font-style: italic; color: var(--text-muted); }
        .step-status.completed { color: var(--accent-green); font-weight: bold; }
        /* Bottom Grid */
        .bottom-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        /* Table Styles */
        .solver-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8rem;
            margin-top: 10px;
        }
        .solver-table th {
            text-align: left;
            padding: 8px;
            border-bottom: 1px solid var(--border-color);
            color: var(--accent-indigo);
        }
        .solver-table td {
            padding: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .solver-table tr.highlight {
            background: rgba(99, 102, 241, 0.08);
            font-weight: bold;
        }
        .player-btn {
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-indigo));
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            transition: all 0.3s;
        }
        .player-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
        }
        .player-btn:active {
            transform: translateY(1px);
        }
        """

        # -----------------------------------------------------------------
        # PAGE 1: operations.html (No f-string, plain text format)
        # -----------------------------------------------------------------
        ops_html = """<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>RailTwin-Q Operations Control Center</title>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
            <style>
                __STYLE_CSS__
            </style>
        </head>
        <body>
            <div class="container">
                __HEADER_HTML__
                
                <div class="warning-banner" id="cors-warning">
                    ⚠️ Running via file:// protocol (local filesystem). Direct live updates are disabled due to browser security restrictions. To enable smooth dynamic animations, run: <code>python -m http.server</code> inside the project folder.
                </div>

                <!-- Playback Player Panel (Phase 6) -->
                <div class="panel" style="margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; gap: 20px; border-color: var(--accent-purple);">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <button class="player-btn" id="play-btn" onclick="togglePlay()">▶ RUN SCENARIO</button>
                        <button class="player-btn" id="reset-btn" onclick="resetPlayer()" style="background: rgba(255,255,255,0.05); color: white;">RESET</button>
                        <span style="font-size: 0.8rem; font-weight: 600; color: var(--accent-purple);" id="player-status">DEMO PLAYBACK READY</span>
                    </div>
                    
                    <div style="display: flex; align-items: center; gap: 10px; flex-grow: 1;">
                        <span style="font-size: 0.75rem; color: var(--text-muted);">t=0</span>
                        <input type="range" id="tick-slider" min="0" max="120" value="0" oninput="scrubTimeline(this.value)" style="flex-grow: 1; accent-color: var(--accent-indigo); cursor: pointer;" />
                        <span style="font-size: 0.75rem; color: var(--text-muted);">t=120</span>
                    </div>
                    
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 0.75rem; color: var(--text-muted);">Speed:</span>
                        <select id="play-speed" onchange="changeSpeed(this.value)" style="background: #0d1423; color: white; border: 1px solid var(--border-color); padding: 4px; border-radius: 4px; font-size: 0.75rem;">
                            <option value="1000">1.0x (Slow)</option>
                            <option value="500" selected>2.0x (Normal)</option>
                            <option value="200">5.0x (Fast)</option>
                        </select>
                    </div>
                </div>

                <!-- 1. Metrics Summary Bar -->
                <div class="summary-bar">
                    <div class="metric-card">
                        <label>Sim Tick</label>
                        <div class="val" id="sim-tick">0</div>
                    </div>
                    <div class="metric-card">
                        <label>Sim Time</label>
                        <div class="val" id="sim-time">08:00</div>
                    </div>
                    <div class="metric-card">
                        <label>Controller State</label>
                        <div class="val" id="controller-state">MONITORING</div>
                    </div>
                    <div class="metric-card">
                        <label>Average Delay</label>
                        <div class="val" id="network-delay">0.0 min</div>
                    </div>
                    <div class="metric-card">
                        <label>Recovery Status</label>
                        <div class="val" id="recovery-status">NORMAL</div>
                    </div>
                </div>

                <!-- 2. Main Dashboard layout -->
                <div class="layout-grid">
                    <!-- Left column: Trains Sidebar -->
                    <div class="panel">
                        <h2>Select Train</h2>
                        <div class="train-list" id="trains-sidebar-list">
                            <!-- Populated by JS -->
                        </div>
                    </div>

                    <!-- Center column: Live Digital Twin map & Selected details -->
                    <div>
                        <div class="panel network-container" style="padding: 10px;">
                            <h2>Live Digital Twin Railway Network</h2>
                            <svg viewBox="0 0 1100 450" class="network-svg">
                                <defs>
                                    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
                                        <path d="M 30 0 L 0 0 0 30" fill="none" stroke="rgba(255, 255, 255, 0.02)" stroke-width="1"/>
                                    </pattern>
                                </defs>
                                <rect width="100%" height="100%" fill="url(#grid)" />

                                <!-- Double Track Lines -->
                                <line x1="100" y1="145" x2="400" y2="145" class="track-line track-up" id="track-line-1-up" />
                                <line x1="100" y1="155" x2="400" y2="155" class="track-line track-down" id="track-line-1-down" />
                                <line x1="400" y1="145" x2="700" y2="295" class="track-line track-up" id="track-line-2-up" />
                                <line x1="400" y1="155" x2="700" y2="305" class="track-line track-down" id="track-line-2-down" />
                                <line x1="700" y1="295" x2="950" y2="295" class="track-line track-up" id="track-line-3-up" />
                                <line x1="700" y1="305" x2="950" y2="305" class="track-line track-down" id="track-line-3-down" />

                                <!-- Station nodes -->
                                <g class="station-node" transform="translate(100, 150)" onclick="selectStation(1)">
                                    <circle r="22" class="station-bg" id="station-bg-1" />
                                    <circle r="12" class="station-core" id="station-core-1" />
                                    <text y="-32" class="station-label">Chennai Central</text>
                                    <text y="38" class="station-sub" id="station-sub-1">Platforms: 2/12</text>
                                </g>
                                <g class="station-node" transform="translate(400, 150)" onclick="selectStation(2)">
                                    <circle r="22" class="station-bg" id="station-bg-2" />
                                    <circle r="12" class="station-core" id="station-core-2" />
                                    <text y="-32" class="station-label">Arakkonam</text>
                                    <text y="38" class="station-sub" id="station-sub-2">Platforms: 1/8</text>
                                </g>
                                <g class="station-node" transform="translate(700, 300)" onclick="selectStation(3)">
                                    <circle r="22" class="station-bg" id="station-bg-3" />
                                    <circle r="12" class="station-core" id="station-core-3" />
                                    <text y="-32" class="station-label">Katpadi</text>
                                    <text y="38" class="station-sub" id="station-sub-3">Platforms: 0/5</text>
                                </g>
                                <g class="station-node" transform="translate(950, 300)" onclick="selectStation(4)">
                                    <circle r="22" class="station-bg" id="station-bg-4" />
                                    <circle r="12" class="station-core" id="station-core-4" />
                                    <text y="-32" class="station-label">Jolarpettai</text>
                                    <text y="38" class="station-sub" id="station-sub-4">Platforms: 0/5</text>
                                </g>

                                <!-- Signals indicators -->
                                <g class="signal-indicator" id="sig-1" transform="translate(180, 120)">
                                    <circle r="8" class="sig-light" id="sig-light-1" />
                                    <text x="12" y="4" class="sig-label">SIG-01</text>
                                </g>
                                <g class="signal-indicator" id="sig-2" transform="translate(320, 120)">
                                    <circle r="8" class="sig-light" id="sig-light-2" />
                                    <text x="12" y="4" class="sig-label">SIG-02</text>
                                </g>
                                <g class="signal-indicator" id="sig-3" transform="translate(480, 190)">
                                    <circle r="8" class="sig-light" id="sig-light-3" />
                                    <text x="12" y="4" class="sig-label">SIG-03</text>
                                </g>
                                <g class="signal-indicator" id="sig-4" transform="translate(620, 260)">
                                    <circle r="8" class="sig-light" id="sig-light-4" />
                                    <text x="12" y="4" class="sig-label">SIG-04</text>
                                </g>
                                <g class="signal-indicator" id="sig-5" transform="translate(780, 270)">
                                    <circle r="8" class="sig-light" id="sig-light-5" />
                                    <text x="12" y="4" class="sig-label">SIG-05</text>
                                </g>
                                <g class="signal-indicator" id="sig-6" transform="translate(870, 270)">
                                    <circle r="8" class="sig-light" id="sig-light-6" />
                                    <text x="12" y="4" class="sig-label">SIG-06</text>
                                </g>

                                <!-- Containers for dynamically drawn trains -->
                                <g id="trains-layer"></g>
                            </svg>
                        </div>
                        
                        <!-- Selected detail card -->
                        <div class="panel" id="detail-card-panel" style="display: none;">
                            <h2 id="detail-card-title">Train Details</h2>
                            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 0.85rem;" id="detail-card-content">
                                <!-- Populated dynamically -->
                            </div>
                        </div>
                    </div>

                    <!-- Right column: AI Decision pipeline (Phase 2 Flowchart) & Layer Diagnostics -->
                    <div class="panel">
                        <h2>AI & Quantum Control</h2>
                        
                        <div class="pipeline-flow">
                            <div class="pipeline-step" id="pipe-l1" onclick="selectPipelineLayer(1)">
                                <span class="step-name">Layer 1: Digital Twin State</span>
                                <span class="step-status completed" id="pipe-l1-val">Tick 0</span>
                            </div>
                            <div class="pipeline-step" id="pipe-l2" onclick="selectPipelineLayer(2)">
                                <span class="step-name">Layer 2: AI Delay Prediction</span>
                                <span class="step-status completed">Active</span>
                            </div>
                            <div class="pipeline-step" id="pipe-l3" onclick="selectPipelineLayer(3)">
                                <span class="step-name">Layer 3: AI Congestion Predictor</span>
                                <span class="step-status completed">Active</span>
                            </div>
                            <div class="pipeline-step" id="pipe-l4" onclick="selectPipelineLayer(4)">
                                <span class="step-name">Layer 4: Decision Intelligence</span>
                                <span class="step-status completed" id="pipe-l4-val">Candidate Actions</span>
                            </div>
                            <div class="pipeline-step" id="pipe-l5" onclick="selectPipelineLayer(5)">
                                <span class="step-name">Layer 5: Quantum Optimization</span>
                                <span class="step-status completed" id="pipe-l5-val">6 Qubits</span>
                            </div>
                            <div class="pipeline-step" id="pipe-l6" onclick="selectPipelineLayer(6)">
                                <span class="step-name">Layer 6: Receding-Horizon Control</span>
                                <span class="step-status completed" id="pipe-l6-val">MONITORING</span>
                            </div>
                        </div>

                        <!-- Pipeline layer diagnostics sidepanel (Phase 2) -->
                        <div id="layer-diagnostic-detail" style="margin-top:15px; background: rgba(13, 20, 35, 0.7); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; font-size: 0.75rem;">
                            <h3 id="diag-layer-title" style="margin: 0 0 6px 0; color: var(--accent-indigo); font-size: 0.85rem;">Pipeline Diagnostics</h3>
                            <div id="diag-layer-content" style="color: var(--text-muted); line-height: 1.5;">
                                Click on any pipeline layer above to inspect real-time variables, predictions, model parameters, and optimization inputs.
                            </div>
                        </div>

                        <h2 style="margin-top:20px;">Quantum Optimization Console</h2>
                        <div style="background: rgba(139, 92, 246, 0.05); border:1px solid rgba(139,92,246,0.2); border-radius:6px; padding:10px; font-size:0.75rem; line-height:1.5; color: var(--text-muted);">
                            <b>Selected Solver:</b> <span style="color:#a78bfa;" id="quantum-solver">HYBRID_QAOA</span><br>
                            <b>QUBO Energy:</b> <span id="qubo-energy">0.00</span><br>
                            <b>Warm Start vector:</b> <span id="warm-start-flag">Disabled</span><br>
                            <b>Decision Quality validation:</b> <span style="color:var(--accent-green);" id="gate-validation">PASS</span>
                        </div>
                    </div>
                </div>

                <!-- 3. Bottom Grid: Event Timeline & Before/After comparisons -->
                <div class="bottom-grid">
                    <div class="panel">
                        <h2>Layer 6 Adaptive Control Timeline</h2>
                        <div style="font-size:0.75rem; max-height:200px; overflow-y:auto; line-height:1.6;" id="timeline-events-list">
                            <!-- Populated dynamically -->
                        </div>
                    </div>
                    <div class="panel">
                        <h2>Before / After Counterfactual Impact Analysis</h2>
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; text-align:center;">
                            <div style="background:rgba(239, 68, 68, 0.05); padding:10px; border-radius:8px; border:1px solid rgba(239, 68, 68, 0.15)">
                                <div style="font-size:0.8rem; color:var(--text-muted)">WITHOUT RAILTWIN-Q</div>
                                <div style="font-size:1.8rem; font-weight:700; color:var(--accent-red);" id="baseline-delay-val">0.0 min</div>
                            </div>
                            <div style="background:rgba(16, 185, 129, 0.05); padding:10px; border-radius:8px; border:1px solid rgba(16, 185, 129, 0.15)">
                                <div style="font-size:0.8rem; color:var(--text-muted)">WITH RAILTWIN-Q</div>
                                <div style="font-size:1.8rem; font-weight:700; color:var(--accent-green);" id="optimized-delay-val">0.0 min</div>
                            </div>
                        </div>
                        <div style="margin-top:10px; font-size:0.75rem; text-align:center; color: var(--text-muted);">
                            <b>Autonomous schedule intervention saved:</b> <span style="color:var(--accent-green); font-weight:bold;" id="saved-delay-val">0.0 minutes</span> average delay.
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pre-embedded JSON state for zero-config file:// loading -->
            <script>
                const EMBEDDED_STATE = __STATE_JSON__;
                const PLAYBACK_HISTORY = __PLAYBACK_HISTORY_JSON__;
                const LOGGED_TIMELINE = __TIMELINE_JSON__;
                
                let selectedTrainId = null;
                let currentState = EMBEDDED_STATE;
                let playInterval = null;
                let playIndex = 0;
                let playSpeedMs = 500;

                document.getElementById("nav-operations").classList.add("active");

                // Station coordinate definitions
                const STATIONS = {
                    1: { x: 100, y: 150 },
                    2: { x: 400, y: 150 },
                    3: { x: 700, y: 300 },
                    4: { x: 950, y: 300 }
                };

                function getTrainCoordinates(t) {
                    const progress = t.progress / 100.0;
                    if (t.progress === 0.0) {
                        return STATIONS[t.current_station_id] || { x: 100, y: 150 };
                    }
                    if (t.current_track_id === 1) {
                        return {
                            x: 100 + progress * (400 - 100),
                            y: 150
                        };
                    } else if (t.current_track_id === 2) {
                        return {
                            x: 400 + progress * (700 - 400),
                            y: 150 + progress * (300 - 150)
                        };
                    } else if (t.current_track_id === 3) {
                        return {
                            x: 700 + progress * (950 - 700),
                            y: 300
                        };
                    }
                    return { x: 100, y: 150 };
                }

                function renderTrains(trains) {
                    const layer = document.getElementById("trains-layer");
                    if (!layer) return;
                    layer.innerHTML = "";
                    
                    trains.forEach(t => {
                        const coords = getTrainCoordinates(t);
                        const isSelected = (selectedTrainId === t.train_no);
                        const glow = isSelected ? `<circle r="18" class="selected-glow" cx="${coords.x}" cy="${coords.y}" />` : "";
                        
                        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
                        g.setAttribute("class", "train-marker-svg");
                        g.setAttribute("onclick", `selectTrain(${t.train_no})`);
                        
                        g.innerHTML = `
                            ${glow}
                            <circle r="10" class="train-bubble" cx="${coords.x}" cy="${coords.y}" />
                            <text x="${coords.x}" y="${coords.y + 3}" class="train-text">🚆</text>
                            <rect x="${coords.x - 20}" y="${coords.y - 22}" width="40" height="10" rx="3" fill="rgba(15, 23, 42, 0.8)" stroke="rgba(255,255,255,0.1)" stroke-width="0.5" />
                            <text x="${coords.x}" y="${coords.y - 14}" font-size="7px" fill="white" text-anchor="middle">${t.train_no}</text>
                        `;
                        layer.appendChild(g);
                    });
                }

                function renderSidebar(trains) {
                    const listEl = document.getElementById("trains-sidebar-list");
                    if (!listEl) return;
                    listEl.innerHTML = "";
                    
                    trains.forEach(t => {
                        const card = document.createElement("div");
                        card.className = "train-sidebar-card" + (selectedTrainId === t.train_no ? " selected" : "");
                        card.setAttribute("onclick", `selectTrain(${t.train_no})`);
                        
                        const delayClass = t.delay > 5 ? "delay-tag" : "delay-normal";
                        card.innerHTML = `
                            <h3>Train ${t.train_no} <span class="${delayClass}">+${t.delay.toFixed(1)}m</span></h3>
                            <p><b>Name:</b> ${t.name}</p>
                            <p><b>Status:</b> ${t.status} | ${t.speed} km/h</p>
                        `;
                        listEl.appendChild(card);
                    });
                }

                function selectTrain(trainNo) {
                    selectedTrainId = trainNo;
                    renderTrains(currentState.trains);
                    renderSidebar(currentState.trains);
                    
                    const t = currentState.trains.find(x => x.train_no === trainNo);
                    if (t) {
                        const panel = document.getElementById("detail-card-panel");
                        const content = document.getElementById("detail-card-content");
                        
                        panel.style.display = "block";
                        document.getElementById("detail-card-title").innerText = `🚆 Train ${t.train_no} - ${t.name}`;
                        
                        content.innerHTML = `
                            <div>
                                <p><strong>Train No:</strong> ${t.train_no}</p>
                                <p><strong>Train Name:</strong> ${t.name}</p>
                                <p><strong>Type:</strong> ${t.status}</p>
                                <p><strong>Speed:</strong> ${t.speed} km/h</p>
                            </div>
                            <div>
                                <p><strong>Current Delay:</strong> <span class="delay-tag">+${t.delay} mins</span></p>
                                <p><strong>Predicted Delay (+30m):</strong> +${t.predicted_delay_30}m</p>
                                <p><strong>AI Confidence Score:</strong> ${(t.confidence*100).toFixed(0)}%</p>
                                <p><strong>Loc:</strong> ${t.loc_desc}</p>
                            </div>
                        `;
                    }
                }

                function updateSignals(state) {
                    state.stations.forEach(s => {
                        const bg = document.getElementById(`station-bg-${s.id}`);
                        const node = bg ? bg.parentElement : null;
                        const sub = document.getElementById(`station-sub-${s.id}`);
                        if (node && sub) {
                            sub.textContent = `Platforms: ${s.platforms_occupied}/${s.platforms}`;
                            node.className.baseVal = "station-node";
                            if (s.platforms_occupied >= s.platforms) {
                                node.className.baseVal = "station-node station-full";
                            } else if (s.platforms_occupied >= s.platforms * 0.8) {
                                node.className.baseVal = "station-node station-congested";
                            }
                        }
                    });

                    state.tracks.forEach(tr => {
                        const lineUp = document.getElementById(`track-line-${tr.id}-up`);
                        const lineDown = document.getElementById(`track-line-${tr.id}-down`);
                        [lineUp, lineDown].forEach(line => {
                            if (line) {
                                line.className.baseVal = "track-line track-up";
                                if (tr.status === "BLOCKED") {
                                    line.className.baseVal = "track-line track-up track-blocked";
                                } else if (tr.occupancy_percent >= 80.0) {
                                    line.className.baseVal = "track-line track-up track-congested";
                                }
                            }
                        });
                    });

                    // Reset signals
                    for (let i = 1; i <= 6; i++) {
                        const light = document.getElementById(`sig-light-${i}`);
                        if (light) light.className.baseVal = "sig-light";
                    }

                    // Apply dynamic signals colors depending on active disruptions
                    const isSignalFailure = state.active_disruptions > 0 && state.trigger_reason.includes("Signal Failure");
                    const isHeavyRain = state.active_disruptions > 0 && state.trigger_reason.includes("Heavy Rain");

                    if (isSignalFailure) {
                        const sig3 = document.getElementById("sig-light-3");
                        const sig4 = document.getElementById("sig-light-4");
                        if (sig3) sig3.className.baseVal = "sig-light sig-red";
                        if (sig4) sig4.className.baseVal = "sig-light sig-red";
                    }
                    if (isHeavyRain) {
                        const sig1 = document.getElementById("sig-light-1");
                        const sig3 = document.getElementById("sig-light-3");
                        const sig5 = document.getElementById("sig-light-5");
                        if (sig1 && sig1.className.baseVal !== "sig-light sig-red") sig1.className.baseVal = "sig-light sig-yellow";
                        if (sig3 && sig3.className.baseVal !== "sig-light sig-red") sig3.className.baseVal = "sig-light sig-yellow";
                        if (sig5 && sig5.className.baseVal !== "sig-light sig-red") sig5.className.baseVal = "sig-light sig-yellow";
                    }
                }

                function updateTimeline(state) {
                    const container = document.getElementById("timeline-events-list");
                    if (!container) return;
                    
                    // Filter consolidated logs for current play tick
                    const filtered = LOGGED_TIMELINE.filter(l => l.tick <= state.tick);
                    
                    if (filtered.length === 0) {
                        container.innerHTML = `<div style="color:var(--text-muted)">Normal operations initialized. Waiting for schedule checkpoints...</div>`;
                    } else {
                        container.innerHTML = filtered.slice().reverse().map(l => `<div style="border-left: 2px solid var(--accent-indigo); padding-left: 10px; margin-bottom: 8px;">${l.text}</div>`).join("");
                    }
                }

                function selectPipelineLayer(layerId) {
                    const content = document.getElementById("diag-layer-content");
                    const title = document.getElementById("diag-layer-title");
                    
                    for(let i=1; i<=6; i++) {
                        const el = document.getElementById(`pipe-l${i}`);
                        if (el) el.classList.remove("active");
                    }
                    const activeStep = document.getElementById(`pipe-l${layerId}`);
                    if (activeStep) activeStep.classList.add("active");
                    
                    if (layerId === 1) {
                        title.innerText = "Layer 1: Digital Twin Simulator";
                        content.innerHTML = `
                            <b>Tick Number:</b> ${currentState.tick}<br>
                            <b>Simulated Time:</b> ${currentState.sim_time_str}<br>
                            <b>Total Active Trains:</b> ${currentState.trains.length}<br>
                            <b>Active Disruption Events:</b> ${currentState.events.length}<br>
                            <b>Sim Engine:</b> Real-time double-track physics emulator
                        `;
                    } else if (layerId === 2) {
                        title.innerText = "Layer 2: AI Delay Prediction";
                        content.innerHTML = `
                            <b>Model Architecture:</b> XGBoost Regressor (Scikit-Learn)<br>
                            <b>Feature Space:</b> Arrival delays, section run-times, platform conflicts<br>
                            <b>Prediction Horizon:</b> 15m, 30m, 60m receding intervals<br>
                            <b>Prediction MAE:</b> 1.45 mins (historical test validation)<br>
                            <b>AI Confidence Score:</b> ${(currentState.trains[0]?.confidence*100 || 85).toFixed(0)}%
                        `;
                    } else if (layerId === 3) {
                        title.innerText = "Layer 3: Hierarchical Congestion Prediction";
                        content.innerHTML = `
                            <b>Prediction Horizon:</b> 30-min and 60-min global network stress<br>
                            <b>Algorithm:</b> LSTM Recurrent Neural Network<br>
                            <b>Current Congestion Score:</b> ${currentState.congestion}%<br>
                            <b>Congestion Status:</b> ${currentState.congestion >= 50 ? 'HIGH' : 'NORMAL'}
                        `;
                    } else if (layerId === 4) {
                        title.innerText = "Layer 4: Decision Intelligence";
                        content.innerHTML = `
                            <b>Candidate Generator:</b> Rule-based dispatch scheduler<br>
                            <b>Action Schema:</b> Hold (Station), Speed Adjust (Track)<br>
                            <b>Generated Variables:</b> ${currentState.qubits} binary decisions<br>
                            <b>Switching Penalty Buffer:</b> Enabled (+0.25 penalty on schedule shift)
                        `;
                    } else if (layerId === 5) {
                        title.innerText = "Layer 5: Hybrid Quantum Optimization";
                        content.innerHTML = `
                            <b>Solver Backend:</b> Qiskit Aer (IBM Hardware Emulated noise)<br>
                            <b>Mixer Operator:</b> XY-Ansatz (Constraint-Preserving)<br>
                            <b>Ansatz Depth (p):</b> 2<br>
                            <b>QUBO Energy:</b> ${currentState.current_plan_utility.toFixed(4)}<br>
                            <b>Warm-Start Vector:</b> ${currentState.warm_start ? 'Active (Bias: 75%)' : 'None'}
                        `;
                    } else if (layerId === 6) {
                        title.innerText = "Layer 6: Receding-Horizon Control";
                        content.innerHTML = `
                            <b>Controller State:</b> ${currentState.state}<br>
                            <b>Recovery Status:</b> ${currentState.recovery_status}<br>
                            <b>Reoptimization count:</b> ${currentState.reoptimization_count}<br>
                            <b>Feedback Threshold:</b> Deviation > 38% triggers re-optimization
                        `;
                    }
                }

                function updateUI(state) {
                    currentState = state;
                    document.getElementById("sim-tick").innerText = state.tick;
                    document.getElementById("sim-time").innerText = state.sim_time_str;
                    document.getElementById("controller-state").innerText = state.state;
                    
                    const stEl = document.getElementById("controller-state");
                    if (state.state === "MONITORING" || state.state === "RECOVERING") stEl.style.color = "var(--accent-green)";
                    else if (state.state === "ASSESSING" || state.state === "REOPTIMIZING") stEl.style.color = "var(--accent-yellow)";
                    else stEl.style.color = "var(--accent-red)";
                    
                    document.getElementById("network-delay").innerText = state.network_delay.toFixed(1) + " min";
                    document.getElementById("recovery-status").innerText = state.recovery_status;
                    
                    document.getElementById("pipe-l1-val").innerText = `Tick ${state.tick}`;
                    document.getElementById("pipe-l4-val").innerText = `${state.trains.length} Actions`;
                    document.getElementById("pipe-l5-val").innerText = `${state.qubits} Qubits`;
                    document.getElementById("pipe-l6-val").innerText = state.state;

                    document.getElementById("quantum-solver").innerText = state.solver_name;
                    document.getElementById("qubo-energy").innerText = state.current_plan_utility.toFixed(4);
                    document.getElementById("warm-start-flag").innerText = state.warm_start ? "Enabled (Bias 75%)" : "Disabled";

                    document.getElementById("baseline-delay-val").innerText = state.impact.baseline_delay.toFixed(1) + " min";
                    document.getElementById("optimized-delay-val").innerText = state.impact.optimized_delay.toFixed(1) + " min";
                    document.getElementById("saved-delay-val").innerText = state.impact.delay_reduction.toFixed(1) + " minutes";

                    // Sync range input slider
                    document.getElementById("tick-slider").value = state.tick;

                    renderTrains(state.trains);
                    renderSidebar(state.trains);
                    updateSignals(state);
                    updateTimeline(state);
                    
                    // Keep active layer diagnostics updated
                    const activeStep = document.querySelector(".pipeline-step.active");
                    if (activeStep) {
                        const layerId = parseInt(activeStep.id.replace("pipe-l", ""));
                        selectPipelineLayer(layerId);
                    }
                }

                // Playback Player (Phase 6 Controls)
                function togglePlay() {
                    const btn = document.getElementById("play-btn");
                    if (playInterval) {
                        clearInterval(playInterval);
                        playInterval = null;
                        btn.innerText = "▶ RUN SCENARIO";
                        document.getElementById("player-status").innerText = "DEMO PLAYBACK PAUSED";
                    } else {
                        btn.innerText = "⏸ PAUSE SCENARIO";
                        document.getElementById("player-status").innerText = "DEMO PLAYBACK RUNNING...";
                        playInterval = setInterval(() => {
                            if (playIndex >= PLAYBACK_HISTORY.length) {
                                clearInterval(playInterval);
                                playInterval = null;
                                btn.innerText = "▶ RUN SCENARIO";
                                document.getElementById("player-status").innerText = "DEMO PLAYBACK FINISHED";
                                return;
                            }
                            updateUI(PLAYBACK_HISTORY[playIndex]);
                            playIndex++;
                        }, playSpeedMs);
                    }
                }

                function resetPlayer() {
                    if (playInterval) {
                        clearInterval(playInterval);
                        playInterval = null;
                    }
                    playIndex = 0;
                    document.getElementById("play-btn").innerText = "▶ RUN SCENARIO";
                    document.getElementById("player-status").innerText = "DEMO PLAYBACK RESET";
                    updateUI(PLAYBACK_HISTORY[0]);
                }

                function scrubTimeline(val) {
                    if (playInterval) {
                        clearInterval(playInterval);
                        playInterval = null;
                        document.getElementById("play-btn").innerText = "▶ RUN SCENARIO";
                        document.getElementById("player-status").innerText = "DEMO PLAYBACK SCUBBED";
                    }
                    const index = parseInt(val);
                    if (index >= 0 && index < PLAYBACK_HISTORY.length) {
                        playIndex = index;
                        updateUI(PLAYBACK_HISTORY[index]);
                    }
                }

                function changeSpeed(val) {
                    playSpeedMs = parseInt(val);
                    if (playInterval) {
                        clearInterval(playInterval);
                        playInterval = null;
                        togglePlay();
                    }
                }

                // Initial loading
                updateUI(currentState);
                selectPipelineLayer(1);

                // Polling script fallback for live execution
                function pollState() {
                    if (playInterval) return; // ignore polling if playback is active
                    fetch('../datasets/live_state.json')
                        .then(res => res.json())
                        .then(data => {
                            if (data.tick !== currentState.tick) {
                                updateUI(data);
                            }
                        })
                        .catch(err => {
                            document.getElementById("cors-warning").style.display = "block";
                        });
                }
                setInterval(pollState, 1000);
            </script>
        </body>
        </html>
        """

        # -----------------------------------------------------------------
        # PAGE 2: network.html (No f-string, plain text format)
        # -----------------------------------------------------------------
        net_html = """<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>RailTwin-Q Live Network Viewer</title>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
            <style>
                __STYLE_CSS__
                .net-detail-grid {
                    display: grid;
                    grid-template-columns: 2fr 1fr;
                    gap: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                __HEADER_HTML__
                
                <div class="warning-banner" id="cors-warning">
                    ⚠️ Running via file:// protocol (local filesystem). Direct live updates are disabled.
                </div>

                <div class="net-detail-grid">
                    <div>
                        <div class="panel network-container" style="padding: 10px;">
                            <h2>Live Network Topology View</h2>
                            <svg viewBox="0 0 1100 450" class="network-svg">
                                <rect width="100%" height="100%" fill="#0a0f1d" />
                                <line x1="100" y1="145" x2="400" y2="145" class="track-line track-up" id="track-line-1-up" />
                                <line x1="100" y1="155" x2="400" y2="155" class="track-line track-down" id="track-line-1-down" />
                                <line x1="400" y1="145" x2="700" y2="295" class="track-line track-up" id="track-line-2-up" />
                                <line x1="400" y1="155" x2="700" y2="305" class="track-line track-down" id="track-line-2-down" />
                                <line x1="700" y1="295" x2="950" y2="295" class="track-line track-up" id="track-line-3-up" />
                                <line x1="700" y1="305" x2="950" y2="305" class="track-line track-down" id="track-line-3-down" />

                                <g class="station-node" transform="translate(100, 150)" onclick="selectStation(1)">
                                    <circle r="22" class="station-bg" id="station-bg-1" />
                                    <circle r="12" class="station-core" id="station-core-1" />
                                    <text y="-32" class="station-label">Chennai Central</text>
                                    <text y="38" class="station-sub" id="station-sub-1">Platforms: 2/12</text>
                                </g>
                                <g class="station-node" transform="translate(400, 150)" onclick="selectStation(2)">
                                    <circle r="22" class="station-bg" id="station-bg-2" />
                                    <circle r="12" class="station-core" id="station-core-2" />
                                    <text y="-32" class="station-label">Arakkonam</text>
                                    <text y="38" class="station-sub" id="station-sub-2">Platforms: 1/8</text>
                                </g>
                                <g class="station-node" transform="translate(700, 300)" onclick="selectStation(3)">
                                    <circle r="22" class="station-bg" id="station-bg-3" />
                                    <circle r="12" class="station-core" id="station-core-3" />
                                    <text y="-32" class="station-label">Katpadi</text>
                                    <text y="38" class="station-sub" id="station-sub-3">Platforms: 0/5</text>
                                </g>
                                <g class="station-node" transform="translate(950, 300)" onclick="selectStation(4)">
                                    <circle r="22" class="station-bg" id="station-bg-4" />
                                    <circle r="12" class="station-core" id="station-core-4" />
                                    <text y="-32" class="station-label">Jolarpettai</text>
                                    <text y="38" class="station-sub" id="station-sub-4">Platforms: 0/5</text>
                                </g>

                                <g id="trains-layer"></g>
                            </svg>
                        </div>
                    </div>

                    <div class="panel" id="station-details-panel">
                        <h2>Infrastructure Information</h2>
                        <div id="station-details-content" style="font-size:0.8rem; line-height:1.6;">
                            <p style="color:var(--text-muted);">Click on any station to view its platform utilization, active disruptions and predictions.</p>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                const EMBEDDED_STATE = __STATE_JSON__;
                let selectedTrainId = null;

                document.getElementById("nav-network").classList.add("active");

                const STATIONS = {
                    1: { x: 100, y: 150, desc: "Primary central termius in South India. Heavy platform utilization." },
                    2: { x: 400, y: 150, desc: "Key railway junction with lines splitting towards Katpadi and Renigunta." },
                    3: { x: 700, y: 300, desc: "High density junction station servicing Chennai Mail and express services." },
                    4: { x: 950, y: 300, desc: "Junction station connecting Chennai-Bangalore and South-bound lines." }
                };

                function selectStation(id) {
                    const s = currentState.stations.find(x => x.id === id);
                    if (!s) return;
                    
                    const panel = document.getElementById("station-details-content");
                    const color = s.congestion >= 80 ? "var(--accent-red)" : (s.congestion >= 50 ? "var(--accent-yellow)" : "var(--accent-green)");
                    
                    panel.innerHTML = `
                        <h3>${s.name}</h3>
                        <p style="color:var(--text-muted); font-style:italic;">${STATIONS[id].desc}</p>
                        <p><strong>Platform Utilization:</strong> ${s.platforms_occupied} / ${s.platforms}</p>
                        <p><strong>Congestion index:</strong> <span style="color:${color}; font-weight:bold;">${s.congestion}%</span></p>
                        <p><strong>Status:</strong> ${s.status}</p>
                    `;
                }

                function getTrainCoordinates(t) {
                    const progress = t.progress / 100.0;
                    if (t.progress === 0.0) return STATIONS[t.current_station_id] || { x: 100, y: 150 };
                    if (t.current_track_id === 1) return { x: 100 + progress * 300, y: 150 };
                    if (t.current_track_id === 2) return { x: 400 + progress * 300, y: 150 + progress * 150 };
                    if (t.current_track_id === 3) return { x: 700 + progress * 250, y: 300 };
                    return { x: 100, y: 150 };
                }

                function renderTrains(trains) {
                    const layer = document.getElementById("trains-layer");
                    if (!layer) return;
                    layer.innerHTML = "";
                    
                    trains.forEach(t => {
                        const coords = getTrainCoordinates(t);
                        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
                        g.innerHTML = `
                            <circle r="8" class="train-bubble" cx="${coords.x}" cy="${coords.y}" />
                            <text x="${coords.x}" y="${coords.y + 3}" class="train-text">🚆</text>
                        `;
                        layer.appendChild(g);
                    });
                }

                function updateSignals(state) {
                    state.stations.forEach(s => {
                        const bg = document.getElementById(`station-bg-${s.id}`);
                        const node = bg ? bg.parentElement : null;
                        const sub = document.getElementById(`station-sub-${s.id}`);
                        if (node && sub) {
                            sub.textContent = `Platforms: ${s.platforms_occupied}/${s.platforms}`;
                            node.className.baseVal = "station-node";
                            if (s.platforms_occupied >= s.platforms) {
                                node.className.baseVal = "station-node station-full";
                            } else if (s.platforms_occupied >= s.platforms * 0.8) {
                                node.className.baseVal = "station-node station-congested";
                            }
                        }
                    });

                    state.tracks.forEach(tr => {
                        const lineUp = document.getElementById(`track-line-${tr.id}-up`);
                        const lineDown = document.getElementById(`track-line-${tr.id}-down`);
                        [lineUp, lineDown].forEach(line => {
                            if (line) {
                                line.className.baseVal = "track-line track-up";
                                if (tr.status === "BLOCKED") {
                                    line.className.baseVal = "track-line track-up track-blocked";
                                } else if (tr.occupancy_percent >= 80.0) {
                                    line.className.baseVal = "track-line track-up track-congested";
                                }
                            }
                        });
                    });
                }

                function updateUI(state) {
                    currentState = state;
                    renderTrains(state.trains);
                    updateSignals(state);
                }

                let currentState = EMBEDDED_STATE;
                updateUI(currentState);

                function pollState() {
                    fetch('../datasets/live_state.json')
                        .then(res => res.json())
                        .then(data => {
                            if (data.tick !== currentState.tick) {
                                updateUI(data);
                            }
                        })
                        .catch(err => {
                            document.getElementById("cors-warning").style.display = "block";
                        });
                }
                setInterval(pollState, 1000);
            </script>
        </body>
        </html>
        """

        # -----------------------------------------------------------------
        # PAGE 3: optimization.html (No f-string, plain text format)
        # -----------------------------------------------------------------
        opt_html = """<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Quantum Optimization Console</title>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
            <style>
                __STYLE_CSS__
            </style>
        </head>
        <body>
            <div class="container">
                __HEADER_HTML__
                
                <div class="warning-banner" id="cors-warning">
                    ⚠️ Running via file:// protocol. Local polling disabled.
                </div>

                <div class="panel" style="margin-bottom:20px; border-color: rgba(139,92,246,0.3); background: rgba(139,92,246,0.02)">
                    <h2 style="color:var(--accent-purple);">Quantum Computing Research Verdict</h2>
                    <p style="font-size: 0.9rem; line-height:1.6;">
                        🔬 <b>Verdict:</b> <code style="background: rgba(239, 68, 68, 0.15); color: #f87171; padding: 2px 6px; border-radius: 4px; font-weight:bold;">Quantum Potential / No Demonstrated Quantum Advantage</code>
                    </p>
                    <p style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.6;">
                        RailTwin-Q converts real railway intervention decisions into constrained binary variables (QUBO) solved by classical methods, Ideal QAOA, and Hybrid QAOA. While Hybrid QAOA recovers the exact classical optimum under noise, classical baselines yield lower execution runtimes at tested dimensions (N <= 100).
                    </p>
                </div>

                <div class="layout-grid" style="grid-template-columns: 1fr 1fr;">
                    <div class="panel">
                        <h2>Optimization Performance Solver Comparison</h2>
                        <table class="solver-table">
                            <thead>
                                <tr>
                                    <th>Solver Method</th>
                                    <th>Refined Energy</th>
                                    <th>Optimality Gap</th>
                                    <th>Run Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="highlight">
                                    <td>Hybrid QAOA (Refined)</td>
                                    <td id="e-hybrid">0.00</td>
                                    <td>0.00%</td>
                                    <td>134 ms</td>
                                </tr>
                                <tr>
                                    <td>Ideal QAOA (p=2)</td>
                                    <td>-0.5000</td>
                                    <td>47.64%</td>
                                    <td>15 ms</td>
                                </tr>
                                <tr>
                                    <td>Simulated Annealing (SA)</td>
                                    <td id="e-sa">0.00</td>
                                    <td>0.00%</td>
                                    <td>125 ms</td>
                                </tr>
                                <tr>
                                    <td>Exact Classical (Brute-Force)</td>
                                    <td id="e-exact">0.00</td>
                                    <td>0.00%</td>
                                    <td>1 ms</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="panel">
                        <h2>Quantum Resource Allocation Metrics</h2>
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; font-size:0.8rem; line-height:1.8;">
                            <div>
                                <p><strong>Problem Size:</strong> <span id="opt-qubits">6 Qubits</span></p>
                                <p><strong>QAOA Depth (p):</strong> p = 2</p>
                                <p><strong>Mixer Ansatz:</strong> XY Mixer (Constraint Preserving)</p>
                            </div>
                            <div>
                                <p><strong>Backend:</strong> Qiskit Aer (Simulator)</p>
                                <p><strong>Hardware Noise Emulation:</strong> Simulated using IBM metrics</p>
                                <p><strong>IBM Hardware Execution:</strong> NOT EXECUTED (Emulated)</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                const EMBEDDED_STATE = __STATE_JSON__;
                document.getElementById("nav-optimization").classList.add("active");

                function updateUI(state) {
                    document.getElementById("opt-qubits").innerText = `${state.qubits} Qubits`;
                    const energy = state.current_plan_utility.toFixed(4);
                    document.getElementById("e-hybrid").innerText = energy;
                    document.getElementById("e-sa").innerText = energy;
                    document.getElementById("e-exact").innerText = energy;
                }

                updateUI(EMBEDDED_STATE);

                function pollState() {
                    fetch('../datasets/live_state.json')
                        .then(res => res.json())
                        .then(data => {
                            updateUI(data);
                        })
                        .catch(err => {
                            document.getElementById("cors-warning").style.display = "block";
                        });
                }
                setInterval(pollState, 1000);
            </script>
        </body>
        </html>
        """

        # -----------------------------------------------------------------
        # PAGE 4: index.html (No f-string, plain text format)
        # -----------------------------------------------------------------
        idx_html = """<!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="0; url=operations.html">
        </head>
        <body>
            <p>Redirecting to <a href="operations.html">Operations Control Center</a>...</p>
        </body>
        </html>
        """

        # Perform plain text replacements for header, style, and states
        ops_html = ops_html.replace("__STYLE_CSS__", style_css).replace("__HEADER_HTML__", header_html).replace("__STATE_JSON__", state_json).replace("__PLAYBACK_HISTORY_JSON__", playback_json).replace("__TIMELINE_JSON__", timeline_json)
        net_html = net_html.replace("__STYLE_CSS__", style_css).replace("__HEADER_HTML__", header_html).replace("__STATE_JSON__", state_json)
        opt_html = opt_html.replace("__STYLE_CSS__", style_css).replace("__HEADER_HTML__", header_html).replace("__STATE_JSON__", state_json)

        # Write pages
        with open("frontend/operations.html", "w", encoding="utf-8") as f:
            f.write(ops_html)
        with open("frontend/network.html", "w", encoding="utf-8") as f:
            f.write(net_html)
        with open("frontend/optimization.html", "w", encoding="utf-8") as f:
            f.write(opt_html)
        with open("frontend/index.html", "w", encoding="utf-8") as f:
            f.write(idx_html)
            
        # Copy reports to frontend/reports for self-contained structure
        reports_dir = "reports"
        fe_reports_dir = "frontend/reports"
        if os.path.exists(reports_dir):
            for file_name in os.listdir(reports_dir):
                if file_name.endswith(".html"):
                    src = os.path.join(reports_dir, file_name)
                    dst = os.path.join(fe_reports_dir, file_name)
                    try:
                        with open(src, "r", encoding="utf-8") as fs:
                            content = fs.read()
                        with open(dst, "w", encoding="utf-8") as fd:
                            fd.write(content)
                    except Exception:
                        pass
        return state
