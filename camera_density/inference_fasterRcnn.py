import torch
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.modeling import build_model
from detectron2.structures import ImageList
import pandas as pd
import os
from PIL import Image, ImageDraw
from torchvision import transforms as T

# Paths to model, images, and CSV
model_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/models/stanford_faster_rcnn.ckpt'
image_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/images/'
csv_file_path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/signals/signals_image_metadata.csv'
save_dir = 'C:/Users/fahad/OneDrive - Oulun yliopisto/OULU/Thesis/camera_density/Dataset/crossings_annotated/'

# Load CSV for Image Metadata
df = pd.read_csv(csv_file_path)

# Preprocessing: Resize image to 640x640, convert to tensor, and normalize
transform = T.Compose([
    T.Resize((640, 640)),  # Resize to 640x640
    T.ToTensor(),  # Convert to tensor
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalization based on ImageNet
])

# Configure Detectron2 model
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = model_path  # Use your custom model
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Set a threshold for this model
cfg.MODEL.DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Build and load model
model = build_model(cfg)
DetectionCheckpointer(model).load(model_path)
model.eval()

# Function to run inference on a single image
def run_inference(image_tensor):
    inputs = [{"image": image_tensor}]
    with torch.no_grad():
        predictions = model(inputs)
    return predictions

# Function to draw bounding boxes on the image
def draw_boxes(image, boxes):
    draw = ImageDraw.Draw(image)
    for box in boxes:
        draw.rectangle(box.tolist(), outline="red", width=3)
    return image

# Perform inference on the dataset, save annotated images
for idx, row in df.iterrows():
    image_name = row['image_name']  # Assuming CSV contains 'image_name' column
    image_path = os.path.join(image_dir, image_name)

    # Open and preprocess image
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image)

    # Run inference
    predictions = run_inference(image_tensor)

    # Process predictions (bounding boxes)
    instances = predictions[0]["instances"]
    boxes = instances.pred_boxes.tensor.cpu().numpy()

    # Draw bounding boxes and save annotated image
    if len(boxes) > 0:
        annotated_image = draw_boxes(image, boxes)
        save_path = os.path.join(save_dir, f"annotated_{image_name}")
        annotated_image.save(save_path)
        print(f"Saved annotated image: {save_path}")
    else:
        print(f"No detections for {image_name}")
