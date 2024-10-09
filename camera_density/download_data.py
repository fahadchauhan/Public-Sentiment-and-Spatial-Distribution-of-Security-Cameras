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
    url = f"https://maps.googleapis.com/maps/api/streetview?size=2048x2048&location={lat},{lon}&fov={fov}&heading={heading}&pitch={pitch}&key={api_key}"

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

# Load the CSV data
df = pd.read_csv(csv_file)

# Iterate over each row in the CSV and download 8 images for each point
for index, row in tqdm(df.iterrows()):
    lat = row['latitude']
    lon = row['longitude']
    full_id = row['full_id']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Sanitize latitude and longitude for filename
    lat_sanitized = sanitize_filename(lat)
    lon_sanitized = sanitize_filename(lon)

    for heading in headings:
        # Define the image file path and name with additional metadata (fov added to filename)
        unique_id = full_id + '-' + str(heading)
        image_name = f'helsinki_signal_unique-id_{unique_id}_full-id_{full_id}_heading_{heading}_fov_{fov}_pitch_{pitch}_lat_{lat_sanitized}_lon_{lon_sanitized}.jpg'
        full_image_name = os.path.join(save_directory, image_name)

        # Download the image
        status_code = download_street_view_image(lat, lon, heading, full_image_name)

        # Append metadata to the list
        metadata_rows.append({
            'unique_id': unique_id,
            'full_id': full_id,
            'latitude': lat,
            'longitude': lon,
            'heading': heading,
            'fov': fov,
            'pitch': pitch,
            'image_name': image_name,
            'timestamp': timestamp,
            'status_code': status_code
        })
    # break

# Convert metadata rows to a DataFrame and save as CSV
metadata_df = pd.DataFrame(metadata_rows)
metadata_df.to_csv(output_csv, index=False)
