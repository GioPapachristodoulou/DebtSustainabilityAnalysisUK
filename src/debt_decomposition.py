import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File path for the analysis results and directory for plots
analysis_file_path = 'data/processed/dsa_analysis_results.csv'
plots_dir = 'plots'

def run_debt_decomposition():
    """
    Performs and visualizes the decomposition of changes in the Debt-to-GDP ratio.
    """
    try:
        # Load the dataset
        df = pd.read_csv(analysis_file_path)
        print("Successfully loaded the analysis results.")

        # --- 1. Calculate Necessary Components ---
        # Ensure calculations are on a per-unit basis, not percentage
        df['debt_ratio'] = df['Debt-to-GDP Ratio (%)'] / 100
        df['pb_ratio'] = df['Primary Balance-to-GDP Ratio (%)'] / 100
        
        # Lagged debt ratio
        df['debt_ratio_lagged'] = df['debt_ratio'].shift(1)
        
        # Nominal GDP Growth (g)
        df['g'] = df['Nominal GDP'].pct_change()
        
        # Effective Interest Rate (r)
        df['r'] = df['Debt Interest'] / df['PSND'].shift(1)
        
        # --- 2. Decompose the Change in Debt Ratio ---
        # Contribution from the primary balance
        df['Primary Balance Effect'] = -df['pb_ratio']
        
        # Contribution from the "snowball effect"
        # Formula: ((r - g) / (1 + g)) * d_t-1
        df['Snowball Effect'] = ((df['r'] - df['g']) / (1 + df['g'])) * df['debt_ratio_lagged']
        
        # Actual change in debt ratio
        df['Debt Ratio Change'] = df['debt_ratio'].diff()
        
        # Contribution from stock-flow adjustments (the residual)
        df['Stock-Flow Adjustment'] = df['Debt Ratio Change'] - df['Primary Balance Effect'] - df['Snowball Effect']
        
        # Convert effects to percentage points for plotting
        cols_to_convert = ['Primary Balance Effect', 'Snowball Effect', 'Stock-Flow Adjustment', 'Debt Ratio Change']
        for col in cols_to_convert:
            df[col] = df[col] * 100

        print("Completed debt decomposition calculations.")

        # --- 3. Visualize the Decomposition ---
        visualize_decomposition(df)
        
        # --- 4. Save the results ---
        decomposition_output_path = 'data/processed/debt_decomposition_results.csv'
        df.to_csv(decomposition_output_path, index=False)
        print(f"Decomposition results saved to {decomposition_output_path}")

    except Exception as e:
        print(f"An error occurred during debt decomposition: {e}")

def visualize_decomposition(df):
    """
    Generates a stacked bar chart of the debt decomposition.
    """
    # Filter for the relevant period (from 2009 onwards as 2008 has no lagged data)
    plot_df = df[df['Year'] >= 2009].copy()
    
    plt.figure(figsize=(16, 9))
    sns.set_theme(style="whitegrid")
    
    # Plot the stacked bars
    plt.bar(plot_df['Year'], plot_df['Primary Balance Effect'], label='Primary Balance Contribution', color='g')
    plt.bar(plot_df['Year'], plot_df['Snowball Effect'], bottom=plot_df['Primary Balance Effect'], label='Snowball Effect (r-g)', color='b')
    plt.bar(plot_df['Year'], plot_df['Stock-Flow Adjustment'], bottom=plot_df['Primary Balance Effect'] + plot_df['Snowball Effect'], label='Stock-Flow Adjustment', color='orange')
    
    # Plot the actual change in debt as a line
    plt.plot(plot_df['Year'], plot_df['Debt Ratio Change'], 'r-o', label='Total Change in Debt-to-GDP Ratio')
    
    plt.title('Decomposition of Annual Change in UK Debt-to-GDP Ratio', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Change in Debt-to-GDP Ratio (Percentage Points)', fontsize=14)
    plt.axvline(x=2024.5, color='k', linestyle='--', label='Forecast Horizon')
    plt.xticks(plot_df['Year'], rotation=45)
    plt.legend()
    plt.tight_layout()
    
    plot_path = os.path.join(plots_dir, 'debt_decomposition.png')
    plt.savefig(plot_path)
    print(f"Debt decomposition plot saved to {plot_path}")
    plt.close()

if __name__ == '__main__':
    run_debt_decomposition()
