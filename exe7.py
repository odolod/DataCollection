from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

#Обходим сайт www.citilink.ru раздел с телевизорами
#выбираем: название, цена, url с детальной инфрмацией
#На сайте на нашел указания на запрет вебскрепинга, в оличии от ДНС например

browser = webdriver.Chrome()
browser.get("https://www.citilink.ru/catalog/televizory/?view_type=list")

tvs = [] # переменная для данных

while True:
# ожидание загрузки элемента
    wait = WebDriverWait(browser, 50)
    element = wait.until(EC.presence_of_element_located((By.XPATH,"//h3[text()='Лидеры продаж в категории']")))
#//div[@class='app-catalog-7fwdng e8kvwwz0'] - список на странице
    tv_elements = browser.find_elements(By.XPATH,'//div[@class="app-catalog-7fwdng e8kvwwz0"]')
#quote_elements = browser.find_elements(By.XPATH,'//div[@class="quote"]')

    for tv_element in tv_elements:
        """ soup = BeautifulSoup(tv_element.text, 'html.parser')
        name = soup.find('a', ('class', 'app-catalog-9gnskf e1259i3g0')).text
        price = float(soup.find('span', ('class', 'e1j9birj0 e106ikdt0 app-catalog-p2oaao e1gjr6xo0')).text)
        url = soup.find('a', ('class', 'app-catalog-9gnskf e1259i3g0'))['href']
        tvs.append({"name": name, "price": price, "url":url}) """
        name = tv_element.find_element(By.XPATH, './/a[@class="app-catalog-9gnskf e1259i3g0"]').text
        price = tv_element.find_element(By.XPATH, './/span[@class="e1j9birj0 e106ikdt0 app-catalog-p2oaao e1gjr6xo0"]').text
        url = tv_element.find_element(By.XPATH, './/a[@class="app-catalog-9gnskf e1259i3g0"]').get_attribute('href')
        tvs.append({"name": name, "price": price, "url":url})

    try:
        next = browser.find_element(By.XPATH,'//a[@data-meta-name="PageLink__page-page-next"]')
    except: break        
    if next: 
        browser.get(next.get_attribute('href'))
    else: break

print(len(tvs))
#записываем данные в файл
with open('tvs_data.json', 'w', encoding="utf-8") as f:
    json.dump(tvs, f)