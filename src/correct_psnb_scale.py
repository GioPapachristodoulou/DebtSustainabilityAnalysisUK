import pandas as pd

# File path for the CSV
csv_file_path = 'data/processed/obr_data.csv'

try:
    # Read the existing CSV file
    df = pd.read_csv(csv_file_path)
    print("Successfully read existing CSV file.")

    # Identify the projection years (2024 and onwards)
    projection_years_mask = df['Year'] >= 2024

    # Correct the scale for PSNB projections by multiplying by 1000 (billions to millions)
    df.loc[projection_years_mask, 'PSNB'] = df.loc[projection_years_mask, 'PSNB'] * 1000
    print("Corrected the scale for PSNB projections from billions to millions.")

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file_path, index=False)
    print(f"Successfully updated PSNB scale in {csv_file_path}.")

    # Display the tail of the updated dataframe to show the corrected values
    print("\nUpdated DataFrame tail:")
    print(df.tail(8))

except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
