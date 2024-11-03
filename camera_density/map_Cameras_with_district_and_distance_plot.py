import folium
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Function to check and adjust for duplicate coordinates with small epsilon adjustments
def adjust_duplicate_coordinates(data, lat_col, lon_col, epsilon=0.00001):
    seen_coordinates = set()  # Track unique coordinates

    for idx, row in data.iterrows():
        lat, lon = row[lat_col], row[lon_col]
        
        # Adjust coordinates if they already exist in seen_coordinates
        while (lat, lon) in seen_coordinates:
            lat += epsilon
            lon += epsilon
            
        # Update the DataFrame with the adjusted coordinates
        data.at[idx, lat_col] = lat
        data.at[idx, lon_col] = lon
        
        # Add the adjusted coordinates to the seen set
        seen_coordinates.add((lat, lon))

# Helper function for spatial join to count cameras in each district
def calculate_camera_counts(district_gdf, id_column):
    districts_with_camera_counts = gpd.sjoin(district_gdf, camera_gdf, how="left", predicate="contains")
    districts_with_camera_counts = districts_with_camera_counts[districts_with_camera_counts['camera_present'] == True]
    camera_counts = districts_with_camera_counts.groupby(id_column).size().reset_index(name='camera_count')
    district_gdf = district_gdf.merge(camera_counts, on=id_column, how='left')
    district_gdf['camera_count'] = district_gdf['camera_count'].fillna(0).astype(int)
    return district_gdf

# Paths to your data files
camera_csv_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/signals_image_metadata_filtered.csv'
major_districts_gpkg_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/geopackage/major_district_suurpiirit_WFS.gpkg'
districts_gpkg_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/geopackage/district_peruspiiri_WFS.gpkg'
sub_districts_gpkg_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/geopackage/sub_small_district_pienalueet_WFS.gpkg'

colors = {'Major District': 'blue', 'District': 'green', 'Small-District': 'orange'}
# Load camera data
camera_data = pd.read_csv(camera_csv_path)
camera_data = camera_data[camera_data['camera_present'] == True].reset_index(drop=True)
camera_data['latitude'] = camera_data['latitude'].astype(float)
camera_data['longitude'] = camera_data['longitude'].astype(float)

# Adjust any duplicate coordinates in the camera data
adjust_duplicate_coordinates(camera_data, 'latitude', 'longitude')

# Convert camera data to a GeoDataFrame
camera_gdf = gpd.GeoDataFrame(
    camera_data,
    geometry=gpd.points_from_xy(camera_data.longitude, camera_data.latitude),
    crs="EPSG:4326"
)

# Load district data and convert CRS if needed
major_districts_gdf = gpd.read_file(major_districts_gpkg_path)
districts_gdf = gpd.read_file(districts_gpkg_path)
sub_districts_gdf = gpd.read_file(sub_districts_gpkg_path)

major_districts_gdf['major_district'] = major_districts_gdf['tunnus'].astype(str) + ": " + major_districts_gdf['nimi_fi']

districts_gdf['district'] = districts_gdf['tunnus'].astype(str) + ": " + districts_gdf['nimi_fi']

sub_districts_gdf['major_district'] = sub_districts_gdf['suurpiiri_tunnus'].astype(str) + ": " + sub_districts_gdf['suurpiiri_nimi_fi']
sub_districts_gdf['district'] = sub_districts_gdf['peruspiiri_tunnus'].astype(str) + ": " + sub_districts_gdf['peruspiiri_nimi_fi']
sub_districts_gdf['sub_district'] = sub_districts_gdf['osaalue_tunnus'].astype(str) + ": " + sub_districts_gdf['osaalue_nimi_fi']

for gdf in [major_districts_gdf, districts_gdf, sub_districts_gdf]:
    if gdf.crs != camera_gdf.crs:
        gdf.to_crs(camera_gdf.crs, inplace=True)

# Create each map with specific configurations

