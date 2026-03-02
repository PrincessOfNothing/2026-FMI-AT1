import numpy as np
from scipy.optimize import fsolve

"""
Question 1 Bond pricing with cont. compounded rate
"""

def solve_price_bond_cont_compounded(y, C, F, n):
    """
    Compute market price of the bond using the continuously compounded yield 'y' in the bond price formula.

    y : continuously compounded yield
    C : Annual Coupon Amount
    F : Face Value
    n : Years to Maturity
    """
    # Present Value of Coupons: C * (e^-y*1 + e^-y*2 + ... + e^-y*n)
    # coupon_pv = sum(C * np.exp(-y * t) for t in range(1, n + 1))
    # C * [ exp(-y) * (1 - exp(-n*y)) / (1 - exp(-y)) ]
    coupon_pv = C * (np.exp(-y) * (1 - np.exp(-n * y))) / (1 - np.exp(-y))
    # Present Value of Face Value: F * e^(-y*n)
    principal_pv = F * np.exp(-y * n)
    price_pv = coupon_pv + principal_pv

    # We want Price
    return price_pv

def solve_continuous_yield(P, C, F, n):
    """
    Solves for the continuously compounded yield 'y' in the bond price formula.

    P : Market Price
    C : Annual Coupon Amount
    F : Face Value
    n : Years to Maturity
    """

    def equation(y):
        # Present Value of Coupons: C * (e^-y*1 + e^-y*2 + ... + e^-y*n)
        # coupon_pv = sum(C * np.exp(-y * t) for t in range(1, n + 1))
        # C * [ exp(-y) * (1 - exp(-n*y)) / (1 - exp(-y)) ]
        coupon_pv = C * (np.exp(-y) * (1 - np.exp(-n * y))) / (1 - np.exp(-y))
        # Present Value of Face Value: F * e^(-y*n)
        principal_pv = F * np.exp(-y * n)

        # We want PV - Price = 0
        return (coupon_pv + principal_pv) - P

    # Initial guess: current yield (C/P) is a reliable starting point
    initial_guess = C / P

    # fsolve finds the root (where the equation returns 0)
    y_solution = fsolve(equation, initial_guess)[0]
    return y_solution


# --- Q1.a ---
market_price = 105
annual_coupon = 5
face_val = 100
maturity_years = 6

y = solve_continuous_yield(market_price, annual_coupon, face_val, maturity_years)

print(f"The continuously compounded yield (y) is: {y:.6f}")
print(f"As a percentage: {y * 100:.4f}%")

# --- Q1.b ---
quarter_coupon = 5/4
maturity_periods = 6*4
yield_quarterly = y/4
market_price_1b = solve_price_bond_cont_compounded(yield_quarterly, quarter_coupon, face_val, maturity_periods)

print(f"The price of the bond is: {market_price_1b:.6f}")

# --- Q2.a ---
bonds = {
    'B1': {'coupon': 6.5, 'maturity': 1, 'price':101.8137},
    'B2': {'coupon': 3.25, 'maturity': 2, 'price':97.7066},
    'B3': {'coupon': 4.8, 'maturity': 3, 'price':101.2414},
    'B4': {'coupon': 1.5,   'maturity': 4, 'price':89.9751},
    'B5': {'coupon': 5.0, 'maturity': 5, 'price': 103.4012},
    'B6': {'coupon': 4.0, 'maturity': 6, 'price': 99.0074},
    'B7': {'coupon': 2.0, 'maturity': 7, 'price': 87.20871}
}
dfs= [bonds['B1']['price']/(bonds['B1']['coupon']+100)]
print(f"The discount factor for 1 year is: {dfs[0]:.6f}")

dfs.append((bonds['B2']['price']- bonds['B2']['coupon']*sum(dfs))/(bonds['B2']['coupon']+100))
print(f"The discount factor for 2 years is: {dfs[-1]:.6f}")

dfs.append((bonds['B3']['price']- bonds['B3']['coupon']*sum(dfs))/(bonds['B3']['coupon']+100))
print(f"The discount factor for 3 years is: {dfs[-1]:.6f}")

dfs.append((bonds['B4']['price']- bonds['B4']['coupon']*sum(dfs))/(bonds['B4']['coupon']+100))
print(f"The discount factor for 4 years is: {dfs[-1]:.6f}")

dfs.append( (bonds['B5']['price']- bonds['B5']['coupon']*sum(dfs))/(bonds['B5']['coupon']+100))
print(f"The discount factor for 5 years is: {dfs[-1]:.6f}")

dfs.append( (bonds['B6']['price']- bonds['B6']['coupon']*sum(dfs))/(bonds['B6']['coupon']+100))
print(f"The discount factor for 6 years is: {dfs[-1]:.6f}")

dfs.append((bonds['B7']['price']- bonds['B7']['coupon']*sum(dfs))/(bonds['B7']['coupon']+100))
print(f"The discount factor for 7 years is: {dfs[-1]:.6f}")

# q2.b
# find price for 8% annual coupon maturity = 7 y
price_8perc_7y = 8.0*sum(dfs)+100.0 * dfs[6]
print(f"The price of a bond with 8% annual coupon for 7 years is: {price_8perc_7y:.6f}")

# --- Question 4 --- Question 5 ---
# Function : to do log-linear interpolation
def log_interp(t, t1, df1, t2, df2):
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


# Function : to expand the df array, ie, from annual to semi
def expand_df_array(input_array, input_freq=1.0, output_freq=0.5):
    """
    input_freq:  1.0 for Annual, 0.5 for Semi
    output_freq: 0.5 for Semi, 0.25 for Quarterly
    """
    n_in = len(input_array)
    total_years = n_in * input_freq
    n_out = int(total_years / output_freq)

    # We need to build the new array
    output_dfs = np.zeros(n_out)

    # Track the "bounding points" for your log_interp
    t_prev, df_prev = 0.0, 1.0  # Time 0 always has DF = 1.0
    input_ptr = 0

    for i in range(n_out):
        t_target = (i + 1) * output_freq

        # Determine the next known point from our input_array
        t_next = (input_ptr + 1) * input_freq
        df_next = input_array[input_ptr]

        # Get the df by Log-Linear Interpolation
        output_dfs[i] = log_interp(t_target, t_prev, df_prev, t_next, df_next)

        # If we just reached a point from the original array, move to the next interval
        if abs(t_target - t_next) < 1e-9:
            t_prev, df_prev = t_next, df_next
            input_ptr += 1

    return output_dfs

# not fall on the grid. log-linear interp. find df
full_dfs_semi = expand_df_array(dfs)
print(full_dfs_semi)

full_dfs_quarterly = expand_df_array(full_dfs_semi, output_freq=0.5)
print(full_dfs_quarterly)

# to be continue: bond pricing of Q4 and Q5

# --- Question 6 ---
# Accrued = coupon * ACT in the period\ ACT of the whole period
# Dirty = clean + Accrued

# --- Question 7 --- # --- Question 8 ---
# Loan Repayment Loan = sum from 1 to n the fixed repayment * B(t_i)
# Q8 rate_new=rate_old+0.005 B(t) = exp(-(rate_new)t)



# --- Question 9 ------ Question 10 ---
# Credit card switching decision by comparing PV_old PV_new