import os

def refine_template_content(content):
    # 1. Unified Card Headers: Make all card headers uniform Slate 900 (trophy, sliders, etc already are Slate 900).
    # Specifically remove green title text from Simulation Outcome.
    old_outcome_header = """                    <div class="sub-card" style="border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.02); justify-content:space-between;">
                        <div>
                            <h4 style="color: var(--accent-green);"><i data-lucide="activity"></i> Simulation Outcome</h4>"""
    
    new_outcome_header = """                    <div class="sub-card" style="border-color: #e2e8f0; background: #ffffff; justify-content:space-between;">
                        <div>
                            <h4 style="color: #0f172a; font-weight: 700; text-transform: uppercase;"><i data-lucide="activity"></i> Simulation Outcome</h4>"""
    content = content.replace(old_outcome_header, new_outcome_header)

    # 2. Table Row Labels (SA, Greedy, Local Search -> Slate #334155)
    old_rows_table = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:700; color:var(--accent-blue);">Simulated Annealing (SA)</td>
                                    <td id="bench-sa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-sa-qual" style="padding:6px; text-align:center; font-weight:bold; color:var(--accent-yellow);">78%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:700; color:var(--accent-cyan);">Greedy Heuristic</td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">2 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:var(--accent-yellow);">72%</td>
                                </tr>
                                <tr>
                                    <td style="padding:6px; font-weight:700; color:var(--accent-green);">Local Search</td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">3 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:var(--accent-yellow);">75%</td>
                                </tr>"""

    new_rows_table = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:600; color:#334155;">Simulated Annealing (SA)</td>
                                    <td id="bench-sa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-sa-qual" style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">78%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:600; color:#334155;">Greedy Heuristic</td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">2 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">72%</td>
                                </tr>
                                <tr>
                                    <td style="padding:6px; font-weight:600; color:#334155;">Local Search</td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">3 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">75%</td>
                                </tr>"""
    content = content.replace(old_rows_table, new_rows_table)

    # 3. Bar Charts (Time and Quality) - template version
    old_time_bar_chart = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>QAOA</span> <span id="bar-qaoa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-qaoa-time-fill" style="background:#6366f1; height:100%; width:80%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>SA</span> <span id="bar-sa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-sa-time-fill" style="background:var(--accent-blue); height:100%; width:10%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Greedy</span> <span>2 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-cyan); height:100%; width:1%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Local Search</span> <span>3 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-green); height:100%; width:1%;"></div>
                                        </div>
                                    </div>"""

    new_time_bar_chart = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>QAOA</span> <span id="bar-qaoa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-qaoa-time-fill" style="background:#6366f1; height:100%; width:80%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>SA</span> <span id="bar-sa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-sa-time-fill" style="background:#94a3b8; height:100%; width:10%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Greedy</span> <span>2 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:1%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Local Search</span> <span>3 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:1%;"></div>
                                        </div>
                                    </div>"""
    content = content.replace(old_time_bar_chart, new_time_bar_chart)

    old_qual_bar_chart = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>QAOA</span> <span>96%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#10b981; height:100%; width:96%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>SA</span> <span>78%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#0ea5e9; height:100%; width:78%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Greedy</span> <span>72%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#0ea5e9; height:100%; width:72%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Local Search</span> <span>75%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#0ea5e9; height:100%; width:75%;"></div>
                                        </div>
                                    </div>"""

    new_qual_bar_chart = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>QAOA</span> <span>96%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#6366f1; height:100%; width:96%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>SA</span> <span>78%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:78%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Greedy</span> <span>72%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:72%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Local Search</span> <span>75%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:75%;"></div>
                                        </div>
                                    </div>"""
    content = content.replace(old_qual_bar_chart, new_qual_bar_chart)

    # 4. Simulation Outcome Top Metrics
    old_top_metrics = """                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Initial Delay</span>
                                    <strong id="sim-outcome-init-delay" style="color:var(--text-primary); font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Final Delay</span>
                                    <strong id="sim-outcome-final-delay" style="color:var(--text-primary); font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:#0d9488; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Initial Congestion</span>
                                    <strong id="sim-outcome-init-cong" style="color:var(--text-primary); font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Final Congestion</span>
                                    <strong id="sim-outcome-final-cong" style="color:var(--text-primary); font-size:1rem;">—%</strong>
                                </div>"""

    new_top_metrics = """                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Initial Delay</span>
                                    <strong id="sim-outcome-init-delay" style="color:#0f172a; font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Final Delay</span>
                                    <strong id="sim-outcome-final-delay" style="color:#0f172a; font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:#10b981; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Initial Congestion</span>
                                    <strong id="sim-outcome-init-cong" style="color:#0f172a; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Final Congestion</span>
                                    <strong id="sim-outcome-final-cong" style="color:#0f172a; font-size:1rem;">—%</strong>
                                </div>"""
    content = content.replace(old_top_metrics, new_top_metrics)

    # Label update for Passenger Hours Saved
    old_pax_label = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>"""
    new_pax_label = """                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>"""
    content = content.replace(old_pax_label, new_pax_label)

    # 5. Network Status pill container and dynamic update
    old_net_status_container = """                            <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px; margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                                <span style="color:var(--text-muted); font-size:0.68rem; text-transform:uppercase;">Network Status</span>
                                <strong id="sim-outcome-net-status" style="color:var(--accent-green); font-size:0.85rem; text-transform:uppercase;">Stable</strong>
                            </div>"""

    new_net_status_container = """                            <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px; margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                                <span style="color:#64748b; font-size:0.68rem; text-transform:uppercase;">Network Status</span>
                                <span id="sim-outcome-net-status" style="font-size:0.75rem; font-weight:700; text-transform:uppercase; padding: 4px 10px; border-radius: 6px;">Stable</span>
                            </div>"""
    content = content.replace(old_net_status_container, new_net_status_container)

    # JS Updater inside template
    old_net_status_js = """            const elNetStatus = document.getElementById("sim-outcome-net-status");
            if (elNetStatus) {{
                elNetStatus.innerText = netStatusText;
                elNetStatus.style.color = (netStatusText === "Stable") ? "var(--accent-green)" : ((netStatusText === "Stabilizing") ? "var(--accent-yellow)" : "var(--accent-red)");
            }}"""

    new_net_status_js = """            const elNetStatus = document.getElementById("sim-outcome-net-status");
            if (elNetStatus) {{
                elNetStatus.innerText = netStatusText;
                if (netStatusText === "Stable") {{
                    elNetStatus.style.background = "#ecfdf5";
                    elNetStatus.style.color = "#10b981";
                    elNetStatus.style.border = "1px solid #a7f3d0";
                }} else if (netStatusText === "Stabilizing") {{
                    elNetStatus.style.background = "#fffbeb";
                    elNetStatus.style.color = "#d97706";
                    elNetStatus.style.border = "1px solid #fde68a";
                }} else {{
                    elNetStatus.style.background = "#fef2f2";
                    elNetStatus.style.color = "#ef4444";
                    elNetStatus.style.border = "1px solid #fecaca";
                }}
            }}"""
    content = content.replace(old_net_status_js, new_net_status_js)

    # 6. Top Status Header Badges (template)
    old_top_badges_t = """            <div style="display: flex; flex-direction: row; align-items: center; gap: 8px; flex-wrap: nowrap;">
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
                <div style="display: flex; align-items: center; gap: 5px; background-color: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">
                    QAOA READY
                </div>
            </div>"""

    new_top_badges_t = """            <div style="display: flex; flex-direction: row; align-items: center; gap: 8px; flex-wrap: nowrap;">
                <div style="font-size: 11px; font-weight: 700; color: #10b981; display: flex; align-items: center; gap: 5px; text-transform: uppercase; background: #ecfdf5; border: 1px solid #a7f3d0; padding: 4px 12px; border-radius: 12px;">
                    <span class="pulse-dot" style="width: 6px; height: 6px; border-radius: 50%; background: #10b981; display: inline-block;"></span>
                    DIGITAL TWIN LIVE
                </div>
                <div style="font-size: 12px; font-weight: 600; color: #334155; font-family: ui-monospace, SFMono-Regular, monospace; background: #f1f5f9; border: 1px solid #e2e8f0; padding: 4px 12px; border-radius: 12px;" id="topbar-sim-clock">
                    Simulation Time: --:--
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background: #f0f9ff; border: 1px solid #bae6fd; padding: 4px 12px; border-radius: 12px; color: #0284c7; font-size: 11px; font-weight: 600;">
                    AI READY
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background-color: #eef2ff; color: #6366f1; border: 1px solid #c7d2fe; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">
                    QAOA READY
                </div>
            </div>"""
    content = content.replace(old_top_badges_t, new_top_badges_t)
    return content

def refine_html_content(content):
    # 1. Unified Card Headers
    old_outcome_header = """                    <div class="sub-card" style="border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.02); justify-content:space-between;">
                        <div>
                            <h4 style="color: var(--accent-green);"><i data-lucide="activity"></i> Simulation Outcome</h4>"""
    
    new_outcome_header = """                    <div class="sub-card" style="border-color: #e2e8f0; background: #ffffff; justify-content:space-between;">
                        <div>
                            <h4 style="color: #0f172a; font-weight: 700; text-transform: uppercase;"><i data-lucide="activity"></i> Simulation Outcome</h4>"""
    content = content.replace(old_outcome_header, new_outcome_header)

    # 2. Table Row Labels (SA, Greedy, Local Search -> Slate #334155)
    old_rows_table = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:700; color:var(--accent-blue);">Simulated Annealing (SA)</td>
                                    <td id="bench-sa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-sa-qual" style="padding:6px; text-align:center; font-weight:bold; color:var(--accent-yellow);">78%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:700; color:var(--accent-cyan);">Greedy Heuristic</td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">2 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:var(--accent-yellow);">72%</td>
                                </tr>
                                <tr>
                                    <td style="padding:6px; font-weight:700; color:var(--accent-green);">Local Search</td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">3 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:var(--accent-yellow);">75%</td>
                                </tr>"""

    new_rows_table = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:600; color:#334155;">Simulated Annealing (SA)</td>
                                    <td id="bench-sa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-sa-qual" style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">78%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:600; color:#334155;">Greedy Heuristic</td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">2 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">72%</td>
                                </tr>
                                <tr>
                                    <td style="padding:6px; font-weight:600; color:#334155;">Local Search</td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">3 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">75%</td>
                                </tr>"""
    content = content.replace(old_rows_table, new_rows_table)

    # 3. Bar Charts (Time and Quality) - HTML version
    old_time_bar_chart = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>QAOA</span> <span id="bar-qaoa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-qaoa-time-fill" style="background:#6366f1; height:100%; width:80%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>SA</span> <span id="bar-sa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-sa-time-fill" style="background:var(--accent-blue); height:100%; width:10%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Greedy</span> <span>2 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-cyan); height:100%; width:1%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Local Search</span> <span>3 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-green); height:100%; width:1%;"></div>
                                        </div>
                                    </div>"""

    new_time_bar_chart = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>QAOA</span> <span id="bar-qaoa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-qaoa-time-fill" style="background:#6366f1; height:100%; width:80%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>SA</span> <span id="bar-sa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-sa-time-fill" style="background:#94a3b8; height:100%; width:10%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Greedy</span> <span>2 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:1%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Local Search</span> <span>3 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:1%;"></div>
                                        </div>
                                    </div>"""
    content = content.replace(old_time_bar_chart, new_time_bar_chart)

    old_qual_bar_chart = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>QAOA</span> <span>96%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#10b981; height:100%; width:96%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>SA</span> <span>78%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#0ea5e9; height:100%; width:78%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Greedy</span> <span>72%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#0ea5e9; height:100%; width:72%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Local Search</span> <span>75%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#0ea5e9; height:100%; width:75%;"></div>
                                        </div>
                                    </div>"""

    new_qual_bar_chart = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>QAOA</span> <span>96%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#6366f1; height:100%; width:96%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>SA</span> <span>78%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:78%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Greedy</span> <span>72%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:72%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Local Search</span> <span>75%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#94a3b8; height:100%; width:75%;"></div>
                                        </div>
                                    </div>"""
    content = content.replace(old_qual_bar_chart, new_qual_bar_chart)

    # 4. Simulation Outcome Top Metrics
    old_top_metrics = """                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Initial Delay</span>
                                    <strong id="sim-outcome-init-delay" style="color:var(--text-primary); font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Final Delay</span>
                                    <strong id="sim-outcome-final-delay" style="color:var(--text-primary); font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:#0d9488; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Initial Congestion</span>
                                    <strong id="sim-outcome-init-cong" style="color:var(--text-primary); font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Final Congestion</span>
                                    <strong id="sim-outcome-final-cong" style="color:var(--text-primary); font-size:1rem;">—%</strong>
                                </div>"""

    new_top_metrics = """                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Initial Delay</span>
                                    <strong id="sim-outcome-init-delay" style="color:#0f172a; font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Final Delay</span>
                                    <strong id="sim-outcome-final-delay" style="color:#0f172a; font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:#10b981; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Initial Congestion</span>
                                    <strong id="sim-outcome-init-cong" style="color:#0f172a; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Final Congestion</span>
                                    <strong id="sim-outcome-final-cong" style="color:#0f172a; font-size:1rem;">—%</strong>
                                </div>"""
    content = content.replace(old_top_metrics, new_top_metrics)

    # Label update for Passenger Hours Saved
    old_pax_label = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>"""
    new_pax_label = """                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>"""
    content = content.replace(old_pax_label, new_pax_label)

    # 5. Network Status pill container and dynamic update
    old_net_status_container = """                            <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px; margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                                <span style="color:var(--text-muted); font-size:0.68rem; text-transform:uppercase;">Network Status</span>
                                <strong id="sim-outcome-net-status" style="color:var(--accent-green); font-size:0.85rem; text-transform:uppercase;">Stable</strong>
                            </div>"""

    new_net_status_container = """                            <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px; margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                                <span style="color:#64748b; font-size:0.68rem; text-transform:uppercase;">Network Status</span>
                                <span id="sim-outcome-net-status" style="font-size:0.75rem; font-weight:700; text-transform:uppercase; padding: 4px 10px; border-radius: 6px;">Stable</span>
                            </div>"""
    content = content.replace(old_net_status_container, new_net_status_container)

    # JS Updater inside HTML
    old_net_status_js = """            const elNetStatus = document.getElementById("sim-outcome-net-status");
            if (elNetStatus) {
                elNetStatus.innerText = netStatusText;
                elNetStatus.style.color = (netStatusText === "Stable") ? "var(--accent-green)" : ((netStatusText === "Stabilizing") ? "var(--accent-yellow)" : "var(--accent-red)");
            }"""

    new_net_status_js = """            const elNetStatus = document.getElementById("sim-outcome-net-status");
            if (elNetStatus) {
                elNetStatus.innerText = netStatusText;
                if (netStatusText === "Stable") {
                    elNetStatus.style.background = "#ecfdf5";
                    elNetStatus.style.color = "#10b981";
                    elNetStatus.style.border = "1px solid #a7f3d0";
                } else if (netStatusText === "Stabilizing") {
                    elNetStatus.style.background = "#fffbeb";
                    elNetStatus.style.color = "#d97706";
                    elNetStatus.style.border = "1px solid #fde68a";
                } else {
                    elNetStatus.style.background = "#fef2f2";
                    elNetStatus.style.color = "#ef4444";
                    elNetStatus.style.border = "1px solid #fecaca";
                }
            }"""
    content = content.replace(old_net_status_js, new_net_status_js)

    # 6. Top Status Header Badges (HTML)
    old_top_badges_h = """            <div style="display: flex; flex-direction: row; align-items: center; gap: 8px; flex-wrap: nowrap;">
                <div style="font-size: 11px; font-weight: 700; color: #065f46; display: flex; align-items: center; gap: 5px; text-transform: uppercase; background: #ecfdf5; border: 1px solid #a7f3d0; padding: 4px 12px; border-radius: 12px;">
                    <span class="pulse-dot" style="width: 6px; height: 6px; border-radius: 50%; background: #10b981; display: inline-block;"></span>
                    DIGITAL TWIN LIVE
                </div>
                <div style="font-size: 12px; font-weight: 600; color: #334155; font-family: ui-monospace, SFMono-Regular, monospace; background: #f1f5f9; border: 1px solid #e2e8f0; padding: 4px 12px; border-radius: 12px;" id="topbar-sim-clock">
                    Simulation Time: --:--
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background: #ecfdf5; border: 1px solid #d1fae5; padding: 4px 12px; border-radius: 12px; color: #065f46; font-size: 0.72rem; font-weight: 700;">
                    AI <span style="width: 5px; height: 5px; border-radius: 50%; background: var(--accent-green); display: inline-block;"></span> READY
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background-color: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">
                    QAOA READY
                </div>
            </div>"""

    new_top_badges_h = """            <div style="display: flex; flex-direction: row; align-items: center; gap: 8px; flex-wrap: nowrap;">
                <div style="font-size: 11px; font-weight: 700; color: #10b981; display: flex; align-items: center; gap: 5px; text-transform: uppercase; background: #ecfdf5; border: 1px solid #a7f3d0; padding: 4px 12px; border-radius: 12px;">
                    <span class="pulse-dot" style="width: 6px; height: 6px; border-radius: 50%; background: #10b981; display: inline-block;"></span>
                    DIGITAL TWIN LIVE
                </div>
                <div style="font-size: 12px; font-weight: 600; color: #334155; font-family: ui-monospace, SFMono-Regular, monospace; background: #f1f5f9; border: 1px solid #e2e8f0; padding: 4px 12px; border-radius: 12px;" id="topbar-sim-clock">
                    Simulation Time: --:--
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background: #f0f9ff; border: 1px solid #bae6fd; padding: 4px 12px; border-radius: 12px; color: #0284c7; font-size: 11px; font-weight: 600;">
                    AI READY
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background-color: #eef2ff; color: #6366f1; border: 1px solid #c7d2fe; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">
                    QAOA READY
                </div>
            </div>"""
    content = content.replace(old_top_badges_h, new_top_badges_h)
    return content

def main():
    # 1. Update services/frontend_generator.py
    generator_path = r"c:\Users\idhay\Desktop\RailTwin-Q\services\frontend_generator.py"
    if os.path.exists(generator_path):
        with open(generator_path, "r", encoding="utf-8") as f:
            gen_content = f.read()
        gen_content_new = refine_template_content(gen_content)
        with open(generator_path, "w", encoding="utf-8") as f:
            f.write(gen_content_new)
        print("Success: Refined template logic inside services/frontend_generator.py!")
    else:
        print("Warning: services/frontend_generator.py not found.")

    # 2. Update frontend/operations.html
    ops_path = r"c:\Users\idhay\Desktop\RailTwin-Q\frontend\operations.html"
    if os.path.exists(ops_path):
        with open(ops_path, "r", encoding="utf-8") as f:
            ops_content = f.read()
        ops_content_new = refine_html_content(ops_content)
        with open(ops_path, "w", encoding="utf-8") as f:
            f.write(ops_content_new)
        print("Success: Refined html directly inside frontend/operations.html!")
    else:
        print("Warning: frontend/operations.html not found.")

if __name__ == "__main__":
    main()
