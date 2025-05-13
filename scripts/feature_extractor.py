# telemetry_ai_coach/scripts/feature_extractor.py

import pandas as pd
import numpy as np

def extract_braking_features(lap_df):
    """
    Analyze braking behavior in a single lap.
    Returns summary stats such as number of brake zones, average brake pressure, and consistency.
    """
    if 'brake' not in lap_df.columns:
        raise ValueError("Brake data not available in lap DataFrame.")

    brake_signal = lap_df['brake'].fillna(0).astype(float)
    brake_threshold = 5.0  # assume signal above 5 indicates braking

    # Identify braking zones
    is_braking = brake_signal > brake_threshold
    transitions = is_braking.astype(int).diff().fillna(0)
    brake_starts = lap_df[transitions == 1].index
    brake_ends = lap_df[transitions == -1].index

    # Edge case: braking continues to end of lap
    if len(brake_ends) < len(brake_starts):
        brake_ends = brake_ends.append(pd.Index([len(lap_df) - 1]))

    brake_zones = list(zip(brake_starts, brake_ends))
    zone_count = len(brake_zones)

    avg_brake_pressure = brake_signal[is_braking].mean()
    brake_duration = sum((lap_df.loc[end, 'time_sec'] - lap_df.loc[start, 'time_sec']) for start, end in brake_zones)

    return {
        "brake_zone_count": zone_count,
        "avg_brake_pressure": avg_brake_pressure,
        "total_brake_duration_sec": brake_duration,
    }

def compare_braking_between_laps(laps):
    """
    Compare braking features across laps to find inconsistencies or patterns.
    """
    results = {}
    for lap_num, lap_df in laps.items():
        results[lap_num] = extract_braking_features(lap_df)
    return results
