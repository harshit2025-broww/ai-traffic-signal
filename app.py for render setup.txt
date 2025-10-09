from fastapi import FastAPI, UploadFile, File
import shutil
import os
from model import count_cars

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Traffic Signal API running ✅"}

@app.post("/traffic")
async def traffic(file: UploadFile = File(...)):
    """
    Endpoint to receive image from ESP32-CAM,
    count cars, calculate timer and return result
    """
    # Save uploaded image temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Count cars using AI
    vehicles = count_cars(file_path)

    # Calculate timer
    if vehicles <= 5:
        timer = 5
    else:
        timer = 5 + (vehicles - 5) * 2

    # Minimum timer = 1 second (in case vehicles < 1)
    timer = max(timer, 1)

    # Clean up temp file
    os.remove(file_path)

    # Return JSON for ESP32
    return {
        "vehicles_detected": vehicles,
        "timer": timer,
        "filename": file.filename
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
