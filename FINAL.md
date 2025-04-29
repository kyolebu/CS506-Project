# CS506 Project – Police Overtime Final Report

### Contributors: Kyle Yu, Wyatt Napier, Eric Nohara-LeClair, Ba Tien (Tien) Le

# Video Link

Video link here...

---

# Main Goal

- Analyze how the BDP budget gets spent, with a specific interest in overtime
- Synthesize recommendations on the allocation of overtime funds based off of our findings

---

# Building and Running Code

```
conda env create -f environment.yml
conda activate myenv
```

- Include Makefile maybe

---

# Final Project Report: Wyatt

## Description of Data Processing

For the roster data, there were many categorical columns which I then one-hot encoded such as 'Sex' and 'Ethnic Grp'. I used the pandas get dummies function to do so. After that, I continued on to encode the job titles. There were at least 9 different rankings of officers that were clear from observing the data:

1. Commissioner
2. Supn-In Chief
3. Supn Bpd
4. Dep Supn
5. Police Captain
6. Police Lieutenant
7. Police Sergeant
8. Police Detective
9. Police Officer
10. other

However, one limitation of this method of grouping the job titles is that there were more specific listings under "Police Officer" which leads to a larger variation in pay, even though Police Officer is the lowest ranking.

I also used the earnings data from 2020, which matched the year of the roster data, and by merging these two datasets on the cleaned names of employees I was able to extract demographic information about the top earners at the BPD. For that earning data to be useful, I used Tien's preprocessing to extract just the BPD employees.

I also calculated the amount of time that the each person has been employed at the time of the sheet's creation by calculating the difference between the 'Eff Date' column and 'As Of' column, but this yielded results that had very little variation so it seemed that it wouldn't add much to our investigation of the dataset.

## Description of Data Modeling Methods

For my initial visualizations, most of my data modeling methods aimed to capture the relationships between features within the BPD roster data using matplotlib. I was also able to use plotly to generate interactive plots where you can hover over each datapoint to ascertain more information about that person such as their ethnicity and specific job title. Finally, I also generated a decision tree as a more interpretable method of inspecting who qualifies as a high earner based on their demographics and job title.

## Data Visualizations

![Gender Distribtuion](./analysis/roster/figures/gender_distribution.png)
![Top 100 Earners Gender Distribution](./analysis/roster/figures/top_100_gender_distribution.png)

#### Takeaways

Although 86.2\% of the Boston Police Department is male, 96 of the 100 top earners are male. This showcases very obvious gender pay inequity among the top earners, which may be exacerbated by the imbalance in gender representation in the BPD.

![Ethnic Group Distribtuion](./analysis/roster/figures/ethnic_group_distribution.png)
![Top 100 Earners Ethnic Group Distribtuion](./analysis/roster/figures/top_100_ethnic_group_distribution.png)

#### Takeaways

Here, white people make up 65% of the overall police force, but interestingly, they only represent 57% of the top earners. Instead, top earning Black members of the BPD outshine their representation within the overall police department. However, Asian and Hispanic members of the BPD still suffer as the most marginalized communities.

<!-- ![Job Title Vs Annual Rate](./analysis/roster/figures/job_title_vs_annual_rt_by_gender.png) -->

![Job Title Vs Rates Combined](./analysis/roster/figures/job_title_vs_rates_seperate.png)

<!-- ![Rate Comparison](./analysis/roster/figures/rate_comparison.png) -->

#### Takeaways

Although income rates with respect to job titles have the smae relationship in both hourly and monthly timeframe, they differ greatly with respect to annual income which leads me to believe that there is something fishy going on with other sources of income besides standard rate.

![High Earner Decision Tree](./analysis/roster/EDA/top_earners_decision_tree2020.png)

#### Takeaways

As you might expect, those with higher ranking (and thus have lower job title index, which you can see above) are more likely to be high earners, which is captured by the root node as well as the left node in the second layer. Also, the right node in the second layer shows that if you are a woman (Sex_M $\leq 0.5$) then you are more likely to be classified as a low earner than a man of a similar position who may be a high earner.

