from flask import Flask, request, jsonify
import requests
import httpx
import uuid

app = Flask(__name__)

GIGACHAT_OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
GIGACHAT_ENDPOINT = "https://gigachat.devices.sberbank.ru/api/v1/"
GIGACHAT_API_KEY = "ODAzN2I3ZWMtZjQ2YS00OTNlLTg2MzktNmI4OTE1NjA1ZmQxOjk5MDgyNWEyLTkxYzctNDQ0OC04ZjE1LTMzOTRmMTA5OTYxMA=="
URL= 'http://172.18.0.3:8000/respond'
logger_URL= 'http://172.18.0.4:8025/logger'

def get_api_key(auth_token: str) -> str:
    rq_uid = str(uuid.uuid4())
    httpx_client = httpx.Client(http2=True, verify=False)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": rq_uid,
        "Authorization": f"Basic {auth_token}",
    }
    data = {"scope": "GIGACHAT_API_CORP"}

    response = httpx_client.post(GIGACHAT_OAUTH_URL, headers=headers, data=data, follow_redirects=True)
    response.raise_for_status()
    return response.json().get("access_token")


def send_gigachat_request(prompt: str, auth_token: str):
    access_token = get_api_key(auth_token)
    httpx_client = httpx.Client(http2=True, verify=False)
    chat = httpx_client.post(
        f"{GIGACHAT_ENDPOINT}chat/completions",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "model": "GigaChat",
            "messages": [{"role": "assistant", "content": prompt}],
        },
    )
    chat.raise_for_status()
    return chat.json().get("choices")[0].get("message").get("content")


@app.route('/api/v1/llm-proxy', methods=['POST'])
def llm_proxy():
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "Invalid input"})
    prompt = data.get("prompt", "")
    try:
       # classification_result = send_gigachat_request(prompt, GIGACHAT_API_KEY)
        classification_result="safe"
        try:
            log_status = requests.post(logger_URL, json={"prompt": prompt, "label": classification_result.lower()})
        except Exception as e:
            return jsonify({"error": "log is not correct", "details": str(e)})
        #log_status.raise_for_status()
        if classification_result.lower() == "unsafe":
            return jsonify({"error": "Malicious input detected"}), 400   
    except Exception as e:
       return jsonify({"error": "Gigachat service unavailable", "details": str(e)})
    try:
        llm_response = requests.post(URL, json={"prompt": prompt})
        llm_response.raise_for_status()
        return jsonify(llm_response.json())
    except Exception as e:
        return jsonify({"error": "LLM service unavailable", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
