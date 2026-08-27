import os

def refine_template_content(content):
    # 1. QAOA READY Badge (template)
    old_qaoa_badge = """                <div style="display: flex; align-items: center; gap: 5px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 4px 12px; border-radius: 12px; color: #475569; font-size: 11px; font-weight: 600;">
                    QAOA READY
                </div>"""
    new_qaoa_badge = """                <div style="display: flex; align-items: center; gap: 5px; background-color: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">
                    QAOA READY
                </div>"""
    content = content.replace(old_qaoa_badge, new_qaoa_badge)

    # 2. Delay Prediction Horizon Bars (template)
    old_horizon_bars = """            // Generate visual blocks
            const drawBlocks = (val) => {{
                const count = Math.min(12, Math.max(1, Math.round(val / 2)));
                return "█".repeat(count).padEnd(12, "░");
            }};

            barsContainer.innerHTML = `
                <div style="margin-bottom: 12px; font-family: monospace; font-size: 0.82rem; line-height: 1.6;">
                    <div>+15m <span style="color:var(--accent-blue);">${{drawBlocks(p15)}}</span> ${{p15.toFixed(1)}}</div>
                    <div>+30m <span style="color:var(--accent-purple);">${{drawBlocks(p30)}}</span> ${{p30.toFixed(1)}}</div>
                    <div>+60m <span style="color:var(--accent-cyan);">${{drawBlocks(p60)}}</span> ${{p60.toFixed(1)}}</div>
                </div>
            `;"""
    
    new_horizon_bars = """            const p15Pct = Math.min(100, Math.round((p15 / maxVal) * 100));
            const p30Pct = Math.min(100, Math.round((p30 / maxVal) * 100));
            const p60Pct = Math.min(100, Math.round((p60 / maxVal) * 100));

            barsContainer.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 12px;">
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-bottom: 4px;">
                            <span>+15m Horizon</span>
                            <strong style="color: #0f172a;">+${{p15.toFixed(1)}} min</strong>
                        </div>
                        <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                            <div style="height: 100%; width: ${{p15Pct}}%; background: #0ea5e9; border-radius: 999px;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-bottom: 4px;">
                            <span>+30m Horizon</span>
                            <strong style="color: #0f172a;">+${{p30.toFixed(1)}} min</strong>
                        </div>
                        <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                            <div style="height: 100%; width: ${{p30Pct}}%; background: #f59e0b; border-radius: 999px;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-bottom: 4px;">
                            <span>+60m Horizon</span>
                            <strong style="color: #ef4444;">+${{p60.toFixed(1)}} min</strong>
                        </div>
                        <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                            <div style="height: 100%; width: ${{p60Pct}}%; background: #ef4444; border-radius: 999px;"></div>
                        </div>
                    </div>
                </div>
            `;"""
    content = content.replace(old_horizon_bars, new_horizon_bars)

    # 3. Prediction Timeline Chart (template & HTML unified)
    old_timeline_svg = """                            <svg viewBox="0 0 400 80" style="width:100%; height:75px; background:#f8fafc; border:1px solid var(--border-color); border-radius:8px;">
                                <!-- Timeline horizontal line -->
                                <line x1="50" y1="40" x2="350" y2="40" stroke="#cbd5e1" stroke-width="3"/>
                                <!-- Points -->
                                <circle cx="50" cy="40" r="6" fill="var(--accent-blue)"/>
                                <text x="50" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--text-secondary)">Current</text>
                                <text x="50" y="58" text-anchor="middle" font-size="10.5" font-weight="800" fill="var(--accent-red)" id="tl-cur-val">0.0</text>
                                
                                <circle cx="150" cy="40" r="6" fill="var(--accent-blue)"/>
                                <text x="150" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--text-secondary)">+15m</text>
                                <text x="150" y="58" text-anchor="middle" font-size="10.5" font-weight="800" fill="var(--text-primary)" id="tl-15-val">0.0</text>
                                
                                <circle cx="250" cy="40" r="6" fill="var(--accent-blue)"/>
                                <text x="250" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--text-secondary)">+30m</text>
                                <text x="250" y="58" text-anchor="middle" font-size="10.5" font-weight="800" fill="var(--text-primary)" id="tl-30-val">0.0</text>
                                
                                <circle cx="350" cy="40" r="6" fill="var(--accent-blue)"/>
                                <text x="350" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--text-secondary)">+60m</text>
                                <text x="350" y="58" text-anchor="middle" font-size="10.5" font-weight="800" fill="var(--text-primary)" id="tl-60-val">0.0</text>
                            </svg>"""

    new_timeline_svg = """                            <svg viewBox="0 0 400 80" style="width:100%; height:75px; background:rgba(37, 99, 235, 0.08); border:1px solid var(--border-color); border-radius:8px;">
                                <!-- Timeline horizontal line -->
                                <line x1="50" y1="40" x2="350" y2="40" stroke="#2563eb" stroke-width="2"/>
                                <!-- Points -->
                                <circle cx="50" cy="40" r="6" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>
                                <text x="50" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--text-secondary)">Current</text>
                                <text x="50" y="58" text-anchor="middle" font-size="10.5" font-weight="800" fill="var(--accent-red)" id="tl-cur-val">0.0</text>
                                
                                <circle cx="150" cy="40" r="6" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>
                                <text x="150" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--text-secondary)">+15m</text>
                                <text x="150" y="58" text-anchor="middle" font-size="10.5" font-weight="800" fill="var(--text-primary)" id="tl-15-val">0.0</text>
                                
                                <circle cx="250" cy="40" r="6" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>
                                <text x="250" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--text-secondary)">+30m</text>
                                <text x="250" y="58" text-anchor="middle" font-size="10.5" font-weight="800" fill="var(--text-primary)" id="tl-30-val">0.0</text>
                                
                                <circle cx="350" cy="40" r="6" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>
                                <text x="350" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--text-secondary)">+60m</text>
                                <text x="350" y="58" text-anchor="middle" font-size="10.5" font-weight="800" fill="var(--text-primary)" id="tl-60-val">0.0</text>
                            </svg>"""
    content = content.replace(old_timeline_svg, new_timeline_svg)

    # 4. Machine Learning Pipeline (Model Details - template & HTML unified)
    old_ml_boxes = """                                    <div style="display: flex; flex-direction: column; gap: 5px;">
                                         <div style="background: #ffffff; border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.58rem; text-align: center; color:var(--text-primary);">XGBoost</div>
                                         <div style="background: #ffffff; border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.58rem; text-align: center; color:var(--text-primary);">LightGBM</div>
                                         <div style="background: #ffffff; border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.58rem; text-align: center; color:var(--text-primary);">Random Forest</div>
                                     </div>
                                     <div style="font-size: 1rem; color: var(--text-muted);">➔</div>
                                     <div style="background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); color: white; padding: 8px 12px; border-radius: 6px; font-weight: 700; font-size: 0.65rem; text-align: center; box-shadow: var(--shadow-sm);">
                                         Ensemble Prediction
                                     </div>"""

    new_ml_boxes = """                                    <div style="display: flex; flex-direction: column; gap: 5px;">
                                         <div style="background: #f8fafc; border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.58rem; text-align: center; color: #475569;">XGBoost</div>
                                         <div style="background: #f8fafc; border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.58rem; text-align: center; color: #475569;">LightGBM</div>
                                         <div style="background: #f8fafc; border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.58rem; text-align: center; color: #475569;">Random Forest</div>
                                     </div>
                                     <div style="font-size: 1rem; color: var(--text-muted);">➔</div>
                                     <div style="background: #0f172a; color: #ffffff; padding: 8px 12px; border-radius: 6px; font-weight: 700; font-size: 0.65rem; text-align: center; box-shadow: var(--shadow-sm);">
                                         Ensemble Prediction
                                     </div>"""
    content = content.replace(old_ml_boxes, new_ml_boxes)

    # 5. Hierarchical Flow Diagram (template & HTML unified)
    old_flow = """                            <div style="background: #ffffff; border: 1px solid var(--border-color); padding: 5px 12px; border-radius: 6px; font-weight: 700; font-size: 0.72rem; min-width: 100px; text-align: center; color: var(--accent-blue);">Station</div>
                            <div style="font-size: 0.95rem; color: var(--text-muted); line-height: 1;">↓</div>
                            <div style="background: #ffffff; border: 1px solid var(--border-color); padding: 5px 12px; border-radius: 6px; font-weight: 700; font-size: 0.72rem; min-width: 100px; text-align: center; color: var(--accent-cyan);">Track</div>
                            <div style="font-size: 0.95rem; color: var(--text-muted); line-height: 1;">↓</div>
                            <div style="background: #ffffff; border: 1px solid var(--border-color); padding: 5px 12px; border-radius: 6px; font-weight: 700; font-size: 0.72rem; min-width: 100px; text-align: center; color: var(--accent-green);">Network</div>"""

    new_flow = """                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 5px 12px; border-radius: 6px; font-weight: 700; font-size: 0.72rem; min-width: 100px; text-align: center; color: #334155;">Station</div>
                            <div style="font-size: 0.95rem; color: var(--text-muted); line-height: 1;">↓</div>
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 5px 12px; border-radius: 6px; font-weight: 700; font-size: 0.72rem; min-width: 100px; text-align: center; color: #334155;">Track</div>
                            <div style="font-size: 0.95rem; color: var(--text-muted); line-height: 1;">↓</div>
                            <div style="background: #ecfdf5; border: 1px solid #a7f3d0; padding: 5px 12px; border-radius: 6px; font-weight: 700; font-size: 0.72rem; min-width: 100px; text-align: center; color: #065f46;">Network</div>"""
    content = content.replace(old_flow, new_flow)
    return content

