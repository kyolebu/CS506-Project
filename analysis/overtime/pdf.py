import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
    ax.hist(data[year], bins=50, density=True, edgecolor='black', alpha=0.7)
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

# Years excluding 2018
filtered_years = [year for year in years if year != 2018]

# Compute means
means = [np.mean(data[year]) for year in filtered_years]

# Include 2018 separately
mean_2018 = np.mean(data[2018])

# Compute standard deviation of means (excluding 2018)
std_dev = np.std(means, ddof=1)
print(std_dev)
mean_of_means = np.mean(means)
print(mean_of_means)

# Create the boxplot
plt.figure(figsize=(8, 5))
plt.boxplot(means, vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))
plt.scatter(mean_2018, 1, color='red', label="2018 Mean", zorder=3)  # Highlight 2018 separately

# Plot standard deviation range
plt.axvline(mean_of_means, color='black', linestyle='dashed', linewidth=1, label="Mean of Means")
plt.axvline(mean_of_means + std_dev, color='purple', linestyle='dotted', linewidth=1, label="+1 Std Dev")
plt.axvline(mean_of_means - std_dev, color='purple', linestyle='dotted', linewidth=1, label="-1 Std Dev")
plt.axvline(mean_of_means + 2 * std_dev, color='blue', linestyle='dotted', linewidth=1, label="+2 Std Dev")
plt.axvline(mean_of_means - 2 * std_dev, color='blue', linestyle='dotted', linewidth=1, label="-2 Std Dev")

# Labels and title
plt.xlabel("Mean Overtime Hours")
plt.title("Distribution of Mean Overtime Hours Across Years (Highlighting 2018)")
plt.legend()
plt.grid(True)
plt.savefig('./figures/pdfs/outlier_with_std.png')
plt.show()

