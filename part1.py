import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# В отдельной переменной указываем сайт, который будем просматривать
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)
# 3 секунды на загрузку веб-страницы
time.sleep(3)

# Находим все карточки с вакансиями с помощью названия класса
vacancies = driver.find_elements(By.CLASS_NAME, 'vacancy-card--H8LvOiOGPll0jZvYpxIF')
print(vacancies)

title, company, salary, link = "", "", "", ""
parsed_data = []

for vacancy in vacancies:
    try:
        # Находим элементы внутри вакансий по значению
        title = vacancy.find_element(By.CSS_SELECTOR, 'span.vacancy-name--SYbxrgpHgHedVTkgI_cA').text
        # Находим названия компаний
        company = vacancy.find_element(By.CSS_SELECTOR, 'span.company-info-text--O32pGCRW0YDmp3BHuNOP').text
        # Находим зарплаты
        salary = vacancy.find_element(By.CSS_SELECTOR, 'span.compensation-text--cCPBXayRjn5GuLFWhGTJ').text
        salary = salary.replace('\u202f', ' ')
        # Находим ссылку с помощью атрибута 'href'
        link = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link').get_attribute('href')
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

# Вносим найденную информацию в список
parsed_data.append([title, company, salary, link])

with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    # Используем модуль csv, чтобы записывать данные в виде таблицы
    writer = csv.writer(file)
    # Создаём первый ряд
    writer.writerow(['Название вакансии', 'Название компании', 'Зарплата', 'Ссылка на вакансию'])
    # Прописываем использование списка как источника для рядов таблицы
    writer.writerows(parsed_data)

# Закрываем подключение браузер
driver.quit()
