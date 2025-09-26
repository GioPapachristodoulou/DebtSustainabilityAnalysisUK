import pandas as pd
import numpy as np

# File path for the processed data
csv_file_path = 'data/processed/obr_data.csv'

def run_analysis():
    """
    Performs the debt sustainability analysis.
    """
    try:
        # Load the dataset
        df = pd.read_csv(csv_file_path)
        print("Successfully loaded the dataset.")

        # --- 1. Calculate Debt-to-GDP Ratio ---
        # PSND is in millions, Nominal GDP is in billions.
        # To get the ratio, we need them in the same units.
        # Debt-to-GDP = (PSND * 1,000,000) / (Nominal GDP * 1,000,000,000) * 100
        # This simplifies to (PSND / (Nominal GDP * 1000)) * 100
        df['Debt-to-GDP Ratio (%)'] = (df['PSND'] / (df['Nominal GDP'] * 10))
        print("Calculated Debt-to-GDP ratio.")

        # --- 2. Calculate Primary Balance ---
        # Primary Balance = PSNB - Debt Interest (both are in millions)
        df['Primary Balance'] = df['PSNB'] - df['Debt Interest']
        print("Calculated Primary Balance.")
        
        # --- 3. Calculate Primary Balance to GDP Ratio ---
        df['Primary Balance-to-GDP Ratio (%)'] = (df['Primary Balance'] / (df['Nominal GDP'] * 10))
        print("Calculated Primary Balance-to-GDP ratio.")

        # Display the DataFrame with the new calculations
        print("\nAnalysis Results:")
        print(df.to_string())
        
        # Save the enhanced data to a new CSV for record-keeping
        analysis_output_path = 'data/processed/dsa_analysis_results.csv'
        df.to_csv(analysis_output_path, index=False)
        print(f"\nAnalysis results saved to {analysis_output_path}")


    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred during analysis: {e}")

if __name__ == '__main__':
    run_analysis()
