from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CLASSIFIER_URL = "http://classifier:5000/classify" #заменить если нужно
LLM_URL = "http://llm:8000/respond" #заменить если нужно 

@app.route('/api/v1/llm-proxy', methods=['POST'])
def llm_proxy():
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "Invalid input"}), 400

    prompt = data.get("prompt", "")

    try:
        classifier_response = requests.post(CLASSIFIER_URL, json={"prompt": prompt})
        classifier_response.raise_for_status()  
        label = classifier_response.json().get("label", "unknown")
    except Exception as e:
        return jsonify({"error": "Classifier service unavailable", "details": str(e)}), 500

    if label == "attack":
        return jsonify({"error": "Malicious input detected"}), 400

    try:
        llm_response = requests.post(LLM_URL, json={"prompt": prompt})
        llm_response.raise_for_status()
        return jsonify(llm_response.json())
    except Exception as e:
        return jsonify({"error": "LLM service unavailable", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
