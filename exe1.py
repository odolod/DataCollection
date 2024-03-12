import requests
import json
import os
from dotenv import load_dotenv

# Учетные данные API
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

client_id = os.getenv("FSQ_CLIENT_ID")
client_secret = os.getenv("FSQ_CLIENT_SECRET")

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса API
query = input("Введите строку поиска: ")
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "near": "Krasnoyarsk",
    "query": query
}

api_token = os.getenv("FSQ_ACCESS_TOKEN")

headers = {
    "Accept": "application/json",
    "Authorization": api_token
}

# Отправка запроса API и получение ответа
response = requests.get(endpoint, params=params,headers=headers)

# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        print("Название:", venue["name"])
        print("Адрес:", venue["location"]["address"])
        print("Рейтинг:", venue["rating"])
        print("\n")
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)
