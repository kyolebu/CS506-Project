import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

years = list(range(2012, 2023))
totals = []
avgs = []

# Loop through each year and load the corresponding CSV file
for year in years:
    try:
        # Load the CSV file for each year into a DataFrame
        file_path = f"../../data/overtime/{year}.csv"  # Adjust path if needed
        print(f"Loading data for year {year} from {file_path}")
        df = pd.read_csv(file_path)
        
        # Ensure OTDATE is in datetime format
        if 'OTDATE' in df.columns:
            df['OTDATE'] = pd.to_datetime(df['OTDATE'])
        else:
            print(f"Warning: 'OTDATE' column not found in {year}.csv")
            continue
        
        # Calculate total overtime hours for the current year
        total_ot = df["OTHOURS"].sum()
        totals.append(total_ot)

        # Calculate average overtime hours per employee for the current year
        total_ot_per_employee = df.groupby("ID")["OTHOURS"].sum()
        avg_employee_ot = total_ot_per_employee.mean()
        avgs.append(avg_employee_ot)

        print(f"Total Overtime for {year}: {total_ot}, Average Overtime Per Employee: {avg_employee_ot}")
        
    except FileNotFoundError:
        print(f"Error: File for year {year} not found. Please check the file path.")
    except Exception as e:
        print(f"Error processing file for year {year}: {e}")

# Forecast the total overtime for the next year (2023) using ARIMA
# Convert totals to a time series
time_series = pd.Series(totals, index=years)

# Fit an ARIMA model
model = ARIMA(time_series, order=(5, 1, 0))  # Adjust the order as needed (p, d, q)
model_fit = model.fit()

# Forecast for the next year (2023)
forecast = model_fit.forecast(steps=1)
predicted_overtime = forecast[0]
print(f"Predicted Total Overtime Hours for 2023: {predicted_overtime}")

# Plot the historical overtime and forecast
plt.figure(figsize=(10, 5))
plt.plot(years, totals, marker='o', linestyle='-', color='b', label="Historical Overtime")
plt.plot(2023, predicted_overtime, marker='o', linestyle='-', color='r', label="Predicted Overtime 2023")
plt.xlabel("Year")
plt.ylabel("Total Overtime Hours")
plt.title("Total Overtime Hours (2012-2022) with 2023 Forecast")
plt.legend()
plt.grid(True)
plt.savefig('./figures/overtime-forecast.png')
plt.close()
