import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.ticker as ticker

# Define data directory
data_dir = 'data/earnings/'

# Years to analyze
years_to_plot = [2018, 2019, 2020, 2021]
file_names = {year: f"employee-earnings-report-{year}.csv" for year in years_to_plot}

# Departments to analyze
departments = {
    "Boston Police Department": "b",
    "Boston Fire Department": "r",
    "BPS": "purple"
}

# Process each year separately
for year, file in file_names.items():
    file_path = os.path.join(data_dir, file)
    
    # Try reading the CSV file
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        print(f"Error reading {file}. Skipping this file.")
        continue
    
    # Normalize column names
    df.columns = [col.strip().replace(" ", "_").upper() for col in df.columns]
    
    # Identify required columns
    department_column = next((col for col in df.columns if 'DEPARTMENT' in col), None)
    total_column = next((col for col in df.columns if 'TOTAL' in col), None)
    overtime_column = next((col for col in df.columns if 'OVERTIME' in col), None)

    if not department_column or not total_column or not overtime_column:
        print(f"Warning: Skipping file {file} as it doesn't have necessary columns.")
        continue
    
    # Clean numeric columns
    for col in [total_column, overtime_column]:
        df[col] = df[col].replace({'\$': '', ',': ''}, regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna(subset=[total_column, overtime_column])

    plt.figure(figsize=(10, 6))

    # Process each department
    for dept, color in departments.items():
        dept_data = df[df[department_column].str.contains(dept, na=False, case=False)]

        if dept_data.empty:
            continue

        total_earnings = np.array(dept_data[total_column])
        overtime = np.array(dept_data[overtime_column])

        # Scatter plot
        plt.scatter(total_earnings, overtime, color=color, label=dept, s=5, alpha=0.7)

        # Fit and plot best-fit curve (Quadratic)
        if len(total_earnings) > 2:
            degree = 2  # Quadratic trend line
            coeffs = np.polyfit(total_earnings, overtime, degree)
            trendline = np.poly1d(coeffs)
            x_vals = np.linspace(min(total_earnings), max(total_earnings), 300)
            plt.plot(x_vals, trendline(x_vals), color=color, linestyle='-', linewidth=2)

    # Labels and formatting
    plt.title(f"Overtime vs. Total Earnings by Department ({year})")
    plt.xlabel("Total Earnings ($)")
    plt.ylabel("Overtime Pay ($)")
    plt.legend()
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # Save plot
    plt.tight_layout()
    plt.savefig(f"./analysis/earnings/figures/figure_intradepartment_overtime_vs_earnings_{year}.png", dpi=300, bbox_inches="tight")
    plt.show()
