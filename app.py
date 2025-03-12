from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Load the trained Q-table (Temporary placeholder)
q_table = np.zeros((100, 100, 100, 3))  

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    market_value = data.get('market_value', 50)
    r_and_d = data.get('r_and_d', 50)
    competitor_threat = data.get('competitor_threat', 50)

    # Convert to Q-table index
    state_idx = tuple(np.clip((np.array([market_value, r_and_d, competitor_threat]) // 2).astype(int), 0, 99))

    # Choose the best action from Q-table
    best_action = np.argmax(q_table[state_idx])

    action_mapping = {0: "Low R&D Investment", 1: "Medium R&D Investment", 2: "High R&D Investment"}
    response = {
        "market_value": market_value,
        "r_and_d": r_and_d,
        "competitor_threat": competitor_threat,
        "recommended_action": action_mapping[best_action]
    }

    return jsonify(response)
import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use Render's PORT
    app.run(host='0.0.0.0', port=port)

