import os

def main():
    filepath = r"c:\Users\idhay\Desktop\RailTwin-Q\services\frontend_generator.py"
    if not os.path.exists(filepath):
        print(f"Error: file not found at {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update brand subtext and icons in brand block
    old_brand = """            <div class="brand">
                <div class="brand-icon"><i data-lucide="train"></i></div>
                <div><div class="brand-title">RailTwin-Q</div><div class="brand-sub">AI + Quantum Railway</div></div>
            </div>"""
            
    new_brand = """            <div class="brand">
                <div class="brand-icon"><i data-lucide="train" style="width: 18px; height: 18px; color: #fff;"></i></div>
                <div>
                    <div class="brand-title">RailTwin-Q</div>
                    <div class="brand-sub">AI + QUANTUM RAILWAY</div>
                </div>
            </div>"""
            
    if old_brand not in content:
        print("Warning: Could not find old brand block.")
    content = content.replace(old_brand, new_brand)

    # 2. Update System Status panel and sync footer at bottom of sidebar
    old_sidebar_bottom = """        <div class="sidebar-bottom">
            <div class="status-header" style="color:#64748b;">System Status</div>
            <div class="status-list" style="color:#94a3b8;">
                <div class="status-row"><span>Ingestion Engine</span><span class="dot"></span></div>
                <div class="status-row"><span>AI Delay Projections</span><span class="dot"></span></div>
                <div class="status-row"><span>Ising Model Mapper</span><span class="dot"></span></div>
                <div class="status-row"><span>Aer QAOA Solver</span><span class="dot"></span></div>
            </div>
            <div class="sim-time-box">
                <div style="font-size:0.62rem;color:#64748b;">Operations Sync <span class="badge-live">LIVE</span></div>
                <div class="sim-time-val" id="sidebar-clock">--:--</div>
            </div>
        </div>"""

    new_sidebar_bottom = """        <div class="sidebar-bottom">
            <div class="system-status-widget">
                <div class="status-header">System Status</div>
                <div class="status-list">
                    <div class="status-row"><span>Ingestion Engine</span><span class="status-dot"></span></div>
                    <div class="status-row"><span>AI Delay Projections</span><span class="status-dot"></span></div>
                    <div class="status-row"><span>Ising Model Mapper</span><span class="status-dot"></span></div>
                    <div class="status-row"><span>Aer QAOA Solver</span><span class="status-dot"></span></div>
                </div>
                <div class="sync-pill-badge">
                    <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10b981; animation: pulse-glow 2s infinite;"></span>
                    SYSTEM ONLINE · SYNC 14ms · <span id="sidebar-clock">--:--</span>
                </div>
            </div>
        </div>"""

    if old_sidebar_bottom not in content:
        print("Warning: Could not find old sidebar bottom block.")
    content = content.replace(old_sidebar_bottom, new_sidebar_bottom)

    # 3. Update the Topbar Header
    old_topbar = """        <header class="topbar">
            <!-- Left Info -->
            <div style="display: flex; flex-direction: column;">
                <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-secondary); letter-spacing: 0.05em;">
                    RAILTWIN-Q / OPERATIONS COMMAND CENTER
                </div>
                <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px; letter-spacing: 0.05em; text-transform: uppercase;">
                    Hybrid Quantum-AI Railway Decision Intelligence
                </div>
            </div>
            <!-- Right Info Flex Container -->
            <div style="display: flex; flex-direction: row; align-items: center; gap: 8px;">
                <div style="font-size: 0.72rem; font-weight: 800; color: #065f46; display: flex; align-items: center; gap: 5px; text-transform: uppercase; background: #ecfdf5; border: 1px solid #d1fae5; padding: 4px 12px; border-radius: 12px;">
                    <span class="pulse-dot" style="width: 6px; height: 6px; border-radius: 50%; background: var(--accent-green); display: inline-block;"></span>
                    DIGITAL TWIN LIVE
                </div>
                <div style="font-size: 0.82rem; font-weight: 600; color: #334155; font-family: monospace; background: #f1f5f9; border: 1px solid #e2e8f0; padding: 4px 12px; border-radius: 12px;" id="topbar-sim-clock">
                    Simulation Time: --:--
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background: #ecfdf5; border: 1px solid #d1fae5; padding: 4px 12px; border-radius: 12px; color: #065f46; font-size: 0.72rem; font-weight: 700;">
                    AI <span style="width: 5px; height: 5px; border-radius: 50%; background: var(--accent-green); display: inline-block;"></span> READY
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background: #fff7ed; border: 1px solid #ffedd5; padding: 4px 12px; border-radius: 12px; color: #ea580c; font-size: 0.72rem; font-weight: 700;">
                    QAOA <span style="width: 5px; height: 5px; border-radius: 50%; background: #ea580c; display: inline-block;"></span> READY
                </div>
            </div>
        </header>"""

    new_topbar = """        <header class="topbar">
            <!-- Left Info -->
            <div style="display: flex; flex-direction: column; gap: 2px;">
                <div style="font-size: 11px; font-weight: 600; letter-spacing: 0.06em; color: #64748b; text-transform: uppercase;">
                    RAILTWIN-Q / OPERATIONS COMMAND CENTER
                </div>
                <h2 style="font-size: 20px; font-weight: 700; color: #0f172a; line-height: 1.2;">
                    Operations Command Center
                </h2>
                <div style="font-size: 12px; color: #64748b;">
                    Hybrid quantum-AI railway decision intelligence
                </div>
            </div>
            <!-- Right Info Flex Container -->
            <div style="display: flex; flex-direction: row; align-items: center; gap: 8px; flex-wrap: nowrap;">
                <div style="font-size: 11px; font-weight: 700; color: #065f46; display: flex; align-items: center; gap: 5px; text-transform: uppercase; background: #ecfdf5; border: 1px solid #a7f3d0; padding: 4px 12px; border-radius: 12px;">
                    <span class="pulse-dot" style="width: 6px; height: 6px; border-radius: 50%; background: #10b981; display: inline-block;"></span>
                    DIGITAL TWIN LIVE
                </div>
                <div style="font-size: 12px; font-weight: 600; color: #334155; font-family: ui-monospace, SFMono-Regular, monospace; background: #f1f5f9; border: 1px solid #e2e8f0; padding: 4px 12px; border-radius: 12px;" id="topbar-sim-clock">
                    Simulation Time: --:--
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 4px 12px; border-radius: 12px; color: #475569; font-size: 11px; font-weight: 600;">
                    AI READY
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 4px 12px; border-radius: 12px; color: #475569; font-size: 11px; font-weight: 600;">
                    QAOA READY
                </div>
            </div>
        </header>"""

    if old_topbar not in content:
        print("Warning: Could not find old topbar block.")
    content = content.replace(old_topbar, new_topbar)

    # 4. Update Methodology bar to inline monospace badge
    old_methodology = """        <!-- SUB HEADER WARNING INDICATOR -->
        <div style="background:#f8fafc;border-bottom:1px solid #e2e8f0;padding:8px 22px;font-size:0.74rem;color:var(--text-secondary);display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
            <div><span>Methodology: </span><b style="color:var(--text-primary);">QAOA probabilistic sampling + classical local refinement</b></div>
        </div>"""

    new_methodology = """        <!-- SUB HEADER WARNING INDICATOR -->
        <div style="background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 10px 22px; display: flex; align-items: center;">
            <span style="font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-right: 8px;">Methodology:</span>
            <code style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 4px 10px; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 11px; color: #64748b;">QAOA probabilistic sampling + classical local refinement</code>
        </div>"""

    if old_methodology not in content:
        print("Warning: Could not find old methodology block.")
    content = content.replace(old_methodology, new_methodology)

    # 5. Update Bottom split panel layout in Tab 2 (HTML structure)
    old_split_panel = """                <!-- Bottom Split Panel (Click Details vs Network State) -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <!-- Left: Selected Details panel -->
                    <div class="sub-card" id="selected-details-container">
                        <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 8px; color: var(--text-primary); text-transform: uppercase;">STATION DETAILS</div>
                        <div style="color: var(--text-muted); font-size: 0.8rem;">Select a station (circles) or train (markers) on the map to display real-time telemetry.</div>
                    </div>
                    <!-- Right: Network State panel -->
                    <div class="sub-card" style="justify-content: space-between;">
                        <h4 style="border-bottom: 1px solid var(--border-color); padding-bottom: 8px; margin-bottom: 10px; color: var(--text-primary);"><i data-lucide="activity"></i> Network State</h4>
                        <div style="display: flex; flex-direction: column; gap: 10px; font-size: 0.82rem;">
                            <div class="status-row"><span>Overall Occupancy:</span><strong id="twin-state-occupancy">—</strong></div>
                            <div class="status-row"><span>Congestion Rating:</span><strong id="twin-state-congestion" style="color: var(--accent-green);">—</strong></div>
                            <div class="status-row"><span>Active Trains:</span><strong id="twin-state-trains">—</strong></div>
                            <div class="status-row"><span>Blocked Track Segments:</span><strong id="twin-state-blocked" style="color: var(--accent-red);">—</strong></div>
                        </div>
                    </div>
                </div>"""

    new_split_panel = """                <!-- Bottom Split Panel (Click Details vs Network State) -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <!-- Left: Selected Details panel -->
                    <div class="sub-card" id="selected-details-container" style="min-height: 250px;">
                        <div style="font-weight: 700; font-size: 12px; letter-spacing: 0.05em; margin-bottom: 4px; color: #0f172a; text-transform: uppercase;">STATION DETAILS</div>
                        <div style="color: var(--text-muted); font-size: 12px; margin-top: 12px;">Select a station (circles) or train (markers) on the map to display real-time telemetry.</div>
                    </div>
                    <!-- Right: Network State panel -->
                    <div class="sub-card" style="min-height: 250px; justify-content: flex-start;">
                        <h4 style="font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 10px; text-transform: uppercase; display: flex; align-items: center; gap: 6px;">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: #f97316;">
                                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                            </svg>
                            NETWORK STATE
                        </h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 10px;">
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; justify-content: center; min-height: 70px;">
                                <span style="font-size: 10px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Overall Occupancy</span>
                                <strong id="twin-state-occupancy" style="font-size: 20px; font-weight: 700; color: #0f172a; font-family: monospace;">—</strong>
                            </div>
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; justify-content: center; min-height: 70px;">
                                <span style="font-size: 10px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Congestion Rating</span>
                                <strong id="twin-state-congestion" style="font-size: 18px; font-weight: 700; color: #10b981; text-transform: uppercase;">—</strong>
                            </div>
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; justify-content: center; min-height: 70px;">
                                <span style="font-size: 10px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Active Trains</span>
                                <strong id="twin-state-trains" style="font-size: 20px; font-weight: 700; color: #0f172a; font-family: monospace;">—</strong>
                            </div>
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; justify-content: center; min-height: 70px;">
                                <span style="font-size: 10px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Blocked Tracks</span>
                                <strong id="twin-state-blocked" style="font-size: 20px; font-weight: 700; color: #ef4444; font-family: monospace;">—</strong>
                            </div>
                        </div>
                    </div>
                </div>"""

    if old_split_panel not in content:
        print("Warning: Could not find old split panel block.")
    content = content.replace(old_split_panel, new_split_panel)

    # 6. Update CSS rules for topbar height, sub-card, status-list, status-row, status-dot and system status widget
    old_topbar_css = "        .topbar {{ height: 58px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; padding: 0 22px; background: #ffffff; position: sticky; top: 0; z-index: 100; box-shadow: var(--shadow-sm); }}"
    new_topbar_css = "        .topbar {{ height: 72px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; padding: 0 22px; background: #ffffff; position: sticky; top: 0; z-index: 100; box-shadow: var(--shadow-sm); }}"
    
    if old_topbar_css not in content:
        print("Warning: Could not find old topbar css definition.")
    content = content.replace(old_topbar_css, new_topbar_css)

    # Clean Conflict Important styles on topbar first child
    old_conflict_important = """        .topbar > div:first-child {{ display: flex !important; flex-direction: column !important; }}
        .topbar > div:first-child > div:first-child {{ font-size: 0.75rem !important; font-weight: 700 !important; color: var(--text-secondary) !important; letter-spacing: 0.05em !important; }}
        .topbar > div:first-child > div:last-child {{ font-size: 11px !important; color: var(--text-muted) !important; margin-top: 2px !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; }}"""

    if old_conflict_important in content:
        content = content.replace(old_conflict_important, "")
    else:
        print("Warning: Could not find conflict important CSS lines.")

    # Rewrite brand-sub in CSS to match 10px uppercase
    old_brand_sub_css = "        .brand-sub {{ font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; }}"
    new_brand_sub_css = "        .brand-sub {{ font-size: 10px; color: #94a3b8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; }}"
    if old_brand_sub_css in content:
        content = content.replace(old_brand_sub_css, new_brand_sub_css)

    # Add custom CSS classes for widget components
    custom_widget_css = """        .system-status-widget {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; margin-top: 12px; display: flex; flex-direction: column; gap: 10px; }}
        .status-header {{ font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; }}
        .status-list {{ display: flex; flex-direction: column; gap: 6px; font-size: 11px; color: #64748b; }}
        .status-row {{ display: flex; justify-content: space-between; align-items: center; }}
        .status-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #10b981; display: inline-block; }}
        .sync-pill-badge {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 4px 10px; font-size: 10px; font-weight: 600; color: #475569; display: flex; align-items: center; justify-content: center; gap: 6px; margin-top: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }}
        
        .pill-status {{ padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 700; text-transform: uppercase; display: inline-block; }}
        .pill-low {{ background: #ecfdf5; border: 1px solid #d1fae5; color: #065f46; }}
        .pill-medium {{ background: #fffbeb; border: 1px solid #fef3c7; color: #b45309; }}
        .pill-high {{ background: #fef2f2; border: 1px solid #fee2e2; color: #991b1b; }}
        .pill-nominal {{ background: #ecfdf5; border: 1px solid #d1fae5; color: #065f46; }}
        .pill-risk {{ background: #fef2f2; border: 1px solid #fee2e2; color: #991b1b; }}
        
        @keyframes pulse-glow {{
            0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ box-shadow: 0 0 0 4px rgba(16, 185, 129, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}"""

    # We will inject this before .main-wrapper
    if ".main-wrapper" in content:
        content = content.replace(".main-wrapper", custom_widget_css + "\n        .main-wrapper")
    else:
        print("Warning: Could not locate .main-wrapper in css rules.")

    # 7. Update sub-card styles in CSS
    old_subcard_css = "        .sub-card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; box-shadow: var(--shadow-sm); }}"
    new_subcard_css = "        .sub-card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px; display: flex; flex-direction: column; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}"
    if old_subcard_css in content:
        content = content.replace(old_subcard_css, new_subcard_css)

    old_subcard_h4_css = "        .sub-card h4 {{ font-size: 0.88rem; font-weight: 700; color: #0f172a; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }}"
    new_subcard_h4_css = "        .sub-card h4 {{ font-size: 12px; font-weight: 700; color: #0f172a; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; letter-spacing: 0.05em; text-transform: uppercase; }}"
    if old_subcard_h4_css in content:
        content = content.replace(old_subcard_h4_css, new_subcard_h4_css)

    # 8. Rewrite the Javascript populating logic in renderSelectedDetails()
    old_station_populator = """                    container.innerHTML = `
                        <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: var(--text-primary); text-transform: uppercase;">STATION DETAILS</div>
                        <div style="font-size: 0.8rem; margin-bottom: 12px; color: var(--text-secondary);">Station: ${{st.name}} | ID: ${{st.id}}</div>
                        
                        <div style="margin-bottom: 12px;">
                            <div style="display:flex; justify-content:space-between; font-size:0.75rem; margin-bottom:3px;">
                                <span>Platform Capacity:</span>
                                <strong>${{platPct}}%</strong>
                            </div>
                            <div style="font-family: monospace; font-size: 1.1rem; color: var(--accent-blue); letter-spacing: 2px;">${{platBar}}</div>
                        </div>
                        
                        <div style="margin-bottom: 12px; font-size:0.75rem; display:flex; justify-content:space-between; border-bottom:1px solid #f1f5f9; padding-bottom:6px;">
                            <span>Current Trains:</span>
                            <strong style="color:var(--text-primary);">${{st.platforms_occupied}}</strong>
                        </div>
                        
                        <div style="margin-bottom: 12px;">
                            <div style="display:flex; justify-content:space-between; font-size:0.75rem; margin-bottom:3px;">
                                <span>Predicted Congestion:</span>
                                <strong>${{congRating}}</strong>
                            </div>
                            <div style="font-family: monospace; font-size: 1.1rem; color: ${{st.congestion >= 75 ? 'var(--accent-red)' : 'var(--accent-yellow)'}}; letter-spacing: 2px;">${{congBar}}</div>
                        </div>
                        
                        <div style="margin-bottom: 12px; font-size:0.75rem; display:flex; justify-content:space-between; border-bottom:1px solid #f1f5f9; padding-bottom:6px;">
                            <span>Predicted Delay +30m:</span>
                            <strong>${{(st.congestion * 0.22).toFixed(1)}} min</strong>
                        </div>
                        
                        <div style="font-size:0.75rem; display:flex; justify-content:space-between; padding-top:4px;">
                            <span>Active Disruption:</span>
                            <strong style="color: ${{activeDis !== 'Nominal' ? 'var(--accent-red)' : 'var(--accent-green)'}};">${{activeDis}}</strong>
                        </div>
                    `;"""

    new_station_populator = """                    const platColor = platPct >= 75 ? "#ef4444" : (platPct >= 45 ? "#f59e0b" : "#10b981");
                    const congColor = st.congestion >= 75 ? "#ef4444" : (st.congestion >= 45 ? "#f59e0b" : "#10b981");
                    
                    const congPill = st.congestion >= 75 ? '<span class="pill-status pill-high">HIGH</span>' : (st.congestion >= 45 ? '<span class="pill-status pill-medium">MEDIUM</span>' : '<span class="pill-status pill-low">LOW</span>');
                    const activeDisPill = activeDis === "Nominal" ? '<span class="pill-status pill-nominal">NOMINAL</span>' : `<span class="pill-status pill-high">\${activeDis}</span>`;
                    
                    container.innerHTML = `
                        <div style="font-weight: 700; font-size: 12px; letter-spacing: 0.05em; margin-bottom: 4px; color: #0f172a; text-transform: uppercase;">STATION DETAILS</div>
                        <div style="font-size: 12px; margin-bottom: 16px; color: #64748b;">Station: \${st.name} | ID: \${st.id}</div>
                        
                        <div style="margin-bottom: 12px; border-bottom: 1px dashed #e2e8f0; padding-bottom: 10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Platform Capacity:</span>
                                <strong style="color:#0f172a;">\${platPct}%</strong>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: \${platPct}%; background: \${platColor}; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 12px; font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px dashed #e2e8f0; padding-bottom:10px; color:#64748b;">
                            <span>Current Trains:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">\${st.platforms_occupied}</strong>
                        </div>
                        
                        <div style="margin-bottom: 12px; border-bottom: 1px dashed #e2e8f0; padding-bottom: 10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Predicted Congestion:</span>
                                <span>\${congPill}</span>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: \subst_congestion%; background: \${congColor}; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 12px; font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px dashed #e2e8f0; padding-bottom:10px; color:#64748b;">
                            <span>Predicted Delay +30m:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">+\${(st.congestion * 0.22).toFixed(1)} min</strong>
                        </div>
                        
                        <div style="font-size:12px; display:flex; justify-content:space-between; align-items:center; color:#64748b; padding-top:2px;">
                            <span>Active Disruption:</span>
                            <span>\${activeDisPill}</span>
                        </div>
                    `.replace('subst_congestion', '${st.congestion}');"""

    if old_station_populator not in content:
        print("Warning: Could not find old_station_populator block.")
    content = content.replace(old_station_populator, new_station_populator)

    # 9. Update train detail populating logic in JS
    old_train_populator = """                    container.innerHTML = `
                        <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 4px; color: var(--text-primary); text-transform: uppercase;">TRAIN T${{t.train_no}}</div>
                        <div style="font-size: 0.8rem; margin-bottom: 12px; color: var(--text-secondary);">${{t.name}}</div>
                        
                        <table style="width:100%; border-collapse:collapse; font-size:0.76rem; text-align:left;">
                            <tr style="height:25px; border-bottom:1px solid #f8fafc;"><td style="color:var(--text-secondary);">Current Speed</td><td style="font-weight:700; text-align:right; color:var(--text-primary);">${{curSpeed}} km/h</td></tr>
                            <tr style="height:25px; border-bottom:1px solid #f8fafc;"><td style="color:var(--text-secondary);">Base Speed</td><td style="font-weight:700; text-align:right; color:var(--text-primary);">${{baseSpeed}} km/h</td></tr>
                            <tr style="height:25px; border-bottom:1px solid #f8fafc;"><td style="color:var(--text-secondary);">Current Delay</td><td style="font-weight:700; color:var(--accent-red); text-align:right;">+${{t.delay.toFixed(1)}} min</td></tr>
                            <tr style="height:25px; border-bottom:1px solid #f8fafc;"><td style="color:var(--text-secondary);">Predicted +15m</td><td style="font-weight:700; text-align:right; color:var(--text-primary);">+${{t.predicted_delay_15.toFixed(1)}} min</td></tr>
                            <tr style="height:25px; border-bottom:1px solid #f8fafc;"><td style="color:var(--text-secondary);">Predicted +30m</td><td style="font-weight:700; text-align:right; color:var(--text-primary);">+${{t.predicted_delay_30.toFixed(1)}} min</td></tr>
                            <tr style="height:25px; border-bottom:1px solid #f8fafc;"><td style="color:var(--text-secondary);">Predicted +60m</td><td style="font-weight:700; text-align:right; color:var(--text-primary);">+${{t.predicted_delay_60.toFixed(1)}} min</td></tr>
                            <tr style="height:28px; border-top:1px solid var(--border-color);"><td style="color:var(--text-secondary); padding-top:4px;">Current Action</td><td style="font-weight:700; color:var(--accent-purple); text-align:right; padding-top:4px;">${{action}}</td></tr>
                            <tr style="height:24px;"><td style="color:var(--text-secondary);">Status</td><td style="font-weight:700; color:${{status === 'AT RISK' ? 'var(--accent-red)' : 'var(--accent-green)'}}; text-align:right;">${{status}}</td></tr>
                        </table>
                    `;"""

    new_train_populator = """                    const speedColor = curSpeed < baseSpeed ? "#f97316" : "#10b981";
                    const statusPill = t.delay > 10 ? '<span class="pill-status pill-high">AT RISK</span>' : '<span class="pill-status pill-nominal">NORMAL</span>';
                    const actionPill = action === "NOMINAL" ? '<span class="pill-status pill-nominal">NOMINAL</span>' : `<span class="pill-status pill-medium">\${action}</span>`;

                    container.innerHTML = `
                        <div style="font-weight: 700; font-size: 12px; letter-spacing: 0.05em; margin-bottom: 4px; color: #0f172a; text-transform: uppercase;">TRAIN DETAILS</div>
                        <div style="font-size: 12px; margin-bottom: 16px; color: #64748b;">Train T\${t.train_no} | \subst_tname</div>
                        
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; border-bottom:1px dashed #e2e8f0; padding-bottom:8px; margin-bottom:8px; color:#64748b;">
                            <span>Current Speed:</span>
                            <strong style="color:\${speedColor}; font-family: monospace; font-size:13px;">\${curSpeed} km/h</strong>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; border-bottom:1px dashed #e2e8f0; padding-bottom:8px; margin-bottom:8px; color:#64748b;">
                            <span>Base Speed:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size:13px;">\${baseSpeed} km/h</strong>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; border-bottom:1px dashed #e2e8f0; padding-bottom:8px; margin-bottom:8px; color:#64748b;">
                            <span>Current Delay:</span>
                            <strong style="color:#ef4444; font-family: monospace; font-size:13px;">+\${t.delay.toFixed(1)} min</strong>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; border-bottom:1px dashed #e2e8f0; padding-bottom:8px; margin-bottom:8px; color:#64748b;">
                            <span>Predicted Delay +15m:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size:13px;">+\${t.predicted_delay_15.toFixed(1)} min</strong>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; border-bottom:1px dashed #e2e8f0; padding-bottom:8px; margin-bottom:8px; color:#64748b;">
                            <span>Predicted Delay +30m:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size:13px;">+\${t.predicted_delay_30.toFixed(1)} min</strong>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; border-bottom:1px dashed #e2e8f0; padding-bottom:8px; margin-bottom:8px; color:#64748b;">
                            <span>Predicted Delay +60m:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size:13px;">+\subst_pred60 min</strong>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; border-bottom:1px dashed #e2e8f0; padding-bottom:8px; margin-bottom:8px; color:#64748b;">
                            <span>Current Action:</span>
                            <span>\${actionPill}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:#64748b; padding-top:2px;">
                            <span>Status:</span>
                            <span>\${statusPill}</span>
                        </div>
                    `.replace('subst_tname', '${t.name}').replace('subst_pred60', '${t.predicted_delay_60.toFixed(1)}');"""

    if old_train_populator not in content:
        print("Warning: Could not find old_train_populator block.")
    content = content.replace(old_train_populator, new_train_populator)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print("Success: Sidebar, Top Header, and Bottom Grid Cards refactored successfully!")

if __name__ == "__main__":
    main()
