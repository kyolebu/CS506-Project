import pandas as pd
import matplotlib.pyplot as plt

years = list(range(2012, 2023))
totals = []
avgs = []
# rank_avgs = []

for year in years:
    df = pd.read_csv(f"../../data/overtime/{year}.csv")

    total_ot_per_employee = df.groupby("ID")["OTHOURS"].sum()
    avg_employee_ot = total_ot_per_employee.mean()
    avgs.append(avg_employee_ot)

    # total_ot_per_rank = df.groupby("RANK")["OTHOURS"].sum()
    # avg_rank_ot = 

    total_ot = df["OTHOURS"].sum()
    totals.append(total_ot)

    print(f"Average Overtime Hours Per Employee in Year {year}: {avg_ot}")

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