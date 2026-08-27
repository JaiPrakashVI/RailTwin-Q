import os

def refine_template_content(content):
    # 1. Table QAOA Highlight
    old_tr = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:700; color:var(--accent-purple);">QAOA (Aer Simulation)</td>"""
    new_tr = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:600; color:#4f46e5;">QAOA (Aer Simulation)</td>"""
    content = content.replace(old_tr, new_tr)

    # 2. Time Bar Chart QAOA bar fill
    old_fill = """                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-qaoa-time-fill" style="background:var(--accent-purple); height:100%; width:80%;"></div>
                                        </div>"""
    new_fill = """                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-qaoa-time-fill" style="background:#6366f1; height:100%; width:80%;"></div>
                                        </div>"""
    content = content.replace(old_fill, new_fill)

    # 3. Solution Quality (%) Progress Bars
    old_qual_bars = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>QAOA</span> <span>96%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-green); height:100%; width:96%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>SA</span> <span>78%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-yellow); height:100%; width:78%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Greedy</span> <span>72%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-yellow); height:100%; width:72%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Local Search</span> <span>75%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-yellow); height:100%; width:75%;"></div>
                                        </div>
                                    </div>"""

    new_qual_bars = """                                    <div>
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
    content = content.replace(old_qual_bars, new_qual_bars)

    # 4. Simulation Outcome Numbers styling
    old_pax_saved = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>
                                    <strong id="sim-outcome-pax-saved" style="color:var(--accent-blue); font-size:1rem;">—</strong>"""
    new_pax_saved = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>
                                    <strong id="sim-outcome-pax-saved" style="color:#10b981; font-size:1rem;">—</strong>"""
    content = content.replace(old_pax_saved, new_pax_saved)

    old_delay_red = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:var(--accent-green); font-size:1rem;">—%</strong>"""
    new_delay_red = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:#0d9488; font-size:1rem;">—%</strong>"""
    content = content.replace(old_delay_red, new_delay_red)

    # 5. Playback Slider (template with escaped double braces)
    old_slider_t = """                        <div style="background: #f1f5f9; border: 1px solid var(--border-color); padding: 15px; border-radius: 12px;">
                            <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.85rem; margin-bottom: 8px;">
                                <span id="scenario-current-tick-lbl" style="color: var(--accent-blue); font-family: monospace;">Current Tick: 0 min (08:00 AM)</span>
                                <span style="color: var(--text-muted);">Total: 120 min</span>
                            </div>
                            <input type="range" id="scenario-tick-slider" min="0" max="120" value="0" style="width: 100%; height: 6px; background: rgba(0, 0, 0, 0.1); border-radius: 4px; outline: none; cursor: pointer; accent-color: var(--accent-blue);">
                        </div>"""

    new_slider_t = """                        <div style="background: #f1f5f9; border: 1px solid var(--border-color); padding: 15px; border-radius: 12px;">
                            <style>
                                #scenario-tick-slider {{
                                    -webkit-appearance: none;
                                    appearance: none;
                                    width: 100%;
                                    height: 6px;
                                    background: #e2e8f0;
                                    border-radius: 999px;
                                    outline: none;
                                }}
                                #scenario-tick-slider::-webkit-slider-runnable-track {{
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
                                }}
                            </style>
                            <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.85rem; margin-bottom: 8px;">
                                <span id="scenario-current-tick-lbl" style="color: #0f172a; font-family: monospace;">Current Tick: 0 min (08:00 AM)</span>
                                <span style="color: var(--text-muted);">Total: 120 min</span>
                            </div>
                            <input type="range" id="scenario-tick-slider" min="0" max="120" value="0">
                        </div>"""
    content = content.replace(old_slider_t, new_slider_t)
    return content

