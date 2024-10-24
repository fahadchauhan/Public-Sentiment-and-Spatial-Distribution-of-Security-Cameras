import os
import pandas as pd

# Define paths
csv_path = "C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/signals_image_metadata.csv"
new_csv_path = "C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/signals_image_metadata_updated.csv"
images_path = "C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/images"

# Load the CSV file
df = pd.read_csv(csv_path)

# Get all image names from the images directory
image_files = [f for f in os.listdir(images_path) if f.endswith('.jpg')]

# Dictionary to map the base name (from CSV) to the actual full filename in the images directory
image_mapping = {}
for image_file in image_files:
    base_name = image_file.split('_', 1)[1]  # Extract the base name (after count, before _jpg)
    image_mapping[base_name] = image_file

# Iterate over the rows in the CSV and update image names if a match is found in the directory
matched_rows = []
for index, row in df.iterrows():
    base_name_from_csv = row['image_name']
    if base_name_from_csv in image_mapping:
        new_image_name = image_mapping[base_name_from_csv]
        df.at[index, 'image_name'] = new_image_name
        matched_rows.append(index)

# Filter the DataFrame to keep only the rows with matching image names
df = df.loc[matched_rows]
df = df.drop_duplicates(subset='image_name')

# Save the updated CSV as a new file
df.to_csv(new_csv_path, index=False)

print("CSV has been updated successfully with the matching image names.")
