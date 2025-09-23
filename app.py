from flask import Flask, request, jsonify
from model import count_vehicles  # import AI model

app = Flask(__name__)

@app.route('/')
def home():
    return "AI Traffic Signal Server is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    file_path = "temp.jpg"
    file.save(file_path)

    # Get vehicle count from AI model
    vehicles = count_vehicles(file_path)

    # Simple traffic logic
    green_time = 30 if vehicles > 5 else 10

    return jsonify({
        "vehicles_detected": vehicles,
        "green_light_time": green_time
    })

if __name__ == '__main__':
    app.run(debug=True)
