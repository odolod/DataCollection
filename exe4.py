import requests
from fake_useragent import UserAgent
import time
import re
import csv
from lxml import etree
from lxml import html

# Запрос веб-страницы
url_main = 'http://books.toscrape.com'
url = 'http://books.toscrape.com/catalogue/page-1.html'

headers = {"User-Agent":UserAgent().chrome}
params = {}

session = requests.session()
links = []
while True:
  page = session.get(url, headers=headers, params=params)
# Парсинг HTML-содержимого веб-страницы с помощью XPath
  tree = html.fromstring(html=page.content)
  
  next_page_link = tree.xpath("//li [@class = 'next']/a/@href") 
  page_list = tree.xpath("//li [@class = 'col-xs-6 col-sm-4 col-md-3 col-lg-3']")  
  
  for book in page_list:
    book = html.fromstring(html.tostring(book))
    links.append(url_main + '/catalogue/' + book.xpath("//h3/a/@href")[0])

  if not next_page_link:
    break
  #Адрес следуюшей
  url = url_main + '/catalogue/' + next_page_link[0]
  #Задержка запроса  
  #time.sleep(1)

#Количество книг
print(len(links))

result = []
result.append(['name', 'price', 'in_stock', 'description'])
#Собираем данные по книгам
for link in links:
  page = session.get(link, headers=headers)
  book = html.fromstring(html=page.content) 
  book_name = book.xpath("//h1/text()")[0]  
  book_price = book.xpath("//p [@class = 'price_color']/text()")[0] 
  book_in_stock = int(re.findall(r'\b\d+\b', book.xpath("//p/text()")[2])[0])
  book_descripion = book.xpath("//p/text()")[10]

  result.append([book_name, book_price, book_in_stock, book_descripion])
 
session.close()

#Пишем в файл csv
with open('books_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(result)

