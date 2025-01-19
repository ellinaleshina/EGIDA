from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/respond', methods=['POST'])
def respond():
    data = request.json
    prompt = data.get("prompt", "")
    return jsonify({"response": f"You sent: {prompt}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)