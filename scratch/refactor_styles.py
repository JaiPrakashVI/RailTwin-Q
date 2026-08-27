import os

def main():
    filepath = r"c:\Users\idhay\Desktop\RailTwin-Q\frontend\operations.html"
    if not os.path.exists(filepath):
        print(f"Error: file not found at {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace straight line tracks in topology-svg
    old_map_tracks = """                            <!-- Preserved exact lines representing tracks -->
                            <line id="map-track-1"  x1="220" y1="220" x2="450" y2="220" class="track-line track-normal"/>
                            <line id="map-track-3"  x1="450" y1="220" x2="680" y2="220" class="track-line track-normal"/>
                            <line id="map-track-5"  x1="680" y1="220" x2="900" y2="220" class="track-line track-normal"/>
                            <line id="map-track-6"  x1="450" y1="220" x2="450" y2="130" class="track-line track-normal"/>
                            <line id="map-track-7"  x1="450" y1="130" x2="450" y2="50"  class="track-line track-normal"/>
                            <line id="map-track-2"  x1="220" y1="220" x2="220" y2="340" class="track-line track-normal"/>
                            <line id="map-track-10" x1="220" y1="340" x2="450" y2="340" class="track-line track-normal"/>
                            <line id="map-track-4"  x1="220" y1="340" x2="220" y2="420" class="track-line track-normal"/>
                            <line id="map-track-8"  x1="220" y1="420" x2="450" y2="220" class="track-line track-normal"/>
                            <line id="map-track-9"  x1="680" y1="220" x2="680" y2="340" class="track-line track-normal"/>"""

    new_map_tracks = """                            <!-- Preserved exact lines representing tracks -->
                            <path id="map-track-1" d="M 220 220 C 290 190, 380 190, 450 220" class="track-line track-normal"/>
                            <path id="map-track-3" d="M 450 220 C 520 250, 610 250, 680 220" class="track-line track-normal"/>
                            <path id="map-track-5" d="M 680 220 C 750 190, 830 190, 900 220" class="track-line track-normal"/>
                            <path id="map-track-6" d="M 450 220 C 480 190, 480 160, 450 130" class="track-line track-normal"/>
                            <path id="map-track-7" d="M 450 130 C 420 110, 420 70, 450 50" class="track-line track-normal"/>
                            <path id="map-track-2" d="M 220 220 C 240 250, 240 310, 220 340" class="track-line track-normal"/>
                            <path id="map-track-10" d="M 220 340 C 290 370, 380 370, 450 340" class="track-line track-normal"/>
                            <path id="map-track-4" d="M 220 340 C 200 360, 200 400, 220 420" class="track-line track-normal"/>
                            <path id="map-track-8" d="M 220 420 C 300 390, 400 310, 450 220" class="track-line track-normal"/>
                            <path id="map-track-9" d="M 680 220 C 660 250, 660 310, 680 340" class="track-line track-normal"/>"""

    # 2. Replace straight line tracks in topology-svg-twin
    old_twin_tracks = """                        <!-- Tracks -->
                        <line id="twin-track-1"  x1="220" y1="220" x2="450" y2="220" class="track-line track-normal"/>
                        <line id="twin-track-3"  x1="450" y1="220" x2="680" y2="220" class="track-line track-normal"/>
                        <line id="twin-track-5"  x1="680" y1="220" x2="900" y2="220" class="track-line track-normal"/>
                        <line id="twin-track-6"  x1="450" y1="220" x2="450" y2="130" class="track-line track-normal"/>
                        <line id="twin-track-7"  x1="450" y1="130" x2="450" y2="50"  class="track-line track-normal"/>
                        <line id="twin-track-2"  x1="220" y1="220" x2="220" y2="340" class="track-line track-normal"/>
                        <line id="twin-track-10" x1="220" y1="340" x2="450" y2="340" class="track-line track-normal"/>
                        <line id="twin-track-4"  x1="220" y1="340" x2="220" y2="420" class="track-line track-normal"/>
                        <line id="twin-track-8"  x1="220" y1="420" x2="450" y2="220" class="track-line track-normal"/>
                        <line id="twin-track-9"  x1="680" y1="220" x2="680" y2="340" class="track-line track-normal"/>"""

    new_twin_tracks = """                        <!-- Tracks -->
                        <path id="twin-track-1" d="M 220 220 C 290 190, 380 190, 450 220" class="track-line track-normal"/>
                        <path id="twin-track-3" d="M 450 220 C 520 250, 610 250, 680 220" class="track-line track-normal"/>
                        <path id="twin-track-5" d="M 680 220 C 750 190, 830 190, 900 220" class="track-line track-normal"/>
                        <path id="twin-track-6" d="M 450 220 C 480 190, 480 160, 450 130" class="track-line track-normal"/>
                        <path id="twin-track-7" d="M 450 130 C 420 110, 420 70, 450 50" class="track-line track-normal"/>
                        <path id="twin-track-2" d="M 220 220 C 240 250, 240 310, 220 340" class="track-line track-normal"/>
                        <path id="twin-track-10" d="M 220 340 C 290 370, 380 370, 450 340" class="track-line track-normal"/>
                        <path id="twin-track-4" d="M 220 340 C 200 360, 200 400, 220 420" class="track-line track-normal"/>
                        <path id="twin-track-8" d="M 220 420 C 300 390, 400 310, 450 220" class="track-line track-normal"/>
                        <path id="twin-track-9" d="M 680 220 C 660 250, 660 310, 680 340" class="track-line track-normal"/>"""

    # 3. Update Javascript train placement coordinate calculation
    old_js_interpolation = """                                const p = t.progress / 100;
                                tx = srcSt.x + (destSt.x - srcSt.x) * p;
                                ty = srcSt.y + (destSt.y - srcSt.y) * p;"""

    new_js_interpolation = """                                const p = t.progress / 100;
                                const controlPoints = {
                                    1: {cx1: 290, cy1: 190, cx2: 380, cy2: 190},
                                    2: {cx1: 240, cy1: 250, cx2: 240, cy2: 310},
                                    3: {cx1: 520, cy1: 250, cx2: 610, cy2: 250},
                                    4: {cx1: 200, cy1: 360, cx2: 200, cy2: 400},
                                    5: {cx1: 750, cy1: 190, cx2: 830, cy2: 190},
                                    6: {cx1: 480, cy1: 190, cx2: 480, cy2: 160},
                                    7: {cx1: 420, cy1: 110, cx2: 420, cy2: 70},
                                    8: {cx1: 300, cy1: 390, cx2: 400, cy2: 310},
                                    9: {cx1: 660, cy1: 250, cx2: 660, cy2: 310},
                                    10: {cx1: 290, cy1: 370, cx2: 380, cy2: 370}
                                };
                                const cp = controlPoints[t.current_track_id];
                                if (cp) {
                                    const mt = 1 - p;
                                    tx = mt*mt*mt * srcSt.x + 3 * mt*mt * p * cp.cx1 + 3 * mt * p*p * cp.cx2 + p*p*p * destSt.x;
                                    ty = mt*mt*mt * srcSt.y + 3 * mt*mt * p * cp.cy1 + 3 * mt * p*p * cp.cy2 + p*p*p * destSt.y;
                                } else {
                                    tx = srcSt.x + (destSt.x - srcSt.x) * p;
                                    ty = srcSt.y + (destSt.y - srcSt.y) * p;
                                }"""

    # Perform replacements
    content = content.replace(old_map_tracks, new_map_tracks)
    content = content.replace(old_twin_tracks, new_twin_tracks)
    content = content.replace(old_js_interpolation, new_js_interpolation)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print("Success: Edges converted to smooth cubic Bézier curves in operations.html.")

if __name__ == "__main__":
    main()
