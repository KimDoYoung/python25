from screeninfo import get_monitors

monitors = get_monitors()

for i, m in enumerate(monitors):
    print(f"[{i}] {m.name} - {m.width}x{m.height} at ({m.x}, {m.y})")
