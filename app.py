from fastapi import FastAPI, UploadFile, File
import shutil
import os
from model import count_cars

app = FastAPI()

@app.get("/")
def home():
    return {"message": "🚦 AI Traffic Signal API is running successfully on Render!"}

@app.post("/traffic")
async def traffic(file: UploadFile = File(...)):
    """
    Endpoint to receive image from ESP32-CAM,
    count vehicles, calculate timer and return JSON response.
    """
    # Save uploaded image temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Count cars using Haarcascade model
    vehicles = count_cars(file_path)

    # Timer logic:
    # - If <= 5 vehicles → 5 seconds
    # - Each additional vehicle adds 2 seconds
    # - Minimum timer = 1 sec
    if vehicles <= 5:
        timer = 5
    else:
        timer = 5 + (vehicles - 5) * 2
    timer = max(timer, 1)

    # Clean up temp file
    os.remove(file_path)

    # Return JSON for ESP32 or Postman test
    return {
        "vehicles_detected": vehicles,
        "green_timer_sec": timer,
        "signal": "green" if vehicles > 0 else "red"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT automatically
    uvicorn.run("app:app", host="0.0.0.0", port=port)
