import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File paths
processed_data_dir = 'data/processed'
plots_dir = 'plots'
gdp_data_path = os.path.join(processed_data_dir, 'dsa_full_analysis.csv')

def run_revenue_analysis():
    """
    Analyzes and visualizes the historical and forecast composition of UK government revenue.
    """
    try:
        # --- 1. Load GDP data to calculate forecast ratios ---
        gdp_df = pd.read_csv(gdp_data_path)[['Year', 'Nominal GDP']]
        gdp_map = gdp_df.set_index('Year')['Nominal GDP']
        print("Successfully loaded GDP data.")

        # --- 2. Historical Data (% of GDP) ---
        hist_data = {
            'Year': range(2008, 2024),
            'Personal Taxes': [16.3, 15.9, 15.8, 15.6, 15.3, 15.1, 15.1, 15.2, 15.6, 15.5, 15.8, 15.6, 17.1, 17.4, 17.9],
            'Business Taxes': [3.9, 4.0, 4.1, 4.1, 3.9, 3.8, 3.9, 3.8, 4.1, 4.0, 4.0, 3.6, 3.4, 4.1, 4.3],
            'Consumption Taxes': [9.2, 9.4, 10.1, 10.7, 10.5, 10.6, 10.6, 10.6, 10.5, 10.4, 10.5, 10.2, 9.7, 10.4, 10.5],
            'Total Receipts': [35.9, 36.1, 37.0, 37.4, 36.9, 36.8, 36.8, 36.9, 37.4, 37.1, 37.4, 36.7, 38.1, 39.3, 40.3]
        }
        hist_df = pd.DataFrame(hist_data)

        # --- 3. Forecast Data (£ billion) ---
        forecast_data = {
            'Year': range(2024, 2030),
            'Personal Taxes': [424.2, 455.4, 482.9, 510.5, 525.1, 545.7],
            'Business Taxes': [ # Sum of Corp Tax, Other Current Taxes, Capital Taxes
                (347.6 - 1.1 - 0.0), # Taxes on production and imports
                (365.2 - 1.3 - 0.0),
                (387.1 - 1.5 - 0.0),
                (402.4 - 1.8 - 0.0),
                (415.3 - 2.0 - 0.0),
                (429.8 - 2.0 - 0.0)
            ],
            'Consumption Taxes': [347.6, 365.2, 387.1, 402.4, 415.3, 429.8],
            'Total Receipts': [1141.2, 1229.5, 1292.3, 1350.7, 1394.0, 1445.0]
        }
        forecast_df = pd.DataFrame(forecast_data)

        # Convert forecast £bn to % of GDP
        for col in forecast_df.columns:
            if col != 'Year':
                forecast_df[col] = (forecast_df[col] / gdp_map[forecast_df['Year']].values) * 100
        print("Converted forecast data to % of GDP.")

        # --- 4. Combine DataFrames ---
        full_df = pd.concat([hist_df, forecast_df], ignore_index=True)
        full_df['Other Revenue'] = full_df['Total Receipts'] - full_df['Personal Taxes'] - full_df['Business Taxes'] - full_df['Consumption Taxes']
        
        print("Combined historical and forecast data.")

        # --- 5. Visualize and Save ---
        visualize_composition(full_df)
        
        output_path = os.path.join(processed_data_dir, 'revenue_composition_full.csv')
        full_df.to_csv(output_path, index=False)
        print(f"Full revenue composition data saved to {output_path}")

    except Exception as e:
        print(f"An error occurred during revenue analysis: {e}")

def visualize_composition(df):
    """
    Generates a stacked area chart of revenue composition from 2008-2029.
    """
    plt.figure(figsize=(16, 9))
    sns.set_theme(style="whitegrid")
    
    plot_cols = ['Personal Taxes', 'Business Taxes', 'Consumption Taxes', 'Other Revenue']
    
    plt.stackplot(df['Year'], df[plot_cols].T, labels=plot_cols, alpha=0.8)
    
    plt.title('Composition of UK Public Sector Revenue (% of GDP), 2008-2029', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Percentage of GDP', fontsize=14)
    plt.legend(loc='upper left')
    plt.xlim(df['Year'].min(), df['Year'].max())
    plt.axvline(x=2024, color='k', linestyle='--', label='Forecast Horizon')
    plt.grid(True)
    
    plot_path = os.path.join(plots_dir, 'revenue_composition_analysis.png')
    plt.savefig(plot_path)
    print(f"Revenue composition plot saved to {plot_path}")
    plt.close()

if __name__ == '__main__':
    run_revenue_analysis()
