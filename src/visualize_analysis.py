import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File path for the analysis results
analysis_file_path = 'data/processed/dsa_analysis_results.csv'

# Directory to save plots
plots_dir = 'plots'

def visualize_results():
    """
    Generates and saves plots for the debt sustainability analysis.
    """
    try:
        # Load the dataset
        df = pd.read_csv(analysis_file_path)
        print("Successfully loaded the analysis results.")

        # Set plot style
        sns.set_theme(style="whitegrid")

        # --- 1. Plot Debt-to-GDP Ratio ---
        plt.figure(figsize=(12, 7))
        debt_gdp_plot = sns.lineplot(x='Year', y='Debt-to-GDP Ratio (%)', data=df, marker='o', color='b')
        plt.title('UK Debt-to-GDP Ratio (2008-2029)', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Debt-to-GDP Ratio (%)', fontsize=12)
        plt.axvline(x=2024, color='r', linestyle='--', label='Forecast Horizon')
        plt.legend()
        plt.grid(True)
        
        # Save the plot
        debt_gdp_plot_path = os.path.join(plots_dir, 'debt_to_gdp_ratio.png')
        plt.savefig(debt_gdp_plot_path)
        print(f"Debt-to-GDP ratio plot saved to {debt_gdp_plot_path}")
        plt.close()

        # --- 2. Plot Primary Balance-to-GDP Ratio ---
        plt.figure(figsize=(12, 7))
        primary_balance_plot = sns.barplot(x='Year', y='Primary Balance-to-GDP Ratio (%)', data=df, palette='viridis')
        plt.title('UK Primary Balance-to-GDP Ratio (2008-2029)', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Primary Balance-to-GDP Ratio (%)', fontsize=12)
        plt.axvline(x=16.5, color='r', linestyle='--', label='Forecast Horizon') # 16.5 is between 2024 and 2025
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot
        primary_balance_plot_path = os.path.join(plots_dir, 'primary_balance_to_gdp_ratio.png')
        plt.savefig(primary_balance_plot_path)
        print(f"Primary Balance-to-GDP ratio plot saved to {primary_balance_plot_path}")
        plt.close()

    except FileNotFoundError:
        print(f"Error: The file {analysis_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred during visualization: {e}")

if __name__ == '__main__':
    visualize_results()
