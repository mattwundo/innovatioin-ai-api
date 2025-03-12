from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
model = joblib.load("r_and_d_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Ensure required fields are present
    if "Revenue" not in data:
        return jsonify({"error": "Missing Revenue value"}), 400

    # Extract revenue value
    revenue = np.array(data["Revenue"]).reshape(1, -1)

    # Make prediction
    predicted_r_and_d = model.predict(revenue)[0]

    response = {
        "Revenue": data["Revenue"],
        "Predicted R&D Spend": predicted_r_and_d
    }

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned PORT
    app.run(host='0.0.0.0', port=port)
