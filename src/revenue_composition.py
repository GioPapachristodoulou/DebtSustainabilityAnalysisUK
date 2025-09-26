import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Directory for plots and processed data
plots_dir = 'plots'
processed_data_dir = 'data/processed'

def analyze_revenue_composition():
    """
    Analyzes and visualizes the composition of UK government revenue as a % of GDP.
    """
    try:
        # --- 1. Create DataFrame from provided historical data ---
        revenue_data = {
            'Year': range(2008, 2024),
            'Total personal taxes': [16.3, 15.9, 15.8, 15.6, 15.3, 15.1, 15.1, 15.2, 15.6, 15.5, 15.8, 15.6, 17.1, 17.4, 17.9],
            'Total business taxes': [3.9, 4.0, 4.1, 4.1, 3.9, 3.8, 3.9, 3.8, 4.1, 4.0, 4.0, 3.6, 3.4, 4.1, 4.3],
            'Total consumption taxes': [9.2, 9.4, 10.1, 10.7, 10.5, 10.6, 10.6, 10.6, 10.5, 10.4, 10.5, 10.2, 9.7, 10.4, 10.5],
            'Public Sector Current Receipts': [35.9, 36.1, 37.0, 37.4, 36.9, 36.8, 36.8, 36.9, 37.4, 37.1, 37.4, 36.7, 38.1, 39.3, 40.3]
        }
        df = pd.DataFrame(revenue_data)
        
        # Calculate 'Other Revenue' as the residual
        df['Other Revenue'] = df['Public Sector Current Receipts'] - df['Total personal taxes'] - df['Total business taxes'] - df['Total consumption taxes']
        
        print("Successfully created revenue composition DataFrame.")

        # --- 2. Visualize the Composition ---
        visualize_composition(df)

        # --- 3. Save the data ---
        output_path = os.path.join(processed_data_dir, 'revenue_composition_gdp.csv')
        df.to_csv(output_path, index=False)
        print(f"Revenue composition data saved to {output_path}")

    except Exception as e:
        print(f"An error occurred during revenue composition analysis: {e}")

def visualize_composition(df):
    """
    Generates a stacked area chart of revenue composition.
    """
    plt.figure(figsize=(14, 8))
    sns.set_theme(style="whitegrid")
    
    # Columns to plot
    plot_cols = ['Total personal taxes', 'Total business taxes', 'Total consumption taxes', 'Other Revenue']
    labels = ['Personal Taxes', 'Business Taxes', 'Consumption Taxes', 'Other Revenue']
    
    # Create the stacked area plot
    plt.stackplot(df['Year'], df[plot_cols].T, labels=labels, alpha=0.8)
    
    plt.title('Composition of UK Public Sector Revenue (% of GDP)', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Percentage of GDP', fontsize=14)
    plt.legend(loc='upper left')
    plt.xlim(df['Year'].min(), df['Year'].max())
    plt.grid(True)
    
    # Annotate the COVID-19 period to show its impact
    plt.axvspan(2019, 2021, color='red', alpha=0.1, label='COVID-19 Impact')
    
    plot_path = os.path.join(plots_dir, 'revenue_composition.png')
    plt.savefig(plot_path)
    print(f"Revenue composition plot saved to {plot_path}")
    plt.close()

if __name__ == '__main__':
    analyze_revenue_composition()
