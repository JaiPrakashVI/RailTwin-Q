import os

def refine_content(content):
    # 1. Update station details dynamic populator in Javascript
    old_populator = """                    const platColor = platPct >= 75 ? "#ef4444" : (platPct >= 45 ? "#f59e0b" : "#10b981");
                    const congColor = st.congestion >= 75 ? "#ef4444" : (st.congestion >= 45 ? "#f59e0b" : "#10b981");
                    
                    const congPill = st.congestion >= 75 ? '<span class="pill-status pill-high">HIGH</span>' : (st.congestion >= 45 ? '<span class="pill-status pill-medium">MEDIUM</span>' : '<span class="pill-status pill-low">LOW</span>');
                    const activeDisPill = activeDis === "Nominal" ? '<span class="pill-status pill-nominal">NOMINAL</span>' : `<span class="pill-status pill-high">\\${activeDis}</span>`;
                    
                    container.innerHTML = `
                        <div style="font-weight: 700; font-size: 12px; letter-spacing: 0.05em; margin-bottom: 4px; color: #0f172a; text-transform: uppercase;">STATION DETAILS</div>
                        <div style="font-size: 12px; margin-bottom: 16px; color: #64748b;">Station: \\${st.name} | ID: \\${st.id}</div>
                        
                        <div style="margin-bottom: 12px; border-bottom: 1px dashed #e2e8f0; padding-bottom: 10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Platform Capacity:</span>
                                <strong style="color:#0f172a;">\\${platPct}%</strong>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: \\${platPct}%; background: \\${platColor}; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 12px; font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px dashed #e2e8f0; padding-bottom:10px; color:#64748b;">
                            <span>Current Trains:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">\\${st.platforms_occupied}</strong>
                        </div>
                        
                        <div style="margin-bottom: 12px; border-bottom: 1px dashed #e2e8f0; padding-bottom: 10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Predicted Congestion:</span>
                                <span>\\${congPill}</span>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: \\subst_congestion%; background: \\${congColor}; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 12px; font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px dashed #e2e8f0; padding-bottom:10px; color:#64748b;">
                            <span>Predicted Delay +30m:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">+\\${(st.congestion * 0.22).toFixed(1)} min</strong>
                        </div>
                        
                        <div style="font-size:12px; display:flex; justify-content:space-between; align-items:center; color:#64748b; padding-top:2px;">
                            <span>Active Disruption:</span>
                            <span>\\${activeDisPill}</span>
                        </div>
                    `.replace('subst_congestion', '${st.congestion}');"""

    # Escape dynamic variables for raw file search if needed (ops_html string format has double-braces in python code)
    new_populator = """                    const congPill = st.congestion >= 75 ? '<span class="pill-status pill-high">HIGH</span>' : (st.congestion >= 45 ? '<span class="pill-status pill-medium">MEDIUM</span>' : '<span class="pill-status pill-low">LOW</span>');
                    const activeDisPill = activeDis === "Nominal" ? '<span class="pill-status pill-nominal">NOMINAL</span>' : `<span class="pill-status pill-high">\\${activeDis}</span>`;
                    
                    container.innerHTML = `
                        <div style="font-weight: 700; font-size: 12px; letter-spacing: 0.05em; margin-bottom: 4px; color: #0f172a; text-transform: uppercase;">STATION DETAILS</div>
                        <div style="font-size: 12px; margin-bottom: 16px; color: #64748b;">Station: \\${st.name} | ID: \\${st.id}</div>
                        
                        <div style="border-bottom: 1px solid #f1f5f9; padding: 8px 0;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Platform Capacity:</span>
                                <strong style="color:#0f172a;">\\${platPct}%</strong>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: \\${platPct}%; background: #f97316; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding: 8px 0; color:#64748b;">
                            <span>Current Trains:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">\\${st.platforms_occupied}</strong>
                        </div>
                        
                        <div style="border-bottom: 1px solid #f1f5f9; padding: 8px 0;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Predicted Congestion:</span>
                                <span>\\${congPill}</span>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: \\subst_congestion%; background: #f97316; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding: 8px 0; color:#64748b;">
                            <span>Predicted Delay +30m:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">+\\${(st.congestion * 0.22).toFixed(1)} min</strong>
                        </div>
                        
                        <div style="font-size:12px; display:flex; justify-content:space-between; align-items:center; color:#64748b; padding-top:8px;">
                            <span>Active Disruption:</span>
                            <span>\\${activeDisPill}</span>
                        </div>
                    `.replace('subst_congestion', '${st.congestion}');"""

    if old_populator in content:
        content = content.replace(old_populator, new_populator)
    else:
        # Fallback for plain HTML version (without python-specific double brace escaping)
        old_populator_html = """                    const platColor = platPct >= 75 ? "#ef4444" : (platPct >= 45 ? "#f59e0b" : "#10b981");
                    const congColor = st.congestion >= 75 ? "#ef4444" : (st.congestion >= 45 ? "#f59e0b" : "#10b981");
                    
                    const congPill = st.congestion >= 75 ? '<span class="pill-status pill-high">HIGH</span>' : (st.congestion >= 45 ? '<span class="pill-status pill-medium">MEDIUM</span>' : '<span class="pill-status pill-low">LOW</span>');
                    const activeDisPill = activeDis === "Nominal" ? '<span class="pill-status pill-nominal">NOMINAL</span>' : `<span class="pill-status pill-high">${activeDis}</span>`;
                    
                    container.innerHTML = `
                        <div style="font-weight: 700; font-size: 12px; letter-spacing: 0.05em; margin-bottom: 4px; color: #0f172a; text-transform: uppercase;">STATION DETAILS</div>
                        <div style="font-size: 12px; margin-bottom: 16px; color: #64748b;">Station: ${st.name} | ID: ${st.id}</div>
                        
                        <div style="margin-bottom: 12px; border-bottom: 1px dashed #e2e8f0; padding-bottom: 10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Platform Capacity:</span>
                                <strong style="color:#0f172a;">${platPct}%</strong>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: ${platPct}%; background: ${platColor}; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 12px; font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px dashed #e2e8f0; padding-bottom:10px; color:#64748b;">
                            <span>Current Trains:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">${st.platforms_occupied}</strong>
                        </div>
                        
                        <div style="margin-bottom: 12px; border-bottom: 1px dashed #e2e8f0; padding-bottom: 10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Predicted Congestion:</span>
                                <span>${congPill}</span>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: ${st.congestion}%; background: ${congColor}; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 12px; font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px dashed #e2e8f0; padding-bottom:10px; color:#64748b;">
                            <span>Predicted Delay +30m:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">+${(st.congestion * 0.22).toFixed(1)} min</strong>
                        </div>
                        
                        <div style="font-size:12px; display:flex; justify-content:space-between; align-items:center; color:#64748b; padding-top:2px;">
                            <span>Active Disruption:</span>
                            <span>${activeDisPill}</span>
                        </div>
                    `;"""

        new_populator_html = """                    const congPill = st.congestion >= 75 ? '<span class="pill-status pill-high">HIGH</span>' : (st.congestion >= 45 ? '<span class="pill-status pill-medium">MEDIUM</span>' : '<span class="pill-status pill-low">LOW</span>');
                    const activeDisPill = activeDis === "Nominal" ? '<span class="pill-status pill-nominal">NOMINAL</span>' : `<span class="pill-status pill-high">${activeDis}</span>`;
                    
                    container.innerHTML = `
                        <div style="font-weight: 700; font-size: 12px; letter-spacing: 0.05em; margin-bottom: 4px; color: #0f172a; text-transform: uppercase;">STATION DETAILS</div>
                        <div style="font-size: 12px; margin-bottom: 16px; color: #64748b;">Station: ${st.name} | ID: ${st.id}</div>
                        
                        <div style="border-bottom: 1px solid #f1f5f9; padding: 8px 0;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Platform Capacity:</span>
                                <strong style="color:#0f172a;">${platPct}%</strong>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: ${platPct}%; background: #f97316; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding: 8px 0; color:#64748b;">
                            <span>Current Trains:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">${st.platforms_occupied}</strong>
                        </div>
                        
                        <div style="border-bottom: 1px solid #f1f5f9; padding: 8px 0;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:6px; color:#64748b;">
                                <span>Predicted Congestion:</span>
                                <span>${congPill}</span>
                            </div>
                            <div style="height: 6px; border-radius: 999px; background: #e2e8f0; overflow: hidden;">
                                <div style="height: 100%; width: ${st.congestion}%; background: #f97316; border-radius: 999px;"></div>
                            </div>
                        </div>
                        
                        <div style="font-size:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding: 8px 0; color:#64748b;">
                            <span>Predicted Delay +30m:</span>
                            <strong style="color:#0f172a; font-family: monospace; font-size: 13px;">+${(st.congestion * 0.22).toFixed(1)} min</strong>
                        </div>
                        
                        <div style="font-size:12px; display:flex; justify-content:space-between; align-items:center; color:#64748b; padding-top:8px;">
                            <span>Active Disruption:</span>
                            <span>${activeDisPill}</span>
                        </div>
                    `;"""
        content = content.replace(old_populator_html, new_populator_html)

    # 2. Update Network State Card Header alignment
    old_ns_header = """                        <h4 style="font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 10px; text-transform: uppercase; display: flex; align-items: center; gap: 6px;">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: #f97316;">
                                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                            </svg>
                            NETWORK STATE
                        </h4>"""

    new_ns_header = """                        <h4 style="font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 10px; text-transform: uppercase; display: flex; align-items: center; gap: 8px; justify-content: flex-start;">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: #f97316; flex-shrink: 0;">
                                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                            </svg>
                            NETWORK STATE
                        </h4>"""

    content = content.replace(old_ns_header, new_ns_header)
    return content

def main():
    # 1. Update frontend_generator.py
    generator_path = r"c:\Users\idhay\Desktop\RailTwin-Q\services\frontend_generator.py"
    if os.path.exists(generator_path):
        with open(generator_path, "r", encoding="utf-8") as f:
            gen_content = f.read()
        gen_content_new = refine_content(gen_content)
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
        ops_content_new = refine_content(ops_content)
        with open(ops_path, "w", encoding="utf-8") as f:
            f.write(ops_content_new)
        print("Success: Refined html directly inside frontend/operations.html!")
    else:
        print("Warning: frontend/operations.html not found.")

if __name__ == "__main__":
    main()