## Overall Results

In general, I saw that there is a large issue of pay inequity in the Boston Police Department and that women are often simply making less than men. Interestingly, there seems to be less inequity with regard to ethnicity of employees. On top of this, as my teammates will explore shortly, there are also some suspicious activities with regard to other sources of income besides base hourly/monthly rate.

---

# Final Project Report: Tien

## Primary Analysis and Data Exploration: 

**Figure 1**:

*Description*: This chart displays the total annual earnings of the Boston Police Department (BPD) from 2011 to 2024. The y-axis represents total earnings in dollars, and the x-axis shows the years. A blue line with markers tracks changes over time, highlighting trends in BPD compensation.

![image](https://github.com/user-attachments/assets/3979076b-61ac-4215-ba2c-2b166afaf583)

*Takewaway*: 

- Steady Growth (2011–2018):
Total earnings rose consistently from around $290 million in 2011 to about $420 million in 2018, indicating increasing payroll and/or staffing.

- Stagnation and Slight Decline (2019–2022):
Earnings plateaued around $420–$430 million, with minor fluctuations. This may suggest budget caps, hiring freezes, or reduced overtime.

- Sharp Spike in 2024:
The most dramatic change is the spike to nearly $570 million in 2024—a sudden ~35% increase from 2023. This could reflect new contracts, major overtime events, or structural changes to payroll.

- COVID-Era Impact (2020–2022):
The mild drop from 2020 through 2022 might be tied to the pandemic’s fiscal or operational effects.

**Figure 2**:

*Description*: This stacked bar chart breaks down the Boston Police Department’s total earnings from 2011 to 2024 by different categories of compensation. Each bar represents a year, and each colored segment corresponds to a type of earning:

- REGULAR (blue): Base salary or standard pay
- OVERTIME (red): Pay for hours beyond regular shifts
- DETAIL (cyan): Special duty or private detail assignments
- RETRO (orange): Retroactive pay
- INJURED (purple): Earnings for injured officers
- OTHER (green): Miscellaneous compensation
- QUINN (pink): Quinn Bill incentives for education

![image](https://github.com/user-attachments/assets/3de633f3-40d8-4979-95b6-c6dd5c972b41)

*Takeaways*

- Regular Pay Dominates:
Across all years, regular earnings form the largest share of total compensation, showing a consistent upward trend.

- Overtime is Substantial:
Overtime pay is the second-largest component, especially notable in 2024, where it sharply increases. It appears to be a major cost driver in total earnings.

- Spike in 2024 Driven by Multiple Factors:
The 2024 spike (seen in the previous chart too) is due to not just overtime, but also large increases in retro, detail, and regular pay — suggesting back pay, increased staffing, or operational changes.

- Retroactive Pay Varies Significantly:
Retro pay appears sporadically but surges in 2014, 2016, and especially in 2024 — possibly tied to delayed contract settlements or pay corrections.

- Detail Pay is Consistently High:
This segment remains prominent in most years and grows again in 2024. This may reflect continued or increased use of officers for private or city-paid details.

- COVID-Era Patterns (2020–2022):
During the pandemic years, most components, including detail and injured pay, saw modest increases or stability, despite wider uncertainties.

**Figure 3**:

*Description*: This line chart shows total annual earnings from 2011 to 2022 for four Boston city departments:

- BPD (Police Department) – blue
- BFD (Fire Department) – red
- BPL (Public Library) – green
- BPS (Public Schools) – purple

The y-axis represents total earnings in dollars, and each line represents a department's payroll trends over time.

![image](https://github.com/user-attachments/assets/00cc76c2-f6c2-459a-a773-26fe376accb0)


*Takeaway*: 

- BPS (Schools) Has the Largest Budget: The Boston Public Schools (BPS) consistently spends the most on earnings, peaking around $690 million in 2013, dropping significantly in 2014, and then gradually climbing back toward $620 million by 2022.
- BPL (Libraries) Has the Smallest Earnings: The library system maintained a modest and relatively flat earnings curve, ranging between $20–30 million annually, indicating a smaller workforce or lower wage structure.
- BPD and BFD both had steady increases in budget, yet BFD did not see a 30% increase like BPD in 2024, as shown in the first figure.
- BPL funding remained relatively low compared to other departments.
- Overall, BPD witnessed the most growth.

**Figure 4**:

*Description*: This scatter plot shows the relationship between total earnings and overtime pay in 2021 for employees of three Boston departments:

- Boston Police Department (BPD) – blue

- Boston Fire Department (BFD) – red

- Boston Public Schools (BPS) – purple

Each dot represents an individual employee. Trend lines are overlaid for each department to show the general relationship between total pay and overtime.

![image](https://github.com/user-attachments/assets/bca15919-2aba-45c4-b6eb-804b0e66f873)

*Takeaways*

- Police Employees Receive the Highest Overtime at High Earnings:
BPD employees (blue) show the strongest upward trend—as total earnings rise, overtime pay increases sharply. Some individuals exceed $150,000 in overtime alone, a much steeper slope than BFD or BPS.

- Fire Department Also Shows Strong Overtime Dependency:
BFD employees (red) follow a similar pattern, though their overtime is less extreme than BPD. Their trend line rises more moderately, with fewer outliers beyond $100,000.

- BPS Has Minimal Overtime Impact:
BPS employees (purple) cluster low on the y-axis, showing minimal overtime pay even at higher earnings. Their trend line is nearly flat, indicating little correlation between overtime and total earnings.

- Overtime Disparities Are Clear:
The distribution and slope differences between departments illustrate how differently overtime is used across the city—BPD appears to rely most heavily on it as a compensation mechanism.

**Overall**:

Across multiple views of Boston city department payroll data, it's clear that the Boston Police Department (BPD) stands out for its significant and growing reliance on overtime pay. From 2011 to 2024, BPD earnings have risen steadily, with a dramatic spike in 2024 driven not only by regular wages but also by surging overtime, retroactive pay, and detail compensation. Compared to other departments like Fire (BFD), Schools (BPS), and Libraries (BPL), the police department consistently incurs higher earnings, particularly through overtime-intensive compensation structures.

A closer look at individual-level data (2021) confirms this trend: BPD employees often earn substantial portions of their income from overtime, with many surpassing $100,000 in OT alone—well above the norms in other departments. This heavy dependence on overtime may reflect staffing shortages, scheduling inefficiencies, or structural budget practices that prioritize variable pay over base salaries.

## Further analysis: 

---

# Final Project Report: Eric

## Guiding Question

Given previous overtime data, predict the amount of overtime paid for the next year. How does this compare with the budget allocation for the BPD?

## Overtime Per Employee Distributions

![Overtime Per Employee Distributions](./analysis/overtime/figures/pdfs/distributions.gif)
![2018 Outlier](./analysis/overtime/figures/pdfs/outlier_with_std.png)

### Goal

Find the distributions of overtime per employee and how they differ over the last 10 years to see if there are any trends/outliers

### Data Processing

- Load data from 2012 - 2022 CSV files, grouping by employee ID
- Determine X and Y axis limits for global scaling for the final animation

### Data Modeling Method

- Histogram based distribution modeling
  - Normalized to represent a PDF
  - 50 bins
- Added mean + median visualizations
- FuncAnimation to animate the changes in probability distributions across years for better visualization
- Box plot to visualize 2018 as an outlier

## Linear Regression

![Predicted Average Overtime Per Employee 2023](./analysis/overtime/figures/predicted-avg-overtime-per-employee-2025.png)
![Predicted Total Overtime 2023](./analysis/overtime/figures/predicted-total-overtime-2025.png)

### Goal

Identify trends and model the relationship between years and overtime data to make predictions for the future

### Data Processing

- Loaded yearly overtime data (2012-2022) from CSV files
- Summed overtime hours for each year and stored in a list
- Checked if data exists before proceeding

### Data Modeling

- Used Linear Regression to model overtime trends over the years
- Trained the model on the years (2012-2022) and their respective overtime totals
- Used model to predict years 2023, 2024, 2025 for both average hours per employee and total hours

## Random Forest Regression Model

![Regression Heatmap 2023](./analysis/overtime/figures/regression/heatmap.png)
![Regression Stacked Bar 2023](./analysis/overtime/figures/regression/stacked-bar.png)

### Goal

Predict total overtime hours for different officer ranks and task assignments in 2023 using historical data (2012–2022)

### Data Processing

- Load yearly CSV files (2012–2022) and combine them into a single dataset
- Convert OTDATE to a datetime object
- Encode categorical variables (RANK and ASSIGNED_DESC) using LabelEncoder
- Saved categorical variable mappings for ASSIGNED_DESC in ./analysis/overtime/csv/assigned_mapping_key.csv
- NOTE: use this key when interpreting the heat map

### Data Modeling

- Features (X): Year, Rank_Encoded, Assigned_Encoded
- Target (y): Total overtime hours (OTHOURS)
- Train Model: Use Random Forest Regressor on data from 2012–2022
- Inputted all possible combinations of officer rank and officer assignment into the trained model

## Department Overtime Analysis

![Overtime Earnings/Total Earnings Ratio by Department over 10 years](./analysis/overtime/figures/department/overtime-earnings-ratio.png)
![Top Overtime Earnings/Total Earnings Ratio by Department over 10 years](./analysis/overtime/figures/department/overtime-earnings-ratio-top.png)
![Top Total Overtime Earnings by Department over 10 years](./analysis/overtime/figures/department/total-overtime-top.png)
![Bottom Total Overtime Earnings by Department over 10 years](./analysis/overtime/figures/department/total-overtime-bottom.png)

### Goal

Find any relationships between department and overtime earnings over the last 10 years in order to better understand how to allocate the overtime budget to different departments.

### Data Processing

- Reformat CSV files for earnings with consistent column headers
- Load yearly earnings CSV files in /data/earnings-reformatted
- Combine yearly data from the last 10 years
- Reformat all numeric columns in the earnings data to turn strings of the format "$1,000,000" into numeric values
- Group by department and find total earnings and overtime earnings / total earnings ratio for each department

## Results

- We see 2018 is statistically an outlier in terms of average overtime per employee
- Otherwise, we see the mean overtime per employee per year hovers around 53.91 hours with a standard deviation of 7.82
- Excluding the outlier year, the distributions of overtime per employee per year is relatively stable
- The linear regression data suggests a slight increase in overtime hours in 2023, 2024, and 2025
  - We can expect around 140,000 - 150,000 overtime hours in the near future
  - 2018 data may skew the model
  - Accuracy may be lower due to small sample size of 10 years
- The Ramdom Forest Regression model suggests that patrol rank officers take the majority of the overtime hours while the LtDet rank officers take the least overtime
- The heatmap suggests that Districts 01 - 18 were the task assgnments which caused the highest levels of overtime across different police ranks, with District 4 in particular contributing the most to overtime hours across police ranks
- Most departments do not earn significant amounts of their total earnings from overtime, with most departments earning less than $10,000,000 in total overtime over the last 10 years
- BPD, Boston Fire Department, and Public Works were among the top overtime earners across all departments, with BPD in particular earning more than double the second highest earner, with almost $1,000,000,000 over the last 10 years

---

# Final Project Report: Kyle

## Data Visualizations

![Mean Earnings Trend](analysis/earnings/EDA/mean_earnings_trend.png)
![Earnings Distribution](analysis/earnings/EDA/earnings_distribution_comparison.png)
![Top Earners](analysis/earnings/EDA/top_earners_2024.png)

## Description of Data Processing

For the earnings data, I worked with multiple CSV files containing Boston Police Department earnings records from 2012 to 2024. One of the main challenges was dealing with inconsistent column naming across different years. I standardized these by mapping various versions to consistent names - for example, 'TOTAL EARNINGS' to 'TOTAL GROSS', 'QUINN' to 'QUINN_EDUCATION', and variations of 'DEPARTMENT' to 'DEPARTMENT_NAME'.

The data also required significant cleaning due to formatting inconsistencies. Many monetary values were stored as strings with dollar signs and commas, which I converted to numeric types for analysis. I also handled NaN values and data type inconsistencies that appeared in different years' files. For each year's data, I filtered specifically for police department employees to focus our analysis on BPD personnel.

## Description of Data Modeling Methods

For my initial visualizations, I focused on creating three main types of analyses using matplotlib and pandas. First, I created a line plot tracking mean earnings trends to show the overall growth in compensation over time. Second, I generated histograms comparing the distribution of earnings between 2012 and 2024 to understand how the spread of salaries has evolved. Finally, I implemented a horizontal bar chart showing the top 10 earners and their pay component breakdown for 2024.

## Results

From my visualizations, I observed several interesting trends in BPD compensation. The mean earnings analysis shows steady growth from $97,515 in 2012 to $131,321 in 2018, with an average annual increase of 4.2% that outpaces inflation. This growth isn't uniform across all officers though - the distribution analysis reveals growing income inequality within the department, with a more pronounced right skew in 2024 and more high-earning outliers.

Looking at the top earners in 2024, we see that the highest-paid officers earned over $575,000 annually, with overtime and detail work often contributing significantly to their total compensation. The Quinn Education incentives also play a notable role, with some officers receiving substantial educational bonuses. Perhaps most notably, injury-related pay has shown significant increases, and the 2024 data reveals a substantial amount of retroactive pay among top earners.

## Next Steps

Moving forward, I want to develop more sophisticated analyses of the earnings data. One priority is creating predictive models for future earnings trends and overtime allocation. I'm particularly interested in using regression analysis to identify which factors contribute most strongly to an officer becoming a high earner. Additionally, I want to investigate the relationship between rank/position and earnings components, as well as study how education levels impact total compensation.

---

# Final Conclusion + Recommendations to BPD

Our analysis explores the BPD overtime budget in a historical context, highlighting pay equity concerns, overtime allocation, and many different factors which had large impacts on overtime pay. It is clear that there is a need for a more strategic approach to the BPD budget allocation. Key findings include:

1. **Pay Equity:** Significant gender and ethnicity disparities exist among top earners in BPD.

2. **Overtime Management:** Overtime hours are projected to reach 140,000-150,000 hours in upcoming years, with patrol officers in District 4 contributing the most. BPD makes by far the highest total overtime earnings, along with Boston Fire Department and Public Works. The majority of other departments earn virtually none of their earnings from overtime pay. Injury pay is the largest category of overtime costs, signaling a need for improved injury management. Court overtime is another significant contributor to total overtime costs.

3. **Geographic and Crime-Based Allocation:** High-crime districts need more flexible overtime policies, while low-crime areas should implement stricter caps and officer reassignment to reduce unnecessary overtime.

Recommendations:

1. **Promote Diversity in High-Earning Roles:** Focus on increasing women and minority representation in roles that lead to higher compensation in BPD.

2. **Control Overtime Spending:** Set a soft cap of 140,000 overtime hours annually and implement a strict approval process based on rank, district, and department.

3. **Dynamic Overtime Policies:** Use crime rates to adjust overtime policies, with flexible spending in high-crime areas and strict caps in low-crime areas.

4. **Track Special Event Overtime:** Separate overtime for special events and use historical data to forecast future staffing needs and prevent overspending.

By implementing these measures, BPD can ensure more efficient, equitable, and strategic use of overtime funds.
