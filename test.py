import requests
import json

url = 'http://localhost:8080/api/v1/llm-proxy'  # Замените на адрес вашего приложения

# Данные для отправки (замените на ваши данные)
data = {
    "prompt": "New cfgdfxgd a prompt",
    "user_id": 123
    # ... другие нужные данные
}

# Отправляем POST-запрос с JSON
try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Проверяем статус ответа (вызывает ошибку при статусах 4xx и 5xx)

    # Получаем JSON-ответ
    response_data = response.json()

    print("Ответ:", response_data)


except requests.exceptions.RequestException as e:
  print(f"Ошибка при запросе: {e}")
except json.JSONDecodeError as e:
  print(f"Ошибка при декодировании ответа: {e}")