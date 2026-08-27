import os

def main():
    filepath = r"c:\Users\idhay\Desktop\RailTwin-Q\services\frontend_generator.py"
    if not os.path.exists(filepath):
        print(f"Error: file not found at {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Search for topbar block with current breadcrumb layout
    old_topbar = """        <!-- THREE-PART TOP BAR -->
        <header class="topbar">
            <!-- Left Info -->
            <div style="display: flex; flex-direction: column;">
                <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-secondary); letter-spacing: 0.05em;">
                    RAILTWIN-Q / OPERATIONS COMMAND CENTER
                </div>
                <div style="font-size: 0.65rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    Hybrid Quantum-AI Railway Decision Intelligence
                </div>
            </div>
            <!-- Center Clock -->
            <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                <div style="font-size: 0.72rem; font-weight: 800; color: var(--accent-green); display: flex; align-items: center; gap: 5px; text-transform: uppercase;">
                    <span class="pulse-dot" style="width: 7px; height: 7px; border-radius: 50%; background: var(--accent-green); display: inline-block;"></span>
                    DIGITAL TWIN LIVE
                </div>
                <div style="font-size: 0.95rem; font-weight: 700; color: var(--text-primary);" id="topbar-sim-clock">
                    Simulation Time: --:--
                </div>
            </div>
            <!-- Right Status Indicators -->
            <div style="display: flex; align-items: center; gap: 10px; font-size: 0.72rem; font-weight: 700;">
                <div style="display: flex; align-items: center; gap: 5px; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); padding: 4px 10px; border-radius: 20px; color: var(--accent-green);">
                    AI <span style="width: 5px; height: 5px; border-radius: 50%; background: var(--accent-green); display: inline-block;"></span> READY
                </div>
                <div style="display: flex; align-items: center; gap: 5px; background: rgba(139, 92, 246, 0.08); border: 1px solid rgba(139, 92, 246, 0.25); padding: 4px 10px; border-radius: 20px; color: var(--accent-purple);">
                    QAOA <span style="width: 5px; height: 5px; border-radius: 50%; background: var(--accent-purple); display: inline-block;"></span> READY
                </div>
            </div>
        </header>"""

    new_topbar = """        <!-- THREE-PART TOP BAR -->
        <header class="topbar">
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

    if old_topbar not in content:
        print("Error: Could not find matching topbar in services/frontend_generator.py")
        return

    content = content.replace(old_topbar, new_topbar)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print("Success: Topbar flex alignment permanently applied to services/frontend_generator.py!")

if __name__ == "__main__":
    main()
