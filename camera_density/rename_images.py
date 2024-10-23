import os

from tqdm import tqdm

# Folder path
folder_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/images'

# List all files in the directory
files = os.listdir(folder_path)

# Sort files to ensure proper numbering
files.sort()

# Starting number
start_number = 418

# Loop through each file and rename it with numbering
for index, filename in tqdm(enumerate(files)):
    # Extract the file extension
    file_extension = os.path.splitext(filename)[1]
    
    # New filename with numbering
    new_filename = f"{start_number + index}_{filename}"
    
    # Full paths for the old and new file names
    old_filepath = os.path.join(folder_path, filename)
    new_filepath = os.path.join(folder_path, new_filename)
    
    # Rename the file
    os.rename(old_filepath, new_filepath)

print("Renaming completed.")
