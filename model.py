import cv2

# Pre-trained Haar cascade for cars
CAR_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_car.xml"
car_cascade = cv2.CascadeClassifier(CAR_CASCADE_PATH)

def detect_cars(image_path: str) -> int:
    """
    Detect number of cars in an image using Haar Cascade.
    """
    img = cv2.imread(image_path)
    if img is None:
        return 0
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 3)

    return len(cars)


def calculate_timer(cars: int) -> int:
    """
    Calculate timer based on number of cars.
    - 5 cars => 5 sec
    - Each extra car (+1) => +2 sec
    - Each less car (-1) => -2 sec
    """
    if cars <= 0:
        return 1  # minimum timer
    
    base_cars = 5
    base_time = 5
    diff = cars - base_cars
    timer = base_time + (diff * 2)

    return max(timer, 1)  # never below 1 sec
