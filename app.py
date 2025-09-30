from fastapi import FastAPI, UploadFile, File
import shutil
import os
from model import count_cars

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Traffic Signal API running"}

@app.post("/traffic")
async def traffic(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Count cars
    cars = count_cars(file_path)

    # Timer rule: base 5 sec for 5 cars, each +1 car = +2 sec
    if cars <= 5:
        timer = 5
    else:
        timer = 5 + (cars - 5) * 2

    # Clean up temp file
    os.remove(file_path)

    return {
        "vehicles_detected": cars,
        "timer": timer,
        "filename": file.filename
    }
