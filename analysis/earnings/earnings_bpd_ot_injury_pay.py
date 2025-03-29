import pandas as pd
import os
import matplotlib.pyplot as plt

data_dir = 'data/earnings/'
file_names = {year: f"employee-earnings-report-{year}.csv" for year in range(2011, 2025)}
output_dir = "./analysis/earnings/figures/charts/"
os.makedirs(output_dir, exist_ok=True)

# Initialize storage for results
bpd_results = {"Year": [], "Total Injury Pay": [], "Injury %": [], "Overtime %": []}

# Loop through each file
for year, file in file_names.items():
    file_path = os.path.join(data_dir, file)
    
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except Exception as e:
        print(f"Error reading {file}: {e}")
        continue

    # Standardize column names
    df.columns = [col.strip().replace(" ", "_").upper() for col in df.columns]

    # Identify relevant columns
    department_column = next((col for col in df.columns if 'DEPARTMENT' in col), None)
    overtime_column = next((col for col in df.columns if 'OVERTIME' in col), None)
    injured_column = next((col for col in df.columns if 'INJURED' in col), None)

    if not department_column or not overtime_column or not injured_column:
        print(f"Skipping {file} - missing necessary columns.")
        continue

    # Filter for Boston Police Department (BPD)
    bpd_data = df[df[department_column] == 'Boston Police Department'].copy()

    # Function to clean currency values & handle (negative) numbers
    def clean_currency(value):
        if isinstance(value, str):
            value = value.replace('$', '').replace(',', '').replace('-', '0').strip()
            # Convert (2.51) → -2.51
            if value.startswith('(') and value.endswith(')'):
                value = '-' + value[1:-1]
        return float(value) if value else 0.0

    # Clean and convert numeric columns
    for col in [overtime_column, injured_column]:
        bpd_data.loc[:, col] = bpd_data[col].astype(str).apply(clean_currency)

    # Calculate total injury pay
    total_injury_pay = bpd_data[injured_column].sum()

    # Calculate percentage of officers receiving injury and overtime pay
    total_officers = len(bpd_data)
    num_injured_officers = (bpd_data[injured_column] > 0).sum()
    num_overtime_officers = (bpd_data[overtime_column] > 0).sum()

    injury_percentage = (num_injured_officers / total_officers) * 100 if total_officers > 0 else 0
    overtime_percentage = (num_overtime_officers / total_officers) * 100 if total_officers > 0 else 0

    # Store results
    bpd_results["Year"].append(year)
    bpd_results["Total Injury Pay"].append(total_injury_pay)
    bpd_results["Injury %"].append(injury_percentage)
    bpd_results["Overtime %"].append(overtime_percentage)

    # ---- Generate Pie Charts ----
    
    #Injury Pay Pie Chart
    injury_labels = ['Received Injury Pay', 'Did Not Receive Injury Pay']
    injury_sizes = [num_injured_officers, total_officers - num_injured_officers]
    plt.figure(figsize=(6, 6))
    plt.pie(injury_sizes, labels=injury_labels, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'], startangle=140)
    plt.title(f'BPD Officers Receiving Injury Pay ({year})')
    plt.savefig(f"{output_dir}bpd_injury_pay_{year}.png")
    plt.close()

    #Overtime Pay Pie Chart
    overtime_labels = ['Received Overtime Pay', 'Did Not Receive Overtime Pay']
    overtime_sizes = [num_overtime_officers, total_officers - num_overtime_officers]
    plt.figure(figsize=(6, 6))
    plt.pie(overtime_sizes, labels=overtime_labels, autopct='%1.1f%%', colors=['#ffcc99', '#99ff99'], startangle=140)
    plt.title(f'BPD Officers Receiving Overtime Pay ({year})')
    plt.savefig(f"{output_dir}bpd_overtime_pay_{year}.png")
    plt.close()

results_df = pd.DataFrame(bpd_results)
output_path = "./analysis/earnings/bpd_injury_overtime_summary.csv"
results_df.to_csv(output_path, index=False)
print(f"Results saved to {output_path}")
print(f"All pie charts saved in: {output_dir}")
