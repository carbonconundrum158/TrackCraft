# telemetry_ai_coach/scripts/lap_segmenter.py

import pandas as pd

def segment_laps(df):
    """
    Segment the telemetry DataFrame into laps based on the 'lap' column.
    Returns a dictionary: {lap_number: DataFrame for that lap}
    """
    if 'lap' not in df.columns:
        raise ValueError("Lap column not found in DataFrame.")

    lap_data = {}
    for lap_num in df['lap'].dropna().unique():
        lap_df = df[df['lap'] == lap_num].copy()
        lap_data[int(lap_num)] = lap_df.reset_index(drop=True)

    return lap_data
