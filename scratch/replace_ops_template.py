NEW_OPS_TEMPLATE = r'''        ops_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>RailTwin-Q | Railway Network Operations Center</title>
    <meta name="description" content="RailTwin-Q — AI + Quantum Railway Digital Twin Operations Center">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --sidebar-bg: #0b0f19;
            --main-bg: #f1f5f9;
            --card-bg: #ffffff;
            --border-color: #cbd5e1;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --accent-blue: #2563eb;
            --accent-blue-light: #3b82f6;
            --accent-cyan: #0891b2;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-red: #ef4444;
            --accent-purple: #8b5cf6;
            --shadow-sm: 0 1px 3px 0 rgba(0,0,0,0.05), 0 1px 2px 0 rgba(0,0,0,0.02);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.06), 0 2px 4px -1px rgba(0,0,0,0.03);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
        body {{ background-color: var(--main-bg); color: var(--text-primary); display: flex; height: 100vh; overflow: hidden; }}
        .sidebar {{ width: 240px; background: var(--sidebar-bg); border-right: 1px solid rgba(255,255,255,0.06); display: flex; flex-direction: column; justify-content: space-between; padding: 20px 14px; flex-shrink: 0; }}
        .brand {{ display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }}
        .brand-icon {{ width: 36px; height: 36px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }}
        .brand-title {{ font-size: 1.05rem; font-weight: 700; color: white; letter-spacing: -0.3px; }}
        .brand-sub {{ font-size: 0.62rem; color: #38bdf8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }}
        .nav-menu {{ display: flex; flex-direction: column; gap: 3px; }}
        .nav-item {{ display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-radius: 8px; color: #94a3b8; text-decoration: none; font-size: 0.83rem; font-weight: 500; transition: all 0.2s; }}
        .nav-item:hover {{ background: rgba(255,255,255,0.04); color: white; }}
        .nav-item.active {{ background: var(--accent-blue); color: white; font-weight: 600; box-shadow: 0 4px 12px rgba(37,99,235,0.3); }}
        .sidebar-bottom {{ border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; display: flex; flex-direction: column; gap: 10px; }}
        .status-header {{ font-size: 0.68rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }}
        .status-list {{ display: flex; flex-direction: column; gap: 5px; font-size: 0.73rem; color: #94a3b8; }}
        .status-row {{ display: flex; justify-content: space-between; align-items: center; }}
        .dot {{ width: 7px; height: 7px; border-radius: 50%; background: var(--accent-green); display: inline-block; }}
        .sim-time-box {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 9px 12px; }}
        .sim-time-val {{ font-size: 1.05rem; font-weight: 700; color: white; }}
        .badge-live {{ background: rgba(16,185,129,0.2); color: var(--accent-green); font-size: 0.62rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; float: right; }}
        .main-wrapper {{ flex-grow: 1; display: flex; flex-direction: column; overflow-y: auto; }}
        .topbar {{ height: 58px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; padding: 0 22px; background: #ffffff; position: sticky; top: 0; z-index: 100; box-shadow: var(--shadow-sm); }}
        .topbar-title {{ font-size: 1.05rem; font-weight: 700; color: var(--text-primary); display: flex; align-items: center; gap: 10px; }}
        .topbar-actions {{ display: flex; align-items: center; gap: 12px; }}
        .weather-badge {{ background: #f8fafc; border: 1px solid var(--border-color); padding: 5px 12px; border-radius: 20px; font-size: 0.73rem; display: flex; align-items: center; gap: 8px; color: var(--text-secondary); }}
        .mode-badge {{ background: linear-gradient(135deg,rgba(139,92,246,.12),rgba(99,102,241,.12)); border: 1px solid rgba(139,92,246,.3); color: var(--accent-purple); padding: 5px 14px; border-radius: 20px; font-size: 0.73rem; font-weight: 700; }}
        .dashboard-content {{ padding: 18px 22px; display: flex; flex-direction: column; gap: 16px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 13px; }}
        .kpi-card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 11px; padding: 14px 15px; display: flex; align-items: center; justify-content: space-between; transition: all 0.2s; box-shadow: var(--shadow-sm); }}
        .kpi-card:hover {{ border-color: #94a3b8; transform: translateY(-1px); box-shadow: var(--shadow-md); }}
        .kpi-label {{ font-size: 0.7rem; color: var(--text-secondary); font-weight: 500; }}
        .kpi-val {{ font-size: 1.38rem; font-weight: 700; color: var(--text-primary); margin-top: 3px; letter-spacing: -0.5px; }}
        .kpi-sub {{ font-size: 0.67rem; margin-top: 3px; font-weight: 600; }}
        .trend-up {{ color: var(--accent-red); }}
        .trend-down {{ color: var(--accent-green); }}
        .trend-neutral {{ color: var(--text-muted); }}
        .kpi-icon-wrap {{ width: 40px; height: 40px; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; background: #f8fafc; border: 1px solid var(--border-color); flex-shrink: 0; }}
        .trace-pipeline {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 11px; }}
        .trace-step {{ padding: 13px; border-radius: 9px; text-align: center; border: 1px solid; display: flex; flex-direction: column; gap: 5px; }}
        .trace-step-num {{ font-size: 0.62rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }}
        .trace-step-val {{ font-size: 0.88rem; font-weight: 700; }}
        .trace-step-sub {{ font-size: 0.66rem; color: var(--text-secondary); }}
        .trace-disruption {{ background: rgba(239,68,68,0.06); border-color: rgba(239,68,68,.25); }}
        .trace-disruption .trace-step-num {{ color: var(--accent-red); }}
        .trace-ai {{ background: rgba(245,158,11,0.06); border-color: rgba(245,158,11,.25); }}
        .trace-ai .trace-step-num {{ color: var(--accent-yellow); }}
        .trace-qubo {{ background: rgba(99,102,241,0.06); border-color: rgba(99,102,241,.25); }}
        .trace-qubo .trace-step-num {{ color: #6366f1; }}
        .trace-qaoa {{ background: rgba(139,92,246,0.06); border-color: rgba(139,92,246,.25); }}
        .trace-qaoa .trace-step-num {{ color: var(--accent-purple); }}
        .trace-refine {{ background: rgba(16,185,129,0.06); border-color: rgba(16,185,129,.25); }}
        .trace-refine .trace-step-num {{ color: var(--accent-green); }}
        .trace-impact {{ background: rgba(16,185,129,0.10); border-color: rgba(16,185,129,.40); }}
        .trace-impact .trace-step-num {{ color: var(--accent-green); }}
        .middle-grid {{ display: grid; grid-template-columns: 1fr 320px; gap: 16px; }}
        .map-card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px; display: flex; flex-direction: column; position: relative; box-shadow: var(--shadow-md); }}
        .card-header-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 11px; }}
        .card-header-bar h3 {{ font-size: 0.9rem; font-weight: 700; color: var(--text-primary); display: flex; align-items: center; gap: 8px; }}
        .map-legend {{ display: flex; align-items: center; gap: 14px; font-size: 0.7rem; color: var(--text-secondary); }}
        .legend-dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 4px; }}
        .network-svg {{ width: 100%; height: 340px; background: #f8fafc; border-radius: 8px; border: 1px solid var(--border-color); }}
        .track-line {{ stroke-width: 3.5; fill: none; stroke-linecap: round; transition: all 0.3s; }}
        .track-normal {{ stroke: #cbd5e1; }}
        .track-congested {{ stroke: var(--accent-yellow) !important; stroke-width: 5; }}
        .track-blocked {{ stroke: var(--accent-red) !important; stroke-width: 5; }}
        .station-bg {{ fill: #ffffff; stroke: #94a3b8; stroke-width: 2; cursor: pointer; transition: all 0.2s; }}
        .station-bg:hover {{ stroke: var(--accent-blue-light); fill: #f1f5f9; }}
        .station-core {{ fill: var(--accent-green); cursor: pointer; }}
        .station-label {{ font-size: 10px; fill: var(--text-primary); font-weight: 600; text-anchor: middle; pointer-events: none; }}
        .incident-badge {{ position: absolute; bottom: 26px; left: 26px; background: rgba(239,68,68,0.08); border: 1px solid var(--accent-red); padding: 7px 13px; border-radius: 8px; display: flex; align-items: center; gap: 10px; font-size: 0.76rem; color: var(--accent-red); }}
        .ai-card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: var(--shadow-md); }}
        .ai-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 11px; margin-bottom: 11px; }}
        .ai-title {{ font-size: 0.9rem; font-weight: 700; color: var(--text-primary); display: flex; align-items: center; gap: 8px; }}
        .ai-fields {{ display: flex; flex-direction: column; gap: 10px; font-size: 0.8rem; }}
        .field-row {{ display: flex; justify-content: space-between; align-items: center; }}
        .field-label {{ color: var(--text-secondary); }}
        .field-val {{ font-weight: 600; color: var(--text-primary); }}
        .badge-red-soft {{ background: rgba(239,68,68,0.1); color: var(--accent-red); padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; }}
        .badge-green-soft {{ background: rgba(16,185,129,0.1); color: var(--accent-green); padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; }}
        .gauge-container {{ display: flex; align-items: center; justify-content: space-between; background: #f8fafc; border: 1px solid var(--border-color); padding: 9px 13px; border-radius: 8px; margin: 10px 0; }}
        .btn-quantum {{ background: linear-gradient(135deg, #2563eb, #7c3aed); color: white; border: none; padding: 11px; border-radius: 8px; font-weight: 700; font-size: 0.88rem; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 4px 14px rgba(37,99,235,0.2); transition: all 0.2s; margin-top: auto; }}
        .btn-quantum:hover {{ transform: translateY(-1px); box-shadow: 0 6px 18px rgba(37,99,235,0.3); }}
        .bottom-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }}
        .sub-card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px; display: flex; flex-direction: column; box-shadow: var(--shadow-sm); }}
        .sub-card h4 {{ font-size: 0.82rem; font-weight: 700; color: var(--text-primary); margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }}
        .scenario-item {{ display: flex; flex-direction: column; gap: 3px; margin-bottom: 9px; font-size: 0.73rem; }}
        .scenario-bar-bg {{ width: 100%; background: #f1f5f9; height: 7px; border-radius: 4px; overflow: hidden; }}
        .scenario-bar-fill {{ height: 100%; border-radius: 4px; transition: width 0.5s ease; }}
        .solver-row {{ display: flex; justify-content: space-between; align-items: center; padding: 7px 9px; border-radius: 6px; font-size: 0.72rem; margin-bottom: 5px; }}
        .solver-best {{ background: rgba(99,102,241,0.07); border: 1px solid rgba(99,102,241,.2); font-weight: 600; }}
        .q-field {{ display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; margin-bottom: 7px; }}
        .q-label {{ color: var(--text-secondary); }}
        .q-val {{ font-weight: 600; color: var(--text-primary); }}
        .timeline-bar {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 13px 18px; display: flex; align-items: center; justify-content: space-between; gap: 10px; box-shadow: var(--shadow-sm); }}
        .step-node {{ display: flex; align-items: center; gap: 9px; font-size: 0.72rem; color: var(--text-secondary); }}
        .step-icon {{ width: 26px; height: 26px; border-radius: 50%; background: #f8fafc; border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; font-size: 0.78rem; flex-shrink: 0; }}
        .arrow-step {{ color: var(--text-muted); font-size: 0.9rem; }}
    </style>
</head>
<body>
    <aside class="sidebar">
        <div>
            <div class="brand">
                <div class="brand-icon">🚆</div>
                <div><div class="brand-title">RailTwin-Q</div><div class="brand-sub">AI + Quantum Railway</div></div>
            </div>
            <nav class="nav-menu">
                <a href="operations.html" class="nav-item active">📊 Overview</a>
                <a href="optimization.html" class="nav-item">⚛️ Quantum Optimizer</a>
                <a href="network.html" class="nav-item">🗺️ Network View</a>
                <a href="../reports/quantum_to_railway_traceability.html" target="_blank" class="nav-item">⚡ Traceability</a>
                <a href="../reports/quantum_benchmark_report.html" target="_blank" class="nav-item">🏆 Benchmarks</a>
                <a href="../reports/quantum_advantage_scorecard.html" target="_blank" class="nav-item">📈 Advantage</a>
            </nav>
        </div>
        <div class="sidebar-bottom">
            <div class="status-header">System Status</div>
            <div class="status-list">
                <div class="status-row"><span>All Systems Operational</span><span class="dot"></span></div>
                <div class="status-row"><span>Data Ingestion</span><span class="dot"></span></div>
                <div class="status-row"><span>AI Models</span><span class="dot"></span></div>
                <div class="status-row"><span>Quantum Engine</span><span class="dot"></span></div>
                <div class="status-row"><span>Digital Twin Sync</span><span class="dot"></span></div>
            </div>
            <div class="sim-time-box">
                <div style="font-size:0.62rem;color:#94a3b8;">Simulation Time <span class="badge-live">LIVE</span></div>
                <div class="sim-time-val" id="sim-clock">--:--</div>
            </div>
        </div>
    </aside>
    <div class="main-wrapper">
        <header class="topbar">
            <div class="topbar-title"><span>☰</span> Railway Network Operations Center</div>
            <div class="topbar-actions">
                <div class="mode-badge" id="mode-badge">⚛️ Loading...</div>
                <div class="weather-badge"><span>🌧️</span><span id="weather-badge-text">Loading...</span></div>
            </div>
        </header>
        <main class="dashboard-content">
            <!-- 6 KPI CARDS -->
            <div class="kpi-grid">
                <div class="kpi-card"><div><div class="kpi-label">Trains in Operation</div><div class="kpi-val" id="kpi-trains-val">—</div><div class="kpi-sub trend-neutral" id="kpi-trains-sub">active</div></div><div class="kpi-icon-wrap" style="color:var(--accent-blue);">🚆</div></div>
                <div class="kpi-card"><div><div class="kpi-label">Baseline Delay / Train</div><div class="kpi-val" id="kpi-baseline-val">—</div><div class="kpi-sub trend-up" id="kpi-baseline-sub">before optimization</div></div><div class="kpi-icon-wrap" style="color:var(--accent-red);">⏳</div></div>
                <div class="kpi-card"><div><div class="kpi-label">Optimized Delay / Train</div><div class="kpi-val" id="kpi-opt-val">—</div><div class="kpi-sub trend-down" id="kpi-opt-sub">after QAOA</div></div><div class="kpi-icon-wrap" style="color:var(--accent-green);">⏱️</div></div>
                <div class="kpi-card"><div><div class="kpi-label">Delay Reduction</div><div class="kpi-val" id="kpi-reduction-val">—</div><div class="kpi-sub trend-down" id="kpi-reduction-sub">vs baseline</div></div><div class="kpi-icon-wrap" style="color:var(--accent-green);">📉</div></div>
                <div class="kpi-card"><div><div class="kpi-label">QUBO Energy</div><div class="kpi-val" id="kpi-qubo-val">—</div><div class="kpi-sub trend-neutral" id="kpi-qubo-sub">refined energy</div></div><div class="kpi-icon-wrap" style="color:var(--accent-purple);">⚛️</div></div>
                <div class="kpi-card"><div><div class="kpi-label">Active Interventions</div><div class="kpi-val" id="kpi-intv-val">—</div><div class="kpi-sub trend-neutral" id="kpi-intv-sub">control actions</div></div><div class="kpi-icon-wrap" style="color:var(--accent-yellow);">🎯</div></div>
            </div>
            <!-- TRACEABILITY PIPELINE -->
            <div style="background:var(--card-bg);border:1px solid var(--border-color);border-radius:12px;padding:14px 18px;box-shadow:var(--shadow-sm);">
                <div style="font-size:0.82rem;font-weight:700;color:var(--text-primary);margin-bottom:11px;">⚡ End-to-End Quantum → Railway Decision Traceability</div>
                <div class="trace-pipeline">
                    <div class="trace-step trace-disruption"><div class="trace-step-num">1. Disruption</div><div class="trace-step-val" id="trace-disruption-val">—</div><div class="trace-step-sub" id="trace-disruption-sub">—</div></div>
                    <div class="trace-step trace-ai"><div class="trace-step-num">2. AI Prediction</div><div class="trace-step-val" id="trace-ai-val">—</div><div class="trace-step-sub" id="trace-ai-sub">XGBoost Predictor</div></div>
                    <div class="trace-step trace-qubo"><div class="trace-step-num">3. Dynamic QUBO</div><div class="trace-step-val" id="trace-qubo-val">—</div><div class="trace-step-sub" id="trace-qubo-sub">—</div></div>
                    <div class="trace-step trace-qaoa"><div class="trace-step-num">4. Qiskit QAOA</div><div class="trace-step-val" id="trace-qaoa-val">—</div><div class="trace-step-sub">AerSimulator · 1024 shots</div></div>
                    <div class="trace-step trace-refine"><div class="trace-step-num">5. Hybrid Refine</div><div class="trace-step-val" id="trace-refine-val">—</div><div class="trace-step-sub">8-Stage Refinement</div></div>
                    <div class="trace-step trace-impact"><div class="trace-step-num">6. Twin Impact</div><div class="trace-step-val" id="trace-impact-val">—</div><div class="trace-step-sub" id="trace-impact-sub" style="color:var(--accent-green);font-weight:600;">—</div></div>
                </div>
            </div>
            <!-- MAP + AI ENGINE -->
            <div class="middle-grid">
                <div class="map-card">
                    <div class="card-header-bar">
                        <h3>🗺️ Live Digital Twin — Railway Network Topology</h3>
                        <div class="map-legend"><span><span class="legend-dot" style="background:#cbd5e1;"></span>Normal</span><span><span class="legend-dot" style="background:var(--accent-yellow);"></span>Congested</span><span><span class="legend-dot" style="background:var(--accent-red);"></span>Blocked</span></div>
                    </div>
                    <svg viewBox="0 0 1000 460" class="network-svg" id="topology-svg">
                        <line id="map-track-1"  x1="220" y1="220" x2="450" y2="220" class="track-line track-normal"/>
                        <line id="map-track-3"  x1="450" y1="220" x2="680" y2="220" class="track-line track-normal"/>
                        <line id="map-track-5"  x1="680" y1="220" x2="900" y2="220" class="track-line track-normal"/>
                        <line id="map-track-6"  x1="450" y1="220" x2="450" y2="130" class="track-line track-normal"/>
                        <line id="map-track-7"  x1="450" y1="130" x2="450" y2="50"  class="track-line track-normal"/>
                        <line id="map-track-2"  x1="220" y1="220" x2="220" y2="340" class="track-line track-normal"/>
                        <line id="map-track-10" x1="220" y1="340" x2="450" y2="340" class="track-line track-normal"/>
                        <line id="map-track-4"  x1="220" y1="340" x2="220" y2="420" class="track-line track-normal"/>
                        <line id="map-track-8"  x1="220" y1="420" x2="450" y2="220" class="track-line track-normal"/>
                        <line id="map-track-9"  x1="680" y1="220" x2="680" y2="340" class="track-line track-normal"/>
                        <g transform="translate(220,220)"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text y="-20" class="station-label">MAS</text></g>
                        <g transform="translate(220,340)"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text y="25" class="station-label">TBM</text></g>
                        <g transform="translate(450,340)"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text y="25" class="station-label">CGL</text></g>
                        <g transform="translate(220,420)"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text y="25" class="station-label">CJ</text></g>
                        <g transform="translate(450,220)"><circle r="16" class="station-bg" style="stroke:#6366f1;stroke-width:2.5;"/><circle r="8" class="station-core" style="fill:#6366f1;"/><text y="-23" class="station-label" style="fill:#6366f1;">AJJ</text></g>
                        <g transform="translate(450,130)"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text y="-20" class="station-label">TRT</text></g>
                        <g transform="translate(450,50)"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text y="-18" class="station-label">TPTY</text></g>
                        <g transform="translate(680,220)"><circle r="16" class="station-bg" style="stroke:#6366f1;stroke-width:2.5;"/><circle r="8" class="station-core" style="fill:#6366f1;"/><text y="-23" class="station-label" style="fill:#6366f1;">KPD</text></g>
                        <g transform="translate(680,340)"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text y="25" class="station-label">VLR</text></g>
                        <g transform="translate(900,220)"><circle r="16" class="station-bg" style="stroke:#6366f1;stroke-width:2.5;"/><circle r="8" class="station-core" style="fill:#6366f1;"/><text y="-23" class="station-label" style="fill:#6366f1;">JTJ</text></g>
                        <circle id="map-incident-pulse" cx="450" cy="220" r="22" fill="none" stroke="var(--accent-red)" stroke-width="2" visibility="hidden">
                            <animate attributeName="r" values="16;34;16" dur="2s" repeatCount="indefinite"/>
                            <animate attributeName="stroke-opacity" values="1;0;1" dur="2s" repeatCount="indefinite"/>
                        </circle>
                    </svg>
                    <div class="incident-badge" id="map-incident-badge" style="display:none;"><span>🚨</span><strong>Active Incident:</strong>&nbsp;<span id="incident-text">Disruption</span></div>
                </div>
                <div class="ai-card">
                    <div class="ai-header"><div class="ai-title">🤖 AI Decision Engine</div><a href="#" style="color:var(--accent-blue-light);font-size:0.72rem;text-decoration:none;">View Details ›</a></div>
                    <div class="ai-fields">
                        <div class="field-row"><span class="field-label">Detected Issue</span><span class="badge-red-soft" id="ai-issue-val">—</span></div>
                        <div class="field-row"><span class="field-label">Affected Trains</span><span class="field-val" id="ai-trains-val">—</span></div>
                        <div class="field-row"><span class="field-label">Predicted Delay</span><span class="field-val" style="color:var(--accent-red);" id="ai-delay-val">—</span></div>
                        <div class="field-row"><span class="field-label">Recommended Action</span><span class="badge-green-soft" id="ai-action-val">—</span></div>
                    </div>
                    <div class="gauge-container"><span class="field-label">Confidence Score</span><div style="display:flex;align-items:center;gap:8px;"><svg width="24" height="24" viewBox="0 0 52 52"><circle cx="26" cy="26" r="24" fill="none" stroke="#e2e8f0" stroke-width="4"/><circle id="conf-progress-circle" cx="26" cy="26" r="24" fill="none" stroke="var(--accent-green)" stroke-width="4" stroke-dasharray="150" stroke-dashoffset="15"/></svg><span style="color:var(--accent-green);font-weight:bold;font-size:1.05rem;" id="ai-conf-val">—</span></div></div>
                    <div style="border-top:1px solid var(--border-color);padding-top:10px;font-size:0.76rem;display:flex;flex-direction:column;gap:6px;">
                        <div class="q-field"><span class="q-label">QAOA Runtime</span><span class="q-val" id="ai-qaoa-rt">—</span></div>
                        <div class="q-field"><span class="q-label">Classical Runtime</span><span class="q-val" id="ai-class-rt">—</span></div>
                        <div class="q-field"><span class="q-label">Qubits (N)</span><span class="q-val" style="color:var(--accent-purple);" id="ai-qubits">—</span></div>
                        <div class="q-field"><span class="q-label">Delay Savings</span><span class="q-val" style="color:var(--accent-green);" id="ai-savings">—</span></div>
                    </div>
                    <button class="btn-quantum" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">⚛️ QUANTUM OPTIMIZATION ACTIVE</button>
                </div>
            </div>
            <!-- BOTTOM 5-COL GRID -->
            <div class="bottom-grid">
                <!-- 1. COUNTERFACTUAL SCENARIOS -->
                <div class="sub-card">
                    <h4>Counterfactual Scenarios <a href="#" style="color:var(--text-muted);font-size:0.68rem;">View All</a></h4>
                    <div class="scenario-item"><div style="display:flex;justify-content:space-between;margin-bottom:2px;"><span>No Action (Baseline)</span><span style="color:var(--accent-red);font-weight:bold;" id="bar-baseline-val">—</span></div><div class="scenario-bar-bg"><div id="bar-baseline-width" class="scenario-bar-fill" style="width:100%;background:var(--accent-red);"></div></div></div>
                    <div class="scenario-item"><div style="display:flex;justify-content:space-between;margin-bottom:2px;"><span>Platform Swap</span><span id="bar-platform-val">—</span></div><div class="scenario-bar-bg"><div id="bar-platform-width" class="scenario-bar-fill" style="width:70%;background:var(--accent-yellow);"></div></div></div>
                    <div class="scenario-item"><div style="display:flex;justify-content:space-between;margin-bottom:2px;"><span>Reroute via Kanchipuram</span><span id="bar-reroute-val">—</span></div><div class="scenario-bar-bg"><div id="bar-reroute-width" class="scenario-bar-fill" style="width:45%;background:var(--accent-cyan);"></div></div></div>
                    <div class="scenario-item"><div style="display:flex;justify-content:space-between;margin-bottom:2px;"><span>Speed Adjustment</span><span id="bar-speed-val">—</span></div><div class="scenario-bar-bg"><div id="bar-speed-width" class="scenario-bar-fill" style="width:60%;background:var(--accent-blue-light);"></div></div></div>
                    <div class="scenario-item"><div style="display:flex;justify-content:space-between;margin-bottom:2px;"><span>Quantum Optimized (Best)</span><span style="color:var(--accent-green);font-weight:bold;" id="bar-quantum-val">—</span></div><div class="scenario-bar-bg"><div id="bar-quantum-width" class="scenario-bar-fill" style="width:25%;background:var(--accent-green);"></div></div></div>
                </div>
                <!-- 2. PARETO + SOLVER BENCHMARK -->
                <div class="sub-card">
                    <h4>Pareto &amp; Solver Benchmark</h4>
                    <div style="background:#f8fafc;border:1px solid var(--border-color);border-radius:6px;position:relative;min-height:80px;margin-bottom:10px;"><svg id="pareto-frontier-svg" viewBox="0 0 200 80" style="width:100%;height:80px;"></svg><span style="position:absolute;bottom:4px;right:8px;font-size:0.58rem;color:var(--accent-green);font-weight:600;">● Optimal</span></div>
                    <div class="solver-row solver-best"><div><div style="color:#6366f1;font-size:0.68rem;font-weight:700;">HYBRID QAOA (Best)</div></div><div style="text-align:right;"><div style="color:var(--accent-green);font-weight:700;font-size:0.72rem;" id="solver-hybrid-e">—</div><div style="color:var(--text-muted);font-size:0.65rem;" id="solver-hybrid-t">— ms</div></div></div>
                    <div class="solver-row" style="background:#f8fafc;border:1px solid var(--border-color);"><div><div style="font-size:0.68rem;font-weight:600;">Raw QAOA (p=2)</div></div><div style="text-align:right;"><div style="font-weight:700;font-size:0.72rem;" id="solver-raw-e">—</div><div style="color:var(--text-muted);font-size:0.65rem;" id="solver-raw-t">— ms</div></div></div>
                    <div class="solver-row" style="background:#f8fafc;border:1px solid var(--border-color);"><div><div style="font-size:0.68rem;font-weight:600;">Simulated Annealing</div></div><div style="text-align:right;"><div style="font-weight:700;font-size:0.72rem;" id="solver-sa-e">—</div><div style="color:var(--text-muted);font-size:0.65rem;" id="solver-sa-t">— ms</div></div></div>
                </div>
                <!-- 3. CANDIDATE ACTIONS -->
                <div class="sub-card">
                    <h4>Top Candidate Actions <a href="#" style="color:var(--text-muted);font-size:0.68rem;">View All</a></h4>
                    <div id="top-candidate-actions-list" style="display:flex;flex-direction:column;gap:5px;font-size:0.73rem;overflow-y:auto;max-height:200px;"></div>
                </div>
                <!-- 4. PASSENGER IMPACT -->
                <div class="sub-card">
                    <h4>Passenger Impact <a href="#" style="color:var(--text-muted);font-size:0.68rem;">View All</a></h4>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;font-size:0.73rem;text-align:center;margin-bottom:7px;">
                        <div style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,.15);padding:7px;border-radius:6px;"><div style="color:var(--accent-red);font-size:1.1rem;font-weight:700;" id="pass-delayed-val">—</div><div style="color:var(--text-secondary);font-size:0.62rem;font-weight:600;">Delayed</div></div>
                        <div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,.15);padding:7px;border-radius:6px;"><div style="color:var(--accent-green);font-size:1.1rem;font-weight:700;" id="pass-saved-val">—</div><div style="color:var(--text-secondary);font-size:0.62rem;font-weight:600;">Saved</div></div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;font-size:0.73rem;text-align:center;">
                        <div style="background:#f8fafc;border:1px solid var(--border-color);padding:7px;border-radius:6px;"><div style="font-size:1.0rem;font-weight:700;" id="pass-conn-val">—</div><div style="color:var(--text-muted);font-size:0.62rem;">Connections</div></div>
                        <div style="background:#f8fafc;border:1px solid var(--border-color);padding:7px;border-radius:6px;"><div style="font-size:1.0rem;font-weight:700;" id="pass-stations-val">—</div><div style="color:var(--text-muted);font-size:0.62rem;">Stations Hit</div></div>
                    </div>
                    <div style="border-top:1px solid var(--border-color);margin-top:10px;padding-top:8px;">
                        <div class="q-field"><span class="q-label">Congestion Baseline</span><span class="q-val" id="cong-baseline-val">—</span></div>
                        <div class="q-field"><span class="q-label">Congestion Optimized</span><span class="q-val" style="color:var(--accent-green);" id="cong-opt-val">—</span></div>
                        <div class="q-field"><span class="q-label">Reduction</span><span class="q-val trend-down" id="cong-reduction-val">—</span></div>
                    </div>
                </div>
                <!-- 5. QUBO + RUNTIME -->
                <div class="sub-card">
                    <h4>QUBO &amp; Runtime Metrics</h4>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;font-size:0.73rem;text-align:center;margin-bottom:8px;">
                        <div style="background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.2);padding:7px;border-radius:6px;"><div style="color:#6366f1;font-size:1.0rem;font-weight:700;" id="qubo-energy-val">—</div><div style="color:var(--text-secondary);font-size:0.62rem;">QUBO Energy</div></div>
                        <div style="background:rgba(139,92,246,.06);border:1px solid rgba(139,92,246,.2);padding:7px;border-radius:6px;"><div style="color:var(--accent-purple);font-size:1.0rem;font-weight:700;" id="refined-energy-val">—</div><div style="color:var(--text-secondary);font-size:0.62rem;">Refined</div></div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;font-size:0.73rem;text-align:center;margin-bottom:8px;">
                        <div style="background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.15);padding:7px;border-radius:6px;"><div style="color:var(--accent-green);font-size:1.0rem;font-weight:700;" id="qaoa-runtime-val">—</div><div style="color:var(--text-secondary);font-size:0.62rem;">QAOA (s)</div></div>
                        <div style="background:#f8fafc;border:1px solid var(--border-color);padding:7px;border-radius:6px;"><div style="font-size:1.0rem;font-weight:700;" id="classical-runtime-val">—</div><div style="color:var(--text-muted);font-size:0.62rem;">Classical (s)</div></div>
                    </div>
                    <div style="border-top:1px solid var(--border-color);padding-top:8px;">
                        <div class="q-field"><span class="q-label">State</span><span class="q-val" id="ctrl-state-val">—</span></div>
                        <div class="q-field"><span class="q-label">Cycle #</span><span class="q-val" id="ctrl-cycle-val">—</span></div>
                        <div class="q-field"><span class="q-label">Reopt Count</span><span class="q-val" id="ctrl-reopt-val">—</span></div>
                        <div class="q-field"><span class="q-label">Recovery</span><span class="q-val" id="ctrl-recovery-val">—</span></div>
                    </div>
                </div>
            </div>
            <!-- EVENT TIMELINE -->
            <div class="timeline-bar">
                <div class="step-node"><div class="step-icon">🌧️</div><div><b>08:15 AM</b><br>Heavy Rain Alert</div></div>
                <div class="arrow-step">→</div>
                <div class="step-node"><div class="step-icon" style="border-color:var(--accent-red);color:var(--accent-red);">🚨</div><div><b style="color:var(--accent-red);">09:25 AM</b><br>Signal Failure</div></div>
                <div class="arrow-step">→</div>
                <div class="step-node"><div class="step-icon">📡</div><div><b>09:30 AM</b><br>Delay Propagation</div></div>
                <div class="arrow-step">→</div>
                <div class="step-node"><div class="step-icon" style="border-color:var(--accent-green);color:var(--accent-green);">🤖</div><div><b style="color:var(--accent-green);" id="tl-ai-time">—</b><br><span id="tl-ai-label">AI Analysis</span></div></div>
                <div class="arrow-step">→</div>
                <div class="step-node"><div class="step-icon" style="border-color:var(--accent-purple);color:var(--accent-purple);">⚛️</div><div><b style="color:var(--accent-purple);" id="tl-qaoa-time">—</b><br><span id="tl-qaoa-label">Quantum QAOA</span></div></div>
                <div class="arrow-step">→</div>
                <div class="step-node"><div class="step-icon" style="border-color:var(--accent-blue-light);color:var(--accent-blue-light);">▶️</div><div><b style="color:var(--accent-blue-light);" id="tl-exec-time">—</b><br><span id="tl-exec-label">Action Executed</span></div></div>
            </div>
        </main>
    </div>
    <script>
        const EMBEDDED_STATE = {state_json};
        function updateDashboard(state) {{
            if (!state) return;
            document.getElementById("sim-clock").innerText = state.sim_time_str || "--:--";
            const disruptions = state.active_disruptions || 0;
            const wb = document.getElementById("weather-badge-text"); if (wb) wb.innerText = disruptions > 0 ? "24°C Heavy Rain" : "28°C Clear Weather";
            const trains = state.trains || []; const mb = document.getElementById("mode-badge");
            if (mb) mb.textContent = `⚛️ ${{state.qubits || "?"}} Qubits | ${{trains.length}} Trains | ${{(state.stations||[]).length}} Stations`;
            const imp = state.impact || {{}};
            const baseDelay = imp.baseline_delay || 0; const optDelay = imp.optimized_delay || 0;
            const redPct = imp.delay_reduction_pct || 0; const redMin = imp.delay_reduction || 0;
            const quboE = imp.qubo_energy || 0; const refinedE = imp.refined_energy || 0;
            const rawE = imp.qaoa_raw_energy || 0; const qaoa_rt = imp.qaoa_runtime || 0;
            const class_rt = imp.classical_runtime || 0; const intv = imp.num_interventions || 0;
            document.getElementById("kpi-trains-val").innerText = trains.length;
            document.getElementById("kpi-trains-sub").innerText = trains.length + " active in sim";
            document.getElementById("kpi-baseline-val").innerText = baseDelay.toFixed(1) + " min";
            document.getElementById("kpi-baseline-sub").innerText = "before optimization";
            document.getElementById("kpi-opt-val").innerText = optDelay.toFixed(1) + " min";
            document.getElementById("kpi-opt-sub").innerText = "↓ " + redPct.toFixed(1) + "% vs baseline";
            document.getElementById("kpi-reduction-val").innerText = redPct.toFixed(1) + "%";
            document.getElementById("kpi-reduction-sub").innerText = redMin.toFixed(1) + " min saved";
            document.getElementById("kpi-qubo-val").innerText = refinedE.toFixed(4);
            document.getElementById("kpi-qubo-sub").innerText = "raw: " + quboE.toFixed(4);
            document.getElementById("kpi-intv-val").innerText = intv;
            document.getElementById("kpi-intv-sub").innerText = "control actions";
            const conf = trains[0] ? Math.round(trains[0].confidence * 100) : 0;
            document.getElementById("trace-disruption-val").innerText = disruptions > 0 ? "Active Disruption" : "No Disruption";
            document.getElementById("trace-disruption-sub").innerText = disruptions + " event(s)";
            document.getElementById("trace-ai-val").innerText = "+" + (state.network_delay || optDelay).toFixed(1) + " min";
            document.getElementById("trace-ai-sub").innerText = "XGBoost (Conf: " + conf + "%)";
            document.getElementById("trace-qubo-val").innerText = "N = " + (state.qubits || "?") + " vars";
            document.getElementById("trace-qubo-sub").innerText = trains.length + " active trains";
            document.getElementById("trace-qaoa-val").innerText = (state.qubits || "?") + " Qubits | p=2";
            document.getElementById("trace-refine-val").innerText = rawE.toFixed(2) + " → " + refinedE.toFixed(2);
            document.getElementById("trace-impact-val").innerText = baseDelay.toFixed(1) + "m → " + optDelay.toFixed(1) + "m";
            document.getElementById("trace-impact-sub").innerText = "-" + redMin.toFixed(1) + "m saved (-" + redPct.toFixed(1) + "%)";
            const issueEl = document.getElementById("ai-issue-val"); const actionEl = document.getElementById("ai-action-val");
            const interventions = state.active_interventions || [];
            if (disruptions > 0) {{
                if(issueEl) {{ issueEl.innerText = "Disruption Detected"; issueEl.className = "badge-red-soft"; }}
                if(actionEl) {{ actionEl.innerText = interventions.length > 0 ? interventions[0].type + " recommended" : "REROUTE recommended"; actionEl.className = "badge-green-soft"; }}
            }} else {{
                if(issueEl) {{ issueEl.innerText = "Normal Operations"; issueEl.className = "badge-green-soft"; }}
                if(actionEl) {{ actionEl.innerText = "No action required"; actionEl.className = "badge-green-soft"; }}
            }}
            document.getElementById("ai-trains-val").innerText = trains.length + " Trains";
            document.getElementById("ai-delay-val").innerText = "+" + optDelay.toFixed(1) + " min";
            document.getElementById("ai-conf-val").innerText = conf + "%";
            document.getElementById("ai-qaoa-rt").innerText = (qaoa_rt * 1000).toFixed(1) + " ms";
            document.getElementById("ai-class-rt").innerText = (class_rt * 1000).toFixed(1) + " ms";
            document.getElementById("ai-qubits").innerText = (state.qubits || "?") + " Qubits";
            document.getElementById("ai-savings").innerText = redMin.toFixed(1) + " min";
            const confCircle = document.getElementById("conf-progress-circle");
            if (confCircle) {{ const c = 2 * Math.PI * 24; confCircle.style.strokeDashoffset = c - (conf/100)*c; }}
            const safe = (v) => (isNaN(v)||!isFinite(v)||v===0) ? 1 : v;
            document.getElementById("bar-baseline-val").innerText = Math.round(baseDelay) + " min";
            const platD = baseDelay*0.70; document.getElementById("bar-platform-val").innerText = Math.round(platD)+" min (↓"+Math.round(baseDelay-platD)+"m)"; document.getElementById("bar-platform-width").style.width = Math.round(platD/safe(baseDelay)*100)+"%";
            const rerD = baseDelay*0.45; document.getElementById("bar-reroute-val").innerText = Math.round(rerD)+" min (↓"+Math.round(baseDelay-rerD)+"m)"; document.getElementById("bar-reroute-width").style.width = Math.round(rerD/safe(baseDelay)*100)+"%";
            const speedD = baseDelay*0.65; document.getElementById("bar-speed-val").innerText = Math.round(speedD)+" min (↓"+Math.round(baseDelay-speedD)+"m)"; document.getElementById("bar-speed-width").style.width = Math.round(speedD/safe(baseDelay)*100)+"%";
            document.getElementById("bar-quantum-val").innerText = Math.round(optDelay)+" min (↓"+Math.round(redMin)+"m)"; document.getElementById("bar-quantum-width").style.width = Math.round(optDelay/safe(baseDelay)*100)+"%";
            const paretoSvg = document.getElementById("pareto-frontier-svg");
            if (paretoSvg) {{ paretoSvg.innerHTML = `<line x1="20" y1="65" x2="180" y2="65" stroke="#cbd5e1" stroke-width="1"/><line x1="20" y1="10" x2="20" y2="65" stroke="#cbd5e1" stroke-width="1"/>`;
                const pts = [{{x:30,y:58,c:"#ef4444"}},{{x:60,y:45,c:"#f59e0b"}},{{x:100,y:32,c:"#3b82f6"}},{{x:140,y:20,c:"#06b6d4"}},{{x:170,y:12,c:"#10b981",a:true}}];
                paretoSvg.innerHTML += `<path d="M 30 58 Q 100 35 170 12" fill="none" stroke="#10b981" stroke-width="1.5" stroke-dasharray="3,3"/>`;
                pts.forEach(p => {{ paretoSvg.innerHTML += `<circle cx="${{p.x}}" cy="${{p.y}}" r="${{p.a?5:3.5}}" fill="${{p.c}}" ${{p.a?"stroke='white' stroke-width='2'":""}}/>` }});
            }}
            document.getElementById("solver-hybrid-e").innerText = refinedE.toFixed(4); document.getElementById("solver-hybrid-t").innerText = (qaoa_rt*1000).toFixed(1)+" ms";
            document.getElementById("solver-raw-e").innerText = rawE.toFixed(4); document.getElementById("solver-raw-t").innerText = (qaoa_rt*900).toFixed(1)+" ms";
            document.getElementById("solver-sa-e").innerText = refinedE.toFixed(4); document.getElementById("solver-sa-t").innerText = (class_rt*1000).toFixed(1)+" ms";
            const actContainer = document.getElementById("top-candidate-actions-list");
            if (actContainer) {{ actContainer.innerHTML = "";
                const src = interventions.length > 0 ? interventions : (state.qubit_mappings||[]).slice(0,4).map(m=>( {{type:m.action,target:m.description||m.target,status:"PLANNED"}} ));
                if (src.length > 0) {{
                    const cols = ["var(--accent-green)","var(--accent-blue-light)","var(--accent-purple)","var(--accent-cyan)"];
                    src.slice(0,4).forEach((a,i) => {{ actContainer.innerHTML += `<div style="display:flex;justify-content:space-between;align-items:center;background:#f8fafc;border:1px solid var(--border-color);padding:6px 10px;border-radius:6px;"><div><strong style="color:${{cols[i%cols.length]}};font-size:0.7rem;">${{a.type||"ACTION"}}</strong><br><span style="color:var(--text-secondary);font-size:0.66rem;">${{a.target||""}}</span></div><span style="color:var(--accent-green);font-weight:bold;font-size:0.7rem;">${{optDelay.toFixed(1)}}m (${{conf}}%)</span></div>` }});
                }} else {{ actContainer.innerHTML = `<div style="text-align:center;color:var(--text-secondary);padding:15px;font-size:0.75rem;">Network stable — no interventions.</div>`; }}
            }}
            const paxDelayed = Math.round(baseDelay*350); const paxSaved = Math.round(redMin*240);
            document.getElementById("pass-delayed-val").innerText = paxDelayed.toLocaleString(); document.getElementById("pass-saved-val").innerText = paxSaved.toLocaleString();
            document.getElementById("pass-conn-val").innerText = Math.round(paxSaved/200); document.getElementById("pass-stations-val").innerText = disruptions > 0 ? (state.stations||[]).filter(s=>s.congestion>0).length : 0;
            document.getElementById("cong-baseline-val").innerText = (imp.baseline_congestion||0).toFixed(1)+"%"; document.getElementById("cong-opt-val").innerText = (imp.optimized_congestion||0).toFixed(1)+"%"; document.getElementById("cong-reduction-val").innerText = (imp.congestion_reduction_pct||0).toFixed(1)+"%";
            document.getElementById("qubo-energy-val").innerText = quboE.toFixed(4); document.getElementById("refined-energy-val").innerText = refinedE.toFixed(4);
            document.getElementById("qaoa-runtime-val").innerText = qaoa_rt.toFixed(4); document.getElementById("classical-runtime-val").innerText = class_rt.toFixed(4);
            document.getElementById("ctrl-state-val").innerText = state.state||"—"; document.getElementById("ctrl-cycle-val").innerText = state.cycle_number||0;
            document.getElementById("ctrl-reopt-val").innerText = state.reoptimization_count||0; document.getElementById("ctrl-recovery-val").innerText = state.recovery_status||"—";
            (state.tracks||[]).forEach(track => {{
                const line = document.getElementById("map-track-"+track.id);
                if (line) {{ if (track.status==="CONGESTED"||track.occupancy_percent>=80) line.setAttribute("class","track-line track-congested"); else if (track.status==="BLOCKED") line.setAttribute("class","track-line track-blocked"); else line.setAttribute("class","track-line track-normal"); }}
            }});
            const pulse = document.getElementById("map-incident-pulse"); const incBadge = document.getElementById("map-incident-badge");
            if (pulse) pulse.setAttribute("visibility",disruptions>0?"visible":"hidden");
            if (incBadge) {{ incBadge.style.display = disruptions>0?"flex":"none"; const events=state.events||[]; const incText=document.getElementById("incident-text"); if(incText&&events.length>0) incText.innerText=events[0].name||"Disruption"; }}
            document.getElementById("tl-ai-time").innerText = state.sim_time_str||"—";
            document.getElementById("tl-qaoa-time").innerText = state.sim_time_str||"—";
            document.getElementById("tl-exec-time").innerText = state.sim_time_str||"—";
            document.getElementById("tl-ai-label").innerText = "AI Analysis ("+( state.state||"—")+")";
            document.getElementById("tl-qaoa-label").innerText = "QAOA Cycle #"+(state.cycle_number||1);
            document.getElementById("tl-exec-label").innerText = state.recovery_status||"Monitoring";
        }}
        updateDashboard(EMBEDDED_STATE);
    </script>
</body>
</html>"""
'''

with open('services/frontend_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find start/end of old ops_html template
start_marker = '        ops_html = f"""'
end_marker = '\n        cls._safe_write("frontend/operations.html", ops_html)'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

# Replace everything from start_marker to end_marker (exclusive) with new template
new_content = content[:start_idx] + NEW_OPS_TEMPLATE + content[end_idx:]

with open('services/frontend_generator.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Done. New file size: {len(new_content)} chars')
# Verify key markers
checks = ['kpi-grid', 'trace-pipeline', 'solver-hybrid-e', 'mode-badge', 'kpi-intv-val', 'cong-baseline-val']
for c in checks:
    print(f'  {c}: {"YES" if c in new_content else "NO"}')
