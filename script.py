import pandas as pd
import numpy as np

# ------ Load data into dataframe ------
file_path = "RBAbondyields.xlsx"
yields = pd.read_excel(file_path)
print(yields.head())

# ------ set the col Date as index
yields['Date'] = pd.to_datetime(yields['Date'])
yields = yields.set_index('Date')

# ------ Question 1 Term Structure of zero coupon bonds ------
# ------ Compute a special date 21-April-2021 first for understanding ------
# Select valuation date
valuation_date = pd.Timestamp('2021-04-21')
row = yields.loc[valuation_date]
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

# Compute the Discount factors in stupid  way. Here I may have mistakes. rate should be y2/k. k is the payment times??
# 2Y. k=2 for semi-annual
# results: {np.float64(0.5): np.float64(0.9996401295533609), np.float64(1.0): np.float64(0.9992803886134601),
# np.float64(1.5): np.float64(0.9989207771336921), np.float64(2.0): np.float64(0.9985612950674679),
# np.float64(2.5): np.float64(0.9980572761430158), np.float64(3.0): np.float64(0.9975535116196479),
# np.float64(3.5): np.float64(0.994113877603141), np.float64(4.0): np.float64(0.9906861036843929),
# np.float64(4.5): np.float64(0.9872701489689603), np.float64(5.0): np.float64(0.9838659727034065),
# np.float64(5.5): np.float64(0.9757864608079169), np.float64(6.0): np.float64(0.9677732979012941),
# np.float64(6.5): np.float64(0.9598259391253362), np.float64(7.0): np.float64(0.9519438440962195),
# np.float64(7.5): np.float64(0.9441264768677544), np.float64(8.0): np.float64(0.9363733058949442),
# np.float64(8.5): np.float64(0.928683803997842), np.float64(9.0): np.float64(0.9210574483257051),
# np.float64(9.5): np.float64(0.9134937203214435), np.float64(10.0): np.float64(0.9059921056863603)}

discount_factors[time_grid[0]] = 1 / (1 + y2/2)
discount_factors[time_grid[1]] = discount_factors[time_grid[0]] / (1 + y2/2)
discount_factors[time_grid[2]] = discount_factors[time_grid[1]] / (1 + y2/2)
discount_factors[time_grid[3]] = discount_factors[time_grid[2]] / (1 + y2/2)
# 3Y.
discount_factors[time_grid[4]] = discount_factors[time_grid[3]] / (1 + y3/2)
discount_factors[time_grid[5]] = discount_factors[time_grid[4]] / (1 + y3/2)
# 5Y.
discount_factors[time_grid[6]] = discount_factors[time_grid[5]] / (1 + y5/2)
discount_factors[time_grid[7]] = discount_factors[time_grid[6]] / (1 + y5/2)
discount_factors[time_grid[8]] = discount_factors[time_grid[7]] / (1 + y5/2)
discount_factors[time_grid[9]] = discount_factors[time_grid[8]] / (1 + y5/2)
# 10Y.
discount_factors[time_grid[10]] = discount_factors[time_grid[9]] / (1 + y10/2)
discount_factors[time_grid[11]] = discount_factors[time_grid[10]] / (1 + y10/2)
discount_factors[time_grid[12]] = discount_factors[time_grid[11]] / (1 + y10/2)
discount_factors[time_grid[13]] = discount_factors[time_grid[12]] / (1 + y10/2)
discount_factors[time_grid[14]] = discount_factors[time_grid[13]] / (1 + y10/2)
discount_factors[time_grid[15]] = discount_factors[time_grid[14]] / (1 + y10/2)
discount_factors[time_grid[16]] = discount_factors[time_grid[15]] / (1 + y10/2)
discount_factors[time_grid[17]] = discount_factors[time_grid[16]] / (1 + y10/2)
discount_factors[time_grid[18]] = discount_factors[time_grid[17]] / (1 + y10/2)
discount_factors[time_grid[19]] = discount_factors[time_grid[18]] / (1 + y10/2)
print(discount_factors)

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
print(bonds['B1']['maturity'] )
payment_schedule = np.arange(0.5, bonds['B1']['maturity'] + 0.5, 0.5)
print(payment_schedule)

# cashflows
cashflows = np.full(len(payment_schedule), 100 * bonds['B1']['coupon']  / 2)
cashflows[-1] += 100
print(cashflows)

# chop discount factors to the length for B1
dfs = np.array(list(discount_factors.values())[:len(payment_schedule)])

# calculate the bond price
# B1 Payment schedule [0.5 1.  1.5 2.  2.5 3.  3.5 4. ]
# B1 Coupons [  1.625   1.625   1.625   1.625   1.625   1.625   1.625 101.625]
# Price : 112.03093207749383
bond_price=np.dot(dfs, cashflows)
print(bond_price)

# calculate F-W duration and convexity
# Duration : 3.8315310962786597
# Convexity: 15.02152101025032
duration = (payment_schedule * cashflows).sum() / bond_price
print(duration)
# Convexity formula need to confirm???
convexity = (payment_schedule ** 2 * cashflows).sum() / bond_price
print(convexity)

# ------ B4 --- Maturity = 8.66666 years ------
# B4 payment schedule [0.5 1.  1.5 2.  2.5 3.  3.5 4.  4.5 5.  5.5 6.  6.5 7.  7.5 8.  8.5 9. ]
print(bonds['B4']['maturity'] )
payment_schedule_B4 = np.arange(0.5, bonds['B4']['maturity'] + 0.5, 0.5)
print(payment_schedule_B4)

# B4 cashflows [  0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5   0.5
# 0.5   0.5   0.5   0.5   0.5 100.5]
cashflows_B4 = np.full(len(payment_schedule_B4), 100 * bonds['B4']['coupon']  / 2)
cashflows_B4[-1] += 100
print(cashflows_B4)

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

# not fall on the grid. log-linear interp for the last df
# 0.9261346948890091
dfs_last=log_interp_df(bonds['B4']['maturity'],payment_schedule_B4[-2],dfs[-2],payment_schedule_B4[-1],dfs[-1])
print(dfs_last)

# get the last item of  payment_schedule_B4 and dfs after interpolation for B4
payment_schedule_B4[-1] = bonds['B4']['maturity']
print(payment_schedule_B4)
dfs[-1]=dfs_last

# calculate the bond price
# B4 Payment schedule [0.5 1.  1.5 2.  2.5 3.  3.5 4.  4.5 5.  5.5 6.  6.5 7.  7.5 8.  8.5 8.66666667 ]
# B4 Price : 101.38276814123634
bond_price_B4=np.dot(dfs, cashflows_B4)
print(bond_price_B4)

# calculate F-W duration
# Duration : 8.968486624209389
duration_B4 = (payment_schedule_B4 * cashflows_B4).sum() / bond_price_B4
print(duration_B4)

# ------ Question 3 Hedging two bonds B1 and B4 ------
# Liability: 120_000_000; 6 years from 21 April 2021 to 21 April 2027
liability_time = 6 # kind of zero coupon
liability_amount = 120_000_000
# Present value of liability. 6 years, 12th payment, starting from 0. should be the 11
liability_df = np.array(list(discount_factors.values())[11])
PresentValue_liability = liability_amount * liability_df
print(PresentValue_liability) #116132795.7481553

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

# prepare the structure of the results
# B1    599026.758091
# B4    483546.371821
hedge_positions = pd.Series({'B1': x1, 'B4': x4})
print(hedge_positions)


