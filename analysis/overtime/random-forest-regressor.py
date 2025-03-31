import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Define the range of years for your data files
years = range(2012, 2023)

# Initialize an empty DataFrame to combine data across years
all_data = pd.DataFrame()

# Loop through each year, load the data, and append to the combined DataFrame
for year in years:
    file_path = f"../../data/overtime/{year}.csv"  # Adjust the path as needed
    yearly_data = pd.read_csv(file_path)
    yearly_data["Year"] = year  # Add the year as a column
    all_data = pd.concat([all_data, yearly_data], ignore_index=True)

# Preprocessing
# Ensure OTDATE is a datetime object and extract the year (redundant but safe)
all_data["OTDATE"] = pd.to_datetime(all_data["OTDATE"], errors="coerce")

# Encode categorical variables: Rank and Assigned Description
rank_encoder = LabelEncoder()
all_data["Rank_Encoded"] = rank_encoder.fit_transform(all_data["RANK"])

assigned_encoder = LabelEncoder()
all_data["Assigned_Encoded"] = assigned_encoder.fit_transform(all_data["ASSIGNED_DESC"])

# Aggregate data for yearly overtime hours by rank and assigned description
aggregated_data = all_data.groupby(["Year", "Rank_Encoded", "Assigned_Encoded"]).agg(
    {"OTHOURS": "sum"}
).reset_index()

# Prepare Features and Target
X = aggregated_data[["Year", "Rank_Encoded", "Assigned_Encoded"]]
y = aggregated_data["OTHOURS"]

# Train the model using data from 2012 to 2022
X_train = X[X["Year"] <= 2022]
y_train = y[X["Year"] <= 2022]

# Predict for 2023
X_predict = X[X["Year"] == 2022].copy()
X_predict["Year"] = 2023  # Update the year to 2023 for predictions

# Train the Random Forest Regressor
model = RandomForestRegressor(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

# Predict overtime hours for 2023
predictions_2023 = model.predict(X_predict)

# Add the predictions to a new DataFrame for analysis
predicted_data_2023 = X_predict.copy()
predicted_data_2023["Predicted_OTHOURS"] = predictions_2023

# Save the predictions to a CSV file for further use
predicted_data_2023.to_csv("./csv/predicted_overtime_2023.csv", index=False)

plt.figure(figsize=(10, 6))
plt.plot(aggregated_data["Year"], aggregated_data["OTHOURS"], label="Historical Data")
plt.scatter(predicted_data_2023["Year"], predicted_data_2023["Predicted_OTHOURS"], color='red', label="2023 Predictions")
plt.xlabel("Year")
plt.ylabel("Total Overtime Hours")
plt.title("Overtime Predictions for Combinations of Officer Rank + Task Being Done in 2023")
plt.legend()
plt.grid(True)
# plt.show()
plt.savefig('./figures/regression/predictions.png')

# DISPLAY DATA

# Load combined historical data and predictions
years = range(2012, 2023)
all_data = pd.DataFrame()

# Loop through years to load historical data
for year in years:
    file_path = f"../../data/overtime/{year}.csv"  # Adjust as needed
    yearly_data = pd.read_csv(file_path)
    yearly_data["Year"] = year
    all_data = pd.concat([all_data, yearly_data], ignore_index=True)

# Add predictions for 2023 to historical data
predicted_data_2023 = pd.read_csv("./predicted_overtime_2023.csv")
predicted_data_2023["Year"] = 2023
predicted_data_2023["OTHOURS"] = predicted_data_2023["Predicted_OTHOURS"]
all_data = pd.concat([all_data, predicted_data_2023], ignore_index=True)

# Aggregate data
aggregated = all_data.groupby(["Year", "Rank_Encoded", "Assigned_Encoded"])["OTHOURS"].sum().reset_index()

# Rank mapping for readable labels
rank_mapping = {idx: rank for idx, rank in enumerate(rank_encoder.classes_)}
aggregated["Rank"] = aggregated["Rank_Encoded"].map(rank_mapping)

# --- Stacked Bar Plot: Historical Data + Predictions ---
rank_year_pivot = aggregated.pivot_table(index="Year", columns="Rank", values="OTHOURS", aggfunc="sum")

rank_year_pivot.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="viridis")
plt.title("Yearly Overtime Hours by Officer Rank Prediction (2023)")
plt.xlabel("Year")
plt.ylabel("Total Overtime Hours")
plt.legend(title="Rank", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
# plt.show()
plt.savefig('./figures/regression/stacked-bar.png')

# --- Heatmap: Rank vs. Assignment for Predicted 2023 ---
predicted_2023 = aggregated[aggregated["Year"] == 2023]
rank_assignment_pivot = predicted_2023.pivot(index="Rank", columns="Assigned_Encoded", values="OTHOURS")

assigned_mapping = {idx: assignment for idx, assignment in enumerate(assigned_encoder.classes_)}

# Create heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(rank_assignment_pivot, cmap="coolwarm", annot=False, fmt=".1f", cbar_kws={"label": "Predicted OT Hours"})
plt.title("Heatmap of Predicted Overtime Hours (2023) by Rank and Assignment")
plt.xlabel("Assignment (Encoded)")
plt.ylabel("Rank")
plt.tight_layout()

# plt.show()
plt.savefig('./figures/regression/heatmap.png')

assigned_mapping_df = pd.DataFrame(list(assigned_mapping.items()), columns=["Encoded Value", "Assignment Description"])
assigned_mapping_df.to_csv("./csv/assigned_mapping_key.csv", index=False)