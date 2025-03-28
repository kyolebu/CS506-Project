import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### leadership rankings so they can be encoded:
'''
1) Commissioner
2) Supn-In Chief
3) Supn Bpd
4) Dep Supn
5) Police Captain
6) Police Lieutenant
7) Police Sergeant
8) Police Detective
9) Police Officer
10) other
'''
titles = [
              "Commissioner", "Supn-In Chief", "Supn Bpd", "Dep Supn",
              "Police Captain", "Police Lieutenant", "Police Sergeant",
              "Police Detective", "Police Officer", "Other"
       ]

### data preprocessing
def preprocess(df):
       '''
       one-hot encode sex and ethnic group
       one-hot encode job title --> this brings it from 17 to 68 columns so maybe not worth and quite sparse
       label-encode job title/ranking
       '''
       df = df.drop(columns=["Union Code", "TskProfID", "Task Profile Descr"]) # get rid of unneccesary info

       # difference between eff date and date of sheet's creation
       df["Eff Date"] = pd.to_datetime(df["Eff Date"], format="%m/%d/%Y")
       df["As Of"] = pd.to_datetime(df["As Of"], format="%m/%d/%Y")
       df["Months Difference"] = (df["As Of"].dt.year - df["Eff Date"].dt.year) * 12 + (df["As Of"].dt.month - df["Eff Date"].dt.month)

       df_encoded = pd.get_dummies(df, columns=['Sex', 'Ethnic Grp']) # generate one-hot encodings
       df_encoded = df_encoded.drop(columns=["Sex_F"]) # removes redundancy from M/F being binary
       df_encoded["Ethnic Grp Categorical"] = df["Ethnic Grp"].astype(str) # append the categorical column for use later?
       df = df_encoded  # df_encoded already contains the one-hot encoded values and the original numerical columns

       # used in to encode job titles
       def encode_ranking(col: pd.Series) -> pd.Series:
              def get_title_index(entry):
                     for idx, title in enumerate(titles, start=1):
                            if title in entry:
                                   return idx
                     return 10  # "other" category

              return col.apply(get_title_index)
       df['Job Title'] = encode_ranking(df['Job Title']) # what if I need to keep all of the job titles because I lost some
       return df

### data analysis -- gender distribution
def plot_gender_dist():
       labels = ['Male', 'Female']
       male_count = sum(df['Sex_M'] == True)
       sizes = [male_count, df.shape[0] - male_count]
       fig, ax = plt.subplots()
       ax.pie(sizes, labels=labels, autopct='%1.1f%%',
              pctdistance=1.25, labeldistance=.6)
       plt.savefig('./figures/gender_distribution.png') # only uncomment when you want to save figure
       plt.show()

### data analysis -- ethnic group
def plot_ethnic_grp_dist():
       labels = ['Asian', 'White', 'Hispanic', 'Black']
       sizes = [sum(df['Ethnic Grp_ASIAN'] == True), sum(df['Ethnic Grp_WHITE'] == True), sum(df['Ethnic Grp_HISPA'] == True), sum(df['Ethnic Grp_BLACK'] == True)]
       fig, ax = plt.subplots()
       ax.pie(sizes, labels=labels, autopct='%1.1f%%',
              pctdistance=1.25, labeldistance=.6)
       plt.savefig('./figures/ethnic_group_distribution.png') # only uncomment when you want to save figure
       plt.show()

### data analysis -- annual rate and ethnic group (maybe add sex as color)
def plot_job_title_vs_annual_rt_vs_gender():
       gender_colors = df['Sex_M'].map({True: 'blue', False: 'red'})
       print(gender_colors)

       plt.scatter(df['Job Title'], df['Annual Rt'], c=gender_colors, alpha=0.5)

       plt.xticks(ticks=range(1, 11), labels=titles, rotation=45, ha='right')
       plt.title("Job Title vs. Annual Rate of Income (by Gender)")
       plt.xlabel("Job Title")
       plt.ylabel("Annual Rt")
       plt.legend(handles=[
              plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Male', alpha=0.5),
              plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Female', alpha=0.5)
       ])
       plt.tight_layout()  # Adjusts plot to fit labels
       plt.savefig('./figures/job_title_vs_annual_rt_by_gender.png') # very interesting outlier
       plt.show()

