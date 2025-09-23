from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple AI logic (later replace with ML model)
def ai_signal_controller(data):
    # Example input: {"road1": 10, "road2": 20, "road3": 5, "road4": 15}
    total = sum(data.values())
    timings = {}
    for road, count in data.items():
        timings[road] = max(10, int((count / total) * 60))  # proportional time allocation
    return timings

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        result = ai_signal_controller(data)
        return jsonify({"signal_timings": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/')
def home():
    return "AI Traffic Signal Server is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
