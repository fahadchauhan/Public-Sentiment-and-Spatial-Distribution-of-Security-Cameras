import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Load the district GeoPackage file
districts_gdf = gpd.read_file("C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/geopackage/major_district_suurpiirit_WFS.gpkg")
print("Districts CRS:", districts_gdf.crs)

# Load the camera data CSV
camera_data = pd.read_csv('C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/signals_image_metadata_filtered.csv')

# Convert camera data to a GeoDataFrame
camera_points = [Point(xy) for xy in zip(camera_data['longitude'], camera_data['latitude'])]
camera_gdf = gpd.GeoDataFrame(camera_data, geometry=camera_points)

# Print the default CRS of the camera GeoDataFrame (if any)
print("Camera GeoDataFrame default CRS (before setting):", camera_gdf.crs)

# Set the CRS of the camera GeoDataFrame to match the districts GeoDataFrame, if needed
camera_gdf = camera_gdf.set_crs(districts_gdf.crs, allow_override=True)

# Now print the CRS again to verify they match
print("Camera CRS after setting:", camera_gdf.crs)
print("Districts CRS after setting:", districts_gdf.crs)