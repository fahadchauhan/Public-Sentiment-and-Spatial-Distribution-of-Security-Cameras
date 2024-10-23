import pandas as pd
import requests
import os
from datetime import datetime
from tqdm import tqdm

# Replace with your actual API key
api_key = 'AIzaSyBL20HXg054eInXj8O6le6vVnn-HhnbBkk'

# Input CSV file (replace backslashes with slashes)
csv_file = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/Images part/Qgis/helsinki_signals_data.csv'

# Directory to save images (replace backslashes with slashes)
save_directory = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/Images part/Dataset/signals/images'

# Ensure the directory exists
os.makedirs(save_directory, exist_ok=True)

# List of headings (directions)
headings = [0, 45, 90, 135, 180, 225, 270, 315]  # North, NE, East, SE, South, SW, West, NW
# headings = [0]

# Field of View (FOV)
fov = 70
pitch = 10

# Output CSV for storing metadata
output_csv = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/Images part/Dataset/signals/signals_image_metadata.csv'

# Create a list to store metadata rows
metadata_rows = []

# Function to sanitize the filename
def sanitize_filename(value):
    return str(value).replace('.', '-')

# Function to download a street view image for given coordinates
def download_street_view_image(lat, lon, heading, image_name):
    fov=360
    pitch = 0
    panoid = "P8-l8zkFvG1vupCLgUo3ZA"
    # heading = 0
    # url = f"https://maps.googleapis.com/maps/api/streetview?size=2048x2048&location={lat},{lon}&fov={fov}&pitch={pitch}&key={api_key}"
    # url = f"https://maps.googleapis.com/maps/api/streetview?size=2048x2048&location={lat},{lon}&fov={fov}&heading={heading}&pitch={pitch}&key={api_key}"
    url = f"https://maps.googleapis.com/maps/api/streetview?size=640x640&pano={panoid}&heading={142}&fov={90}&pitch={0}&key={api_key}"

    # Send a request to Google Street View API
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the image to the specified file
        with open(image_name, 'wb') as file:
            file.write(response.content)
        # print(f"Image saved: {image_name}")
    else:
        print(f"Error: {response.status_code}, could not download image.")
    return response.status_code



lat = 62.2396342
lon = 25.7459492

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Sanitize latitude and longitude for filename
lat_sanitized = sanitize_filename(lat)
lon_sanitized = sanitize_filename(lon)
full_id = f"1_{lat_sanitized}_{lon_sanitized}"

for heading in headings:
    # Define the image file path and name with additional metadata (fov added to filename)
    unique_id = full_id
    image_name = f'stan_helsinki_without_heading_signal_unique-id_{unique_id}_full-id_{full_id}_heading_{heading}_fov_{fov}_pitch_{pitch}_lat_{lat_sanitized}_lon_{lon_sanitized}.jpg'
    full_image_name = os.path.join(save_directory, image_name)

    # Download the image
    status_code = download_street_view_image(lat, lon, heading, full_image_name)

    # Append metadata to the list
    metadata_rows.append({
        'unique_id': unique_id,
        'full_id': full_id,
        'latitude': lat,
        'longitude': lon,
        'heading': 360,
        'fov': fov,
        'pitch': pitch,
        'image_name': image_name,
        'timestamp': timestamp,
        'status_code': status_code
    })