import os

def refine_template_content(content):
    # 1. Solver Comparison Table badges and bold column styling
    old_table = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:600; color:#4f46e5;">QAOA (Aer Simulation)</td>
                                    <td id="bench-qaoa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-qaoa-qual" style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">96%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
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

    new_table = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px;"><span style="background: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; padding: 2px 6px; border-radius: 4px; display: inline-block; font-weight: 600;">QAOA (Aer Simulation)</span></td>
                                    <td id="bench-qaoa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-qaoa-qual" style="padding:6px; text-align:center; font-weight:bold; color:#059669;">96%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px;"><span style="background: #fffbeb; color: #b45309; border: 1px solid #fde68a; padding: 2px 6px; border-radius: 4px; display: inline-block; font-weight: 600;">Simulated Annealing (SA)</span></td>
                                    <td id="bench-sa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-sa-qual" style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">78%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px;"><span style="background: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 2px 6px; border-radius: 4px; display: inline-block; font-weight: 600;">Greedy Heuristic</span></td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">2 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">72%</td>
                                </tr>
                                <tr>
                                    <td style="padding:6px;"><span style="background: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 2px 6px; border-radius: 4px; display: inline-block; font-weight: 600;">Local Search</span></td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">3 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">75%</td>
                                </tr>"""
    content = content.replace(old_table, new_table)

    # 2. Execution Time Bars fill color (SA, Greedy, Local -> Sky Blue #38bdf8)
    old_time_bars = """                                    <div>
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

    new_time_bars = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>SA</span> <span id="bar-sa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-sa-time-fill" style="background:#38bdf8; height:100%; width:10%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Greedy</span> <span>2 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#38bdf8; height:100%; width:1%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Local Search</span> <span>3 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#38bdf8; height:100%; width:1%;"></div>
                                        </div>
                                    </div>"""
    content = content.replace(old_time_bars, new_time_bars)

    # Solution Quality Bars fill colors (QAOA -> Emerald #10b981, SA -> Royal Blue #3b82f6, Greedy/Local -> Amber #f59e0b)
    old_qual_bars = """                                    <div>
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

    new_qual_bars = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>QAOA</span> <span>96%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#10b981; height:100%; width:96%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>SA</span> <span>78%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#3b82f6; height:100%; width:78%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Greedy</span> <span>72%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#f59e0b; height:100%; width:72%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Local Search</span> <span>75%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#f59e0b; height:100%; width:75%;"></div>
                                        </div>
                                    </div>"""
    content = content.replace(old_qual_bars, new_qual_bars)

    # 3. Simulation Outcome: subtle background cards (#f8fafc), semantic coloring
    old_outcome_boxes = """                            <div style="font-size:0.76rem; line-height:1.4; color:var(--text-secondary); margin-top:8px; display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
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
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>
                                    <strong id="sim-outcome-pax-saved" style="color:#10b981; font-size:1rem;">—</strong>
                                </div>
                            </div>"""

    new_outcome_boxes = """                            <div style="font-size:0.76rem; line-height:1.4; color:var(--text-secondary); margin-top:8px; display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Initial Delay</span>
                                    <strong id="sim-outcome-init-delay" style="color:#0f172a; font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Final Delay</span>
                                    <strong id="sim-outcome-final-delay" style="color:#0f172a; font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:#059669; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Initial Congestion</span>
                                    <strong id="sim-outcome-init-cong" style="color:#d97706; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Final Congestion</span>
                                    <strong id="sim-outcome-final-cong" style="color:#d97706; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>
                                    <strong id="sim-outcome-pax-saved" style="color:#0d9488; font-size:1rem;">—</strong>
                                </div>
                            </div>"""
    content = content.replace(old_outcome_boxes, new_outcome_boxes)

    # 4. Hardware Ansätz Detail quantum pills
    old_ansatz = """                        <h4 style="color:var(--text-primary);"><i data-lucide="hash"></i> Hardware Ansätz Detail</h4>
                        <div style="font-size:0.75rem; line-height:1.5; color:var(--text-secondary); display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:8px;">
                            <div>
                                <b>Device Coupling Map:</b> ibm_kyoto<br>
                                <b>Transpiled Qubits:</b> 10 qubits<br>
                                <b>ANSATZ GATES:</b> 166 (CX=4)
                            </div>
                            <div>
                                <b>Error Mitigation:</b> PEC / ZNE<br>
                                <b>Aer Simulation:</b> 1024 shots<br>
                                <b>Optimization Loop:</b> COBYLA
                            </div>
                        </div>"""

    new_ansatz = """                        <h4 style="color:var(--text-primary);"><i data-lucide="hash"></i> Hardware Ansätz Detail</h4>
                        <div style="font-size:0.75rem; line-height:1.8; color:var(--text-secondary); display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:8px;">
                            <div>
                                <b>Device Coupling Map:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">ibm_kyoto</span><br>
                                <b>Transpiled Qubits:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">10 qubits</span><br>
                                <b>ANSATZ GATES:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">166 (CX=4)</span>
                            </div>
                            <div>
                                <b>Error Mitigation:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">PEC / ZNE</span><br>
                                <b>Aer Simulation:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">1024 shots</span><br>
                                <b>Optimization Loop:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">COBYLA</span>
                            </div>
                        </div>"""
    content = content.replace(old_ansatz, new_ansatz)

    # 5. Playback Slider (template style block with transparent track and orange thumb)
    old_slider_style = """                                #scenario-tick-slider::-webkit-slider-runnable-track {{
                                    width: 100%;
                                    height: 6px;
                                    background: #e2e8f0;
                                    border-radius: 999px;
                                }}
                                #scenario-tick-slider::-webkit-slider-thumb {{
                                    -webkit-appearance: none;
                                    appearance: none;
                                    width: 16px;
                                    height: 16px;
                                    border-radius: 50%;
                                    background: #0f172a;
                                    border: 2px solid #ffffff;
                                    box-shadow: 0 0 0 1px #cbd5e1;
                                    cursor: pointer;
                                    margin-top: -5px;
                                }}
                                #scenario-tick-slider::-moz-range-track {{
                                    width: 100%;
                                    height: 6px;
                                    background: #e2e8f0;
                                    border-radius: 999px;
                                }}
                                #scenario-tick-slider::-moz-range-thumb {{
                                    width: 16px;
                                    height: 16px;
                                    border-radius: 50%;
                                    background: #0f172a;
                                    border: 2px solid #ffffff;
                                    box-shadow: 0 0 0 1px #cbd5e1;
                                    cursor: pointer;
                                }}"""

    new_slider_style = """                                #scenario-tick-slider::-webkit-slider-runnable-track {{
                                    width: 100%;
                                    height: 6px;
                                    background: transparent;
                                    border-radius: 999px;
                                }}
                                #scenario-tick-slider::-webkit-slider-thumb {{
                                    -webkit-appearance: none;
                                    appearance: none;
                                    width: 16px;
                                    height: 16px;
                                    border-radius: 50%;
                                    background: #ea580c;
                                    border: 2px solid #ffffff;
                                    box-shadow: 0 0 0 1px #ea580c;
                                    cursor: pointer;
                                    margin-top: -5px;
                                }}
                                #scenario-tick-slider::-moz-range-track {{
                                    width: 100%;
                                    height: 6px;
                                    background: transparent;
                                    border-radius: 999px;
                                }}
                                #scenario-tick-slider::-moz-range-thumb {{
                                    width: 16px;
                                    height: 16px;
                                    border-radius: 50%;
                                    background: #ea580c;
                                    border: 2px solid #ffffff;
                                    box-shadow: 0 0 0 1px #ea580c;
                                    cursor: pointer;
                                }}"""
    content = content.replace(old_slider_style, new_slider_style)

    # JS Updater Slider Fill function inside template
    old_slider_js_t = """        if (slider) {{
            slider.addEventListener("input", function() {{
                const tick = parseInt(this.value);
                const snap = SIMULATION_HISTORY[tick] || SIMULATION_HISTORY[SIMULATION_HISTORY.length - 1];
                if (snap) {{
                    updateDashboard(snap);
                    document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: \${tick} min (\${snap.sim_time_str})`;
                }}
            }});
        }}"""

    new_slider_js_t = """        if (slider) {{
            const updateSliderFill = () => {{
                const val = slider.value;
                const min = slider.min ? parseInt(slider.min) : 0;
                const max = slider.max ? parseInt(slider.max) : 120;
                const pct = ((val - min) / (max - min)) * 100;
                slider.style.background = `linear-gradient(to right, #f97316 0%, #f97316 \${pct}%, #e2e8f0 \${pct}%, #e2e8f0 100%)`;
            }};
            slider.addEventListener("input", function() {{
                const tick = parseInt(this.value);
                const snap = SIMULATION_HISTORY[tick] || SIMULATION_HISTORY[SIMULATION_HISTORY.length - 1];
                if (snap) {{
                    updateDashboard(snap);
                    document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: \${tick} min (\${snap.sim_time_str})`;
                }}
                updateSliderFill();
            }});
            updateSliderFill();
        }}"""
    content = content.replace(old_slider_js_t, new_slider_js_t)

    # Network Status negative state (template version)
    old_net_status_js_t = """            const elNetStatus = document.getElementById("sim-outcome-net-status");
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

    new_net_status_js_t = """            const elNetStatus = document.getElementById("sim-outcome-net-status");
            if (elNetStatus) {{
                elNetStatus.innerText = netStatusText;
                if (netStatusText === "Stable") {{
                    elNetStatus.style.background = "#ecfdf5";
                    elNetStatus.style.color = "#10b981";
                    elNetStatus.style.border = "1px solid #a7f3d0";
                    elNetStatus.style.fontWeight = "700";
                }} else if (netStatusText === "Stabilizing") {{
                    elNetStatus.style.background = "#fffbeb";
                    elNetStatus.style.color = "#d97706";
                    elNetStatus.style.border = "1px solid #fde68a";
                    elNetStatus.style.fontWeight = "700";
                }} else {{
                    elNetStatus.style.background = "#fef2f2";
                    elNetStatus.style.color = "#dc2626";
                    elNetStatus.style.border = "1px solid #fecaca";
                    elNetStatus.style.fontWeight = "700";
                }}
            }}"""
    content = content.replace(old_net_status_js_t, new_net_status_js_t)
    return content

def refine_html_content(content):
    # Same as refine_template_content, but with single braces for style tag inside HTML
    old_table = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:600; color:#4f46e5;">QAOA (Aer Simulation)</td>
                                    <td id="bench-qaoa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-qaoa-qual" style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">96%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
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

    new_table = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px;"><span style="background: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; padding: 2px 6px; border-radius: 4px; display: inline-block; font-weight: 600;">QAOA (Aer Simulation)</span></td>
                                    <td id="bench-qaoa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-qaoa-qual" style="padding:6px; text-align:center; font-weight:bold; color:#059669;">96%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px;"><span style="background: #fffbeb; color: #b45309; border: 1px solid #fde68a; padding: 2px 6px; border-radius: 4px; display: inline-block; font-weight: 600;">Simulated Annealing (SA)</span></td>
                                    <td id="bench-sa-time" style="padding:6px; text-align:center; font-family:monospace;">— ms</td>
                                    <td id="bench-sa-qual" style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">78%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px;"><span style="background: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 2px 6px; border-radius: 4px; display: inline-block; font-weight: 600;">Greedy Heuristic</span></td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">2 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">72%</td>
                                </tr>
                                <tr>
                                    <td style="padding:6px;"><span style="background: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 2px 6px; border-radius: 4px; display: inline-block; font-weight: 600;">Local Search</span></td>
                                    <td style="padding:6px; text-align:center; font-family:monospace;">3 ms</td>
                                    <td style="padding:6px; text-align:center; font-weight:bold; color:#0f172a;">75%</td>
                                </tr>"""
    content = content.replace(old_table, new_table)

    old_time_bars = """                                    <div>
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

    new_time_bars = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>SA</span> <span id="bar-sa-time-lbl">— ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-sa-time-fill" style="background:#38bdf8; height:100%; width:10%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Greedy</span> <span>2 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#38bdf8; height:100%; width:1%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Local Search</span> <span>3 ms</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#38bdf8; height:100%; width:1%;"></div>
                                        </div>
                                    </div>"""
    content = content.replace(old_time_bars, new_time_bars)

    old_qual_bars = """                                    <div>
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

    new_qual_bars = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>QAOA</span> <span>96%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#10b981; height:100%; width:96%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>SA</span> <span>78%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#3b82f6; height:100%; width:78%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Greedy</span> <span>72%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#f59e0b; height:100%; width:72%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600; color:#0f172a;">
                                            <span>Local Search</span> <span>75%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:#f59e0b; height:100%; width:75%;"></div>
                                        </div>
                                    </div>"""
    content = content.replace(old_qual_bars, new_qual_bars)

    # 3. Simulation Outcome: subtle background cards (#f8fafc), semantic coloring
    old_outcome_boxes = """                            <div style="font-size:0.76rem; line-height:1.4; color:var(--text-secondary); margin-top:8px; display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
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
                                </div>
                                <div style="background:#ffffff; border:1px solid var(--border-color); padding:8px 10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>
                                    <strong id="sim-outcome-pax-saved" style="color:#10b981; font-size:1rem;">—</strong>
                                </div>
                            </div>"""

    new_outcome_boxes = """                            <div style="font-size:0.76rem; line-height:1.4; color:var(--text-secondary); margin-top:8px; display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Initial Delay</span>
                                    <strong id="sim-outcome-init-delay" style="color:#0f172a; font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Final Delay</span>
                                    <strong id="sim-outcome-final-delay" style="color:#0f172a; font-size:1rem;">— min</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:#059669; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Initial Congestion</span>
                                    <strong id="sim-outcome-init-cong" style="color:#d97706; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Final Congestion</span>
                                    <strong id="sim-outcome-final-cong" style="color:#d97706; font-size:1rem;">—%</strong>
                                </div>
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; border-radius:8px;">
                                    <span style="color:#64748b; display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>
                                    <strong id="sim-outcome-pax-saved" style="color:#0d9488; font-size:1rem;">—</strong>
                                </div>
                            </div>"""
    content = content.replace(old_outcome_boxes, new_outcome_boxes)

    # 4. Hardware Ansätz Detail
    old_ansatz = """                        <h4 style="color:var(--text-primary);"><i data-lucide="hash"></i> Hardware Ansätz Detail</h4>
                        <div style="font-size:0.75rem; line-height:1.5; color:var(--text-secondary); display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:8px;">
                            <div>
                                <b>Device Coupling Map:</b> ibm_kyoto<br>
                                <b>Transpiled Qubits:</b> 10 qubits<br>
                                <b>ANSATZ GATES:</b> 166 (CX=4)
                            </div>
                            <div>
                                <b>Error Mitigation:</b> PEC / ZNE<br>
                                <b>Aer Simulation:</b> 1024 shots<br>
                                <b>Optimization Loop:</b> COBYLA
                            </div>
                        </div>"""

    new_ansatz = """                        <h4 style="color:var(--text-primary);"><i data-lucide="hash"></i> Hardware Ansätz Detail</h4>
                        <div style="font-size:0.75rem; line-height:1.8; color:var(--text-secondary); display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:8px;">
                            <div>
                                <b>Device Coupling Map:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">ibm_kyoto</span><br>
                                <b>Transpiled Qubits:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">10 qubits</span><br>
                                <b>ANSATZ GATES:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">166 (CX=4)</span>
                            </div>
                            <div>
                                <b>Error Mitigation:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">PEC / ZNE</span><br>
                                <b>Aer Simulation:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">1024 shots</span><br>
                                <b>Optimization Loop:</b> <span style="background: #f3f4f6; color: #312e81; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px;">COBYLA</span>
                            </div>
                        </div>"""
    content = content.replace(old_ansatz, new_ansatz)

    # 5. Playback Slider (HTML version style tags - single braces)
    old_slider_style = """                                #scenario-tick-slider::-webkit-slider-runnable-track {
                                    width: 100%;
                                    height: 6px;
                                    background: #e2e8f0;
                                    border-radius: 999px;
                                }
                                #scenario-tick-slider::-webkit-slider-thumb {
                                    -webkit-appearance: none;
                                    appearance: none;
                                    width: 16px;
                                    height: 16px;
                                    border-radius: 50%;
                                    background: #0f172a;
                                    border: 2px solid #ffffff;
                                    box-shadow: 0 0 0 1px #cbd5e1;
                                    cursor: pointer;
                                    margin-top: -5px;
                                }
                                #scenario-tick-slider::-moz-range-track {
                                    width: 100%;
                                    height: 6px;
                                    background: #e2e8f0;
                                    border-radius: 999px;
                                }
                                #scenario-tick-slider::-moz-range-thumb {
                                    width: 16px;
                                    height: 16px;
                                    border-radius: 50%;
                                    background: #0f172a;
                                    border: 2px solid #ffffff;
                                    box-shadow: 0 0 0 1px #cbd5e1;
                                    cursor: pointer;
                                }"""

    new_slider_style = """                                #scenario-tick-slider::-webkit-slider-runnable-track {
                                    width: 100%;
                                    height: 6px;
                                    background: transparent;
                                    border-radius: 999px;
                                }
                                #scenario-tick-slider::-webkit-slider-thumb {
                                    -webkit-appearance: none;
                                    appearance: none;
                                    width: 16px;
                                    height: 16px;
                                    border-radius: 50%;
                                    background: #ea580c;
                                    border: 2px solid #ffffff;
                                    box-shadow: 0 0 0 1px #ea580c;
                                    cursor: pointer;
                                    margin-top: -5px;
                                }
                                #scenario-tick-slider::-moz-range-track {
                                    width: 100%;
                                    height: 6px;
                                    background: transparent;
                                    border-radius: 999px;
                                }
                                #scenario-tick-slider::-moz-range-thumb {
                                    width: 16px;
                                    height: 16px;
                                    border-radius: 50%;
                                    background: #ea580c;
                                    border: 2px solid #ffffff;
                                    box-shadow: 0 0 0 1px #ea580c;
                                    cursor: pointer;
                                }"""
    content = content.replace(old_slider_style, new_slider_style)

    # JS Updater Slider Fill function inside HTML
    old_slider_js = """        if (slider) {
            slider.addEventListener("input", function() {
                const tick = parseInt(this.value);
                const snap = SIMULATION_HISTORY[tick] || SIMULATION_HISTORY[SIMULATION_HISTORY.length - 1];
                if (snap) {
                    updateDashboard(snap);
                    document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: ${tick} min (${snap.sim_time_str})`;
                }
            });
        }"""

    new_slider_js = """        if (slider) {
            const updateSliderFill = () => {
                const val = slider.value;
                const min = slider.min ? parseInt(slider.min) : 0;
                const max = slider.max ? parseInt(slider.max) : 120;
                const pct = ((val - min) / (max - min)) * 100;
                slider.style.background = `linear-gradient(to right, #f97316 0%, #f97316 ${pct}%, #e2e8f0 ${pct}%, #e2e8f0 100%)`;
            };
            slider.addEventListener("input", function() {
                const tick = parseInt(this.value);
                const snap = SIMULATION_HISTORY[tick] || SIMULATION_HISTORY[SIMULATION_HISTORY.length - 1];
                if (snap) {
                    updateDashboard(snap);
                    document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: ${tick} min (${snap.sim_time_str})`;
                }
                updateSliderFill();
            });
            updateSliderFill();
        }"""
    content = content.replace(old_slider_js, new_slider_js)

    # Network Status negative state (HTML version)
    old_net_status_js_h = """            const elNetStatus = document.getElementById("sim-outcome-net-status");
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

    new_net_status_js_h = """            const elNetStatus = document.getElementById("sim-outcome-net-status");
            if (elNetStatus) {
                elNetStatus.innerText = netStatusText;
                if (netStatusText === "Stable") {
                    elNetStatus.style.background = "#ecfdf5";
                    elNetStatus.style.color = "#10b981";
                    elNetStatus.style.border = "1px solid #a7f3d0";
                    elNetStatus.style.fontWeight = "700";
                } else if (netStatusText === "Stabilizing") {
                    elNetStatus.style.background = "#fffbeb";
                    elNetStatus.style.color = "#d97706";
                    elNetStatus.style.border = "1px solid #fde68a";
                    elNetStatus.style.fontWeight = "700";
                }} else {
                    elNetStatus.style.background = "#fef2f2";
                    elNetStatus.style.color = "#dc2626";
                    elNetStatus.style.border = "1px solid #fecaca";
                    elNetStatus.style.fontWeight = "700";
                }
            }"""
    content = content.replace(old_net_status_js_h, new_net_status_js_h)
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
