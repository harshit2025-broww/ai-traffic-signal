from ultralytics import YOLO

# Use smallest YOLOv8 nano model (fast + low RAM)
MODEL_PATH = "yolov8n.pt"

def count_vehicles(image_path):
    # Load model only when function is called → saves memory
    model = YOLO(MODEL_PATH)
    results = model(image_path)

    # Count number of detections
    count = len(results[0].boxes)
    return count
