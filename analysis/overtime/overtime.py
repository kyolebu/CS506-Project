import pandas as pd

year = 2012
for _ in range(10):
    year += 1

    df = pd.read_csv(f"../../data/overtime/{year}-overtime.csv")

    formatted_hours_worked = df["Hours Worked"].apply(lambda x: x / 100 if x >= 24 else x)
    formatted_hours_paid = df["Hours Paid"].apply(lambda x: x / 100 if x >= 24 else x)
    
    df["Overtime Hours"] = formatted_hours_paid - formatted_hours_worked

    # total_ot = sum(df["Overtime Hours"])
    # avg_ot = total_ot / df.shape[0]

    total_ot_per_employee = df.groupby("Emp. ID")["Overtime Hours"].sum()
    avg_ot = total_ot_per_employee.mean()

    print(f"Average Overtime Hours Per Employee in Year {year}: {avg_ot}")
