import os

# Function to delete empty .txt files from the labels folder
def delete_empty_txt_files(labels_folder):
    empty_files_count = 0
    # Recursively scan the labels folder (including subfolders: train, test, val)
    for root, dirs, files in os.walk(labels_folder):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                
                # Check if the file is empty
                if os.stat(file_path).st_size == 0:
                    print(f"Deleting empty label file: {file_path}")
                    os.remove(file_path)
                    empty_files_count += 1
    print(f"Total empty files deleted: {empty_files_count}")

# Function to scan all .txt files from the labels folder and store the filenames
def get_all_label_filenames(labels_folder):
    txt_filenames = set()
    
    # Recursively scan the labels folder (including subfolders: train, test, val)
    for root, dirs, files in os.walk(labels_folder):
        for file in files:
            if file.endswith('.txt'):
                # Store the file name without the .txt extension
                txt_filenames.add(file.replace('.txt', ''))
                
    return txt_filenames

# Function to remove images that do not have a corresponding .txt file in the labels folder
def remove_images_without_txt(images_folder, valid_label_filenames):
    # Recursively scan the images folder (including subfolders: train, test, val)
    for root, dirs, files in os.walk(images_folder):
        for file in files:
            if file.endswith('.jpg'):
                image_name = file.replace('.jpg', '')  # Get the image name without extension

                # Check if the image has a corresponding label in the set
                if image_name not in valid_label_filenames:
                    image_file_path = os.path.join(root, file)
                    print(f"Removing image (no matching .txt): {image_file_path}")
                    os.remove(image_file_path)
                # else:
                #     print(f"Keeping image (matching .txt found): {os.path.join(root, file)}")

# Define paths for the labels and images folders
labels_folder = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/labels'
images_folder = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/images'

# Step 1: Delete empty .txt files in the labels folder
delete_empty_txt_files(labels_folder)

# Step 2: Scan all .txt files in the labels folder and get the valid filenames (without extensions)
valid_label_filenames = get_all_label_filenames(labels_folder)

# Step 3: Remove images that do not have a corresponding .txt file in the labels folder
remove_images_without_txt(images_folder, valid_label_filenames)
