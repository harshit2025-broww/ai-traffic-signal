import cv2
import os

# Load Haar Cascade from the same project folder
CASCADE_PATH = os.path.join(os.path.dirname(__file__), "haarcascade_car.xml")
car_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def count_cars(image_path: str) -> int:
    """
    Detect both real and toy cars using a more sensitive Haar Cascade.
    Optimized for ESP32-CAM image quality and small-scale objects.
    """
    img = cv2.imread(image_path)
    if img is None:
        print("⚠️ Image not loaded correctly!")
        return 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 🧩 Enhanced detection parameters
    cars = car_cascade.detectMultiScale(
        gray,
        scaleFactor=1.02,    # Higher sensitivity to distance/size
        minNeighbors=2,      # Lower = detects smaller or partial cars
        minSize=(15, 15),    # Detects even toy cars
        maxSize=(500, 500)   # Avoids huge false positives
    )

    print(f"Detected {len(cars)} vehicle(s)")
    return len(cars)
