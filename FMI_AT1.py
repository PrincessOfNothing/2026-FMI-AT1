import pandas as pd
import numpy as np

# ------ Load data into dataframe ------
file_path = "RBAbondyields.xlsx"
yields = pd.read_excel(file_path)
print("**************** yield Data head ***************")
print(yields.head())

# ------ set the col Date as index
yields['Date'] = pd.to_datetime(yields['Date'])
yields = yields.set_index('Date')

# ------ Question 1 Term Structure of zero coupon bonds ------
# ------ Compute a special date 21-April-2021 first for understanding ------
# Select valuation date
valuation_date = pd.Timestamp('2021-04-21')
row = yields.loc[valuation_date]

print(f"The yield data at the RBA F2 table for the date {valuation_date}")
print(row)

# Maturities in years and corresponding column names
maturities = [2, 3, 5, 10]
yield_cols = ['2Y', '3Y', '5Y', '10Y']

# Semi-annual time grid up to 10 years
time_grid = np.arange(0.5, 10.5, 0.5)

# prepare the data structure for results
discount_factors = {}

# fetch the ytm of 2 years, 3 years, 5 years and 10 years
y2 = row["2Y"] / 100
y3 = row["3Y"] / 100
y5 = row["5Y"] / 100
y10 = row["10Y"] / 100

# Compute the Discount factors in stupid  way.
print("**************** Question 1 DFs ***************")
# the first 0.5 df by log-linear interpolation
coeffs=[100.0+y2/2*100,y2/2*100,y2/2*100,y2/2*100,-100.0]
roots=np.roots(coeffs)
discount_factors[time_grid[0]] = [root.real for root in roots if np.isreal(root) and root.real >0][0]
discount_factors[time_grid[1]] = discount_factors[time_grid[0]]**2
discount_factors[time_grid[2]] = discount_factors[time_grid[0]]**3
discount_factors[time_grid[3]] = discount_factors[time_grid[0]]**4
# check if it sums up to the face value 100
print(np.dot(np.array(list(discount_factors.values())),[y2/2*100,y2/2*100,y2/2*100,100.0+y2/2*100]))

# Extend further to 3 years
discount_factors[time_grid[4]] = (100.0-sum(discount_factors.values())*y3/2*100)/(100.0+y3/2*100)
discount_factors[time_grid[5]] = (100.0-sum(discount_factors.values())*y3/2*100)/(100.0+y3/2*100)

# Extend further to 5 years
discount_factors[time_grid[6]] = (100.0-sum(discount_factors.values())*y5/2*100)/(100.0+y5/2*100)
print(np.dot(np.array(list(discount_factors.values())),[y5/2*100,y5/2*100,y5/2*100,y5/2*100,y5/2*100,y5/2*100,100.0+y5/2*100]))

discount_factors[time_grid[7]] = (100.0-sum(discount_factors.values())*y5/2*100)/(100.0+y5/2*100)
print(np.dot(np.array(list(discount_factors.values())),[y5/2*100,y5/2*100,y5/2*100,y5/2*100,y5/2*100,y5/2*100,y5/2*100,100.0+y5/2*100]))
discount_factors[time_grid[8]] = (100.0-sum(discount_factors.values())*y5/2*100)/(100.0+y5/2*100)
discount_factors[time_grid[9]] = (100.0-sum(discount_factors.values())*y5/2*100)/(100.0+y5/2*100)

# Extend further to 10 years
discount_factors[time_grid[10]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)
discount_factors[time_grid[11]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)
discount_factors[time_grid[12]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)
discount_factors[time_grid[13]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)
discount_factors[time_grid[14]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)
discount_factors[time_grid[15]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)
discount_factors[time_grid[16]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)
discount_factors[time_grid[17]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)
discount_factors[time_grid[18]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)
discount_factors[time_grid[19]] = (100.0-sum(discount_factors.values())*y10/2*100)/(100.0+y10/2*100)

# print out the discount factors
print(f"Derive the discount factors for the date: {valuation_date}")
for time, df in discount_factors.items():
    print(f"The discount factor for {time}y is {df}")

# Validate at the end
n = len(discount_factors)
coupon_payment = (y10 / 2) * 100
cash_flows = [coupon_payment] * (n - 1) + [100.0 + coupon_payment]
price = np.dot(np.array(list(discount_factors.values())), cash_flows)

# Check the price
if np.isclose(price, 100.0, atol=1e-7):
    print(f"The Validation of Discount factors  successful! The Bond Price is {price:.6f} == par value 100.")
else:
    print(f"The Validation of Discount factors failed. The Bond Price is {price:.6f} <> par value 100.")
    print("Something may be wrong; the price should be exactly 100.00.")

# -----Question 2 Bond price, Duration and Convexity ------
# Bond defined by coupon and maturity in months
bonds = {
    'B1': {'coupon': 0.0325, 'maturity': 48/12},
    'B2': {'coupon': 0.0425, 'maturity': 63/12},
    'B3': {'coupon': 0.0225, 'maturity': 85/12},
    'B4': {'coupon': 0.01,   'maturity': 104/12}
}

