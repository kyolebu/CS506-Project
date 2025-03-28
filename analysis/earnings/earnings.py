import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

data_dir = 'data/earnings/'

# List all the files for years 2011 to 2024
file_names = [f"employee-earnings-report-{year}.csv" for year in range(2011, 2025)]

# Initialize a list to hold the total earnings for each year
total_earnings_by_year = []

# Loop through each file to process data
for file in file_names:
    file_path = os.path.join(data_dir, file)
    
    # Try to read the data from the CSV file with a different encoding (ISO-8859-1)
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        print(f"Error reading {file}. Skipping this file.")
        continue
    
    # Normalize the column names (remove spaces, make case consistent)
    df.columns = [col.strip().replace(" ", "_").upper() for col in df.columns]
    
    # Identify the column names related to department and total earnings
    department_column = [col for col in df.columns if 'DEPARTMENT' in col]
    total_column = [col for col in df.columns if 'TOTAL' in col]
    
    if not department_column or not total_column:
        print(f"Warning: Skipping file {file} as it doesn't have both department and total columns.")
        continue
    
    # Extract the relevant columns
    department_column = department_column[0]  # Get the first match
    total_column = total_column[0]  # Get the first match

    # Clean the "TOTAL_EARNINGS" or "TOTAL_GROSS" column and convert it to numeric (removing $ and commas)
    df[total_column] = df[total_column].replace({'\$': '', ',': ''}, regex=True)
    
    # Convert to numeric, coercing errors to NaN, then drop rows with NaN values in the total column
    df[total_column] = pd.to_numeric(df[total_column], errors='coerce')
    df = df.dropna(subset=[total_column])
    
    # Filter for Boston Police Department (BPD) data
    bpd_data = df[df[department_column] == 'Boston Police Department']
    
    # Sum up the total earnings for this year and append to the list
    total_earnings_by_year.append(bpd_data[total_column].sum())

# Prepare the data for plotting
years = range(2011, 2025)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(years, total_earnings_by_year, marker='o', color='b', linestyle='-', linewidth=2, markersize=6)
plt.title("Boston Police Department Total Earnings (2011-2024)")
plt.xlabel("Year")
plt.ylabel("Total Earnings ($)")

# Use a ScalarFormatter to make the y-axis labels more human-readable
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Set the x-ticks and grid
plt.xticks(years)
plt.grid(True)

plt.savefig("./analysis/earnings/figures/figure_totalearnings.png", dpi=300, bbox_inches="tight")

