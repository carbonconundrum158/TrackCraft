import pandas as pd
from scripts.insight_engine import analyze_braking_per_corner

def main():
    # Load telemetry data
    df = pd.read_csv('data/sample_lap_with_distance.csv')

    # Perform analysis
    feedback = analyze_braking_per_corner(df)

    # Display feedback
    for line in feedback:
        print(line)

if __name__ == "__main__":
    main()
