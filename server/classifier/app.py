from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    prompt = data.get("prompt", "")
    if "attack" in prompt.lower():
        return jsonify({"label": "attack"})
    return jsonify({"label": "safe"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
