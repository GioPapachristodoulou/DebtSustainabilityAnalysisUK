import pandas as pd
import numpy as np

# --- Configuration ---
CSV_FILE_PATH = 'data/processed/obr_data.csv'

# --- Data from user ---
# Historical Public Sector Net Borrowing (PSNB)
# For years 2007/08 to 2022/23, which we map to 2008 to 2023
psnb_historical_data = [
    47125, 119372, 159906, 141786, 121290, 123911, 102465, 96867, 81516,
    54804, 58916, 44267, 61453, 312942, 121091, 139213
]

def update_psnb_historical():
    """
    Reads the existing CSV, adds the historical PSNB data,
    and updates the CSV file.
    """
    try:
        # Read the existing data
        df = pd.read_csv(CSV_FILE_PATH, index_col='Year')
        print("Successfully read existing CSV file.")

    except FileNotFoundError:
        print(f"Error: The file {CSV_FILE_PATH} was not found.")
        return

    # Add the historical PSNB data
    psnb_years = range(2008, 2008 + len(psnb_historical_data))
    df['PSNB'] = pd.Series(psnb_historical_data, index=psnb_years)
    
    print("\nHistorical PSNB data added.")

    # Save the updated dataframe, overwriting the old file
    df.to_csv(CSV_FILE_PATH)
    print(f"Successfully updated historical PSNB in {CSV_FILE_PATH}.")
    print("Updated data preview:")
    print(df.head())
    print(df.tail())

if __name__ == '__main__':
    update_psnb_historical()