# 1. Map with Major Districts and Camera Counts
major_districts_gdf = calculate_camera_counts(major_districts_gdf, 'id')
map_major = folium.Map(location=[camera_gdf['latitude'].mean(), camera_gdf['longitude'].mean()], zoom_start=12)

folium.GeoJson(
    major_districts_gdf,
    style_function= lambda x: {
                        'fillColor': 'gray',
                        'color': colors['Major District'],
                        'weight': 1,
                        'fillOpacity': 0.5
                    },
    highlight_function= lambda x: {
                        'fillColor': colors['Major District'],
                        'color': colors['Major District'],
                        'weight': 1,
                        'fillOpacity': 0.3
                    },
    tooltip=folium.GeoJsonTooltip(fields=['major_district', 'camera_count'], aliases=['Major-District', 'Number of Cameras'])
).add_to(map_major)
for _, row in camera_gdf.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Camera at (lat:{row['latitude']}, lon:{row['longitude']})<br>Heading: {row['heading']}",
        icon=folium.Icon(color="red", icon="camera")
    ).add_to(map_major)
map_major.save("C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/helsinki_major_districts_with_cameras.html")

# 2. Map with District Boundaries and Camera Counts at District Level
districts_gdf = calculate_camera_counts(districts_gdf, 'id')
map_sub = folium.Map(location=[camera_gdf['latitude'].mean(), camera_gdf['longitude'].mean()], zoom_start=12)

districts_gdf = districts_gdf.copy().merge(
    sub_districts_gdf[['major_district', 'peruspiiri_tunnus']],
    left_on='tunnus', right_on='peruspiiri_tunnus', how='left',
    suffixes=('', '')  # Use suffix to distinguish columns if needed
)

# Add districts layer with green borders and interactive highlighting
folium.GeoJson(
    districts_gdf,
    style_function=lambda x: {
        'fillColor': 'transparent',  # No fill inside
        'color': colors['District'],  # Green border color
        'weight': 2,
        'fillOpacity': 0  # Transparent fill
    },
    highlight_function=lambda x: {
        'fillColor': colors['District'],  # Highlight fill on hover
        'color': colors['District'],  # Border highlight color
        'weight': 2,
        'fillOpacity': 0.3  # Light opacity on hover
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['major_district', 'district', 'camera_count'], 
        aliases=['Major District', 'District', 'Number of Cameras']
    )
).add_to(map_sub)

# Now, add major districts layer with blue borders
folium.GeoJson(
    major_districts_gdf,
    style_function=lambda x: {
        'fillColor': 'gray',  # No fill to avoid overlap
        'color': colors['Major District'],  # Blue border color
        'weight': 3,  # Thicker weight to make it prominent
        'fillOpacity': 0.4,  # No fill opacity for border-only display
        'opacity': 1  # Ensure border opacity to keep borders visible
    },
    interactive=False
).add_to(map_sub)

for _, row in camera_gdf.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Camera at (lat:{row['latitude']}, lon:{row['longitude']})<br>Heading: {row['heading']}",
        icon=folium.Icon(color="red", icon="camera")
    ).add_to(map_sub)
map_sub.save("C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/helsinki_districts_with_cameras.html")

# 3. Map with sub-District small district Boundaries and Camera Counts at sub-District small district Level
sub_districts_gdf = calculate_camera_counts(sub_districts_gdf, 'osaalue_tunnus')

# Dissolve geometries at the sub-district level to get one boundary per sub-district
sub_districts_gdf_dissolved = sub_districts_gdf.dissolve(by='osaalue_tunnus', as_index=False)
sub_districts_gdf_dissolved['camera_count'] = sub_districts_gdf_dissolved.groupby('osaalue_tunnus')['camera_count'].transform('sum')

map_small = folium.Map(location=[camera_gdf['latitude'].mean(), camera_gdf['longitude'].mean()], zoom_start=12)

