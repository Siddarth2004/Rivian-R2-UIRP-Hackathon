import gzip
import geopandas as gpd
import matplotlib
from shapely.geometry import Polygon, MultiPolygon
from shapely.geometry import Point
from pyproj import CRS  # for coordinate reference system handling
# Step 2: Read the .gpkg file using GeoPandas
gdf = gpd.read_file('3km_world.gpkg')
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
    poly_arr = []
    if isinstance(row['geometry'], Polygon):
        poly_arr = [coord for coord in row['geometry'].exterior.coords]
    elif isinstance(row['geometry'], MultiPolygon):
        for polygon in row['geometry'].geoms:
            poly_arr.extend([coord for coord in polygon.exterior.coords])
    # polygon_coords = row['geometry'].exterior.coords
    polygon_coords = row['geometry'].centroid
    poly_arr.append(polygon_coords)
    all_coordinates.append(poly_arr)
    polygon_populations = row['population']
    all_populations.append(polygon_populations)
def get_populations():
    return all_populations
def get_coordinates():
    return all_coordinates
