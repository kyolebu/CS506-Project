import os

cwd = os.getcwd()

### tests for main figures in analysis/roster
roster_path = os.path.join(cwd, 'analysis/roster/')
# assertions for figures in EDA folder
assert(os.path.exists(os.path.join(roster_path, 'EDA/top_earners_decision_tree2020.png'))), "ERROR: decision tree file doesn't exist"
# assertions for figures in figures folder
assert(os.path.exists(os.path.join(roster_path, 'figures/ethnic_group_distribution.png'))), "ERROR: ethnic group distribution file doesn't exist"
assert(os.path.exists(os.path.join(roster_path, 'figures/gender_distribution.png'))), "ERROR: gender distribution file doesn't exist"
assert(os.path.exists(os.path.join(roster_path, 'figures/top_100_ethnic_group_distribution.png'))), "ERROR: top 100 earners ethnic group distribution file doesn't exist"
assert(os.path.exists(os.path.join(roster_path, 'figures/top_100_gender_distribution.png'))), "ERROR: top 100 earners gender distribution file doesn't exist"
assert(os.path.exists(os.path.join(roster_path, 'figures/job_title_vs_annual_rt_by_gender.png'))), "ERROR: job title vs annual rate by gender file doesn't exist"
assert(os.path.exists(os.path.join(roster_path, 'figures/job_title_vs_rates_seperate.png'))), "ERROR: job title vs rates file doesn't exist"

# assertions for overtime figures
overtime_path = os.path.join(cwd, 'analysis/overtime/')
assert(os.path.exists(os.path.join(overtime_path, 'figures/predicted-avg-overtime-per-employee-2025.png')))
assert(os.path.exists(os.path.join(overtime_path, 'figures/predicted-total-overtime-2025.png')))
assert(os.path.exists(os.path.join(overtime_path, 'figures/pdfs/outlier_with_std.png')))
assert(os.path.exists(os.path.join(overtime_path, 'figures/pdfs/fast-distributions.gif')))
assert(os.path.exists(os.path.join(overtime_path, 'figures/regression/heatmap.png')))
assert(os.path.exists(os.path.join(overtime_path, 'figures/regression/predictions.png')))
assert(os.path.exists(os.path.join(overtime_path, 'figures/regression/stacked-bar.png')))

# assertions for overtime regression csv files
assert(os.path.exists(os.path.join(overtime_path, 'csv/assigned_mapping_key.csv')))
assert(os.path.exists(os.path.join(overtime_path, 'csv/predicted_overtime_2023.csv')))
