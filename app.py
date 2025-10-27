from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from ultralytics import YOLO

app = FastAPI()

# Load YOLOv8 model (ensure you have yolov8n.pt in your environment)
model = YOLO('yolov8n.pt')

@app.post("/traffic")
async def traffic_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    # Convert image bytes to OpenCV image
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)

    # Run detection
    results = model(img)

    # Count cars only
    car_count = 0
    for box in results[0].boxes:
        cls_id = int(box.cls)
        label = model.names[cls_id]
        if label == 'car':
            car_count += 1

    # Timer logic:
    # If no vehicles: timer = 0 (red signal)
    # If vehicles == 5: timer = 5 seconds
    # If vehicles > 5: timer = 5 + 2*(extra vehicles)
    # If vehicles < 5 and >0: timer = 5 seconds

    if car_count == 0:
        timer = 0  # Red signal default
    elif car_count <= 5:
        timer = 5
    else:
        extra = car_count - 5
        timer = 5 + (extra * 2)

    return {
        "vehicles_detected": car_count,
        "timer": timer
    }