# ------ B1 --- Maturity = exactly 4 years ------
# payment schedule
payment_schedule = np.arange(0.5, bonds['B1']['maturity'] + 0.5, 0.5)

# cashflows
cashflows = np.full(len(payment_schedule), 100 * bonds['B1']['coupon']  / 2)
cashflows[-1] += 100

# chop discount factors to the length for B1
dfs = np.array(list(discount_factors.values())[:len(payment_schedule)])

# calculate the bond price
# B1 Payment schedule [0.5 1.  1.5 2.  2.5 3.  3.5 4. ]
# B1 Coupons [  1.625   1.625   1.625   1.625   1.625   1.625   1.625 101.625]
print("**************** Question 2 B1 Price Duration Convexity ***************")
bond_price=np.dot(dfs, cashflows)
print(f"The pricing of the bond B1: {bond_price:.4f}")

# calculate F-W duration and convexity
duration = (payment_schedule * cashflows * dfs).sum() / bond_price
convexity = (payment_schedule ** 2 * cashflows * dfs).sum() / bond_price
print(f"Fisher-Weil Duration of the bond B1: {duration:.4f} years")
print(f"Fisher-Weil Convexity of the bond B1: {convexity:.4f}")

# ------ B2 B3 B4 --- Maturity years ------
# B4 payment schedule [0.5 1.  1.5 2.  2.5 3.  3.5 4.  4.5 5.  5.5 6.  6.5 7.  7.5 8.  8.5 9. ]
payment_schedule_B4 = np.arange(0.5, bonds['B4']['maturity'] + 0.5, 0.5)

# B4 cashflows [  0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5
# 0.5   0.5   0.5   0.5   0.5 100.5]
cashflows_B4 = np.full(len(payment_schedule_B4), 100 * bonds['B4']['coupon']  / 2)
cashflows_B4[-1] += 100
print("**************** Question 2 B4 Price Duration Convexity ***************")
print(f"The cashflows of the bond B4: {cashflows_B4}")

# chop discount factors to the length for B4
dfs = np.array(list(discount_factors.values())[:len(payment_schedule_B4)])

# --- Function : to do log-linear interpolation ---
def log_interp_df(t, t1, df1, t2, df2):
    """
    Calculates the Discount Factor at time t using log-linear interpolation.

    Parameters:
    t  : Target time (e.g., 5.25 years)
    t1 : Start time of known interval
    df1: Discount factor at t1
    t2 : End time of known interval
    df2: Discount factor at t2
    """
    # 1. Take the natural log of the known discount factors
    ln_df1 = np.log(df1)
    ln_df2 = np.log(df2)

    # 2. Perform standard linear interpolation on the log values
    # Formula: y = y1 + (t - t1) * (y2 - y1) / (t2 - t1)
    ln_df_t = ln_df1 + (t - t1) * (ln_df2 - ln_df1) / (t2 - t1)

    # 3. Convert back
    return np.exp(ln_df_t)

# the last point does not fall on the time grid. adjust by log-linear interp.
dfs_last=log_interp_df(bonds['B4']['maturity'],payment_schedule_B4[-2],dfs[-2],payment_schedule_B4[-1],dfs[-1])
payment_schedule_B4[-1] = bonds['B4']['maturity']
print(f"The payment schedule of the bond B4: {payment_schedule_B4}")
print(f"The interpolated df is {dfs_last}, which is in {dfs[-2]}:{dfs[-1]}")
dfs[-1]=dfs_last

# calculate the bond price
# B4 Payment schedule [0.5 1.  1.5 2.  2.5 3.  3.5 4.  4.5 5.  5.5 6.  6.5 7.  7.5 8.  8.5 8.66666667 ]
# B4 cashflows : [  0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5
#    0.5   0.5   0.5   0.5   0.5 100.5]
bond_price_B4=np.dot(dfs, cashflows_B4)
print(f"The pricing of the bond B4: {bond_price_B4:.4f}")

# calculate F-W duration
duration_B4 = (payment_schedule_B4 * cashflows_B4 * dfs).sum() / bond_price_B4
print(f"Fisher-Weil Duration of the bond B4: {duration_B4:.4f} years")
convexity_B4 = (payment_schedule_B4 ** 2 * cashflows_B4 * dfs).sum() / bond_price
print(f"Fisher-Weil Convexity of the bond B4: {convexity_B4:.4f}")

# ------ Question 3 Hedging two bonds B1 and B4 ------
# Liability: 120_000_000; 6 years from 21 April 2021 to 21 April 2027
liability_time = 6 # kind of zero coupon
liability_amount = 120_000_000
# Present value of liability.
liability_df = np.array(list(discount_factors.values())[11])
PresentValue_liability = liability_amount * liability_df

# Solve the linear system of two equations

A = np.array([
    [bond_price, bond_price_B4],
    [bond_price * duration, bond_price_B4 * duration_B4]
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


