import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

# Define the directory where the data files are located
data_dir = 'data/earnings/'

# List all the files for years 2011 to 2024
file_names = [f"employee-earnings-report-{year}.csv" for year in range(2011, 2025)]

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
    
    # Identify the column names related to department, total earnings, and overtime
    department_column = [col for col in df.columns if 'DEPARTMENT' in col]
    total_column = [col for col in df.columns if 'TOTAL' in col]
    overtime_column = [col for col in df.columns if 'OVERTIME' in col]
    
    if not department_column or not total_column or not overtime_column:
        print(f"Warning: Skipping file {file} as it doesn't have the necessary columns.")
        continue
    
    # Extract the relevant columns
    department_column = department_column[0]  # Get the first match
    total_column = total_column[0]  # Get the first match
    overtime_column = overtime_column[0]  # Get the first match

    # Clean the "TOTAL_EARNINGS" or "TOTAL_GROSS" column and convert it to numeric (removing $ and commas)
    df[total_column] = df[total_column].replace({'\$': '', ',': ''}, regex=True)
    df[overtime_column] = df[overtime_column].replace({'\$': '', ',': ''}, regex=True)
    
    # Convert to numeric, coercing errors to NaN
    df[total_column] = pd.to_numeric(df[total_column], errors='coerce')
    df[overtime_column] = pd.to_numeric(df[overtime_column], errors='coerce')
    
    # Fill NaN values with 0 unless both total earnings and overtime are NaN
    df[total_column].fillna(0, inplace=True)
    df[overtime_column].fillna(0, inplace=True)
    
    # Drop rows where both total earnings and overtime are NaN (which is now impossible since we filled them with 0)
    df = df[~((df[total_column] == 0) & (df[overtime_column] == 0))]
    
    # Filter for Boston Police Department (BPD) data
    bpd_data = df[df[department_column] == 'Boston Police Department']
    
    # Prepare data for plotting
    total_earnings = bpd_data[total_column].tolist()
    overtime = bpd_data[overtime_column].tolist()
    
    # Plot the data as a scatter plot for this year
    year = file.split('-')[-1].split('.')[0]  # Extract the year from the file name
    
    plt.figure(figsize=(10, 6))
    plt.scatter(total_earnings, overtime, color='b', marker='o', s=10)

    # Set plot title and labels
    plt.title(f"BPD: Total Earnings vs Overtime Pay ({year}) - Employee Level")
    plt.xlabel("Total Earnings ($)")
    plt.ylabel("Overtime Pay ($)")

    # Add a grid
    plt.grid(True)

    # Use a ScalarFormatter to make the y-axis and x-axis labels more human-readable
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # Save the plot for the specific year
    plt.tight_layout()
    plt.savefig(f"./analysis/earnings/figures/plots/figure_bpd_total_earnings_vs_overtime_{year}.png", dpi=300, bbox_inches="tight")
    plt.close()  # Close the plot to avoid showing it immediately (useful when saving multiple plots)