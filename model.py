import cv2
import os

CASCADE_PATH = os.path.join(os.path.dirname(__file__), "haarcascade_car.xml")
car_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def count_cars(image_path: str) -> int:
    img = cv2.imread(image_path)
    if img is None:
        return 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)
    return len(cars)
