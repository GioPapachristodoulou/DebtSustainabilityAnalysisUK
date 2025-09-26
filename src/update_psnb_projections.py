import pandas as pd
import numpy as np

# File path for the CSV
csv_file_path = 'data/processed/obr_data.csv'

# PSNB projection data provided by the user
psnb_projections_data = {
    2024: 137.3,
    2025: 117.7,
    2026: 97.2,
    2027: 80.2,
    2028: 77.4,
    2029: 74.0
}

try:
    # Read the existing CSV file
    df = pd.read_csv(csv_file_path)
    print("Successfully read existing CSV file.")

    # Set 'Year' as the index to easily update rows
    df.set_index('Year', inplace=True)

    # Update the 'PSNB' column with the projection data
    for year, value in psnb_projections_data.items():
        if year in df.index:
            df.loc[year, 'PSNB'] = value

    # Reset the index to have 'Year' as a column again
    df.reset_index(inplace=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file_path, index=False)
    print(f"Successfully updated PSNB projections in {csv_file_path}.")

    # Display the head and tail of the updated dataframe
    print("\nUpdated DataFrame head:")
    print(df.head())
    print("\nUpdated DataFrame tail:")
    print(df.tail())

except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
