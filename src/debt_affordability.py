import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File paths
analysis_file_path = 'data/processed/dsa_analysis_results.csv'
output_file_path = 'data/processed/dsa_full_analysis.csv'
plots_dir = 'plots'

def run_affordability_analysis():
    """
    Calculates and visualizes the debt affordability ratio.
    """
    try:
        # Load the dataset
        df = pd.read_csv(analysis_file_path)
        print("Successfully loaded the analysis results.")

        # --- 1. Add Total Revenue Data ---
        # Data provided by the user and from OBR forecasts
        total_revenue_data = {
            2008: 583854, 2009: 569099, 2010: 563967, 2011: 603409, 2012: 624923,
            2013: 636794, 2014: 663829, 2015: 690628, 2016: 714078, 2017: 757572,
            2018: 780660, 2019: 813448, 2020: 826494, 2021: 793539, 2022: 919925,
            2023: 1017488,
            # Forecasts in billions, converted to millions
            2024: 1105.5 * 1000, 2025: 1192.2 * 1000, 2026: 1253.8 * 1000,
            2027: 1310.8 * 1000, 2028: 1352.8 * 1000, 2029: 1402.4 * 1000
        }
        df['Total Revenue'] = df['Year'].map(total_revenue_data)
        print("Added Total Revenue data.")

        # --- 2. Calculate Debt Affordability Ratio ---
        # Interest Payments as a % of Total Revenue
        df['Debt Affordability Ratio (%)'] = (df['Debt Interest'] / df['Total Revenue']) * 100
        print("Calculated Debt Affordability Ratio.")

        # --- 3. Visualize the Result ---
        visualize_affordability(df)

        # --- 4. Save the final dataset ---
        df.to_csv(output_file_path, index=False)
        print(f"Full analysis including affordability metrics saved to {output_file_path}")

    except Exception as e:
        print(f"An error occurred during affordability analysis: {e}")

def visualize_affordability(df):
    """
    Generates a plot for the Debt Affordability Ratio.
    """
    plt.figure(figsize=(12, 7))
    sns.set_theme(style="whitegrid")
    
    plt.plot(df['Year'], df['Debt Affordability Ratio (%)'], marker='o', linestyle='-', color='purple')
    
    plt.title('UK Debt Affordability: Interest Payments as a Percentage of Revenue', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Interest Payments / Revenue (%)', fontsize=12)
    plt.axvline(x=2024, color='r', linestyle='--', label='Forecast Horizon')
    plt.legend()
    plt.grid(True, which='both', linestyle='-', linewidth=0.5)
    
    # Highlight the recent peak
    peak_year = 2022
    peak_value = df[df['Year'] == peak_year]['Debt Affordability Ratio (%)'].iloc[0]
    plt.annotate(f'Peak: {peak_value:.1f}%', 
                 xy=(peak_year, peak_value), 
                 xytext=(peak_year - 4, peak_value + 1),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=12)
    
    plot_path = os.path.join(plots_dir, 'debt_affordability_ratio.png')
    plt.savefig(plot_path)
    print(f"Debt affordability plot saved to {plot_path}")
    plt.close()

if __name__ == '__main__':
    run_affordability_analysis()
