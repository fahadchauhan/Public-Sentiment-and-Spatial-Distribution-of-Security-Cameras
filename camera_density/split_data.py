import os
import shutil
from pathlib import Path
import random
from tqdm import tqdm

def split_dataset(images_dir, labels_dir, output_dir, val_ratio=0.1, test_ratio=0.1, bg_ratio=0.1):
    # Get all image files in the images directory
    image_files = list(Path(images_dir).glob('*.jpg'))

    # Shuffle image files for random splitting
    random.shuffle(image_files)

    # Split images into labeled and background (empty label) images
    labeled_images = []
    background_images = []

    for image_path in tqdm(image_files, desc="Classifying images"):
        # Find corresponding label file
        label_file = Path(labels_dir) / (image_path.stem + '.txt')
        
        if label_file.exists() and label_file.stat().st_size > 0:
            labeled_images.append((image_path, label_file))
        else:
            background_images.append((image_path, label_file if label_file.exists() else None))

    # print(f"len(labeled_images): {len(labeled_images)}")
    # print(f"len(background_images): {len(background_images)}")
    # Split labeled images into train, val, and test
    total_labeled = len(labeled_images)
    test_count = int(total_labeled * test_ratio)
    val_count = int(total_labeled * val_ratio)

    test_images = labeled_images[:test_count]
    val_images = labeled_images[test_count:test_count + val_count]
    train_images = labeled_images[test_count + val_count:]

    # Split background images (10% in train and val only, none in test)
    bg_count_train = max(1, int(len(train_images) * bg_ratio))
    bg_count_val = max(1, int(len(val_images) * bg_ratio))

    bg_images_train = random.sample(background_images, min(bg_count_train, len(background_images)))
    remaining_backgrounds = list(set(background_images) - set(bg_images_train))
    bg_images_val = random.sample(remaining_backgrounds, min(bg_count_val, len(remaining_backgrounds)))

    # Define output directories
    dirs = {
        'train': {
            'images': Path(output_dir) / 'images' / 'train',
            'labels': Path(output_dir) / 'labels' / 'train'
        },
        'val': {
            'images': Path(output_dir) / 'images' / 'val',
            'labels': Path(output_dir) / 'labels' / 'val'
        },
        'test': {
            'images': Path(output_dir) / 'images' / 'test',
            'labels': Path(output_dir) / 'labels' / 'test'
        }
    }

    # Create directories if they don't exist
    for split, paths in dirs.items():
        paths['images'].mkdir(parents=True, exist_ok=True)
        paths['labels'].mkdir(parents=True, exist_ok=True)

    # Function to copy images and labels
    def copy_files(image_label_pairs, split):
        for image_path, label_path in tqdm(image_label_pairs, desc=f"Copying {split} set"):
            shutil.copy(image_path, dirs[split]['images'] / image_path.name)
            if label_path and label_path.exists():
                shutil.copy(label_path, dirs[split]['labels'] / label_path.name)

    # Copy files to the respective directories
    copy_files(train_images + bg_images_train, 'train')
    copy_files(val_images + bg_images_val, 'val')
    copy_files(test_images, 'test')

    print("Dataset split completed.")

# Define paths to input and output directories
images_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/images'
labels_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_all/labels'
output_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/'

# Split dataset
split_dataset(images_dir, labels_dir, output_dir)
