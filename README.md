# 🏁 TrackCraft AI Coach

**TrackCraft** is a Python-based tool that analyzes lap telemetry from racing data to deliver turn-by-turn performance feedback in plain English.

### 🚗 Features
- Compares multiple laps to identify braking improvements
- Highlights the best line through each corner
- Outputs lap time summaries
- Generates corner-specific coaching like:
  - "Turn 1 was fastest as the driver braked 32 feet earlier with lighter brake pressure and a shorter brake zone."

### 📊 Input
CSV file containing telemetry data with:
- `lap`
- `distance`
- `brake`
- `speed`
- `time_sec`

### 🧠 How It Works
The script:
1. Segments your telemetry by laps and corners.
2. Extracts braking points, durations, speeds.
3. Compares lap segments to identify what made a turn faster.

### ✅ Example
🔧 Turn 1 — Best: Lap 3 (3.40s, exit 85.0 mph)
Turn 1 was fastest as the driver braked 32.5 feet earlier with lighter brake pressure (8.7% less) and a shorter brake zone of 90.2 feet.

### 🔧 Run It
```bash
python main.py data/sample_lap.csv
