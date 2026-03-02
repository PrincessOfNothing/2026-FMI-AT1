import pandas as pd
import numpy as np

# ------ Load data ------
file_path = "RBAbondyields.xlsx"
yields = pd.read_excel(file_path)

# Prepare Date index
yields['Date'] = pd.to_datetime(yields['Date'])
yields = yields.set_index('Date')

# Clean data: Remove rows where any key yields are missing
yields = yields.dropna(subset=['2Y', '3Y', '5Y', '10Y'])

def get_discount_factors(row):
    y2 = row["2Y"] / 100
    y3 = row["3Y"] / 100
    y5 = row["5Y"] / 100
    y10 = row["10Y"] / 100

    time_grid = np.arange(0.5, 10.5, 0.5)
    dfs = {}

    # --- 2-Year Bootstrapping (Solve for root) ---
    coeffs = [100.0 + y2 / 2 * 100, y2 / 2 * 100, y2 / 2 * 100, y2 / 2 * 100, -100.0]
    roots = np.roots(coeffs)
    # Get the real positive root
    base_df = [root.real for root in roots if np.isreal(root) and root.real > 0][0]

    # First 4 periods (0.5 to 2.0y)
    for i in range(4):
        dfs[time_grid[i]] = base_df ** (i + 1)

    # --- 3-Year Extension ---
    # Indices 4 and 5
    for i in [4, 5]:
        dfs[time_grid[i]] = (100.0 - sum(dfs.values()) * y3 / 2 * 100) / (100.0 + y3 / 2 * 100)

    # --- 5-Year Extension ---
    # Indices 6 to 9
    for i in range(6, 10):
        dfs[time_grid[i]] = (100.0 - sum(dfs.values()) * y5 / 2 * 100) / (100.0 + y5 / 2 * 100)

    # --- 10-Year Extension ---
    # Indices 10 to 19
    for i in range(10, 20):
        dfs[time_grid[i]] = (100.0 - sum(dfs.values()) * y10 / 2 * 100) / (100.0 + y10 / 2 * 100)

    return dfs


all_dfs_results = []

# Loop through every date in the filtered dataframe
for date, row in yields.iterrows():
    # Calculate DFs for this date
    dfs_dict = get_discount_factors(row)

    # Store the results for analysis
    all_dfs_results.append({
        'Date': date,
        'DF_0_5Y': dfs_dict[0.5],
        'DF_1_0Y': dfs_dict[1.0],
        'DF_1_5Y': dfs_dict[1.5],
        'DF_2_0Y': dfs_dict[2.0],
        'DF_2_5Y': dfs_dict[2.5],
        'DF_3_0Y': dfs_dict[3.0],
        'DF_3_5Y': dfs_dict[3.5],
        'DF_4_0Y': dfs_dict[4.0],
        'DF_4_5Y': dfs_dict[4.5],
        'DF_5_0Y': dfs_dict[5.0],
        'DF_5_5Y': dfs_dict[5.5],
        'DF_6_0Y': dfs_dict[6.0],
        'DF_6_5Y': dfs_dict[6.5],
        'DF_7_0Y': dfs_dict[7.0],
        'DF_7_5Y': dfs_dict[7.5],
        'DF_8_0Y': dfs_dict[8.0],
        'DF_8_5Y': dfs_dict[8.5],
        'DF_9_0Y': dfs_dict[9.0],
        'DF_9_5Y': dfs_dict[9.5],
        'DF_1_0Y': dfs_dict[10.0]
    })

# Convert results to a new DataFrame
results_df = pd.DataFrame(all_dfs_results).set_index('Date')

print("Calculations complete for all dates.")
print(results_df.head())
results_df.to_excel("Discount factors-RBAbondyields.xlsx")