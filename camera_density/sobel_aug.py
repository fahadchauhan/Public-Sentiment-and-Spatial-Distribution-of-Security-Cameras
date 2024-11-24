import cv2
import numpy as np
import os
import shutil
from tqdm import tqdm

# Directories
# input_base_dir = 'D:/ByteCorp/Dataset/og_xview/images'
# label_base_dir = 'D:/ByteCorp/Dataset/og_xview/labels'
# output_base_dir = 'D:/ByteCorp/Dataset/og_xview_augs/og_xview_sobel_aug'

input_base_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/images'
label_base_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/labels'
output_base_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_train_sobel_aug'

# Ensure base output directory exists for images and labels
os.makedirs(os.path.join(output_base_dir, 'images'), exist_ok=True)
os.makedirs(os.path.join(output_base_dir, 'labels'), exist_ok=True)

# Function to apply the Sobel filter to an image
def apply_sobel_filter(image):
    # Apply Sobel Edge Detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel_edges = cv2.magnitude(sobel_x, sobel_y)
    sobel_edges = np.uint8(255 * sobel_edges / np.max(sobel_edges))

    return sobel_edges

# Function to modify the filename to move "aug" to the end
def modify_filename(filename):
    base_name, ext = os.path.splitext(filename)
    parts = base_name.split('_')

    # Check if "aug" is in the filename and move it to the end if it exists
    if 'aug' in parts:
        parts.remove('aug')
    new_base_name = '_'.join(parts) + '_sobel_aug'
    return new_base_name + ext

# Function to copy original images and labels to the output directory
def copy_files(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename)
        if os.path.isfile(src_file):
            shutil.copy(src_file, dst_file)

# Loop through train, val, and test directories
for dataset_type in ['train', 'val', 'test']:
    # Input and output directories for images
    input_image_dir = os.path.join(input_base_dir, dataset_type)
    output_image_dir = os.path.join(output_base_dir, 'images', dataset_type)
    os.makedirs(output_image_dir, exist_ok=True)  # Ensure output image directory exists

    # Input and output directories for labels
    input_label_dir = os.path.join(label_base_dir, dataset_type)
    output_label_dir = os.path.join(output_base_dir, 'labels', dataset_type)
    os.makedirs(output_label_dir, exist_ok=True)  # Ensure output label directory exists

    # if dataset_type in ['train', 'val']:
    if dataset_type in ['train']:
        # Process images for Sobel filter and copy original images to the output directory
        for filename in tqdm(os.listdir(input_image_dir), desc=f'Processing {dataset_type} images'):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                # Load the image
                image_path = os.path.join(input_image_dir, filename)
                image = cv2.imread(image_path)

                # Apply Sobel filter
                sobel = apply_sobel_filter(image)

                # Modify the filename to move "aug" to the end and add "_sobel"
                new_filename = modify_filename(filename)

                # Save the Sobel processed image directly to the respective train or val folder
                cv2.imwrite(os.path.join(output_image_dir, new_filename), sobel)

                # Copy the original image to the output directory
                shutil.copy(image_path, os.path.join(output_image_dir, filename))

                # Handle label file copying and renaming
                label_filename = os.path.splitext(filename)[0] + '.txt'  # Assume label file has .txt extension
                label_src_path = os.path.join(input_label_dir, label_filename)
                if os.path.isfile(label_src_path):
                    new_label_filename = modify_filename(label_filename)
                    shutil.copy(label_src_path, os.path.join(output_label_dir, new_label_filename))
                    shutil.copy(label_src_path, os.path.join(output_label_dir, label_filename))
    else:
        # If test dataset, just copy the original images and labels without applying Sobel filter
        copy_files(input_image_dir, output_image_dir)
        copy_files(input_label_dir, output_label_dir)

print("Processing and copying of images and labels is complete for train, val, and test sets!")
