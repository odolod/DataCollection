import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import re
import json

# Запрос веб-страницы
#url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
url_main = 'http://books.toscrape.com'
url = 'http://books.toscrape.com/catalogue/page-1.html'

headers = {"User-Agent":UserAgent().chrome}
params = {}

session = requests.session()
links = []
while True:
  page = session.get(url, headers=headers, params=params)
# Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
  soup = BeautifulSoup(page.content, 'html.parser')
  next_page_link = soup.find('li', ('class', 'next'))

  page_list = soup.find_all('li', ('class', 'col-xs-6 col-sm-4 col-md-3 col-lg-3')) 
  #print(soup.find('li', ('class', 'current')).text)
  for book in page_list:
    links.append(url_main + '/catalogue/' + book.find('h3').findChild()['href'])
  
  if not next_page_link:
    break
  #Адрес следуюшей
  url = url_main + '/catalogue/' + next_page_link.findChild()['href']
  #Задержка запроса  
  #time.sleep(1)

#Количество книг
print(len(links))

result = []

for link in links:
  page = session.get(link, headers=headers)
  soup = BeautifulSoup(page.content, 'html.parser')
  book_name = soup.find('h1').text
  book_price = soup.find('p', ('class', 'price_color')).text
  book_in_stock = int(re.findall(r'\b\d+\b', soup.find('p', ('class', 'instock availability')).text)[0])
  book_descripion = soup.find_all('p')[3].text
  result.append({'name':book_name, 'price':book_price, 'in_stock':book_in_stock, 'description':book_descripion})
 
session.close()

with open('books_data.json', 'w') as f:
    json.dump(result, f)

