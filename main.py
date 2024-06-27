import pandas as pd
import folium
import numpy as np
import random
import math
from populationDensities import get_coordinates
from populationDensities import get_populations
from shapely.geometry import Point
from folium import Circle
from shapely.geometry import Polygon, MultiPolygon
import csv





def allocate_ev_chargers(hexagons):
    total_population = sum(hexagon[2] for hexagon in hexagons)
    total_chargers_to_add = 40
    chargers_to_add_list = []
    for hexagon in hexagons:
        if total_population < 5:
            chargers_to_add = 0
        else:
            population_ratio = hexagon[2] / total_population
            chargers_to_add = int(total_chargers_to_add * population_ratio)
        chargers_to_add_list.append(chargers_to_add)
    # Adjust to ensure total chargers added equals total_chargers_to_add
    current_total_chargers_added = sum(chargers_to_add_list)
    remaining_chargers_to_add = total_chargers_to_add - current_total_chargers_added
    # Distribute remaining chargers evenly to match the total
    if remaining_chargers_to_add > 0:
        for i in range(remaining_chargers_to_add):
            chargers_to_add_list[i % len(hexagons)] += 1
    return chargers_to_add_list
#Will contain: [(Lat, Long), [list of EV chargers], population]
# modified slightly to account for new DS format
def reward(hex_data):
    return hex_data[2]*(1 - .2*(hex_data[4]))
# listofhexdata is a list of (ppl, chargers, coords of hex center) so [(ppl0, chargers0, hex center0), (ppl1, chargers1, hex center1), etc]
# output is [i0, i1, i2] where i0 = number of chargers to add to hexagon 0
def find_chargers_to_add_forall_hexagons(listofhexdata, k_chargers):
    for z in range (len(listofhexdata)):
        listofhexdata[z].append(len(listofhexdata[z][1]))
    # AllHexData [(l,l), [list of chargers], population, count of chargers]
    memo = [0]*k_chargers
    where_to_add_chargers = [0]*len(listofhexdata) # [[(l,l), [list of chargers], population, count], [etc]]
    for k in range(1, k_chargers):
        maxr = -1
        idx_to_add = -1
        for i in range (len(listofhexdata)):
            if (memo[k] < memo[k-1] + reward(listofhexdata[i])):
                maxr = memo[k-1] + reward(listofhexdata[i])
                idx_to_add = i
        if (maxr == -1): return []
        where_to_add_chargers[idx_to_add] = where_to_add_chargers[idx_to_add] + 1
        listofhexdata[idx_to_add][4] = listofhexdata[idx_to_add][4] + 1
        memo[k] = maxr
    return where_to_add_chargers
# Function that adds new EV charging stations
def add_new_stations(existing_stations, center, num_new_stations, vertices_hex):
    """
    Adds new nodes by reflecting the mean of existing nodes across the center of the hexagon.
    Parameters:
    - existing_stations: List of tuples representing the (latitude, longitude) of existing stations in a specific hexagon.
    - center: Tuple representing the (latitude, longitude) of the center of the hexagon.
    - num_new_stations: Number of new stations to be added.
    Returns:
    - List of tuples representing the (latitude, longitude) of all nodes (existing + new).
    """
    all_stations = existing_stations[:]
    new_stations = []
    verts = vertices_hex
    if(len(existing_stations) == 0):
        new_node = generate_random_point_in_incircle(verts)
        all_stations.append(new_node)
        new_stations.append(new_node)
        num_new_stations = num_new_stations - 1
    for _ in range(num_new_stations):
         # Calculate the mean of the existing nodes
        mean_x = np.mean([node[0] for node in all_stations])
        mean_y = np.mean([node[1] for node in all_stations])
        mean_point = (mean_x, mean_y)
        # Reflect the mean point across the center
        # print(mean_point)
        # print(center)
        new_node = reflect_point_across_center(mean_point, center)
        # print(new_node)
        # Add the new station to the list of stations
        all_stations.append(new_node)
        new_stations.append(new_node)
    return new_stations
# Helper function that reflects a point across the center of the hexagon
def reflect_point_across_center(point, center):
    return [2 * center[0] - point[0], 2 * center[1] - point[1]]
def calculate_incircle(vertices):
    """
    Calculate the incenter and inradius of a hexagon defined by its vertices.
    Parameters:
    - vertices: List of tuples representing the (latitude, longitude) of the hexagon's vertices.
    Returns:
    - incenter: Tuple representing the (latitude, longitude) of the incenter.
    - inradius: Inradius of the hexagon.
    """
    # Extract coordinates
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    # Calculate coordinates of the incenter
    A = sum(x) / len(vertices)
    B = sum(y) / len(vertices)
    # Calculate inradius
    distances = [math.dist((A, B), v) for v in vertices]
    inradius = min(distances)
    return (A, B), inradius
def generate_random_point_in_incircle(vertices):
    """
    Generate a random point within the inscribed circle (incircle) of a hexagon defined by its vertices,
    ensuring that the point is not the center.
    Parameters:
    - vertices: List of tuples representing the (latitude, longitude) of the hexagon's vertices.
    Returns:
    - A tuple representing the (latitude, longitude) of the random coordinate within the incircle.
    """
    # Calculate incenter and inradius
    incenter, inradius = calculate_incircle(vertices)
    while True:
        # Generate a random angle in radians
        angle = random.uniform(0, 2 * math.pi)
        # Generate a random distance from the center (incenter)
        distance = random.uniform(0, inradius)
        # Calculate the random point's coordinates
        x = incenter[0] + distance * math.cos(angle)
        y = incenter[1] + distance * math.sin(angle)
        # Ensure the point is not the center (incenter)
        if (x, y) != incenter:
            return (x, y)






