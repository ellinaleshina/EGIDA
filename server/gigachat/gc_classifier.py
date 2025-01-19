import httpx
import openai
import uuid
from prompt import prompt

def get_api_key(auth_token: str) -> str:
    rq_uid = str(uuid.uuid4())
    httpx_client = httpx.Client(http2=True, verify=False)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": rq_uid,
        "Authorization": f"Basic {auth_token}",
    }
    data = {
        "scope": "GIGACHAT_API_CORP",
    }
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    response = httpx_client.post(url, headers=headers, data=data, follow_redirects=True)
    response.raise_for_status()
    response_json = response.json()
    return response_json.get("access_token")

def send_gigachat_request(prompt: str):
    GIGACHAT_ENDPOINT = "https://gigachat.devices.sberbank.ru/api/v1/"
    GIGACHAT_API_KEY = ""
    httpx_client = httpx.Client(http2=True, verify=False)
    chat = openai.OpenAI(
        api_key=get_api_key(GIGACHAT_API_KEY), base_url=GIGACHAT_ENDPOINT, http_client=httpx_client
    )
    resp = chat.chat.completions.create(
        model="GigaChat",
        messages=[
            {"role": "assistant", "content": prompt},
        ],
    )
    return resp.choices[0].message.content

if __name__ == '__main__':
    text = input("Введите текст для анализа: ")
    response = send_gigachat_request(prompt)
    return response
