import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

choices = [
    {"url": "https://www.divan.ru/category/svet", "file": "divan_lights.csv"},
    {"url": "https://www.divan.ru/category/kovry", "file": "divan_carpets.csv"},
    {"url": "https://www.divan.ru/category/kompyuternye-kresla-i-stulya", "file": "divan_chairs.csv"},
    {"url": "https://www.divan.ru/category/sadovaya-mebel", "file": "divan_garden.csv"},
    {"url": "https://www.divan.ru/category/promo-flowers", "file": "divan_sale.csv"}
]

choice = 0
while True:
    print("1. Освещение")
    print("2. Ковры")
    print("3. Компьютерные кресла")
    print("4. Садовая мебель")
    print("5. Товары по акции")
    try:
        choice = int(input("Выберите категорию товара: "))
    except ValueError:
        print("\n---> Введите число от 1 до 5")
        continue
    else:
        if choice in range(1, 6):
            break
        print("\n---> Введите число от 1 до 5")
        continue

goods_url = choices[choice - 1].get("url")
csv_file = choices[choice - 1].get("file")

driver = webdriver.Chrome()
parsed_data = []

# Парсим открытую страницу
def get_goods_info():
    goods = driver.find_elements(By.CSS_SELECTOR, 'div._Ud0k')
    for item in goods:
        try:
            name = item.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text
            price = item.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute('content')
            link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            continue
        else:
            parsed_data.append([name, price, link])

# Открываем все страницы выбранной категории, иначе получим не более 48 товаров
page = 1
while True:
    if requests.get(goods_url).status_code != 200:
        break
    driver.get(goods_url)
    time.sleep(3)

    get_goods_info()

    page += 1
    goods_url = f"{choices[choice - 1].get('url')}/page-{page}"

# Запись данных
if len(parsed_data):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена', 'Ссылка на товар'])
        writer.writerows(parsed_data)
    print(f"---> Найдено {len(parsed_data)} товаров")
else:
    print("Данные не найдены")

driver.quit()
