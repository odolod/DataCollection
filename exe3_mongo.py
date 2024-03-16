from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import json

# Загружаем файл данных
with open('books_data.json', 'r') as f:
    books_data = json.load(f)  

# Добываем пароль для подключения
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
password = os.getenv("MONGO_PASSWORD")
uri = "mongodb+srv://od:"+password+"@cluster0.awhrb9b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
cloud_client = MongoClient(uri, server_api=ServerApi('1'))
local_client = MongoClient('mongodb://localhost:27017/')

# Загружаем данные, база данных books и коллекция toscrape 
# созданы вручную в Compass
try:
    cloud_client['books']["toscrape"].insert_many(books_data)
    print("В MongoDB данные загружены в облако")
except Exception as e:
    print(f"Ошибка: {e}")

try:
    local_client['books']["toscrape"].insert_many(books_data)
    print("В MongoDB данные загружены локально")
except Exception as e:
    print(f"Ошибка: {e}")


