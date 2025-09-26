import pandas as pd
import os
import logging

# --- Configuration ---
LOG_LEVEL = logging.INFO
DATA_PATH = 'data/raw'
PROCESSED_PATH = 'data/processed'
OUTPUT_FILE = os.path.join(PROCESSED_PATH, 'obr_data.csv')

# --- File and Sheet Mapping ---
FILE_CONFIG = {
    'gdp': {
        'file': 'Economy_Detailed_forecast_tables_March_2025.xlsx',
        'sheet': '1.2',
        'header_keyword': 'GDP at market prices',
        'column_index': 14,
        'data_column_name': 'Nominal GDP'
    },
    'debt': {
        'file': 'Aggregates_Detailed_forecast_tables_March_2025.xlsx',
        'sheet': '6.2',
        'header_keyword': 'Public sector net debt',
        'column_index': 1, 
        'data_column_name': 'PSND'
    },
    'borrowing': {
        'file': 'Aggregates_Detailed_forecast_tables_March_2025.xlsx',
        'sheet': '6.2',
        'header_keyword': 'Public sector net borrowing',
        'column_index': 1, 
        'data_column_name': 'PSNB'
    },
    'interest': {
        'file': 'Debt_interest_Detailed_forecast_tables_March_2025.xlsx',
        'sheet': '3.9',
        'header_keyword': 'Total public service pensions expenditure',
        'column_index': 1, 
        'data_column_name': 'Debt Interest'
    }
}

# --- Setup Logging ---
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

def find_header_row(df, keyword):
    """Finds the row number containing the keyword."""
    for i, row in df.iterrows():
        for cell in row:
            if isinstance(cell, str) and keyword in cell:
                return i
    return None

def extract_series(data_key):
    """Extracts a single data series based on the configuration."""
    config = FILE_CONFIG[data_key]
    file_path = os.path.join(DATA_PATH, config['file'])
    
    logging.info(f"Extracting '{config['data_column_name']}' from {config['file']}/{config['sheet']}")
    
    try:
        df = pd.read_excel(file_path, sheet_name=config['sheet'], header=None)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None

    header_row = find_header_row(df, config['header_keyword'])
    if header_row is None:
        logging.error(f"Keyword '{config['header_keyword']}' not found in {config['sheet']}.")
        return None
        
    logging.info(f"Found header for '{config['data_column_name']}' at row {header_row}")

    # Extract the data, starting from the row after the header
    series_df = df.iloc[header_row + 1:, [0, config['column_index']]]
    series_df.columns = ['Year', config['data_column_name']]
    series_df = series_df.dropna()

    # Clean the 'Year' column
    series_df['Year'] = series_df['Year'].apply(lambda x: str(x).split('-')[0])
    series_df = series_df[series_df['Year'].str.isnumeric()]
    series_df['Year'] = series_df['Year'].astype(int)
    series_df = series_df[series_df['Year'] > 2000]

    # Set index and convert to numeric
    series_df.set_index('Year', inplace=True)
    series_df[config['data_column_name']] = pd.to_numeric(series_df[config['data_column_name']])
    
    logging.info(f"Successfully extracted and cleaned '{config['data_column_name']}'.")
    return series_df

def main():
    """Main function to extract, clean, and merge all data."""
    if not os.path.exists(PROCESSED_PATH):
        os.makedirs(PROCESSED_PATH)

    # Extract all data series
    gdp_df = extract_series('gdp')
    debt_df = extract_series('debt')
    borrowing_df = extract_series('borrowing')
    interest_df = extract_series('interest')

    # Merge the dataframes
    final_df = pd.concat([gdp_df, debt_df, borrowing_df, interest_df], axis=1)
    final_df.reset_index(inplace=True)

    # Save the final dataframe
    final_df.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"All data has been merged and saved to {OUTPUT_FILE}")
    print("\n--- Final Data Preview ---")
    print(final_df.head())
    print("\n--- Data Info ---")
    final_df.info()


if __name__ == '__main__':
    main()
