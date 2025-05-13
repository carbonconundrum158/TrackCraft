# telemetry_ai_coach/scripts/parser_racechrono.py

import pandas as pd

def parse_racechrono_csv(filepath):
    """
    Parses a RaceChrono CSV export and maps it to the standard telemetry schema.
    """
    try:
        df = pd.read_csv(filepath)

        column_map = {
            'Time': 'time_sec',
            'Speed (kph)': 'speed_kph',
            'Throttle': 'throttle',
            'Brake': 'brake',
            'RPM': 'rpm',
            'Latitude': 'lat',
            'Longitude': 'lon',
            'Lap': 'lap',
            'Steering angle': 'steering',
        }

        # Rename known columns
        df.rename(columns={k: v for k, v in column_map.items() if k in df.columns}, inplace=True)

        # Fill in missing but expected columns with NaN
        for col in ['throttle', 'brake', 'rpm', 'steering']:
            if col not in df.columns:
                df[col] = pd.NA

        # Ensure time is numeric and in seconds
        if 'time_sec' in df.columns:
            df['time_sec'] = pd.to_numeric(df['time_sec'], errors='coerce')

        # Drop rows without time or speed
        df.dropna(subset=['time_sec', 'speed_kph'], inplace=True)

        return df

    except Exception as e:
        print(f"Error parsing RaceChrono file: {e}")
        return None



def load_telemetry(filepath, source_type):
    """
    Dispatch function to load telemetry data from various supported sources.
    """
    if source_type == "racechrono":
        return parse_racechrono_csv(filepath)
    # Future source types can be added here:
    # elif source_type == "motec":
    #     return parse_motec_csv(filepath)
    # elif source_type == "aim":
    #     return parse_aim_csv(filepath)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")