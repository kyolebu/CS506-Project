import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

data_dir = 'data/earnings/'

# List all the files for years 2011 to 2022
file_names = [f"employee-earnings-report-{year}.csv" for year in range(2011, 2023)]

departments = [
    "Boston Police Department",
    "Boston Fire Department",
    "Boston Public Library",
    "Boston Public Schools"
]

total_earnings_by_year = {dept: [] for dept in departments}

years = range(2011, 2023)

for file in file_names:
    file_path = os.path.join(data_dir, file)
    
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        print(f"Error reading {file}. Skipping this file.")
        continue
    
    df.columns = [col.strip().replace(" ", "_").upper() for col in df.columns]
    
    department_column = [col for col in df.columns if 'DEPARTMENT' in col]
    total_column = [col for col in df.columns if 'TOTAL' in col]
    
    if not department_column or not total_column:
        print(f"Warning: Skipping file {file} as it doesn't have both department and total columns.")
        continue
    
    department_column = department_column[0]
    total_column = total_column[0]
    
    df[total_column] = df[total_column].replace({'\\$': '', ',': ''}, regex=True)
    df[total_column] = pd.to_numeric(df[total_column], errors='coerce')
    df = df.dropna(subset=[total_column])
    
    for dept in departments:
        if dept == "Boston Public Schools":
            dept_data = df[df[department_column].str.contains("Boston Public Schools|BPS", na=False, case=False)]
        else:
            dept_data = df[df[department_column] == dept]
        total_earnings_by_year[dept].append(dept_data[total_column].sum())
    
plt.figure(figsize=(12, 7))
colors = ['b', 'r', 'g', 'purple']
labels = ["BPD", "BFD", "BPL", "BPS"]

for idx, dept in enumerate(departments):
    plt.plot(years, total_earnings_by_year[dept], marker='o', linestyle='-', linewidth=2, markersize=6, color=colors[idx], label=labels[idx])

plt.title("Total Earnings by Department (2011-2022)")
plt.xlabel("Year")
plt.ylabel("Total Earnings ($)")
plt.legend()
plt.xticks(years)
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.grid(True)

plt.savefig("./analysis/earnings/figures/figure_totalearnings_comparison.png", dpi=300, bbox_inches="tight")
plt.show()
