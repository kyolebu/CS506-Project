import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# Load data for all years
years = range(2012, 2023)
data = {}

for year in years:
    df = pd.read_csv(f"../../data/overtime/{year}.csv")
    total_ot_per_employee = df.groupby("ID")["OTHOURS"].sum()
    data[year] = total_ot_per_employee.values

# Determine the global x limits across all years
all_values = [value for year_data in data.values() for value in year_data]
x_min, x_max = min(all_values), max(all_values)

# Calculate the maximum density across all years for consistent scaling
max_density = 0
for year in years:
    counts, bins = np.histogram(data[year], bins=20, density=True)
    max_density = max(max_density, max(counts))

# Create the figure and axis for the animation
fig, ax = plt.subplots(figsize=(10, 5))

def update(year):
    ax.clear()
    # Calculate mean and median
    mean = np.mean(data[year])
    median = np.median(data[year])

    # Plot histogram
    ax.hist(data[year], bins=20, density=True, edgecolor='black', alpha=0.7)
    ax.axvline(mean, color='red', linestyle='dashed', linewidth=2, label=f"Mean: {mean:.2f}")
    ax.axvline(median, color='green', linestyle='dashed', linewidth=2, label=f"Median: {median:.2f}")

    # Add labels and title
    ax.set_title(f"Normalized Distribution of Total Overtime Hours Per Employee in {year}")
    ax.set_xlabel("Total Overtime Hours")
    ax.set_ylabel("Probability Density")
    ax.grid(True)
    ax.set_xlim(x_min, x_max)  # Set consistent x-axis limits
    ax.set_ylim(0, max_density)  # Set consistent y-axis limits
    ax.legend()  # Show legend for mean and median

ani = FuncAnimation(fig, update, frames=years, repeat=True, interval=1000)

# Save the animation as an MP4 file
output_path = "./figures/pdfs/distributions.gif"
writer = 'pillow'
ani.save(output_path, writer=writer)

print(f"Animation saved to {output_path}")