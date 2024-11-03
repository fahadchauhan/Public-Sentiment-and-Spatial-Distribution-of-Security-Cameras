import pandas as pd
import os
from tqdm import tqdm

# Load the CSV file
csv_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/signals_image_metadata.csv'
csv_data = pd.read_csv(csv_path)

# Path to the folder containing the .txt files
txt_folder = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/labels/'

# Get a list of non-empty .txt files
camera_images = []
for txt_file in tqdm(os.listdir(txt_folder)):
    if txt_file.endswith('.txt'):
        base_name = txt_file.replace('.txt', '.jpg').split('_', 1)[1]
        # print(f'txt_file: {txt_file}')
        # print(f'base_name: {base_name}')
        txt_file_path = os.path.join(txt_folder, txt_file)
        if os.path.getsize(txt_file_path) > 0:  # Check if the file size is greater than zero
            camera_images.append(base_name)

# Add a new column to the CSV to indicate camera presence
csv_data['camera_present'] = csv_data['image_name'].apply(lambda x: x in camera_images)

# Save the updated CSV
updated_csv_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/signals_image_metadata_with_cameras.csv'
csv_data.to_csv(updated_csv_path, index=False)

print("Updated CSV file saved successfully.")
