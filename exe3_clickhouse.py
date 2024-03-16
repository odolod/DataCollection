from clickhouse_driver import Client
import json

# Загружаем файл данных
with open('books_data.json', 'r') as f:
    books_data = json.load(f)  

# Подключение к серверу ClickHouse
client = Client('localhost')

# Создание базы данных (если она не существует)
client.execute('CREATE DATABASE IF NOT EXISTS books')

# Создание таблицы
client.execute('''
CREATE TABLE IF NOT EXISTS books.toscrape (
    name String,
    price String,
    in_stock UInt64,
    description String
) ENGINE = MergeTree()
ORDER BY name
''')

print("Таблица создана успешно.")

# Вставка данных в таблицу
for book in books_data:
    # Вставка данных о книге
    client.execute("""
    INSERT INTO books.toscrape (
        name, price, in_stock,
        description
    ) VALUES""",
    [(book['name'] or "",
      book['price'] or "",
      book['in_stock'] or 0,
      book['description'] or "")])

print("Данные введены успешно.")

# Проверка успешности вставки
result = client.execute("SELECT * FROM books.toscrape")
print("Вставленная запись:", result[0])
