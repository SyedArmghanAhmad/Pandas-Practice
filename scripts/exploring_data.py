import pandas as pd
import matplotlib.pyplot as plt

output_folder = r"E:\Pandas-Practice\outputs"

#load the Titanic dataset
file_path = r"E:\Pandas-Practice\data\titanic.csv"
df = pd.read_csv(file_path)

#Explore the dataset
print("First 5 rows of the dataset: ")
print(df.head()) # Preview the data

print("\nDataset Information: ")
print(df.info()) # Check column types and non-null values

print("\nStatistical Summary: ")
print(df.describe()) # Summary of numeric columns

# Check the missing values
print("\nMissing Values: ")
print(df.isnull().sum())

# Clean the dataset
# Fill missing 'Age' values with the median
median_age = df["Age"].median()
df["Age"] = df["Age"].fillna(median_age)
#Analyzing the Cabin Column
print("\nCabin Column Analysis:")
print(df["Cabin"].value_counts(dropna=False)) # Include missing values in counts
print("\nPercentage of Missing Values in Cabin:")
print(df["Cabin"].isnull().mean() * 100, "%")
# since the missing data is over 70% its better to drop the column. we'll still extract useful data before dropping it
# Extract deck information
df["Deck"] = df["Cabin"].str[0].fillna("Unknown")
# we will Add a binary feature indicating if the passenger has a cabin
df["Has_Cabin"] = df["Cabin"].notnull().astype(int)
# Now we will Drop the original Cabin column because further details aren't needed
df.drop(columns = ["Cabin"], inplace = True)

#check the dataset now
print("\nUpdated Dataset:")
print(df.head())
#Analyzing the Embarked Column
print("\nEmbarked Column Analysis:")
print(df["Embarked"].value_counts(dropna=False)) # Include missing values in counts
print("\nPercentage of Missing Values in Embarked:")
print(df["Embarked"].isnull().mean() * 100, "%")
# Drop rows with missing 'Embarked' values
df.dropna(subset=["Embarked"], inplace=True)
# now we will rename Columns
df.rename(columns={"Survived": "Has_Survived", "Pclass": "Passenger_Class","SibSp": "Num_Siblings_Spouses", "Parch": "Num_Parents_Childern"},inplace=True)

# View the updated column names
print("\nUpdated Columns:")
print(df.columns)
# we will save cleaned Data for now
output_path = r"E:\Pandas-Practice\outputs\cleaned_data.csv"
df.to_csv(output_path, index=False)
print(f"Cleaned data saved at {output_path}")
# Analysis and Visualization

#Survival rate by passenger class
survival_by_class = df.groupby("Passenger_Class")["Has_Survived"].mean()
print("\nSurvival Rate by Passenger Class:")
print(survival_by_class)

# Survival rate by Gender
survival_by_gender = df.groupby("Sex")["Has_Survived"].mean()
print("\nSurvival Rate by Gender:")
print(survival_by_gender)

# Survival rate by Age Group(you can create age bins if needed)
age_bins = [0,12,20,40,60,100]
age_labels = ['0-12','13-20','21-40','41-60','60+']
df['Age_Group'] = pd.cut(df['Age'], bins=age_bins,labels=age_labels,right=False)
survival_by_age_group = df.groupby("Age_Group",observed = False)["Has_Survived"].mean()
print("\nSurvival Rate by Age Group:")
print(survival_by_age_group)

# Survival by Gender and Age group
survival_by_gender_age = df.groupby(["Sex","Age_Group"],observed = False)["Has_Survived"].mean()
print("\nSurvival Rate by Gender and Age Group:")
print(survival_by_gender_age)

# Names of survivors by Gender
survivors_by_gender = df[df["Has_Survived"] == 1].groupby("Sex")["Name"].apply(list)
print("\nNames of Survivors by Gender:")
print(survivors_by_gender)

# Names of survivors by Age group
survivors_by_age_group = df[df["Has_Survived"] == 1].groupby("Age_Group", observed=False)["Name"].apply(list)
print("\nNames of Survivors by Age Group:")
print(survivors_by_age_group)
#Now we will do some filteration
#Extract young female Passengers
young_female_passengers = df[(df["Age"] < 18) & (df["Sex"] == "female")]
print("\nYoung Female Passengers:")
print(young_female_passengers)

