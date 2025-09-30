from fastapi import FastAPI, UploadFile, File
import os
import uvicorn
from model import detect_cars, calculate_timer

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Traffic Signal Running ✅"}

@app.post("/traffic")
async def traffic_signal(file: UploadFile = File(...)):
    # Save uploaded image
    contents = await file.read()
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(contents)

    # Detect cars
    cars = detect_cars(file_location)

    # Calculate timer
    timer = calculate_timer(cars)

    # Remove temp file
    os.remove(file_location)

    return {
        "cars_detected": cars,
        "signal_timer": timer
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
