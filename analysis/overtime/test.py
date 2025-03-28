import pandas as pd
import matplotlib.pyplot as plt

# Load data for a specific year (e.g., 2022)
year = 2022
df = pd.read_csv(f"../../data/overtime/{year}.csv")

# Group by employee (ID) and calculate the total overtime hours
total_ot_per_employee = df.groupby("ID")["OTHOURS"].sum()

# Plot the normalized distribution of total overtime hours per employee (PDF)
plt.figure(figsize=(10, 5))
plt.hist(total_ot_per_employee.values, bins=20, color='b', edgecolor='black', density=True)  # density=True normalizes the histogram
plt.xlabel("Total Overtime Hours")
plt.ylabel("Probability Density")
plt.title(f"Normalized Distribution of Total Overtime Hours Per Employee in {year}")
plt.grid(True)

# Save the plot as a file
plt.savefig(f'./figures/overtime-pdf-{year}.png')

# Show the plot
plt.show()
