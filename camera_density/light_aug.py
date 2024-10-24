import albumentations as A
import cv2
import os
from tqdm import tqdm
import shutil

# Function to read YOLO format bounding boxes and convert to Pascal VOC
def read_yolo_labels(label_path, img_width, img_height):
    bboxes = []
    labels = []
    with open(label_path, 'r') as file:
        for line in file.readlines():
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            # Convert from YOLO to Pascal VOC
            x_min = (x_center - width / 2) * img_width
            y_min = (y_center - height / 2) * img_height
            x_max = (x_center + width / 2) * img_width
            y_max = (y_center + height / 2) * img_height
            bboxes.append([x_min, y_min, x_max, y_max])
            labels.append(int(class_id))  # Append the class label as an integer
    return bboxes, labels

# Function to convert Pascal VOC bounding boxes back to YOLO format
def convert_to_yolo_format(bboxes, img_width, img_height):
    yolo_bboxes = []
    for bbox in bboxes:
        x_min, y_min, x_max, y_max = bbox
        # Convert from Pascal VOC to YOLO
        x_center = (x_min + x_max) / 2 / img_width
        y_center = (y_min + y_max) / 2 / img_height
        width = (x_max - x_min) / img_width
        height = (y_max - y_min) / img_height
        yolo_bboxes.append([x_center, y_center, width, height])
    return yolo_bboxes

# Function to write YOLO format bounding boxes
def write_yolo_labels(label_path, bboxes, labels):
    with open(label_path, 'w') as file:
        for bbox, label in zip(bboxes, labels):
            x_center, y_center, width, height = bbox
            file.write(f"{label} {x_center} {y_center} {width} {height}\n")

# Function to clamp bounding boxes to ensure all values are between 0 and the image size
def clamp_bboxes(bboxes, img_width, img_height):
    clamped_bboxes = []
    for bbox in bboxes:
        x_min, y_min, x_max, y_max = bbox
        # Clamp values to stay within the image boundaries
        x_min = max(0, min(x_min, img_width))
        y_min = max(0, min(y_min, img_height))
        x_max = max(0, min(x_max, img_width))
        y_max = max(0, min(y_max, img_height))
        clamped_bboxes.append([x_min, y_min, x_max, y_max])
    return clamped_bboxes

# Augmentation pipeline using Pascal VOC format
transform = A.Compose([
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
    A.CLAHE(clip_limit=4.0, tile_grid_size=(8, 8), p=0.5),
    A.RandomGamma(gamma_limit=(80, 120), p=0.5),
    A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.5)
], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['labels']))


# Function to process a folder
def process_folder(image_folder, label_folder, output_image_folder, output_label_folder):
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)
    if not os.path.exists(output_label_folder):
        os.makedirs(output_label_folder)
    
    for image_filename in tqdm(os.listdir(image_folder)):
        if image_filename.endswith('.png') or image_filename.endswith('.jpg'):
            image_path = os.path.join(image_folder, image_filename)
            label_path = os.path.join(label_folder, image_filename.replace('.png', '.txt').replace('.jpg', '.txt'))
            
            if not os.path.exists(label_path):
                continue  # Skip images without corresponding label files
            
            # Read image
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img_height, img_width, _ = image.shape
            
            # Read labels and convert from YOLO format to Pascal VOC
            bboxes, labels = read_yolo_labels(label_path, img_width, img_height)
            
            # Clamp bounding boxes BEFORE augmentation
            clamped_bboxes = clamp_bboxes(bboxes, img_width, img_height)
            
            # Apply augmentations in Pascal VOC format
            transformed = transform(image=image, bboxes=clamped_bboxes, labels=labels)
            transformed_image = transformed["image"]
            transformed_bboxes = transformed["bboxes"]
            transformed_labels = transformed["labels"]
            
            # Convert back to YOLO format
            img_height, img_width, _ = transformed_image.shape
            yolo_bboxes = convert_to_yolo_format(transformed_bboxes, img_width, img_height)
            
            # Convert the augmented image back to BGR colorspace for saving
            transformed_image_bgr = cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR)
            
            # Add "aug" to filenames before saving
            image_filename_aug = image_filename.replace('.png', '_light_aug.png').replace('.jpg', '_light_aug.jpg')
            label_filename_aug = image_filename.replace('.png', '_light_aug.txt').replace('.jpg', '_light_aug.txt')
            
            # Save transformed image and labels
            output_image_path = os.path.join(output_image_folder, image_filename_aug)
            output_label_path = os.path.join(output_label_folder, label_filename_aug)
            cv2.imwrite(output_image_path, transformed_image_bgr)
            write_yolo_labels(output_label_path, yolo_bboxes, transformed_labels)

# Define input and output directories
input_image_base_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/images'
input_label_base_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/labels'
output_image_base_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_bg_train_light_aug/images'
output_label_base_path = "C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_bg_train_light_aug/labels"

# Process train and val folders
for split in ['train', 'val']:
    process_folder(
        image_folder=os.path.join(input_image_base_path, split),
        label_folder=os.path.join(input_label_base_path, split),
        output_image_folder=os.path.join(output_image_base_path, split),
        output_label_folder=os.path.join(output_label_base_path, split)
    )

print("Augmentation and saving complete.")

# Function to copy files from source to destination, maintaining folder structure
def copy_files(src_folder, dest_folder):
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            # Construct full file paths
            src_file = os.path.join(root, file)
            # Create the corresponding destination folder structure
            relative_path = os.path.relpath(root, src_folder)
            dest_file_dir = os.path.join(dest_folder, relative_path)
            if not os.path.exists(dest_file_dir):
                os.makedirs(dest_file_dir)
            # Copy the file
            shutil.copy2(src_file, dest_file_dir)


input_xview = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals'
output_aug = "C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_bg_train_light_aug"

# Copy 'test' folder from the original dataset
copy_files(os.path.join(input_xview, 'images/test'), os.path.join(output_aug, 'images/test'))
copy_files(os.path.join(input_xview, 'labels/test'), os.path.join(output_aug, 'labels/test'))

# Copy 'train' and 'val' from original folder
copy_files(os.path.join(input_xview, 'images/train'), os.path.join(output_aug, 'images/train'))
copy_files(os.path.join(input_xview, 'images/val'), os.path.join(output_aug, 'images/val'))
copy_files(os.path.join(input_xview, 'labels/train'), os.path.join(output_aug, 'labels/train'))
copy_files(os.path.join(input_xview, 'labels/val'), os.path.join(output_aug, 'labels/val'))

print("Files have been copied successfully.")