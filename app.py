import os
from flask import Flask, request, jsonify
from model import count_vehicles

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    count = count_vehicles(file)
    
    # traffic light logic
    if count <= 5:
        green_time = 10
    elif count <= 15:
        green_time = 20
    else:
        green_time = 30

    return jsonify({
        "vehicles_detected": count,
        "green_light_duration": green_time
    })

if __name__ == '__main__':
    # Get port from environment variable (Render sets PORT automatically)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
