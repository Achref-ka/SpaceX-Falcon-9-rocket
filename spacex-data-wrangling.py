# Space X Falcon 9 First Stage Landing Prediction

#In this lab, we will perform some Exploratory Data Analysis (EDA) to find some patterns in the data and determine what would be the label for training supervised models.

'''
In the data set, there are several different cases where the booster did not land successfully. 
Sometimes a landing was attempted but failed due to an accident; for example, True Ocean means the mission outcome was successfully landed 
to a specific region of the ocean while False Ocean means the mission outcome was unsuccessfully landed to a specific region of the ocean. 
True RTLS means the mission outcome was successfully landed to a ground pad False RTLS means the mission outcome was unsuccessfully landed to a ground pad.
True ASDS means the mission outcome was successfully landed on a drone ship False ASDS means the mission outcome was unsuccessfully landed on a drone ship.

In this lab we will mainly convert those outcomes into Training Labels with 1 means the booster successfully landed 0 means it was unsuccessful.

Objectives
Perform exploratory Data Analysis and determine Training Labels

Exploratory Data Analysis
Determine Training Labels
'''

# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, 
# along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

# Data Analysis - Load Space X dataset, from last section

df=pd.read_csv("c://kodilla/Data_Science/Data_Vizualization/dataset_part_1.csv")
print(df.head(10))

# Identify and calculate the percentage of the missing values in each attribute

print(df.isnull().sum()/len(df)*100)

# Identify which columns are numerical and categorical:

print(df.dtypes)

# TASK 1: Calculate the number of launches on each site
# The data contains several Space X launch facilities: Cape Canaveral Space Launch Complex 40 VAFB SLC 4E , Vandenberg Air Force Base Space Launch Complex 4E (SLC-4E), 
# Kennedy Space Center Launch Complex 39A KSC LC 39A .The location of each Launch Is placed in the column LaunchSite
# Next, let's see the number of launches for each site.
# Use the method value_counts() on the column LaunchSite to determine the number of launches on each site:

launch_counts = df['LaunchSite'].value_counts()
print(launch_counts)

# TASK 2: Calculate the number and occurrence of each orbit

# Use the method .value_counts() to determine the number and occurrence of each orbit in the column Orbit

orbit_counts = df['Orbit'].value_counts()
print(orbit_counts)

#TASK 3: Calculate the number and occurence of mission outcome of the orbits

# Use the method .value_counts() on the column Outcome to determine the number of landing_outcomes.Then assign it to a variable landing_outcomes.


landing_outcomes = df['Outcome'].value_counts()
print(landing_outcomes)

for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)
    
# We create a set of outcomes where the second stage did not land successfully:

bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
print()
print(bad_outcomes)
print()

# TASK 4: Create a landing outcome label from Outcome column
# Using the Outcome, create a list where the element is zero if the corresponding row in Outcome is in the set bad_outcome; otherwise, it's one. 
# Then assign it to the variable landing_class:


bad_outcomes = {'False ASDS', 'False Ocean', 'False RTLS'}

# Create a landing_class label
df['landing_class'] = df['Outcome'].apply(lambda x: 0 if x in bad_outcomes else 1)

# Display the updated DataFrame
print(df[['Outcome', 'landing_class']])


# This variable will represent the classification variable that represents the outcome of each launch. 
# If the value is zero, the first stage did not land successfully; one means the first stage landed Successfully

df['Class'] = df['landing_class']
df[['Class']].head(8)
print()
print(df.head(5))
# We can use the following line of code to determine the success rate:
print()
print(df["Class"].mean())

# We can now export it to a CSV for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.


df.to_csv("dataset_part_2.csv", index=False)
