import pandas as pd
import numpy as np

# --- Configuration ---
CSV_FILE_PATH = 'data/processed/obr_data.csv'

# --- Data from user ---
# Public sector net debt (PSND) as a percentage of GDP
# For years 2023-24 to 2029-30, which we map to 2024 to 2030
psnd_projections_percent = {
    2024: 95.5,
    2025: 95.9,
    2026: 95.1,
    2027: 95.8,
    2028: 96.1,
    2029: 96.3,
    # 2030: 96.1 # We don't have GDP for 2030, so we'll skip this for now
}

def update_psnd_projections():
    """
    Reads the existing CSV, calculates absolute PSND from percentages,
    and updates the CSV file.
    """
    try:
        # Read the existing data
        df = pd.read_csv(CSV_FILE_PATH, index_col='Year')
        print("Successfully read existing CSV file.")
        print("Original data preview:")
        print(df.head())

    except FileNotFoundError:
        print(f"Error: The file {CSV_FILE_PATH} was not found.")
        return

    # Calculate and update the PSND for projection years
    for year, psnd_percent in psnd_projections_percent.items():
        if year in df.index and 'Nominal GDP' in df.columns and pd.notna(df.loc[year, 'Nominal GDP']):
            gdp = df.loc[year, 'Nominal GDP']
            # The historical PSND is in millions, GDP is in billions.
            # The percentages are based on GDP, so we calculate the absolute value in billions.
            # Then multiply by 1000 to be consistent with the historical data format (millions).
            absolute_psnd = (psnd_percent / 100) * gdp * 1000
            df.loc[year, 'PSND'] = absolute_psnd
            print(f"Updated PSND for {year}: {absolute_psnd:.2f}")
        else:
            print(f"Warning: Cannot calculate PSND for {year}. Year or Nominal GDP not found.")

    # Save the updated dataframe, overwriting the old file
    df.to_csv(CSV_FILE_PATH)
    print(f"\nSuccessfully updated PSND projections in {CSV_FILE_PATH}.")
    print("Updated data preview:")
    print(df.tail(10)) # Show the tail to see the new values

if __name__ == '__main__':
    update_psnd_projections()
