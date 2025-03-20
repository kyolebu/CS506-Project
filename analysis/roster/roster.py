import pandas as pd
import matplotlib.pyplot as plt

### read csv
df = pd.read_csv(f"../../data/roster/bpd-roster-2020.csv")

### data preprocessing
# one-hot encode sex and ethnic group
# one-hot encode job title --> this brings it from 17 to 68 columns so maybe not worth and quite sparse
# calculate time served (as of 2020)
print(df.head()) # prior to preprocessing

df = df.drop(columns=["Union Code", "TskProfID", "Task Profile Descr"]) # get rid of unneccesary info

# difference between eff date and date of sheet's creation
df["Eff Date"] = pd.to_datetime(df["Eff Date"], format="%m/%d/%Y")
df["As Of"] = pd.to_datetime(df["As Of"], format="%m/%d/%Y")
df["Months Difference"] = (df["As Of"].dt.year - df["Eff Date"].dt.year) * 12 + (df["As Of"].dt.month - df["Eff Date"].dt.month)

df_encoded = pd.get_dummies(df, columns=['Sex', 'Ethnic Grp']) # generate one-hot encodings
df_encoded = df_encoded.drop(columns=["Sex_F"]) # removes redundancy from M/F being binary
df = df_encoded  # df_encoded already contains the one-hot encoded values and the original numerical columns

print(df.head()) # after preprocessing

### data analysis -- gender distribution
labels = ['Male', 'Female']
male_count = sum(df['Sex_M'] == True)
sizes = [male_count, df.shape[0] - male_count]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%',
       pctdistance=1.25, labeldistance=.6)
plt.show()
# plt.savefig('./figures/gender_distribution.png') # only uncomment when you want to save figure

### data analysis -- ethnic group
labels = ['Asian', 'White', 'Hispanic', 'Black']
sizes = [sum(df['Ethnic Grp_ASIAN'] == True), sum(df['Ethnic Grp_WHITE'] == True), sum(df['Ethnic Grp_HISPA'] == True), sum(df['Ethnic Grp_BLACK'] == True)]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%',
       pctdistance=1.25, labeldistance=.6)
plt.show()
# plt.savefig('./figures/ethnic_group_distribution.png') # only uncomment when you want to save figure

### data analysis -- annual rate and ethnic group (maybe add sex as color)
# Melt one-hot encoded ethnic group columns into a single column
df_melted = df.melt(id_vars=["Annual Rt"], 
                     value_vars=["Ethnic Grp_ASIAN", "Ethnic Grp_BLACK", "Ethnic Grp_HISPA", "Ethnic Grp_WHITE"],
                     var_name="Ethnic Grp", 
                     value_name="Is_Member")

# Filter only rows where the one-hot encoding is True (1)
df_melted = df_melted[df_melted["Is_Member"] == True]

# Convert column names to readable format
df_melted["Ethnic Grp"] = df_melted["Ethnic Grp"].str.replace("Ethnic Grp_", "")

# Group by Ethnic Group and extract Annual Rate values
ethnic_groups = df_melted["Ethnic Grp"].unique()
grouped_data = [df_melted[df_melted["Ethnic Grp"] == grp]["Annual Rt"] for grp in ethnic_groups]

# Plot boxplot using Matplotlib
plt.figure(figsize=(8, 5))
plt.boxplot(grouped_data, labels=ethnic_groups, patch_artist=True)

# Labels and title
plt.xlabel("Ethnic Group")
plt.ylabel("Annual Rate")
plt.title("Annual Rate Distribution by Ethnic Group")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show plot
plt.show()
plt.savefig('./figures/ethnic_group_vs_annual_rate.png') # only uncomment when you want to save figure