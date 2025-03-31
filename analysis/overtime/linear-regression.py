import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt

years = list(range(2012, 2023))
totals = []  # Ensure this gets populated

# Load data for each year
for year in years:
    df = pd.read_csv(f"../../data/overtime/{year}.csv")  # Ensure the correct file path
    total_ot = df["OTHOURS"].sum()
    totals.append(total_ot)

# Ensure totals has data
if not totals:
    raise ValueError("No overtime data found. Check your data files.")

# Convert years and totals to NumPy arrays
X = np.array(years).reshape(-1, 1)
y = np.array(totals)

# Fit a linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict for 2023, 2024, and 2025
future_years = np.array([[2023], [2024], [2025]])
predicted_totals = model.predict(future_years)

for year, pred in zip([2023, 2024, 2025], predicted_totals):
    print(f"Predicted Total Overtime Hours for {year}: {pred:.2f}")

# Plot the trend with predictions
plt.figure(figsize=(10, 5))
plt.plot(years, totals, marker='o', linestyle='-', color='b', label="Actual Data")
plt.scatter([2023, 2024, 2025], predicted_totals, color='r', label="Predictions (2023-2025)")
plt.xlabel("Year")
plt.ylabel("Total Overtime Hours")
plt.title("Total Yearly Overtime Hours with Predictions (2012-2025)")
plt.legend()
plt.grid(True)
plt.savefig('./figures/predicted-total-overtime-2025.png')
plt.show()