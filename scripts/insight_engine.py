# telemetry_ai_coach/scripts/insight_engine.py

import pandas as pd
from collections import defaultdict

def analyze_braking_per_corner(df):
    """
    Analyze braking metrics per corner across laps and provide concise summary feedback.
    """
    feedback = []

    corners = {
        'Turn 1': (100, 200),
        'Turn 2': (300, 400),
        'Turn 3': (500, 600),
    }

    required_columns = {'lap', 'distance', 'brake', 'speed', 'time_sec'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"DataFrame must contain columns: {required_columns}")

    metrics_by_corner = defaultdict(list)
    lap_times = {}

    for lap in df['lap'].unique():
        lap_data = df[df['lap'] == lap]
        lap_time = lap_data['time_sec'].iloc[-1] - lap_data['time_sec'].iloc[0]
        lap_times[lap] = lap_time

        for turn_name, (start_dist, end_dist) in corners.items():
            corner_data = lap_data[(lap_data['distance'] >= start_dist) & (lap_data['distance'] <= end_dist)]
            if corner_data.empty:
                continue

            braking_data = corner_data[corner_data['brake'] > 0]
            if braking_data.empty:
                continue

            braking_start = braking_data['distance'].iloc[0]
            braking_end = braking_data['distance'].iloc[-1]
            braking_duration = braking_end - braking_start

            entry_speed = corner_data.loc[corner_data['distance'] == braking_start, 'speed']
            entry_speed = entry_speed.iloc[0] if not entry_speed.empty else corner_data['speed'].iloc[0]

            min_speed = corner_data['speed'].min()
            exit_speed = corner_data['speed'].iloc[-1]
            time_in_corner = corner_data['time_sec'].iloc[-1] - corner_data['time_sec'].iloc[0]

            valid_exit = exit_speed > min_speed + 10 and time_in_corner > 0.5

            metrics_by_corner[turn_name].append({
                'lap': lap,
                'braking_start': braking_start,
                'braking_duration': braking_duration,
                'entry_speed': entry_speed,
                'min_speed': min_speed,
                'exit_speed': exit_speed,
                'time_in_corner': time_in_corner,
                'valid_exit': valid_exit
            })

    # Summary of lap times
    feedback.append("🕒 Lap Time Summary:")
    for lap, t in sorted(lap_times.items()):
        feedback.append(f"Lap {lap}: {t:.2f} seconds")

    # Corner-by-corner summary
    for turn, laps in metrics_by_corner.items():
        best = min(laps, key=lambda x: x['time_in_corner'] if x['valid_exit'] else float('inf'))
        feedback.append(f"\n🔧 {turn} — Best: Lap {best['lap']} ({best['time_in_corner']:.2f}s, exit {best['exit_speed'] * 0.621371:.1f} mph)")

        # Describe in plain English why this was the best
        previous_laps = [l for l in laps if l['lap'] != best['lap']]
        if previous_laps:
            ref = previous_laps[0]
            brake_diff = ref['braking_start'] - best['braking_start']
            pressure_diff = ((ref['min_speed'] - best['min_speed']) / ref['min_speed']) * 100 if ref['min_speed'] != 0 else 0
            duration_diff = ref['braking_duration'] - best['braking_duration']

            if pressure_diff > 0:
                feedback.append(
                    f"{turn} was fastest as the driver braked {brake_diff * 3.28084:.1f} feet earlier, applied {pressure_diff:.1f}% more pressure, and only braked for {best['braking_duration'] * 3.28084:.1f} feet."
                )
            else:
                feedback.append(
                    f"{turn} was fastest as the driver braked {brake_diff * 3.28084:.1f} feet earlier with lighter brake pressure ({abs(pressure_diff):.1f}% less) and a shorter brake zone of {best['braking_duration'] * 3.28084:.1f} feet."
                )
        else:
            feedback.append(f"Lap {best['lap']} managed a clean line with consistent speed and smooth exit.")

    return feedback
