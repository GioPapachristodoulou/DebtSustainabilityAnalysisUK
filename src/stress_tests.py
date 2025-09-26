import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File path for the analysis results and directory for plots
analysis_file_path = 'data/processed/dsa_analysis_results.csv'
plots_dir = 'plots'

def run_stress_tests():
    """
    Performs and visualizes stress tests on UK debt sustainability.
    """
    try:
        # Load the baseline dataset
        baseline_df = pd.read_csv(analysis_file_path)
        print("Successfully loaded the baseline analysis results.")

        # --- Scenario 1: Interest Rate Shock ---
        ir_shock_df = perform_interest_rate_shock(baseline_df.copy())
        print("Completed Interest Rate Shock scenario.")

        # --- Scenario 2: GDP Growth Shock ---
        gdp_shock_df = perform_gdp_growth_shock(baseline_df.copy())
        print("Completed GDP Growth Shock scenario.")

        # --- Visualization ---
        visualize_scenarios(baseline_df, ir_shock_df, gdp_shock_df)
        print("Stress test visualizations saved.")
        
        # --- Save Results ---
        stress_test_output_path = 'data/processed/stress_test_results.xlsx'
        with pd.ExcelWriter(stress_test_output_path) as writer:
            baseline_df.to_excel(writer, sheet_name='Baseline', index=False)
            ir_shock_df.to_excel(writer, sheet_name='Interest_Rate_Shock', index=False)
            gdp_shock_df.to_excel(writer, sheet_name='GDP_Growth_Shock', index=False)
        print(f"All stress test results saved to {stress_test_output_path}")


    except FileNotFoundError:
        print(f"Error: The file {analysis_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred during stress testing: {e}")

def perform_interest_rate_shock(df):
    """
    Simulates a +1 percentage point shock to interest rates from 2025.
    """
    # Calculate baseline implied interest rate
    df['Implied Interest Rate'] = df['Debt Interest'] / df['PSND'].shift(1)
    
    # Apply a +0.01 (1 ppt) shock from 2025 onwards
    shock_period = df['Year'] >= 2025
    df.loc[shock_period, 'Implied Interest Rate'] += 0.01

    # Recalculate debt dynamics for the forecast period
    for year in range(2025, 2030):
        idx = df[df['Year'] == year].index[0]
        prev_idx = df[df['Year'] == year - 1].index[0]

        # Recalculate Debt Interest
        df.loc[idx, 'Debt Interest'] = df.loc[prev_idx, 'PSND'] * df.loc[idx, 'Implied Interest Rate']
        
        # Recalculate PSNB (Primary Balance + new Debt Interest)
        df.loc[idx, 'PSNB'] = df.loc[idx, 'Primary Balance'] + df.loc[idx, 'Debt Interest']
        
        # Recalculate PSND (Previous PSND + new PSNB)
        df.loc[idx, 'PSND'] = df.loc[prev_idx, 'PSND'] + df.loc[idx, 'PSNB']
        
        # Recalculate Debt-to-GDP Ratio
        df.loc[idx, 'Debt-to-GDP Ratio (%)'] = (df.loc[idx, 'PSND'] / (df.loc[idx, 'Nominal GDP'] * 10))
        
    return df

def perform_gdp_growth_shock(df):
    """
    Simulates a -1 percentage point shock to nominal GDP growth from 2025.
    """
    # Calculate baseline nominal GDP growth rate
    df['Nominal GDP Growth'] = df['Nominal GDP'].pct_change()
    
    # Apply a -0.01 (1 ppt) shock to growth from 2025 onwards
    shock_period = df['Year'] >= 2025
    df.loc[shock_period, 'Nominal GDP Growth'] -= 0.01

    # Recalculate GDP and debt dynamics
    for year in range(2025, 2030):
        idx = df[df['Year'] == year].index[0]
        prev_idx = df[df['Year'] == year - 1].index[0]

        # Recalculate Nominal GDP
        df.loc[idx, 'Nominal GDP'] = df.loc[prev_idx, 'Nominal GDP'] * (1 + df.loc[idx, 'Nominal GDP Growth'])
        
        # Recalculate Primary Balance based on fiscal sensitivity (0.5% of GDP)
        gdp_diff = (df.loc[idx, 'Nominal GDP'] - df[df['Year'] == year]['Nominal GDP'].iloc[0]) * 1_000_000_000
        primary_balance_shock = gdp_diff * 0.005 # 0.5% sensitivity
        df.loc[idx, 'Primary Balance'] += primary_balance_shock / 1_000_000 # convert back to millions
        
        # Recalculate PSNB and PSND
        df.loc[idx, 'PSNB'] = df.loc[idx, 'Primary Balance'] + df.loc[idx, 'Debt Interest']
        df.loc[idx, 'PSND'] = df.loc[prev_idx, 'PSND'] + df.loc[idx, 'PSNB']
        
        # Recalculate Debt-to-GDP Ratio
        df.loc[idx, 'Debt-to-GDP Ratio (%)'] = (df.loc[idx, 'PSND'] / (df.loc[idx, 'Nominal GDP'] * 10))
        
    return df

def visualize_scenarios(baseline_df, ir_shock_df, gdp_shock_df):
    """
    Generates a plot comparing the Debt-to-GDP ratio across scenarios.
    """
    plt.figure(figsize=(12, 8))
    sns.set_theme(style="whitegrid")

    plt.plot(baseline_df['Year'], baseline_df['Debt-to-GDP Ratio (%)'], marker='o', linestyle='-', label='Baseline')
    plt.plot(ir_shock_df['Year'], ir_shock_df['Debt-to-GDP Ratio (%)'], marker='x', linestyle='--', label='Interest Rate Shock (+1 ppt)')
    plt.plot(gdp_shock_df['Year'], gdp_shock_df['Debt-to-GDP Ratio (%)'], marker='s', linestyle='--', label='GDP Growth Shock (-1 ppt)')

    plt.title('Debt-to-GDP Ratio: Stress Test Scenarios', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Debt-to-GDP Ratio (%)', fontsize=12)
    plt.axvline(x=2024, color='grey', linestyle=':', label='Forecast Horizon')
    plt.legend()
    plt.grid(True, which='both', linestyle='-', linewidth=0.5)
    
    plot_path = os.path.join(plots_dir, 'stress_test_scenarios.png')
    plt.savefig(plot_path)
    plt.close()

if __name__ == '__main__':
    run_stress_tests()
