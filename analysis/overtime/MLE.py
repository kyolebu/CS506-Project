import pandas as pd
import numpy as np
import scipy.stats as stats

# Load and combine data
dfs = []
for year in range(2012, 2023):
    df = pd.read_csv(f"../../data/overtime/{year}.csv")
    df["YEAR"] = year
    dfs.append(df)

full_df = pd.concat(dfs, ignore_index=True)

# Compute mean and standard deviation of OT for each year
year_stats = full_df.groupby("YEAR")["OTHOURS"].agg(["mean", "std"]).reset_index()
year_stats.columns = ["YEAR", "MEAN_OT", "STD_OT"]

print(year_stats)

def compute_likelihood(ot_hours, year_stats):
    likelihoods = {}
    for _, row in year_stats.iterrows():
        year = row["YEAR"]
        mu = row["MEAN_OT"]
        sigma = row["STD_OT"]
        
        # Compute probability density
        prob = stats.norm(mu, sigma).pdf(ot_hours)
        likelihoods[year] = prob

    return likelihoods

# Example: Compute likelihoods for 100 OT hours
ot_value = 100
likelihoods = compute_likelihood(ot_value, year_stats)

# Normalize to get probabilities
total_prob = sum(likelihoods.values())
posterior_probs = {year: prob / total_prob for year, prob in likelihoods.items()}

test_ot_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # Different overtime values

for ot in test_ot_values:
    likelihoods = compute_likelihood(ot, year_stats)
    posterior_probs = {year: prob / sum(likelihoods.values()) for year, prob in likelihoods.items()}
    most_likely_year = max(posterior_probs, key=posterior_probs.get)
    print(f"Most likely year for {ot} OT hours: {most_likely_year}")