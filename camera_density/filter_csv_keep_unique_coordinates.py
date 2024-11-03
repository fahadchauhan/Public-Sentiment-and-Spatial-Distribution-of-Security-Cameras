import pandas as pd

# Load the updated CSV file with the 'camera_present' column
csv_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/signals_image_metadata_with_cameras.csv'
csv_data = pd.read_csv(csv_path)

# Separate rows where 'camera_present' is True
camera_present_data = csv_data[csv_data['camera_present'] == True]

# Get the rows with 'heading' 0 for each 'full_id' where no cameras are present
no_camera_data = csv_data[csv_data['camera_present'] == False]
no_camera_data = no_camera_data[no_camera_data['heading'] == 0]

# Find full_ids with no camera present at any heading
no_camera_full_ids = set(no_camera_data['full_id']) - set(camera_present_data['full_id'])

# Keep only rows from no_camera_data where 'full_id' is in no_camera_full_ids
fallback_data = no_camera_data[no_camera_data['full_id'].isin(no_camera_full_ids)]

# Combine the data with cameras present and the fallback data
final_data = pd.concat([camera_present_data, fallback_data])

# Save the final filtered data to a new CSV file
filtered_csv_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/signals_image_metadata_filtered.csv'
final_data.to_csv(filtered_csv_path, index=False)

print("Filtered CSV file saved successfully.")
