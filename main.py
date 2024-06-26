import pandas as pd
import folium 
from populationDensities import get_coordinates
from populationDensities import get_populations 

# Replace 'Electric and Alternative Fuel Charging Stations.csv' with the actual path to your CSV file
file_path = 'Electric and Alternative Fuel Charging Stations.csv'
df_stations = pd.read_csv(file_path)

chicago_elec_data = df_stations[(df_stations['City'] == 'Chicago') & (df_stations['Fuel Type Code'] == 'ELEC')]
# Select only 'Latitude' and 'Longitude' columns
chicago_coordinates = chicago_elec_data[['Latitude', 'Longitude']]

# Create a map centered around Chicago
chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=12)

for index, row in chicago_elec_data.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Station Name'], icon=folium.Icon(color='red')).add_to(chicago_map)

# Print the DataFrame to verify
# print(df.head())

def is_within_chicago(lat, lng):
    return 40 <= lat <= 42 and -88.0 <= lng <= -86

curCord = get_coordinates()
print(len(curCord))

# print(curCord)

# Add markers for valid coordinates
for index in range(len(curCord)):
    lat = curCord[index].y
    lng = curCord[index].x
    if is_within_chicago(lat, lng):
        print("Lat: " + str(lat) + " Lang: " + str(lng))
        folium.Marker([lat, lng], icon=folium.Icon(color='blue')).add_to(chicago_map)

# Save the map as an HTML file
chicago_map.save('chicago_map.html')
