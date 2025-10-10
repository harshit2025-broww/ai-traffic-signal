import cv2
import os

# Load Haar Cascade (stored in project)
CASCADE_PATH = os.path.join(os.path.dirname(__file__), "haarcascade_car.xml")
car_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def count_cars(image_path: str) -> int:
    """
    Detect cars (including small or toy cars) using Haar Cascade
    """
    img = cv2.imread(image_path)
    if img is None:
        return 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Adjusted parameters for sensitivity
    cars = car_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=1,
        minSize=(20, 20)
    )
    
    return len(cars)
