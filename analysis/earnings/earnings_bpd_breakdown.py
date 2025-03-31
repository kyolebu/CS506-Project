import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

data_dir = 'data/earnings/'

# List all the files for years 2011 to 2024
years = list(range(2011, 2025))  # Ensure years is a list

file_names = [f"employee-earnings-report-{year}.csv" for year in years]

# Updated categories to include "DETAIL" and a dynamic "QUINN" column
categories = ["REGULAR", "OVERTIME", "OTHER", "INJURED", "RETRO", "DETAIL"]
total_earnings_by_year = {category: [0] * len(years) for category in categories}
total_earnings_by_year["QUINN"] = [0] * len(years)  # Quinn column will be identified dynamically

# Loop through each file to process data
for idx, file in enumerate(file_names):
    file_path = os.path.join(data_dir, file)
    
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        print(f"Error reading {file}. Skipping this file.")
        continue
    
    df.columns = [col.strip().replace(" ", "_").upper() for col in df.columns]
    
    department_column = next((col for col in df.columns if 'DEPARTMENT' in col), None)
    total_column = next((col for col in df.columns if 'TOTAL' in col), None)
    
    if not department_column or not total_column:
        print(f"Warning: Skipping file {file} as it doesn't have both department and total columns.")
        continue
    
    # Find the "QUINN" column
    quinn_column = next((col for col in df.columns if 'QUINN' in col), None)
    if quinn_column and "QUINN" not in categories:
        categories.append("QUINN")  # Add QUINN to categories if found
        total_earnings_by_year["QUINN"] = [0] * len(years)

    # Replace the dollar sign and commas, then convert to numeric
    df[total_column] = df[total_column].replace({'\\$': '', ',': ''}, regex=True).infer_objects(copy=False)
    df[total_column] = pd.to_numeric(df[total_column], errors='coerce')
    df = df.dropna(subset=[total_column])
    
    # Filter only Boston Police Department employees
    bpd_data = df[df[department_column] == 'Boston Police Department']

    # Now we process the breakdown columns
    breakdown_columns = categories.copy()
    
    for category_col in breakdown_columns:
        if category_col in bpd_data.columns:
            if bpd_data[category_col].notna().any():
                # Use infer_objects(copy=False) to prevent the FutureWarning
                bpd_data.loc[:, category_col] = (
                    bpd_data[category_col].replace({'\\$': '', ',': ''}, regex=True)
                    .infer_objects(copy=False)
                )
                bpd_data.loc[:, category_col] = pd.to_numeric(bpd_data[category_col], errors='coerce')

    # Extract the current year index
    year_idx = idx  # Since idx matches the order in `years`
    
    # Sum the breakdown categories for each year
    for category in breakdown_columns:
        if category in bpd_data.columns:
            total_earnings_by_year[category][year_idx] = bpd_data[category].sum()


for category in total_earnings_by_year:
    assert len(total_earnings_by_year[category]) == len(years), f"Mismatch in {category}"

bottom_values = [0] * len(years)

colors = ['b', 'r', 'g', 'purple', 'orange', 'cyan', 'pink']

plt.figure(figsize=(12, 7))

# Loop through each category and stack the bars
for idx, category in enumerate(categories):
    plt.bar(years, total_earnings_by_year[category], bottom=bottom_values, color=colors[idx % len(colors)], label=category)
    
    # Update the bottom values for stacking
    bottom_values = [bottom + total for bottom, total in zip(bottom_values, total_earnings_by_year[category])]

# Adding title and labels
plt.title("Boston Police Department Earnings Breakdown (2011-2024)")
plt.xlabel("Year")
plt.ylabel("Total Earnings ($)")
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xticks(years)
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.savefig("./analysis/earnings/figures/figure_bpd_earnings_breakdown_stacked.png", dpi=300, bbox_inches="tight")
plt.show()