def plot_job_title_vs_rates_combined():
       plt.xticks(ticks=range(1, 11), labels=titles, rotation=45, ha='right')
       plt.title("Job Title vs. Rates of Income")
       plt.xlabel("Job Title")
       plt.ylabel("Rate")

       # Create polynomial trendlines for hrly rate, monthly rt, and annual rt
       # Fit polynomial of degree 2 (quadratic trendline)
       for rate_col in ['Hrly Rate', 'Monthly Rt', 'Annual Rt']:
              # Use the Job Title index for x values
              x = df['Job Title']
              y = df[rate_col]
              
              # Fit a 2nd-degree polynomial to the data
              coefficients = np.polyfit(x, y, 2)  # 2 for quadratic polynomial
              poly = np.poly1d(coefficients)
              
              # Generate x values for plotting the trendline
              x_vals = np.linspace(1, 10, 100)
              y_vals = poly(x_vals)
              
              # Plot the polynomial trendline
              plt.plot(x_vals, y_vals, label=f'{rate_col} Trendline')

       # Add trendline legend and display the plot
       plt.legend(loc='upper right')
       plt.yscale('log')
       plt.tight_layout()  # Adjusts plot to fit labels
       plt.savefig('./figures/job_title_vs_rates_combined.png')
       plt.show()

def plot_job_title_vs_rates_seperate():
       # Create subplots, one for each rate (Hourly Rate, Monthly Rate, Annual Rate)
       fig, axs = plt.subplots(1, 3, figsize=(18, 6))  # 1 row, 3 columns
       
       # Gender colors for the scatter plot
       gender_colors = df['Sex_M'].map({True: 'blue', False: 'red'})
       
       # Iterate over the columns for 'Hrly Rt', 'Monthly Rt', and 'Annual Rt'
       for i, rate_col in enumerate(['Hrly Rate', 'Monthly Rt', 'Annual Rt']):
              ax = axs[i]  # Get the corresponding axis for the current subplot
              x = df['Job Title']
              y = df[rate_col]
              
              # Scatter plot for each rate vs Job Title
              ax.scatter(x, y, c=gender_colors, alpha=0.5)
              
              # Fit a 2nd-degree polynomial to the data
              coefficients = np.polyfit(x, y, 2)  # 2 for quadratic polynomial
              poly = np.poly1d(coefficients)
              
              # Generate x values for plotting the trendline
              x_vals = np.linspace(1, 10, 100)
              y_vals = poly(x_vals)
              
              ax.plot(x_vals, y_vals, label=f'{rate_col} Trendline', color='green') # plot poly trendline
              
              ax.set_title(f"Job Title vs {rate_col}")
              ax.set_xlabel("Job Title")
              ax.set_ylabel(rate_col)
              
              # Set job titles as x-axis labels
              ax.set_xticks(range(1, 11))
              ax.set_xticklabels(titles, rotation=45, ha='right')

              plt.legend(handles=[
                     plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Male', alpha=0.5),
                     plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Female', alpha=0.5)
              ])
       
       plt.tight_layout()
       plt.savefig('./figures/job_title_vs_rates_seperate.png')
       plt.show()

### data analysis -- print info about person with highest annual rt
def max_annual_rt():
       row = df[df["Annual Rt"] == df["Annual Rt"].max()] # investigating outlier from job_title_vs_annual_rt_vs_gender
       print(row[["Ethnic Grp Categorical", "Sex_M", "Job Title"]].iloc[0])


### running code:

### read csv
df = pd.read_csv(f"../../data/roster/bpd-roster-2020.csv")
print(df.head()) # prior to preprocessing
df = preprocess(df)
print(df.head()) # after preprocessing

### plots
# plot_ethnic_grp_dist()
# plot_gender_dist()
# plot_job_title_vs_annual_rt_vs_gender()
# plot_job_title_vs_rates_combined()
# plot_job_title_vs_rates_seperate()