# Save the extracted data into a separate CSV
output_path = r"E:\Pandas-Practice\outputs\young_female_passengers.csv"
young_female_passengers.to_csv(output_path, index=False)

print(f"Young female passengers data saved to {output_path}")

# now we wil add derived columns
# A Family Size Column
df["Family_Size"] = df["Num_Siblings_Spouses"] + df["Num_Parents_Childern"] + 1 # this 1 is the passenger
print("\nAdded Family Size Column:")
print(df[["Family_Size"]].head())
print(df[["Family_Size"]])  # This will print the entire column


# Age distribution
df["Age"].hist(bins=20, edgecolor = "black")
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.savefig(f"{output_folder}/age_distribution.jpg",format='jpg',dpi=300)
plt.show()

# Survival rate by gender
survival_by_gender.plot(kind="bar", color=["pink","blue"] , edgecolor = "black")
plt.title("Survival Rate by Gender")
plt.xlabel("Gender")
plt.ylabel("Survival Rate")

# Adjust the size of the x-axis labels (gender labels)
plt.xticks(fontsize=8)  # You can adjust the value to make it smaller or larger

plt.savefig(f"{output_folder}/survival_rate_by_gender.jpg",format='jpg',dpi=300)
plt.show()

# Counting Age groups
# Count the number of passengers in each age group
age_group_counts = df['Age_Group'].value_counts()
#plotting the Pie Chart
# Plot the pie chart
plt.figure(figsize=(8, 6))

# Use smaller font size and change some visual aspects like colors and explode effect
colors = plt.cm.Paired(range(len(age_group_counts)))  # Set distinct colors for the pie chart
plt.pie(age_group_counts, labels=age_group_counts.index, autopct='%1.1f%%', startangle=90,
        textprops={'fontsize': 10, 'fontweight': 'light'}, colors=colors, explode=[0.1]*len(age_group_counts))

# Title and other settings
plt.title("Distribution of Passengers by Age Group", fontsize=12, fontweight='bold', pad=20)
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

# Show the chart
plt.savefig(f"{output_folder}/distribution_of_passengers_by_age_group.jpg", format='jpg', dpi=300)
plt.show()

#Survival Rate by Passenger Class
survival_by_class.plot(kind="bar", color="green", edgecolor="black")
plt.title("Survival Rate by Passenger Class")
plt.xlabel("Passenger Class")
plt.ylabel("Survival Rate")
plt.savefig(f"{output_folder}/survival_by_class.jpg", format='jpg', dpi=300)
plt.show()

#Survival Rate by Embarked (Port of Embarkation)
survival_by_embarked = df.groupby("Embarked")["Has_Survived"].mean()
survival_by_embarked.plot(kind="bar", color=["lightblue", "lightcoral", "lightgreen"], edgecolor="black")
plt.title("Survival Rate by Embarked")
plt.xlabel("Embarked (Port)")
plt.ylabel("Survival Rate")
plt.savefig(f"{output_folder}/survival_by_embarked.jpg", format='jpg', dpi=300)
plt.show()

#Age vs. Survival
plt.figure(figsize=(8,6))
plt.scatter(df['Age'], df['Has_Survived'], alpha=0.5, c=df['Has_Survived'], cmap='coolwarm', edgecolors='w', s=100)
plt.title("Age vs. Survival")
plt.xlabel("Age")
plt.ylabel("Survived (1 = Yes, 0 = No)")
plt.savefig(f"{output_folder}/age_vs_survival.jpg", format='jpg', dpi=300)
plt.show()

#Fare Distribution
df['Fare'].hist(bins=20, edgecolor="black")
plt.title("Fare Distribution")
plt.xlabel("Fare")
plt.ylabel("Frequency")
plt.savefig(f"{output_folder}/Fare_distribution.jpg", format='jpg', dpi=300)
plt.show()

#Survival Rate by Age Group
survival_by_age_group.plot(kind="bar", color="purple", edgecolor="black")
plt.title("Survival Rate by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Survival Rate")
plt.savefig(f"{output_folder}/survival_rate_by_group.jpg", format='jpg', dpi=300)
plt.show()
