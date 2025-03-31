import pandas as pd
import matplotlib.pyplot as plt

years = list(range(2012, 2023))
totals = []
avgs = []

# Loop through each year and load the corresponding CSV file
for year in years:
    try:
        # Load the CSV file for each year into a DataFrame
        df = pd.read_csv(f"../../data/overtime/{year}.csv")  # Adjust path if needed
        
        # Check if 'OTDATE' column exists
        if 'OTDATE' in df.columns:
            # Convert OTDATE to datetime format
            df['OTDATE'] = pd.to_datetime(df['OTDATE'])
        else:
            print(f"Warning: 'OTDATE' column not found in {year}.csv")
            continue  # Skip to the next year if 'OTDATE' column is missing
        
        # Calculate total overtime per employee by grouping by "ID"
        total_ot_per_employee = df.groupby("ID")["OTHOURS"].sum()

        # Calculate the average overtime hours per employee for the current year
        avg_employee_ot = total_ot_per_employee.mean()
        avgs.append(avg_employee_ot)

        # Calculate total overtime hours for the current year
        total_ot = df["OTHOURS"].sum()
        totals.append(total_ot)

        # Print average overtime for this year
        print(f"Average Overtime Hours Per Employee in Year {year}: {avg_employee_ot}")
        
    except FileNotFoundError:
        print(f"Error: File for year {year} not found. Please check the file path.")
    except Exception as e:
        print(f"Error processing file for year {year}: {e}")

# Average overtime plot
plt.figure(figsize=(10, 5))
plt.plot(years, avgs, marker='o', linestyle='-', color='b')
plt.xlabel("Year")
plt.ylabel("Average Overtime Hours")
plt.title("Average Yearly Overtime Hours Per Employee (2012-2022)")
plt.grid(True)
plt.savefig('./figures/avg-overtime-per-employee.png')
plt.close()

# Total overtime plot
plt.figure(figsize=(10, 5))
plt.plot(years, totals, marker='o', linestyle='-', color='b')
plt.xlabel("Year")
plt.ylabel("Total Overtime Hours")
plt.title("Total Yearly Overtime Hours (2012-2022)")
plt.grid(True)
plt.savefig('./figures/total-overtime.png')
plt.close()

import seaborn as sns
import matplotlib.pyplot as plt

# Stacked Bar Plot: Yearly Trends by Rank
rank_year_data = all_data.groupby(["Year", "RANK"])["OTHOURS"].sum().reset_index()
rank_year_pivot = rank_year_data.pivot(index="Year", columns="RANK", values="OTHOURS")

rank_year_pivot.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="viridis")
plt.title("Yearly Overtime Hours by Rank")
plt.xlabel("Year")
plt.ylabel("Total Overtime Hours")
plt.legend(title="Rank")
plt.grid(True)
plt.tight_layout()
plt.show()

# Heatmap: Rank vs. Assignment vs. Hours
rank_assignment_data = all_data.groupby(["Rank_Encoded", "Assigned_Encoded"])["OTHOURS"].sum().reset_index()
rank_assignment_pivot = rank_assignment_data.pivot("Rank_Encoded", "Assigned_Encoded", "OTHOURS")

plt.figure(figsize=(12, 8))
sns.heatmap(rank_assignment_pivot, cmap="coolwarm", annot=True, fmt=".1f", cbar_kws={"label": "Total Overtime Hours"})
plt.title("Heatmap of Overtime Hours by Rank and Assignment")
plt.xlabel("Assigned Description (Encoded)")
plt.ylabel("Rank (Encoded)")
plt.tight_layout()
plt.show()

# Line Plot: Yearly Trends for a Specific Rank
specific_rank_data = all_data[all_data["Rank_Encoded"] == 0]  # Example: Filtering for a specific rank
yearly_hours = specific_rank_data.groupby("Year")["OTHOURS"].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=yearly_hours, x="Year", y="OTHOURS", marker="o", label="Rank 0")
plt.title("Yearly Overtime Hours Trend for Rank 0")
plt.xlabel("Year")
plt.ylabel("Total Overtime Hours")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
