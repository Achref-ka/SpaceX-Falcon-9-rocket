# Objectives¶

# In this lab, you will make a get request to the SpaceX API. You will also do some basic data wrangling and formating.
# Request to the SpaceX API
# Clean the requested data

# Import Libraries and Define Auxiliary Functions

# Requests allows us to make HTTP requests which we will use to get data from an API
import requests
# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Datetime is a library that allows us to represent dates
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)

# Below we will define a series of helper functions that will help us use the API to extract information using identification numbers in the launch data.
# From the rocket column we would like to learn the booster name.

# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
       if x:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])


# From the launchpad we would like to know the name of the launch site being used, the logitude, and the latitude.

# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
       if x:
         response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
         Longitude.append(response['longitude'])
         Latitude.append(response['latitude'])
         LaunchSite.append(response['name'])



# From the payload we would like to learn the mass of the payload and the orbit that it is going to.

# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    for load in data['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])
        

# From cores we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, wheter the core is reused, 
# wheter legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, 
# and the serial of the core.

# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])


# Now let's start requesting rocket launch data from SpaceX API with the following URL:

spacex_url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)


# Check the content of the response

# print(response.content)  #    ;)

# You should see the response contains massive information about SpaceX launches. Next, let's try to discover some more relevant information for this project.

# Task 1: Request and parse the SpaceX launch data using the GET request
# To make the requested JSON results more consistent, we will use the following static response object for this project:

static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'

# We should see that the request was successfull with the 200 status response code

print(response.status_code)  # if 200 then :)

# Now we decode the response content as a Json using .json() and turn it into a Pandas dataframe using .json_normalize()

# Use json_normalize method to convert the JSON result into a dataframe
data = response.json()

# If you're using the static JSON URL, you can use the following line instead:
# data = requests.get(static_json_url).json()

# Check the type of data
print(type(data))  # Make sure data is a dictionary or a suitable type

# Normalize the JSON data into a flat table
df = pd.json_normalize(data)
print()
print(type(data))  # Make sure data is a dictionary or a suitable type
print()


# Display the first few rows of the dataframe
# print(df.head(4))

# You will notice that a lot of the data are IDs. For example the rocket column has no information about the rocket just an identification number.
# We will now use the API again to get information about the launches using the IDs given for each launch. Specifically we will be using columns rocket, payloads, launchpad, and cores.
print(df.columns)

# Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
data = df[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]





# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]

# From the rocket we would like to learn the booster name
# From the payload we would like to learn the mass of the payload and the orbit that it is going to
# From the launchpad we would like to know the name of the launch site being used, the longitude, and the latitude.
# From cores we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, 
# whether gridfins were used, whether the core is reused, whether legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, 
# the number of times this specific core has been reused, and the serial of the core.

# The data from these requests will be stored in lists and will be used to create a new dataframe.

#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# These functions will apply the outputs globally to the above variables. Let's take a looks at BoosterVersion variable. Before we apply getBoosterVersion the list is empty:
print("Booster Version: ", BoosterVersion)

# Now, let's apply  getBoosterVersion function method to get the booster version

# Call getBoosterVersion
getBoosterVersion(data)

# The list has now been update
print(BoosterVersion[0:5])

# We can apply the rest of the functions here:

# Call getLaunchSite
getLaunchSite(data)

# Call getPayloadData
getPayloadData(data)

# Call getCoreData
getCoreData(data)


# Finally lets construct our dataset using the data we have obtained. We we combine the columns into a dictionary.

launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}


# Then, we need to create a Pandas data frame from the dictionary launch_dict.

df_final = pd.DataFrame(launch_dict)



print(df_final.head(5))


# Task 2: Filter the dataframe to only include Falcon 9 launches
# Finally we will remove the Falcon 1 launches keeping only the Falcon 9 launches. 
# Filter the data dataframe using the BoosterVersion column to only keep the Falcon 9 launches. Save the filtered data to a new dataframe called data_falcon9.


# data_falcon9 = data[data['BoosterVersion'] == 'Falcon9']

# data['BoosterVersion']!='Falcon 1'


# Filtruj DataFrame, aby uzyskać tylko loty z rakietą Falcon 9

# data_falcon9 = df_final[data['BoosterVersion'] != 'Falcon 1']
data_falcon9 = df_final[df_final['BoosterVersion'] == 'Falcon 9']


# Now that we have removed some values we should reset the FlgihtNumber column

data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))

# Display the Falcon 9 launches DataFrame
print(data_falcon9.head(4))

# Data Wrangling
# We can see below that some of the rows are missing values in our dataset.

print(data_falcon9.isnull().sum())

# Before we can continue we must deal with these missing values. The LandingPad column will retain None values to represent when landing pads were not used.

# Task 3: Dealing with Missing Values
# Calculate below the mean for the PayloadMass using the .mean(). 
# Then use the mean and the .replace() function to replace np.nan values in the data with the mean you calculated.


# Calculate the mean for PayloadMass
mean_payload_mass = data_falcon9['PayloadMass'].mean()

# Replace NaN values with the mean
data_falcon9['PayloadMass'].replace(np.nan, mean_payload_mass, inplace=True)

# Check if there are any remaining missing values
print(data_falcon9.isnull().sum())

# You should see the number of missing values of the PayLoadMass change to zero.
# Now we should have no missing values in our dataset except for in LandingPad.
# We can now export it to a CSV for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.

data_falcon9.to_csv(dataset_part_1.csv', index=False)