# Function to calculate hexagon vertices
def calculate_hexagon_vertices(center_lat, center_lng, size):
    vertices = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = np.deg2rad(angle_deg)
        vertex_lat = center_lat + size * np.cos(angle_rad)
        vertex_lng = center_lng + size * np.sin(angle_rad)
        vertices.append([vertex_lat, vertex_lng])
    # Close the polygon
    vertices.append(vertices[0])
    return vertices

# Example coordinates of the hexagon center and size
hexagon_size_degrees = 0.038  # Approximately 3 km in degrees (adjust as needed)

# Replace 'Electric and Alternative Fuel Charging Stations.csv' with the actual path to your CSV file
file_path = 'Electric and Alternative Fuel Charging Stations.csv'
df_stations = pd.read_csv(file_path)

############# Identify bounds based on User Input (Bounds of map) #############
map_bounds = {}

with open("map_bounds.csv", mode='r', newline='') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        corner = row['corner']
        latitude = float(row['latitude'])
        longitude = float(row['longitude'])
        map_bounds[corner] = [latitude, longitude]
###########################

elec_data = df_stations[
    (df_stations["Latitude"] >= map_bounds["southEast"][0]) &
    (df_stations["Latitude"] <= map_bounds["northEast"][0]) &
    (df_stations["Longitude"] >= map_bounds["northWest"][1]) &
    (df_stations["Longitude"] <= map_bounds["northEast"][1]) &
    (df_stations['Fuel Type Code'] == 'ELEC')
]
# Select only 'Latitude' and 'Longitude' columns
elec_coordinates = elec_data[['Latitude', 'Longitude']]

# Create a map centered around User specified location
local_map = folium.Map(location=[(map_bounds["northEast"][0]+map_bounds["southWest"][0])/2, (map_bounds["northWest"][1]+map_bounds["northEast"][1])/2])
curEVLocations = []

for index, row in elec_data.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Station Name'], icon=folium.Icon(color='red')).add_to(local_map)
    curEVLocations.append((row['Latitude'], row['Longitude']))

# Print the DataFrame to verify
# print(df.head())

def is_within_bounds(lat, lng):
    return map_bounds["southEast"][0] <= lat <= map_bounds["northEast"][0] and map_bounds["northWest"][1] <= lng <= map_bounds["northEast"][1]


max_density = 500000
min_density = 0
curCord = get_coordinates()
curDens = get_populations()
print(len(curCord))
AllHexData = [] #Will contain: [(Lat, Long), [list of EV chargers], population, [6 verts tuples]]
# print(curCord)
# Add markers for valid coordinates
for index in range(len(curCord)):
    # print(curCord[index])
    curHex = Point(curCord[index][7])
    lat = curHex.y
    lng = curHex.x
    density = curDens[index]
    if is_within_bounds(lat, lng):
        # print("Lat: " + str(lat) + " Lang: " + str(lng))
        # folium.Marker([lat, lng], icon=folium.Icon(color='blue'), popup=curDens[index]).add_to(chicago_map)
        # Add circle with radius 3km (3000 meters)
        # Normalize density to a range between 0 and 1
        normalized_density = (density - min_density) / (max_density - min_density)
        # hexagon_vertices = calculate_hexagon_vertices(lat, lng, hexagon_size_degrees)
        # Swap (latitude, longitude) to (longitude, latitude)
        curCord_swapped = [(lng, lat) for (lat, lng) in curCord[index][0:6]]
        currentBoundary = Polygon(curCord_swapped)
        currentHex = []
        EVsinBoundary = []
        for allEVs in curEVLocations:
            if currentBoundary.contains(Point(allEVs)):
                EVsinBoundary.append(allEVs)
        currentHex.append((lat,lng))
        currentHex.append(EVsinBoundary)
        currentHex.append(density)
        currentHex.append(curCord_swapped)
        AllHexData.append(currentHex)
        # print(currentHex)
        hexagon_vertices = curCord_swapped
        # Scale radius based on normalized density (adjust this factor as needed)
        # radius = 3464
        # Determine color based on normalized density
        color = '#%02x%02x%02x' % (int(255 * (1 - normalized_density)), int(255 * normalized_density), 0)
        # Add circle marker with shaded color and radius
        # Circle(
        #     location=[lat, lng],
        #     radius=radius,
        #     color=color,
        #     fill=True,
        #     fill_color=color,
        #     fill_opacity=0.7,
        #     popup=f'Population Density: {density}'
        # ).add_to(chicago_map)
            # Draw the hexagon polygon on the map
        folium.Polygon(
            locations=hexagon_vertices,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f'Population Density: {density}'
        ).add_to(local_map)
numberAdded = allocate_ev_chargers(AllHexData)
print(numberAdded)
outputs = []
start = 0
for hex in AllHexData:
    outputs.append(add_new_stations(hex[1], hex[0], numberAdded[start], hex[3]))
    start+=1
print(outputs)
for points in outputs:
    for point in points:
        folium.Marker(
            location=point,
            icon=folium.Icon(color='purple'),
            popup=f'New Location: {point}'  # Optional popup with location info
        ).add_to(local_map)
# print(AllHexData)
# bob = find_chargers_to_add_forall_hexagons(AllHexData, 40)
# print(bob)
# Save the map as an HTML file
local_map.save('chicago_map.html')