def refine_html_content(content):
    # 1. QAOA READY Badge (HTML)
    old_qaoa_badge = """                <div style="display: flex; align-items: center; gap: 5px; background: #fff7ed; border: 1px solid #ffedd5; padding: 4px 12px; border-radius: 12px; color: #ea580c; font-size: 0.72rem; font-weight: 700;">
                    QAOA <span style="width: 5px; height: 5px; border-radius: 50%; background: #ea580c; display: inline-block;"></span> READY
                </div>"""
    new_qaoa_badge = """                <div style="display: flex; align-items: center; gap: 5px; background-color: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">
                    QAOA READY
                </div>"""
    content = content.replace(old_qaoa_badge, new_qaoa_badge)

    # 2. Delay Prediction Horizon Bars (HTML)
    old_horizon_bars = """            // Generate visual blocks
            const drawBlocks = (val) => {
                const count = Math.min(12, Math.max(1, Math.round(val / 2)));
                return "█".repeat(count).padEnd(12, "░");
            };

            barsContainer.innerHTML = `
                <div style="margin-bottom: 12px; font-family: monospace; font-size: 0.82rem; line-height: 1.6;">
                    <div>+15m <span style="color:var(--accent-blue);">${drawBlocks(p15)}</span> ${p15.toFixed(1)}</div>
                    <div>+30m <span style="color:var(--accent-purple);">${drawBlocks(p30)}</span> ${p30.toFixed(1)}</div>
                    <div>+60m <span style="color:var(--accent-cyan);">${drawBlocks(p60)}</span> ${p60.toFixed(1)}</div>
                </div>
            `;"""
    
    new_horizon_bars = """            const p15Pct = Math.min(100, Math.round((p15 / maxVal) * 100));
            const p30Pct = Math.min(100, Math.round((p30 / maxVal) * 100));
            const p60Pct = Math.min(100, Math.round((p60 / maxVal) * 100));

            barsContainer.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 12px;">
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-bottom: 4px;">
                            <span>+15m Horizon</span>
                            <strong style="color: #0f172a;">+${p15.toFixed(1)} min</strong>
                        </div>
                        <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                            <div style="height: 100%; width: ${p15Pct}%; background: #0ea5e9; border-radius: 999px;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-bottom: 4px;">
                            <span>+30m Horizon</span>
                            <strong style="color: #0f172a;">+${p30.toFixed(1)} min</strong>
                        </div>
                        <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                            <div style="height: 100%; width: ${p30Pct}%; background: #f59e0b; border-radius: 999px;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-bottom: 4px;">
                            <span>+60m Horizon</span>
                            <strong style="color: #ef4444;">+${p60.toFixed(1)} min</strong>
                        </div>
                        <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                            <div style="height: 100%; width: ${p60Pct}%; background: #ef4444; border-radius: 999px;"></div>
                        </div>
                    </div>
                </div>
            `;"""
    content = content.replace(old_horizon_bars, new_horizon_bars)

    # 3. Apply general common replacements (Prediction Timeline, Machine Learning, Hierarchical Flow)
    content = refine_template_content(content)
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
