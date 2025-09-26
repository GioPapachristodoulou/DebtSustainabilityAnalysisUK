import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File path for the analysis results and directory for plots
analysis_file_path = 'data/processed/dsa_analysis_results.csv'
plots_dir = 'plots'

def run_monte_carlo_simulation():
    """
    Performs and visualizes a Monte Carlo simulation for debt sustainability.
    """
    try:
        # Load the baseline dataset
        df = pd.read_csv(analysis_file_path)
        print("Successfully loaded the baseline analysis results.")

        # --- 1. Parameterize Shocks from Historical Data ---
        hist_df = df[df['Year'] < 2025].copy()
        hist_df['Nominal GDP Growth'] = hist_df['Nominal GDP'].pct_change()
        hist_df['Implied Interest Rate'] = hist_df['Debt Interest'] / hist_df['PSND'].shift(1)
        
        # Standard deviation of historical shocks
        gdp_growth_std = hist_df['Nominal GDP Growth'].std()
        interest_rate_std = hist_df['Implied Interest Rate'].std()
        primary_balance_std = hist_df['Primary Balance-to-GDP Ratio (%)'].std() / 100 # as fraction of GDP

        print(f"Historical Std Dev (GDP Growth): {gdp_growth_std:.4f}")
        print(f"Historical Std Dev (Interest Rate): {interest_rate_std:.4f}")
        print(f"Historical Std Dev (Primary Balance/GDP): {primary_balance_std:.4f}")

        # --- 2. Run Simulation ---
        n_sims = 10000
        forecast_years = range(2025, 2030)
        
        # Store results
        sim_results = np.zeros((len(forecast_years), n_sims))

        baseline_forecast = df[df['Year'] >= 2025].set_index('Year')

        for n in range(n_sims):
            # Create a copy of the forecast to modify in this simulation run
            sim_df = df.copy().set_index('Year')
            
            for i, year in enumerate(forecast_years):
                prev_year = year - 1

                # Generate random shocks
                gdp_shock = np.random.normal(0, gdp_growth_std)
                ir_shock = np.random.normal(0, interest_rate_std)
                pb_shock = np.random.normal(0, primary_balance_std)

                # Apply shocks
                sim_gdp_growth = sim_df.loc[year, 'Nominal GDP'] / sim_df.loc[prev_year, 'Nominal GDP'] - 1 + gdp_shock
                sim_df.loc[year, 'Nominal GDP'] = sim_df.loc[prev_year, 'Nominal GDP'] * (1 + sim_gdp_growth)

                sim_implied_ir = sim_df.loc[year, 'Debt Interest'] / sim_df.loc[prev_year, 'PSND'] + ir_shock
                sim_df.loc[year, 'Debt Interest'] = sim_df.loc[prev_year, 'PSND'] * sim_implied_ir

                sim_primary_balance = (baseline_forecast.loc[year, 'Primary Balance-to-GDP Ratio (%)'] / 100 + pb_shock) * sim_df.loc[year, 'Nominal GDP'] * 1000
                
                # Recalculate dynamics
                sim_psnb = sim_primary_balance + sim_df.loc[year, 'Debt Interest']
                sim_psnd = sim_df.loc[prev_year, 'PSND'] + sim_psnb
                sim_df.loc[year, 'PSND'] = sim_psnd
                
                debt_to_gdp = (sim_psnd / (sim_df.loc[year, 'Nominal GDP'] * 10))
                sim_df.loc[year, 'Debt-to-GDP Ratio (%)'] = debt_to_gdp
                
                # Store result
                sim_results[i, n] = debt_to_gdp

        print(f"Completed {n_sims} simulations.")

        # --- 3. Process and Visualize Results ---
        percentiles = np.percentile(sim_results, [5, 25, 50, 75, 95], axis=1)
        percentile_df = pd.DataFrame(percentiles.T, index=forecast_years, columns=['P5', 'P25', 'P50 (Median)', 'P75', 'P95'])
        
        visualize_fan_chart(df, percentile_df)
        
        # --- 4. Save Results ---
        mc_output_path = 'data/processed/monte_carlo_percentiles.csv'
        percentile_df.to_csv(mc_output_path)
        print(f"Monte Carlo percentile results saved to {mc_output_path}")


    except Exception as e:
        print(f"An error occurred during Monte Carlo simulation: {e}")

def visualize_fan_chart(baseline_df, percentile_df):
    """
    Generates and saves a fan chart of the Monte Carlo simulation results.
    """
    plt.figure(figsize=(14, 8))
    sns.set_theme(style="whitegrid")
    
    years = percentile_df.index
    
    # Plot shaded percentile bands
    plt.fill_between(years, percentile_df['P5'], percentile_df['P95'], color='b', alpha=0.1, label='90% Confidence Interval')
    plt.fill_between(years, percentile_df['P25'], percentile_df['P75'], color='b', alpha=0.2, label='50% Confidence Interval')
    
    # Plot median and baseline
    plt.plot(years, percentile_df['P50 (Median)'], 'b-', marker='o', label='Median Simulation')
    baseline_plot_df = baseline_df[baseline_df['Year'] >= 2024]
    plt.plot(baseline_plot_df['Year'], baseline_plot_df['Debt-to-GDP Ratio (%)'], 'r--', marker='o', label='OBR Baseline Forecast')

    plt.title('Monte Carlo Simulation of UK Debt-to-GDP Ratio (10,000 Simulations)', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Debt-to-GDP Ratio (%)', fontsize=12)
    plt.legend()
    plt.grid(True, which='both', linestyle='-', linewidth=0.5)
    
    plot_path = os.path.join(plots_dir, 'monte_carlo_fan_chart.png')
    plt.savefig(plot_path)
    print(f"Fan chart saved to {plot_path}")
    plt.close()


if __name__ == '__main__':
    run_monte_carlo_simulation()
