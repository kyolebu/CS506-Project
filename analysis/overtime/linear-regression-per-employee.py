import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt

years = list(range(2012, 2023))
avgs = []  # Store average overtime per employee

# Load data and compute average overtime per employee
for year in years:
    df = pd.read_csv(f"../../data/overtime/{year}.csv")  # Ensure the file path is correct
    total_ot_per_employee = df.groupby("ID")["OTHOURS"].sum()
    avg_employee_ot = total_ot_per_employee.mean()
    avgs.append(avg_employee_ot)

# Ensure avgs has data
if not avgs:
    raise ValueError("No overtime data found. Check your data files.")

# Convert years and averages to NumPy arrays
X = np.array(years).reshape(-1, 1)
y = np.array(avgs)

# Fit a linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict for 2023, 2024, and 2025
future_years = np.array([[2023], [2024], [2025]])
predicted_avgs = model.predict(future_years)

for year, pred in zip([2023, 2024, 2025], predicted_avgs):
    print(f"Predicted Average Overtime Hours Per Employee for {year}: {pred:.2f}")

# Plot actual and predicted data
plt.figure(figsize=(10, 5))
plt.plot(years, avgs, marker='o', linestyle='-', color='b', label="Actual Data")
plt.scatter([2023, 2024, 2025], predicted_avgs, color='r', label="Predictions (2023-2025)")
plt.xlabel("Year")
plt.ylabel("Average Overtime Hours")
plt.title("Average Yearly Overtime Hours Per Employee with Predictions (2012-2025)")
plt.legend()
plt.grid(True)
plt.savefig('./figures/predicted-avg-overtime-per-employee-2025.png')
plt.show()

###################################################################################

from statsmodels.tsa.arima.model import ARIMA

# Fit ARIMA model (p=1, d=1, q=1 is a common starting point)
arima_model = ARIMA(avgs, order=(1, 1, 1))
arima_fit = arima_model.fit()

# Predict for 2023, 2024, 2025
future_preds = arima_fit.forecast(steps=3)

for year, pred in zip([2023, 2024, 2025], future_preds):
    print(f"Predicted Overtime Hours for {year}: {pred:.2f}")

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(years, avgs, marker='o', linestyle='-', color='b', label="Actual Data")
plt.scatter([2023, 2024, 2025], future_preds, color='r', label="Predictions")
plt.xlabel("Year")
plt.ylabel("Average Overtime Hours per Employee")
plt.title("ARIMA Time Series Prediction")
plt.legend()
plt.grid(True)
plt.show()