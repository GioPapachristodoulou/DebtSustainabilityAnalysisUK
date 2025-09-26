import pandas as pd
import os

def extract_and_clean_data():
    """
    Extracts and cleans data from OBR Excel files.
    """
    # Define file paths
    data_path = 'data/raw'
    processed_path = 'data/processed'
    
    # Create processed data directory if it doesn't exist
    if not os.path.exists(processed_path):
        os.makedirs(processed_path)

    # File paths
    debt_interest_file = os.path.join(data_path, 'Debt_interest_Detailed_forecast_tables_March_2025.xlsx')
    fiscal_revisions_file = os.path.join(data_path, 'Fiscal_forecast_revisions_database_March_2025.xlsx')
    expenditure_file = os.path.join(data_path, 'Expenditure_Detailed_forecast_tables_March_2025.xlsx')
    receipts_file = os.path.join(data_path, 'Receipts_Detailed_forecast_tables_March_2025.xlsx')
    economy_file = os.path.join(data_path, 'Economy_Detailed_forecast_tables_March_2025.xlsx')
    long_term_file = os.path.join(data_path, 'Long-term-economic-determinants-March-2025-EFO.xlsx')

    # --- Data Extraction and Cleaning ---

    # 1. Economy Data (GDP)
    gdp_df = pd.read_excel(economy_file, sheet_name='1.2', header=4)
    gdp_df = gdp_df.iloc[1:, [0, 1]]
    gdp_df.columns = ['Year', 'Nominal GDP']
    gdp_df = gdp_df.dropna()
    gdp_df['Year'] = gdp_df['Year'].apply(lambda x: int(str(x).split('-')[0]))
    gdp_df = gdp_df[gdp_df['Year'] > 2000]
    gdp_df.set_index('Year', inplace=True)
    gdp_df['Nominal GDP'] = pd.to_numeric(gdp_df['Nominal GDP'])

    # 2. Public Sector Net Debt
    debt_df = pd.read_excel(expenditure_file, sheet_name='4.17', header=4)
    debt_df = debt_df.iloc[1:, [0, 5]]
    debt_df.columns = ['Year', 'PSND']
    debt_df = debt_df.dropna()
    debt_df['Year'] = debt_df['Year'].apply(lambda x: int(str(x).split('-')[0]))
    debt_df = debt_df[debt_df['Year'] > 2000]
    debt_df.set_index('Year', inplace=True)
    debt_df['PSND'] = pd.to_numeric(debt_df['PSND'])


    # 3. Public Sector Net Borrowing (Deficit)
    psnb_df = pd.read_excel(expenditure_file, sheet_name='4.17', header=4)
    psnb_df = psnb_df.iloc[1:, [0, 1]]
    psnb_df.columns = ['Year', 'PSNB']
    psnb_df = psnb_df.dropna()
    psnb_df['Year'] = psnb_df['Year'].apply(lambda x: int(str(x).split('-')[0]))
    psnb_df = psnb_df[psnb_df['Year'] > 2000]
    psnb_df.set_index('Year', inplace=True)
    psnb_df['PSNB'] = pd.to_numeric(psnb_df['PSNB'])


    # 4. Debt Interest
    interest_df = pd.read_excel(debt_interest_file, sheet_name='5.1', header=4)
    interest_df = interest_df.iloc[1:, [0, 1]]
    interest_df.columns = ['Year', 'Debt Interest']
    interest_df = interest_df.dropna()
    interest_df['Year'] = interest_df['Year'].apply(lambda x: int(str(x).split('-')[0]))
    interest_df = interest_df[interest_df['Year'] > 2000]
    interest_df.set_index('Year', inplace=True)
    interest_df['Debt Interest'] = pd.to_numeric(interest_df['Debt Interest'])


    # --- Merging Data ---
    final_df = pd.concat([gdp_df, debt_df, psnb_df, interest_df], axis=1)
    final_df.reset_index(inplace=True)
    
    # Select and rename columns
    final_df = final_df[['Year', 'Nominal GDP', 'PSND', 'PSNB', 'Debt Interest']]
    
    # Save to CSV
    output_file = os.path.join(processed_path, 'obr_data.csv')
    final_df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
    print(final_df.head())

if __name__ == '__main__':
    extract_and_clean_data()