def refine_html_content(content):
    # Same as refine_template_content, but with single braces for style tag inside HTML
    old_tr = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:700; color:var(--accent-purple);">QAOA (Aer Simulation)</td>"""
    new_tr = """                                <tr style="border-bottom:1px solid #f1f5f9;">
                                    <td style="padding:6px; font-weight:600; color:#4f46e5;">QAOA (Aer Simulation)</td>"""
    content = content.replace(old_tr, new_tr)

    old_fill = """                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-qaoa-time-fill" style="background:var(--accent-purple); height:100%; width:80%;"></div>
                                        </div>"""
    new_fill = """                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div id="bar-qaoa-time-fill" style="background:#6366f1; height:100%; width:80%;"></div>
                                        </div>"""
    content = content.replace(old_fill, new_fill)

    old_qual_bars = """                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>QAOA</span> <span>96%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-green); height:100%; width:96%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>SA</span> <span>78%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-yellow); height:100%; width:78%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Greedy</span> <span>72%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-yellow); height:100%; width:72%;"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-bottom:2px; font-weight:600;">
                                            <span>Local Search</span> <span>75%</span>
                                        </div>
                                        <div style="background:#e2e8f0; height:6px; border-radius:3px; width:100%; overflow:hidden;">
                                            <div style="background:var(--accent-yellow); height:100%; width:75%;"></div>
                                        </div>
                                    </div>"""

    new_qual_bars = """                                    <div>
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
    content = content.replace(old_qual_bars, new_qual_bars)

    old_pax_saved = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>
                                    <strong id="sim-outcome-pax-saved" style="color:var(--accent-blue); font-size:1rem;">—</strong>"""
    new_pax_saved = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Passenger Hours Saved</span>
                                    <strong id="sim-outcome-pax-saved" style="color:#10b981; font-size:1rem;">—</strong>"""
    content = content.replace(old_pax_saved, new_pax_saved)

    old_delay_red = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:var(--accent-green); font-size:1rem;">—%</strong>"""
    new_delay_red = """                                    <span style="color:var(--text-muted); display:block; font-size:0.68rem; text-transform:uppercase;">Delay Reduction</span>
                                    <strong id="sim-outcome-delay-red" style="color:#0d9488; font-size:1rem;">—%</strong>"""
    content = content.replace(old_delay_red, new_delay_red)

    # Playback Slider (HTML style tags - single braces)
    old_slider_html = """                        <div style="background: #f1f5f9; border: 1px solid var(--border-color); padding: 15px; border-radius: 12px;">
                            <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.85rem; margin-bottom: 8px;">
                                <span id="scenario-current-tick-lbl" style="color: var(--accent-blue); font-family: monospace;">Current Tick: 0 min (08:00 AM)</span>
                                <span style="color: var(--text-muted);">Total: 120 min</span>
                            </div>
                            <input type="range" id="scenario-tick-slider" min="0" max="120" value="0" style="width: 100%; height: 6px; background: rgba(0, 0, 0, 0.1); border-radius: 4px; outline: none; cursor: pointer; accent-color: var(--accent-blue);">
                        </div>"""

    new_slider_html = """                        <div style="background: #f1f5f9; border: 1px solid var(--border-color); padding: 15px; border-radius: 12px;">
                            <style>
                                #scenario-tick-slider {
                                    -webkit-appearance: none;
                                    appearance: none;
                                    width: 100%;
                                    height: 6px;
                                    background: #e2e8f0;
                                    border-radius: 999px;
                                    outline: none;
                                }
                                #scenario-tick-slider::-webkit-slider-runnable-track {
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
                                }
                            </style>
                            <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.85rem; margin-bottom: 8px;">
                                <span id="scenario-current-tick-lbl" style="color: #0f172a; font-family: monospace;">Current Tick: 0 min (08:00 AM)</span>
                                <span style="color: var(--text-muted);">Total: 120 min</span>
                            </div>
                            <input type="range" id="scenario-tick-slider" min="0" max="120" value="0">
                        </div>"""
    content = content.replace(old_slider_html, new_slider_html)
    return content

def main():
    # 1. Update frontend_generator.py
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

    # 2. Update operations.html directly
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
