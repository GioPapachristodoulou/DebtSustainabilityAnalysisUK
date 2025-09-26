import pandas as pd
import numpy as np

# File path for the CSV
csv_file_path = 'data/processed/obr_data.csv'

# Historical debt interest data provided by the user (in millions)
# For years 2008 to 2023
historical_debt_interest = [
    34895,  # 2008
    24431,  # 2009
    39324,  # 2010
    45004,  # 2011
    37969,  # 2012
    38472,  # 2013
    37588,  # 2014
    33041,  # 2015
    35659,  # 2016
    42487,  # 2017
    42094,  # 2018
    36845,  # 2019
    25132,  # 2020
    47552,  # 2021
    114670, # 2022
    111300  # 2023 (Placeholder, will be updated if user provides it)
]

# Debt interest projection data (in billions, needs to be converted to millions)
# For years 2024 to 2029
debt_interest_projections = {
    2024: 87.5,
    2025: 101.5,
    2026: 104.8,
    2027: 113.4,
    2028: 121.1,
    2029: 129.3
}

try:
    # Read the existing CSV file
    df = pd.read_csv(csv_file_path)
    print("Successfully read existing CSV file.")

    # Set 'Year' as the index for easier data alignment
    df.set_index('Year', inplace=True)

    # --- Update Historical Data ---
    # Create a Series for the historical data with the correct index
    historical_years = range(2008, 2024)
    historical_series = pd.Series(historical_debt_interest, index=historical_years)

    # Update the 'Debt Interest' column for historical years
    df.loc[historical_years, 'Debt Interest'] = historical_series
    print("Historical debt interest data added for years 2008-2023.")

    # --- Update Projection Data ---
    # Convert projections from billions to millions and update the DataFrame
    for year, value_billion in debt_interest_projections.items():
        if year in df.index:
            df.loc[year, 'Debt Interest'] = value_billion * 1000
    print("Debt interest projection data added for years 2024-2029.")

    # Reset the index to have 'Year' as a column again
    df.reset_index(inplace=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file_path, index=False)
    print(f"Successfully updated 'Debt Interest' column in {csv_file_path}.")

    # Display the entire DataFrame to show the newly populated column
    print("\nFinal DataFrame with Debt Interest:")
    print(df.to_string())

except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
