import gzip
import geopandas as gpd
import matplotlib
from pyproj import CRS  # for coordinate reference system handling
# Step 2: Read the .gpkg file using GeoPandas
gdf = gpd.read_file('kontur_population_3km_plz_work.gpkg')
gdf_4326 = gdf.to_crs(epsg=4326)
# Extract the first row's geometry
# first_polygon = gdf_4326.loc[3000, 'geometry']
# first_population = first_polygon_4326 = gdf_4326.loc[300, 'population']
# target_crs = CRS.from_epsg(3857)  # Web Mercator projection (EPSG:3857)
# print(len(gdf_4326))
all_coordinates = []
all_populations = []
# Iterate through each geometry and extract the coordinates
for idx, row in gdf_4326.iterrows():
    polygon_coords = row['geometry'].centroid
    all_coordinates.append(polygon_coords)
    polygon_populations = row['population']
    all_populations.append(polygon_populations)

def get_populations():
    return all_populations

def get_coordinates(): 
    return all_coordinates 