import pandas as pd
import matplotlib.pyplot as plt

### read csv
df = pd.read_csv(f"../../data/roster/bpd-roster-2020.csv")

### data preprocessing
# one-hot encode sex and ethnic group
# one-hot encode job title --> this brings it from 17 to 68 columns so maybe not worth and quite sparse
# calculate age
# calculate time served (as of 2020)
print(df.head()) # prior to preprocessing

df = df.drop(columns=["Union Code", "TskProfID", "Task Profile Descr"]) # get rid of unneccesary info

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
plt.savefig('./figures/gender_distribution.png') # only uncomment when you want to save figure

### data analysis -- ethnic group
labels = ['Asian', 'White', 'Hispanic', 'Black']
sizes = [sum(df['Ethnic Grp_ASIAN'] == True), sum(df['Ethnic Grp_WHITE'] == True), sum(df['Ethnic Grp_HISPA'] == True), sum(df['Ethnic Grp_BLACK'] == True)]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%',
       pctdistance=1.25, labeldistance=.6)
plt.show()
plt.savefig('./figures/ethnic_group_distribution.png') # only uncomment when you want to save figure

### data analysis -- 