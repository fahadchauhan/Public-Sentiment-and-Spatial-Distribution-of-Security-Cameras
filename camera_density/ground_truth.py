import os
import json
from PIL import Image
from tqdm import tqdm

def yolo_to_coco(image_width, image_height, center_x, center_y, width, height):
    """Convert YOLO format (center_x, center_y, width, height) to COCO format (xmin, ymin, width, height)."""
    xmin = (center_x - width / 2) * image_width
    ymin = (center_y - height / 2) * image_height
    bbox_width = width * image_width
    bbox_height = height * image_height
    return [xmin, ymin, bbox_width, bbox_height]

def get_image_dimensions(image_path):
    """Get the dimensions (width, height) of an image."""
    with Image.open(image_path) as img:
        return img.width, img.height

def load_and_convert_ground_truth(yolo_dir, image_dir):
    """Load YOLO annotations from .txt files and convert them to COCO format."""
    ground_truth = []
    for txt_file in tqdm(os.listdir(yolo_dir)):
        if txt_file.endswith('.txt'):
            image_id = txt_file.replace('.txt', '')
            # Construct the path to the corresponding image file
            image_path = os.path.join(image_dir, f"{image_id}.jpg")  # Adjust extension if needed
            if not os.path.exists(image_path):
                print(f"Image {image_path} not found. Skipping...")
                continue

            # Get the dimensions of the image
            image_width, image_height = get_image_dimensions(image_path)

            with open(os.path.join(yolo_dir, txt_file), 'r') as f:
                for line in f:
                    class_id, center_x, center_y, width, height = map(float, line.strip().split())
                    # Convert YOLO coordinates (normalized) to COCO format (absolute pixel values)
                    bbox = yolo_to_coco(
                        image_width,  # Image width
                        image_height,  # Image height
                        center_x,
                        center_y,
                        width,
                        height
                    )
                    ground_truth.append({
                        "image_id": image_id,
                        "category_id": int(class_id),
                        "bbox": bbox,
                        "score": 1.0  # Assign a score of 1.0 for ground truth (optional)
                    })
    return ground_truth

def save_ground_truth_as_coco(ground_truth, output_path):
    """Save the converted ground truth data to a JSON file in COCO format."""
    with open(output_path, 'w') as f:
        json.dump(ground_truth, f, indent=4)

yolo_annotations_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_train_sobel_aug/labels/val'
image_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_train_sobel_aug/images/val'
output_json_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_train_sobel_aug/ground_truth_val.json'

# Load and convert ground truth annotations
ground_truth_data = load_and_convert_ground_truth(yolo_annotations_dir, image_dir)

# Save ground truth data as COCO JSON
save_ground_truth_as_coco(ground_truth_data, output_json_path)

yolo_annotations_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_train_sobel_aug/labels/test'
image_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_train_sobel_aug/images/test'
output_json_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals_train_sobel_aug/ground_truth_test.json'

# Load and convert ground truth annotations
ground_truth_data = load_and_convert_ground_truth(yolo_annotations_dir, image_dir)

# Save ground truth data as COCO JSON
save_ground_truth_as_coco(ground_truth_data, output_json_path)


print(f"Ground truth data saved successfully to {output_json_path}")
