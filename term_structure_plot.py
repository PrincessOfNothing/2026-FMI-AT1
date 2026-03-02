import matplotlib.pyplot as plt
import numpy as np

# Data
times = np.arange(0.5, 10.5, 0.5)
dfs = [
    0.9996401295533605, 0.9992803886134592, 0.9989207771336908, 0.9985612950674662,
    0.9974780902562848, 0.9969746180741572, 0.9758950438149039, 0.9725300897045261,
    0.9691767381903875, 0.9658349492659274, 0.9107002630708712, 0.903221588319585,
    0.8958043284797723, 0.888447979211898, 0.8811520403180644, 0.873916015708002,
    0.866739413365337, 0.859621745314136, 0.8525625275857263, 0.8455612801857879
]

# Plotting
plt.plot(times, dfs, marker='o', linestyle='-', color='b')
plt.title('Term Structure of Discount Factors (21 April 2021)')
plt.xlabel('Time to Maturity (Years)')
plt.ylabel('Discount Factor')
plt.grid(True)
plt.xticks(np.arange(0, 11, 1))

# Save the plot
plt.savefig('discount_factors_plot.png')
