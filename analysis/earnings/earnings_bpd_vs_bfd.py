import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

data_dir = 'data/earnings/'

# List all the files for years 2011 to 2024
years = list(range(2011, 2025))
file_names = [f"employee-earnings-report-{year}.csv" for year in years]

# Categories we need to extract
categories = ["OVERTIME", "INJURED"]

# Initialize dictionaries to store earnings by year for BPD and BFD
bpd_earnings = {category: [0] * len(years) for category in categories}
bfd_earnings = {category: [0] * len(years) for category in categories}

# Function to clean and convert earnings columns
def clean_and_convert(series):
    series = series.astype(str).str.strip()
    series = series.str.replace(r'[\$,]', '', regex=True)  # Remove $ and commas
    series = series.str.replace(r'\((.*?)\)', r'-\1', regex=True)  # Convert (2.51) to -2.51
    return pd.to_numeric(series, errors='coerce').fillna(0)  # Convert to float, replace NaN with 0

# Loop through each file to process data
for idx, file in enumerate(file_names):
    file_path = os.path.join(data_dir, file)
    
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        print(f"Error reading {file}. Skipping this file.")
        continue
    
    # Normalize the column names
    df.columns = [col.strip().replace(" ", "_").upper() for col in df.columns]
    
    # Identify the department column
    department_column = next((col for col in df.columns if 'DEPARTMENT' in col), None)
    if not department_column:
        print(f"Skipping {file}: No department column found.")
        continue
    
    # Process only BPD and BFD data
    bpd_data = df[df[department_column] == 'Boston Police Department'].copy()
    bfd_data = df[df[department_column] == 'Boston Fire Department'].copy()

    # Extract overtime & injured pay, ensuring proper type conversion
    for category in categories:
        if category in df.columns:
            bpd_data.loc[:, category] = clean_and_convert(bpd_data[category])
            bfd_data.loc[:, category] = clean_and_convert(bfd_data[category])
            
            bpd_earnings[category][idx] = bpd_data[category].sum()
            bfd_earnings[category][idx] = bfd_data[category].sum()

# 🎨 Plot the data
plt.figure(figsize=(12, 6))
colors = {"OVERTIME": "b", "INJURED": "r"}

for category in categories:
    plt.plot(years, bpd_earnings[category], marker='o', linestyle='-', color=colors[category], label=f"BPD {category}")
    plt.plot(years, bfd_earnings[category], marker='s', linestyle='--', color=colors[category], label=f"BFD {category}")

plt.title("BPD vs. BFD: Overtime & Injured Pay (2011-2024)")
plt.xlabel("Year")
plt.ylabel("Total Earnings ($)")
plt.legend()
plt.xticks(years)
plt.grid(True, linestyle="--", alpha=0.7)

# Format y-axis as dollars
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Save and display the figure
plt.savefig("./analysis/earnings/figures/figure_bpd_vs_bfd.png", dpi=300, bbox_inches="tight")
plt.show()
