import pandas as pd
import numpy as np

# Data provided by the user
gdp_data = [
    1593.6, 1548.8, 1608.6, 1662.6, 1713.7, 1781.4, 1862.5, 1916.5, 1991.6, 
    2082.5, 2152.3, 2233.9, 2103.5, 2285.4, 2526.4, 2717.3, 2848.0, 2967.6, 
    3073.4, 3190.2, 3309.2, 3432.5
]

psnd_data = [
    567200, 787200, 1027900, 1168700, 1261200, 1366200, 1461100, 1552900, 
    1599700, 1718000, 1757300, 1776900, 1815000, 2152900, 2381900, 2530400
]

# Create a DataFrame
years = range(2008, 2030)
df = pd.DataFrame(index=years)
df.index.name = 'Year'

# Add data, aligning by index (year)
df['Nominal GDP'] = pd.Series(gdp_data, index=range(2008, 2008 + len(gdp_data)))

# The PSND data is for 2007/08 to 2022/23, so we map it to years 2008 to 2023
psnd_years = range(2008, 2008 + len(psnd_data))
df['PSND'] = pd.Series(psnd_data, index=psnd_years)

# Initialize other columns with NaN
df['PSNB'] = np.nan
df['Debt Interest'] = np.nan

# Reorder columns
df = df[['Nominal GDP', 'PSND', 'PSNB', 'Debt Interest']]

# Save to CSV, ensuring it overwrites
file_path = '/workspaces/DebtSustainabilityAnalysisUK/data/processed/obr_data.csv'
df.to_csv(file_path)

print(f"File '{file_path}' has been successfully created and populated.")
print("File content preview:")
print(df.head())
