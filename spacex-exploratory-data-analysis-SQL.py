# Using this Python notebook you will:

# Understand the Spacex DataSet
# Load the dataset into the corresponding table in a Db2 database
# Execute SQL queries to answer assignment questions

# Let us first load the SQL extension and establish a connection with the database

import csv, sqlite3
import pandas as pd

con = sqlite3.connect("my_data1.db")
cur = con.cursor()

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

# This below code is added to remove blank rows from table
# %sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null

# Tasks:
# Now write and execute SQL queries to solve the assignment tasks.

# Note: If the column names are in mixed case enclose it in double quotes For Example "Landing_Outcome"



# Task 1 - Display the names of the unique launch sites in the space mission

# SQL query to get the names of unique launch sites
query = "SELECT DISTINCT \"Launch_Site\" FROM SPACEXTBL;"

# Execute the query
cur.execute(query)

# Fetch all the results
results = cur.fetchall()

# Display the results
for result in results:
    print(result[0])



# Task 2 - Display 5 records where launch sites begin with the string 'CCA'

# SQL query to get 5 records where launch sites begin with 'CCA'
query = "SELECT * FROM SPACEXTBL WHERE \"Launch_Site\" LIKE 'CCA%' LIMIT 5;"

# Execute the query
cur.execute(query)

# Fetch all the results
results = cur.fetchall()

# Display the results
for result in results:
    print(result)


# Task 3 - Display the total payload mass carried by boosters launched by NASA (CRS)

# SQL query to get the total payload mass for NASA (CRS) launches
query = "SELECT SUM(\"PAYLOAD_MASS__KG_\") as total_payload_mass FROM SPACEXTBL WHERE \"Customer\" = 'NASA (CRS)';"

# Execute the query
cur.execute(query)

# Fetch the result
result = cur.fetchone()

# Display the total payload mass
print("Total Payload Mass for NASA (CRS) launches:", result[0])



# Task 4 - Display average payload mass carried by booster version F9 v1.1

# SQL query to get the average payload mass for booster version F9 v1.1
query = "SELECT AVG(\"PAYLOAD_MASS__KG_\") as average_payload_mass FROM SPACEXTBL WHERE \"Booster_Version\" = 'F9 v1.1';"

# Execute the query
cur.execute(query)

# Fetch the result
result = cur.fetchone()

# Display the average payload mass
print("Average Payload Mass for booster version F9 v1.1:", result[0])



# Task 5 - List the date when the first succesful landing outcome in ground pad was acheived. Use min function

# SQL query to get the date of the first successful landing on a ground pad
query = "SELECT MIN(\"Date\") as first_successful_landing_date FROM SPACEXTBL WHERE \"Landing_Outcome\" = 'Success' AND \"Launch_Site\" IS NOT NULL;"

# Execute the query
cur.execute(query)

# Fetch the result
result = cur.fetchone()

# Display the date of the first successful landing on a ground pad
print("Date of the first successful landing on a ground pad:", result[0])


# Task 6 - List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000

# SQL query to get the names of boosters meeting the specified conditions
query = """
    SELECT "Booster_Version"
    FROM SPACEXTBL
    WHERE "Landing_Outcome" = 'Success (drone ship)'
      AND "PAYLOAD_MASS__KG_" > 4000
      AND "PAYLOAD_MASS__KG_" < 6000;
"""

# Execute the query
cur.execute(query)

# Fetch all the results
results = cur.fetchall()

# Display the names of the boosters
for result in results:
    print(result[0])


# Task 7 - List the total number of successful and failure mission outcomes

# SQL query to get the total number of successful and failure mission outcomes
query = """
    SELECT "Mission_Outcome", COUNT(*) as num_outcomes
    FROM SPACEXTBL
    WHERE "Mission_Outcome" LIKE '%Success%'
       OR "Mission_Outcome" LIKE '%Failure%'
    GROUP BY "Mission_Outcome";
"""


# Execute the query
cur.execute(query)

# Fetch all the results
results = cur.fetchall()

# Display the total number of successful and failure mission outcomes
for result in results:
    print(f"{result[0]}: {result[1]}")


# Task 8 - List the names of the booster_versions which have carried the maximum payload mass. Use a subquery

# SQL query to get the names of booster_versions with the maximum payload mass
query = """
    SELECT "Booster_Version"
    FROM SPACEXTBL
    WHERE "PAYLOAD_MASS__KG_" = (
        SELECT MAX("PAYLOAD_MASS__KG_")
        FROM SPACEXTBL
    );
"""

# Execute the query
cur.execute(query)

# Fetch all the results
results = cur.fetchall()

# Display the names of booster_versions with the maximum payload mass
for result in results:
    print(result[0])


# Task 9 - List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.
# Note: SQLLite does not support monthnames. So you need to use substr(Date, 6,2) as month to get the months and substr(Date,0,5)='2015' for year.


# SQL query to get records for the specified conditions
query = """
    SELECT
        substr("Date", 6, 2) as month,
        "Landing_Outcome",
        "Booster_Version",
        "Launch_Site"
    FROM SPACEXTBL
    WHERE substr("Date", 0, 5) = '2015'
        AND "Landing_Outcome" = 'Failure (drone ship)';
"""

# Execute the query
cur.execute(query)

# Fetch all the results
results = cur.fetchall()

# Display the records
for result in results:
    print(result)



# Task 10 - Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.

# SQL query to rank landing outcomes between specific dates
query = """
    SELECT
        "Landing_Outcome",
        COUNT(*) as num_outcomes
    FROM SPACEXTBL
    WHERE "Date" BETWEEN '2010-06-04' AND '2017-03-20'
    GROUP BY "Landing_Outcome"
    ORDER BY num_outcomes DESC;
"""

# Execute the query
cur.execute(query)

# Fetch all the results
results = cur.fetchall()

# Display the ranked landing outcomes
print()
for result in results:
    print(f"{result[0]}: {result[1]}")










# Close the connection
con.close()