from flask import Flask, request, jsonify
import os
from model import count_vehicles

app = Flask(__name__)

# Root route (health check)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "AI Traffic Signal Server is running!"})

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    try:
        vehicles = count_vehicles(filepath)
        response = {
            "vehicles_detected": vehicles,
            "green_light_duration": min(60, max(10, vehicles * 2))  # simple logic
        }
    except Exception as e:
        response = {"error": str(e)}

    return jsonify(response)

if __name__ == "__main__":
    # important: 0.0.0.0 for Render, port from env
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
