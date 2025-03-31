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