# Add small districts layer with orange borders and interactive highlighting
folium.GeoJson(
    sub_districts_gdf_dissolved,
    style_function= lambda x: {
        'fillColor': 'transparent',
        'color': colors['Small-District'],
        'weight': 3,
        'fillOpacity': 0
    },
    highlight_function= lambda x: {
        'fillColor': colors['Small-District'],
        'color': colors['Small-District'],
        'weight': 3,
        'fillOpacity': 0.3
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['major_district', 'district', 'sub_district', 'camera_count'],
        aliases=['Major-District', 'District', 'Sub-District', 'Number of Cameras']
    )
).add_to(map_small)

# Add districts layer with green borders
folium.GeoJson(
    districts_gdf,
    style_function=lambda x: {
        'fillColor': 'transparent',  # No fill inside
        'color': colors['District'],  # Green border color
        'weight': 2,
        'fillOpacity': 0  # Transparent fill
    },
    interactive=False
).add_to(map_small)

# Now, add major districts layer with blue borders
folium.GeoJson(
    major_districts_gdf,
    style_function=lambda x: {
        'fillColor': 'gray',  # No fill to avoid overlap
        'color': colors['Major District'],  # Blue border color
        'weight': 3,  # Thicker weight to make it prominent
        'fillOpacity': 0.4,  # No fill opacity for border-only display
        'opacity': 1  # Ensure border opacity to keep borders visible
    },
    interactive=False
).add_to(map_small)
for _, row in camera_gdf.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Camera at (lat:{row['latitude']}, lon:{row['longitude']})<br>Heading: {row['heading']}",
        icon=folium.Icon(color="red", icon="camera")
    ).add_to(map_small)
map_small.save("C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/helsinki_sub_districts_with_cameras.html")

print("Maps created and saved as 'helsinki_major_districts_with_cameras.html', 'helsinki_districts_with_cameras.html', and 'helsinki_sub_districts_with_cameras.html'")


# Calculate Average Distance of Unique Camera Locations (unique full_id coordinates)
unique_locations = camera_data.drop_duplicates(subset=['full_id', 'latitude', 'longitude']).reset_index(drop=True)

# Calculate distances between consecutive unique locations
unique_distances = []
for i in range(len(unique_locations) - 1):
    coord1 = (unique_locations.loc[i, 'latitude'], unique_locations.loc[i, 'longitude'])
    coord2 = (unique_locations.loc[i + 1, 'latitude'], unique_locations.loc[i + 1, 'longitude'])
    unique_distances.append(geodesic(coord1, coord2).meters)

# Average distance of unique camera locations in kilometers
average_distance_unique_locations_km = (sum(unique_distances) / len(unique_distances)) / 1000 if unique_distances else 0

# Calculate Average Distance of All Camera Locations (including multiple cameras per location)
camera_data = camera_data.sort_values(by=['latitude', 'longitude']).reset_index(drop=True)

all_distances = []
for i in range(len(camera_data) - 1):
    coord1 = (camera_data.loc[i, 'latitude'], camera_data.loc[i, 'longitude'])
    coord2 = (camera_data.loc[i + 1, 'latitude'], camera_data.loc[i + 1, 'longitude'])
    all_distances.append(geodesic(coord1, coord2).meters)

# Average distance of all cameras in kilometers
average_distance_all_cameras_km = (sum(all_distances) / len(all_distances)) / 1000 if all_distances else 0

# Print the calculated averages
print("Average distance of unique camera locations:", average_distance_unique_locations_km, "km")
print("Average distance of all cameras:", average_distance_all_cameras_km, "km")

# Plotting the results and saving the plot
categories = ['Unique Camera Locations', 'Camera Locations']
average_distances_km = [average_distance_unique_locations_km, average_distance_all_cameras_km]

plt.figure(figsize=(18, 8))
plt.barh(categories, average_distances_km, color=['#FF6F61', '#4C9F70'])
plt.xlabel("Average Distance (km)")
plt.title("Average Distance of Cameras in Helsinki")
plt.savefig("C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/average_camera_distance_plot.png")
# plt.show()