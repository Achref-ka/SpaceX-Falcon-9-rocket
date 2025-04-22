# SpaceX Falcon 9 Data Vizualization 

# Objectives:
# Perform exploratory Data Analysis and Feature Engineering using Pandas and Matplotlib
# Exploratory Data Analysis
# Preparing Data Feature Engineering


import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

# First, let's read the SpaceX dataset into a Pandas dataframe and print its summary



file_path = "dataset_part_2.csv"

df=pd.read_csv(file_path)
print(df.head(5))

# First, let's try to see how the FlightNumber (indicating the continuous launch attempts.) and Payload variables would affect the launch outcome.

# We can plot out the FlightNumber vs. PayloadMassand overlay the outcome of the launch. We see that as the flight number increases, the first stage is more likely to land successfully. 
# The payload mass is also important; it seems the more massive the payload, the less likely the first stage will return.

sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 4)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()


# We see that different launch sites have different success rates. CCAFS LC-40, has a success rate of 60 %, while KSC LC-39A and VAFB SLC 4E has a success rate of 77%. ????

# Next, let's drill down to each site visualize its detailed launch records.

# TASK 1: Visualize the relationship between Flight Number and Launch Site

# Use the function catplot to plot FlightNumber vs LaunchSite, set the parameter x parameter to FlightNumber,set the y to Launch Site and set the parameter hue to 'class'

# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value


sns.catplot(x="FlightNumber", y="LaunchSite", hue="Class", data=df, aspect=4, kind="swarm")
plt.xlabel("FlightNumber", fontsize=20)
plt.ylabel("LaunchSite", fontsize=20)
plt.show()

# Now try to explain the patterns you found in the Flight Number vs. Launch Site scatter point plots.

### TASK 2: Visualize the relationship between Payload and Launch Site

# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value

sns.catplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df, aspect=4, kind="swarm")
plt.xlabel("PayloadMass", fontsize=20)
plt.ylabel("LaunchSite", fontsize=20)
plt.show()

# Now if you observe Payload Vs. Launch Site scatter point chart you will find for the VAFB-SLC launchsite there are no rockets launched for heavypayload mass(greater than 10000).

# TASK  3: Visualize the relationship between success rate of each orbit type

# Next, we want to visually check if there are any relationship between success rate and orbit type.

# Let's create a bar chart for the sucess rate of each orbit

# Next, we want to visually check if there are any relationship between success rate and orbit type.

# Let's create a bar chart for the sucess rate of each orbit

# Group the data by Orbit and calculate the success rate for each orbit
orbit_success_rate = df.groupby('Orbit')['Class'].mean().reset_index()

# Plot a bar chart for the success rate of each orbit
plt.figure(figsize=(10, 6))
sns.barplot(x='Orbit', y='Class', data=orbit_success_rate, palette='viridis')
plt.xlabel('Orbit Type', fontsize=15)
plt.ylabel('Success Rate', fontsize=15)
plt.title('Success Rate of Each Orbit Type', fontsize=20)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.show()

# Analyze the ploted bar chart try to find which orbits have high sucess rate.

# TASK  4: Visualize the relationship between FlightNumber and Orbit type

# For each orbit, we want to see if there is any relationship between FlightNumber and Orbit type.

# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit, and hue to be the class value
# You should see that in the LEO orbit the Success appears related to the number of flights; on the other hand, there seems to be no relationship between flight number when in GTO orbit.

# Plot a scatter point chart with x-axis as FlightNumber, y-axis as Orbit, and hue as the class value
plt.figure(figsize=(12, 8))
sns.scatterplot(x='FlightNumber', y='Orbit', hue='Class', data=df, palette='viridis')
plt.xlabel('Flight Number', fontsize=15)
plt.ylabel('Orbit Type', fontsize=15)
plt.title('Relationship between Flight Number and Orbit Type', fontsize=20)
plt.show()


# TASK  5: Visualize the relationship between Payload and Orbit type

# Similarly, we can plot the Payload vs. Orbit scatter point charts to reveal the relationship between Payload and Orbit type

# Plot a scatter point chart with x axis to be Payload and y axis to be the Orbit, and hue to be the class value

plt.figure(figsize=(12, 8))
sns.scatterplot(x='PayloadMass', y='Orbit', hue='Class', data=df, palette='viridis')
plt.xlabel('Payload Mass (kg)', fontsize=15)
plt.ylabel('Orbit Type', fontsize=15)
plt.title('Relationship between Payload Mass and Orbit Type', fontsize=20)
plt.show()

# With heavy payloads the successful landing or positive landing rate are more for Polar,LEO and ISS.
# However for GTO we cannot distinguish this well as both positive landing rate and negative landing(unsuccessful mission) are both there here.


# TASK  6: Visualize the launch success yearly trend

# You can plot a line chart with x axis to be Year and y axis to be average success rate, to get the average launch success trend.

# The function will help you get the year from the date:

# A function to Extract years from the date 

    
# Plot a line chart with x axis to be the extracted year and y axis to be the success rate


# Function to Extract years from the date
def extract_year(date):
    return date.split("-")[0]

df['Year'] = df['Date'].apply(extract_year)

# Plot a line chart with x-axis as the extracted year and y-axis as the average success rate
plt.figure(figsize=(12, 8))
sns.lineplot(x='Year', y='Class', data=df, estimator='mean', ci=None, marker='o', color='b')
plt.xlabel('Year', fontsize=15)
plt.ylabel('Average Success Rate', fontsize=15)
plt.title('Launch Success Yearly Trend', fontsize=20)
plt.show()

# you can observe that the sucess rate since 2013 kept increasing till 2020

# By now, you should obtain some preliminary insights about how each important variable would affect the success rate, 
# we will select the features that will be used in success prediction in the future module.


features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
print(features.head(4))

# TASK  7: Create dummy variables to categorical columns

# Use the function get_dummies and features dataframe to apply OneHotEncoder to the column Orbits, LaunchSite, LandingPad, and Serial. 
# Assign the value to the variable features_one_hot, display the results using the method head. Your result dataframe must include all features including the encoded ones.

# HINT: Use get_dummies() function on the categorical columns

# Create dummy variables for categorical columns
features_one_hot = pd.get_dummies(df[['Orbit', 'LaunchSite', 'LandingPad', 'Serial']])

# Concatenate the dummy variables with the original DataFrame
df_encoded = pd.concat([df, features_one_hot], axis=1)

# Display the results
print(df_encoded.head())

# TASK  8: Cast all numeric columns to `float64`

# Cast all numeric columns to float64
numeric_columns = df_encoded.select_dtypes(include=['float64', 'int64']).columns
df_encoded[numeric_columns] = df_encoded[numeric_columns].astype('float64')

# Display the results
print(df_encoded.head())


# Now that our features_one_hot dataframe only contains numbers cast the entire dataframe to variable type float64

# HINT: use astype function
# We can now export it to a CSV for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.



# Convert 'Date' column to datetime type
df_encoded['Date'] = pd.to_datetime(df_encoded['Date'])



# Identify non-numeric columns
non_numeric_columns = df_encoded.select_dtypes(exclude=['float64']).columns

# Exclude non-numeric columns from casting
df_encoded[df_encoded.columns.difference(non_numeric_columns)] = df_encoded[df_encoded.columns.difference(non_numeric_columns)].astype('float64')

# Display the results
print(df_encoded.head())


df_encoded.to_csv("c://kodilla/Data_Science/Data_Vizualization/dataset_part_3.csv", index=False)