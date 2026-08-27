import os

def main():
    filepath = r"c:\Users\idhay\Desktop\RailTwin-Q\services\frontend_generator.py"
    if not os.path.exists(filepath):
        print(f"Error: file not found at {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update trains.forEach loop header to include idx parameter
    old_foreach = "                trains.forEach(t => {{"
    new_foreach = "                trains.forEach((t, idx) => {{"
    
    if old_foreach not in content:
        print("Warning: Could not find trains.forEach loop header.")
    content = content.replace(old_foreach, new_foreach)

    # 2. Alternating Left / Right Tag Positioning
    old_text_creation = """                        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                        text.setAttribute("x", tx);
                        text.setAttribute("y", ty + dy - 8);
                        text.setAttribute("text-anchor", "middle");"""

    new_text_creation = """                        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                        const isLeft = (idx % 2 === 0);
                        if (isLeft) {{
                            text.setAttribute("x", tx - 9);
                            text.setAttribute("y", ty + dy + 3);
                            text.setAttribute("text-anchor", "end");
                        }} else {{
                            text.setAttribute("x", tx + 9);
                            text.setAttribute("y", ty + dy + 3);
                            text.setAttribute("text-anchor", "start");
                        }}"""

    if old_text_creation not in content:
        print("Warning: Could not find old_text_creation block.")
    content = content.replace(old_text_creation, new_text_creation)

    # 3. MAS Station Label shift (left side placement to avoid overlapping train clusters)
    old_mas_tab1 = '<g transform="translate(220,220)" id="map-station-1"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text y="-20" class="station-label">MAS</text></g>'
    new_mas_tab1 = '<g transform="translate(220,220)" id="map-station-1"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text x="-22" y="4" class="station-label" style="text-anchor: end;">MAS</text></g>'
    
    if old_mas_tab1 not in content:
        print("Warning: Could not find MAS tab1 block.")
    content = content.replace(old_mas_tab1, new_mas_tab1)

    old_mas_tab2 = '<g transform="translate(220,220)" id="twin-station-1" class="clickable-station" onclick="onStationClick(event, 1)"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text y="-20" class="station-label">MAS</text></g>'
    new_mas_tab2 = '<g transform="translate(220,220)" id="twin-station-1" class="clickable-station" onclick="onStationClick(event, 1)"><circle r="14" class="station-bg"/><circle r="7" class="station-core"/><text x="-22" y="4" class="station-label" style="text-anchor: end;">MAS</text></g>'
    
    if old_mas_tab2 not in content:
        print("Warning: Could not find MAS tab2 block.")
    content = content.replace(old_mas_tab2, new_mas_tab2)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print("Success: Alternating left/right train tags and side MAS label positioning permanently applied!")

if __name__ == "__main__":
    main()
