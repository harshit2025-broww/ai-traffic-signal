from ultralytics import YOLO

# Load pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")  # 'n' = nano (fast, lightweight)

def count_vehicles(image_path):
    """
    Detect vehicles in an image and return count.
    """
    results = model.predict(image_path, imgsz=640)
    count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])  # class ID
            # YOLO class IDs: 2=car, 3=motorbike, 5=bus, 7=truck
            if cls in [2, 3, 5, 7]:
                count += 1

    return count
