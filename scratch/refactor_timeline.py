import os

def refine_template_content(content):
    # 1. Replace Playback Timeline Script block
    old_slider_block = """        if (slider) {{
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

    new_slider_block = """        function updateSliderFill() {{
            if (!slider) return;
            const val = slider.value;
            const min = slider.min ? parseInt(slider.min) : 0;
            const max = slider.max ? parseInt(slider.max) : 120;
            const pct = ((val - min) / (max - min)) * 100;
            slider.style.background = `linear-gradient(to right, #f97316 0%, #f97316 \${pct}%, #e2e8f0 \${pct}%, #e2e8f0 100%)`;
        }}

        if (slider) {{
            slider.addEventListener("input", function() {{
                const tick = parseInt(this.value);
                const snap = SIMULATION_HISTORY.find(h => h.tick === tick) || SIMULATION_HISTORY[SIMULATION_HISTORY.length - 1];
                if (snap) {{
                    updateDashboard(snap);
                    document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: \${tick} min (\${snap.sim_time_str})`;
                }}
                updateSliderFill();
            }});
            updateSliderFill();
        }}"""
    content = content.replace(old_slider_block, new_slider_block)

    # 2. Update dashboard initialization
    old_init = """        // Initialize dashboard with current state
        updateDashboard(EMBEDDED_STATE);"""

    new_init = """        // Initialize dashboard with current state
        updateDashboard(EMBEDDED_STATE);
        if (slider) {{
            slider.max = SIMULATION_HISTORY.length > 0 ? SIMULATION_HISTORY.length - 1 : 120;
            slider.value = EMBEDDED_STATE.tick;
            updateSliderFill();
            document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: \${slider.value} min (\${EMBEDDED_STATE.sim_time_str})`;
        }}"""
    content = content.replace(old_init, new_init)

    # 3. Update pollLiveState slider fill auto-advance
    old_poll = """                        if (prevVal === prevMax || prevVal === state.tick - 1 || prevVal === slider.max - 1) {{
                            slider.value = slider.max;
                            document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: \${slider.value} min (\${state.sim_time_str})`;
                        }}"""

    new_poll = """                        if (prevVal === prevMax || prevVal === state.tick - 1 || prevVal === slider.max - 1) {{
                            slider.value = slider.max;
                            document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: \${slider.value} min (\${state.sim_time_str})`;
                            updateSliderFill();
                        }}"""
    content = content.replace(old_poll, new_poll)
    return content

def refine_html_content(content):
    # HTML version (single braces)
    old_slider_block = """        if (slider) {
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

    new_slider_block = """        function updateSliderFill() {
            if (!slider) return;
            const val = slider.value;
            const min = slider.min ? parseInt(slider.min) : 0;
            const max = slider.max ? parseInt(slider.max) : 120;
            const pct = ((val - min) / (max - min)) * 100;
            slider.style.background = `linear-gradient(to right, #f97316 0%, #f97316 ${pct}%, #e2e8f0 ${pct}%, #e2e8f0 100%)`;
        }

        if (slider) {
            slider.addEventListener("input", function() {
                const tick = parseInt(this.value);
                const snap = SIMULATION_HISTORY.find(h => h.tick === tick) || SIMULATION_HISTORY[SIMULATION_HISTORY.length - 1];
                if (snap) {
                    updateDashboard(snap);
                    document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: ${tick} min (${snap.sim_time_str})`;
                }
                updateSliderFill();
            });
            updateSliderFill();
        }"""
    content = content.replace(old_slider_block, new_slider_block)

    old_init = """        // Initialize dashboard with current state
        updateDashboard(EMBEDDED_STATE);"""

    new_init = """        // Initialize dashboard with current state
        updateDashboard(EMBEDDED_STATE);
        if (slider) {
            slider.max = SIMULATION_HISTORY.length > 0 ? SIMULATION_HISTORY.length - 1 : 120;
            slider.value = EMBEDDED_STATE.tick;
            updateSliderFill();
            document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: ${slider.value} min (${EMBEDDED_STATE.sim_time_str})`;
        }"""
    content = content.replace(old_init, new_init)

    old_poll = """                        if (prevVal === prevMax || prevVal === state.tick - 1 || prevVal === slider.max - 1) {
                            slider.value = slider.max;
                            document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: ${slider.value} min (${state.sim_time_str})`;
                        }"""

    new_poll = """                        if (prevVal === prevMax || prevVal === state.tick - 1 || prevVal === slider.max - 1) {
                            slider.value = slider.max;
                            document.getElementById("scenario-current-tick-lbl").innerText = `Current Tick: ${slider.value} min (${state.sim_time_str})`;
                            updateSliderFill();
                        }"""
    content = content.replace(old_poll, new_poll)
    return content

def main():
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
