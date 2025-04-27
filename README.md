# CS506 Project – Police Overtime

Contributors: Kyle Yu, Wyatt Napier, Eric Nohara-LeClair, Ba Tien (Tien) Le

### Description

The Boston Police Department (BPD) has an operating budget of $400 million and an in-depth analysis on how this budget spent is increasingly important. Over the years, there have been two sides to policing in this country. The first is a group of public safety servants protecting the neighborhood from bad faith actors, while the second is empowering individuals with the authority to impede someone else’s agency welcomes all kinds of bias into the management of public safety. Because of this, audits are careful analysis of budget spending, specifically overtime, are needed to ensure the equal power between the police and the community.

### Goal

The goal of this project is to analyze how this budget gets spent by the BPD, with a specific interest in how they register overtime.

### Data Collection

Spark provides the data:

- Employee earnings data (search/filter for police)
- Payroll definitions
- BPD field activity datag
- BPD Roster
- Overtime data 2012-2022 (includes court, special events, detail)
- 2025 City of Boston Operating Budget

### Modeling Data

We plan on using clustering, regression, and decision trees in order to analyze trends in BPD budget spending. We'll use libraries and frameworks like sklearn, matplotlib, and numpy.

### Visualzing Data

We plan on using scatter plots to compare feature x to feature y, bar charts, heat maps, line graphs, confusion matrices.

### Test Plan

We want to conduct data validation so that we ensure our data is consistent between datasets, remove null values that might affect our results, and deal with outliers in our data that may be unrepresentative of the population. Then, we want to split our data using the 80/20 method to train and test our models.
