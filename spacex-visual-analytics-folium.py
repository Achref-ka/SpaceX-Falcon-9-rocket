# Launch Sites Locations Analysis with Folium

# The launch success rate may depend on many factors such as payload mass, orbit type, and so on. It may also depend on the location and proximities of a launch site, i.e., 
# the initial position of rocket trajectories. Finding an optimal location for building a launch site certainly involves many factors and hopefully we could discover some of 
# the factors by analyzing the existing launch site locations.

# You will be performing more interactive visual analytics using Folium

# Objectives:
# This lab contains the following tasks:

# TASK 1: Mark all launch sites on a map
# TASK 2: Mark the success/failed launches for each site on the map
# TASK 3: Calculate the distances between a launch site to its proximities
# After completed the above tasks, you should be able to find some geographical patterns about launch sites.  I will see ;)

import folium
import pandas as pd

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

## Task 1: Mark all launch sites on a map

# First, let's try to add each site's location on a map using site's latitude and longitude coordinates
# The following dataset with the name spacex_launch_geo.csv is an augmented dataset with latitude and longitude added for each site.


url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'

spacex_df=pd.read_csv(url)

# Now, you can take a look at what are the coordinates for each site.

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`

spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

print(launch_sites_df)

# Above coordinates are just plain numbers that can not give you any intuitive insights about where are those launch sites. 
# If you are very good at geography, you can interpret those numbers directly in your mind. If not, that's fine too. Let's visualize those locations by pinning them on a map.
# We first need to create a folium Map object, with an initial center location to be NASA Johnson Space Center at Houston, Texas.

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# We could use folium.Circle to add a highlighted circle area with a text label on a specific coordinate. For example,

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

'''
and you should find a small yellow circle near the city of Houston and you can zoom-in to see a larger circle.

Now, let's add a circle for each launch site in data frame launch_sites

TODO: Create and add folium.Circle and folium.Marker for each launch site on the site map

An example of folium.Circle:

folium.Circle(coordinate, radius=1000, color='#000000', fill=True).add_child(folium.Popup(...))

An example of folium.Marker:

folium.map.Marker(coordinate, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'label', ))
'''

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label

# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label

for index, site_info in launch_sites_df.iterrows():
    # Create a Circle for each launch site
    folium.Circle(
        location=[site_info['Lat'], site_info['Long']],
        radius=1000,  # You can adjust the radius as needed
        color='#000000',  # You can change the color as needed
        fill=True,
    ).add_child(folium.Popup(site_info['Launch Site'])).add_to(site_map)

    # Create a Marker for each launch site with a text label
    folium.map.Marker(
        [site_info['Lat'], site_info['Long']],
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % site_info['Launch Site'],
        )
    ).add_to(site_map)

# Now, you can explore the map by zoom-in/out the marked areas , and try to answer the following questions:

# Are all launch sites in proximity to the Equator line? Are all launch sites in very close proximity to the coast?

# Task 2: Mark the success/failed launches for each site on the map
# Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates. 
# Recall that data frame spacex_df has detailed launch records, and the class column indicates if this launch was successful or not

print(spacex_df.tail(10))
# Wyświetl nazwy kolumn w DataFrame
print(spacex_df.columns)

# Next, let's create markers for all launch records. If a launch was successful (class=1), then we use a green marker and if a launch was failed, we use a red marker (class=0)
# Note that a launch only happens in one of the four launch sites, which means many launch records will have the exact same coordinate. 
# Marker clusters can be a good way to simplify a map containing many markers having the same coordinate.
# Let's first create a MarkerCluster object


marker_cluster = MarkerCluster()    # tu stanąłem

# Create a new column in launch_sites dataframe called marker_color to store the marker colors based on the class value

# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
# For each launch result in spacex_df data frame, add a folium.Marker to marker_cluster


# Create a new column in launch_sites dataframe called marker_color to store the marker colors based on the class value
launch_sites_df['marker_color'] = ''

# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
# Funkcja do ustawiania koloru markera na podstawie wartości w kolumnie 'class'
def set_marker_color(row):
    if row['class'] == 1:
        return 'green'
    elif row['class'] == 0:
        return 'red'
    
    

# Apply a function to set marker colors directly in spacex_df
spacex_df['marker_color'] = spacex_df.apply(set_marker_color, axis=1)


# Display the updated spacex_df
print(spacex_df[['Launch Site', 'Lat', 'Long', 'class', 'marker_color']])


# for each row in spacex_df data frame create a Marker object with its coordinate and customize the Marker's icon property to indicate if this launch 
# was successed or failed, e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']

# For each row in spacex_df data frame, create a Marker object with its coordinates
for index, launch_result in spacex_df.iterrows():
    # Customize the Marker's icon property to indicate success or failure
    marker_color = launch_result['marker_color']
    folium.Marker(
        location=[launch_result['Lat'], launch_result['Long']],
        popup=f"Launch Site: {launch_result['Launch Site']}, Class: {launch_result['class']}",
        icon=folium.Icon(color='white', icon_color=marker_color)
    ).add_to(marker_cluster)


# Add the marker_cluster to the site_map
site_map.add_child(marker_cluster)

# From the color-labeled markers in marker clusters, you should be able to easily identify which launch sites have relatively high success rates.


# TASK 3: Calculate the distances between a launch site to its proximities

# Next, we need to explore and analyze the proximities of launch sites.

# Let's first add a MousePosition on the map to get coordinate for a mouse over a point on the map. 
# As such, while you are exploring the map, you can easily find the coordinates of any points of interests (such as railway)



# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)

# Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. 
# Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


# Mark down a point on the closest coastline using MousePosition and calculate the distance between the coastline point and the launch site.

# find coordinate of the closet coastline:  e.g.,: Lat: 28.56367  Lon: -80.57163

# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property: for example

coastline_coordinate = [28.56327, -80.56797]
launch_site_coordinate = [28.562302, -80.577356]

# Calculate the distance between the coastline and the launch site

distance_to_coastline = calculate_distance(launch_site_coordinate[0], launch_site_coordinate[1], coastline_coordinate[0], coastline_coordinate[1])


distance_marker = folium.Marker(
    coastline_coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_to_coastline),
        )
    ).add_to(site_map)



# Draw a PolyLine between a launch site to the selected coastline point

# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate


lines = folium.PolyLine(locations=[launch_site_coordinate, coastline_coordinate], weight=1)
site_map.add_child(lines)



# Save the map to an HTML file
site_map.save("SpaceX_map.html")
