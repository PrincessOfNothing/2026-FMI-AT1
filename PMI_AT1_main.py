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

# ------ Question 1 Term Structure of zero coupon bonds ------
print("**************** Question 1 Term Structure of zero coupon bonds ***************")
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

def validate_discount_factors(row, discount_factors):
    y2 = row["2Y"] / 100
    y3 = row["3Y"] / 100
    y5 = row["5Y"] / 100
    y10 = row["10Y"] / 100

    # Validate 5Y
    n = 10
    coupon_payment = (y5 / 2) * 100
    cash_flows = [coupon_payment] * (n - 1) + [100.0 + coupon_payment]
    price = np.dot(np.array(list(discount_factors.values())[:10]), cash_flows)

    # Check the price
    if np.isclose(price, 100.0, atol=1e-7):
        print(f"The Validation for 5 years segment successful! The Bond Price is {price:.6f} == par value 100.")
    else:
        print(f"The Validation for 5 years segment failed. The Bond Price is {price:.6f} <> par value 100.")


    # Validate 10Y  at the end
    n = len(discount_factors)
    coupon_payment = (y10 / 2) * 100
    cash_flows = [coupon_payment] * (n - 1) + [100.0 + coupon_payment]
    price = np.dot(np.array(list(discount_factors.values())), cash_flows)

    # Check the price
    if np.isclose(price, 100.0, atol=1e-7):
        print(f"The Validation for 10 years segment  successful! The Bond Price is {price:.6f} == par value 100.")
    else:
        print(f"The Validation for 10 years segment  failed. The Bond Price is {price:.6f} <> par value 100.")

all_dfs_results = []
dict_all_dfs_results = {}
# Loop through every date in the filtered dataframe
for date, row in yields.iterrows():
    # Calculate DFs for this date
    dfs_dict = get_discount_factors(row)

    #validate_discount_factors(row,dfs_dict) # validate my df results for 5y and 10y

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
        'DF_10_0Y': dfs_dict[10.0]
    })

# Convert results to a new DataFrame
df_all_discount_factors = pd.DataFrame(all_dfs_results).set_index('Date')

print("Calculations complete for all dates.")
print(df_all_discount_factors.head())
df_all_discount_factors.to_excel("All Discount factors.xlsx")

# --- Question 2 ---
print("**************** Question 2 Price Duration Convexity ***************")
# Bond defined by coupon and maturity in months
bonds = {
    'B1': {'coupon': 0.0325, 'maturity': 48/12},
    'B2': {'coupon': 0.0425, 'maturity': 63/12},
    'B3': {'coupon': 0.0225, 'maturity': 85/12},
    'B4': {'coupon': 0.01,   'maturity': 104/12}
}
bond_metrics = {}

def calculate_bond_metrics(bond_name, bond_info, full_discount_factors):
    """
    Calculates Price, Fisher-Weil Duration, and Fisher-Weil Convexity
    """
    maturity = bond_info['maturity']
    coupon_rate = bond_info['coupon']

    # 1. Create the payment schedule
    payment_schedule = np.arange(0.5, maturity + 0.5, 0.5)

    # 2. Generate cashflows (Face Value = 100)
    cashflows = np.full(len(payment_schedule), 100 * coupon_rate / 2)
    cashflows[-1] += 100

    # 3. Fetch discount factors for each 0.5y step
    bond_dfs = np.array(full_discount_factors[0:len(payment_schedule)])
    # 4. Log-linear interpolation for fractional maturities (e.g., B4 at 8.67y)
    if maturity % 0.5 != 0:
        t1 = payment_schedule[-2]
        df1 = bond_dfs[-2]
        t2 = payment_schedule[-1]
        df2 = bond_dfs[-1]

        ln_df_t = np.log(df1) + (maturity - t1) * (np.log(df2) - np.log(df1)) / (t2 - t1)
        interpolated_df = np.exp(ln_df_t)

        payment_schedule[-1] = maturity
        bond_dfs[-1] = interpolated_df

    # 5. Calculations
    price = np.dot(bond_dfs, cashflows)
    duration = (payment_schedule * cashflows * bond_dfs).sum() / price
    convexity = (payment_schedule ** 2 * cashflows * bond_dfs).sum() / price

    # 6. STORE results back into the dictionary
    bond_info['price'] = price
    bond_info['duration'] = duration
    bond_info['convexity'] = convexity

    return bond_info


valuation_date = pd.Timestamp('2021-04-21')
discount_factors = df_all_discount_factors.loc[valuation_date]
dfs_array=discount_factors.values

for name, info in bonds.items():
    bond_metrics[name] = calculate_bond_metrics(name, info, dfs_array)

# 2. View all results as a clean table:
results_table = pd.DataFrame.from_dict(bond_metrics, orient='index')
print(results_table[['coupon', 'maturity', 'price', 'duration', 'convexity']])
results_table.to_excel("Bonds_valuation_risk.xlsx")

# ------ Question 3 Duration Hedging  ------
# Liability: 120_000_000; 6 years from 21 April 2021 to 21 April 2027
liability_time = 6 # kind of zero coupon
liability_amount = 120_000_000
# Present value of liability.
liability_df =dfs_array[11]
PresentValue_liability = liability_amount * liability_df
print(PresentValue_liability)

price_b1 = bonds['B1']['price']
dur_b1 = bonds['B1']['duration']
price_b4 = bonds['B4']['price']
dur_b4 = bonds['B4']['duration']

# Solve the linear system of two equations

A = np.array([
    [price_b1, price_b4],
    [price_b1*dur_b1, price_b4*dur_b4]
])
b = np.array([
    PresentValue_liability,
    PresentValue_liability * liability_time
])

x1, x4 = np.linalg.solve(A, b)

# structure the results of Duration Hedging
print("**************** Question 3 Duration Hedging ***************")
hedge_positions = pd.Series({'B1': x1, 'B4': x4})
print("The duration hedge positon is ")
print(hedge_positions)



