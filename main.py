import pandas as pd
import folium 
import numpy as np
from populationDensities import get_coordinates
from populationDensities import get_populations 
from shapely.geometry import Point
from folium import Circle
from shapely.geometry import Polygon, MultiPolygon

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

chicago_elec_data = df_stations[(df_stations['City'] == 'Chicago') & (df_stations['Fuel Type Code'] == 'ELEC')]
# Select only 'Latitude' and 'Longitude' columns
chicago_coordinates = chicago_elec_data[['Latitude', 'Longitude']]

# Create a map centered around Chicago
chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=12)
curEVLocations = []

for index, row in chicago_elec_data.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Station Name'], icon=folium.Icon(color='red')).add_to(chicago_map)
    curEVLocations.append((row['Latitude'], row['Longitude']))

# Print the DataFrame to verify
# print(df.head())

def is_within_chicago(lat, lng):
    return 41.6 <= lat <= 42.1 and -87.9 <= lng <= -87.5

max_density = 500000
min_density = 0

curCord = get_coordinates()
curDens = get_populations()
print(len(curCord))

AllHexData = [] #Will contain: [(Lat, Long), [list of EV chargers], population]

# print(curCord)

# Add markers for valid coordinates
for index in range(len(curCord)):
    # print(curCord[index])
    curHex = Point(curCord[index][7])
    lat = curHex.y
    lng = curHex.x
    density = curDens[index]
    if is_within_chicago(lat, lng):
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
        ).add_to(chicago_map)

# print(AllHexData)

# Save the map as an HTML file
chicago_map.save('chicago_map.html')
