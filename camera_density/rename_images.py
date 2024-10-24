import os
import pandas as pd

# Define paths
csv_path = "C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/signals_image_metadata.csv"
new_csv_path = "C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/signals_image_metadata_updated.csv"
images_path = "C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/images"
labels_path = "C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/labels"

# Load the CSV file
df = pd.read_csv(csv_path)

# Iterate over the image files and update their names along with label files
for count, image_file in enumerate(os.listdir(images_path)):
    if image_file.endswith('.jpg'):
        print(f"image_file: {image_file}")
        new_image_name = image_file.rsplit('_jpg', 1)[0] + '.jpg'
        count = new_image_name.split('_', 1)[0]
        base_name = new_image_name.split('_', 1)[1]

        print(f"base_name: {base_name}")
        
        # Rename the image file
        old_image_path = os.path.join(images_path, image_file)
        new_image_path = os.path.join(images_path, new_image_name)
        os.rename(old_image_path, new_image_path)
        
        # Update the corresponding label file
        label_file = image_file.replace('.jpg', '.txt')
        new_label_file = new_image_name.replace('.jpg', '.txt')
        
        old_label_path = os.path.join(labels_path, label_file)
        new_label_path = os.path.join(labels_path, new_label_file)
        if os.path.exists(old_label_path):
            os.rename(old_label_path, new_label_path)



print("Images and labels have been updated successfully.")
