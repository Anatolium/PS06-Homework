import requests
from bs4 import BeautifulSoup
import pprint

url = "http://quotes.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 1 – очистка данных — удаление лишних пробелов, спецсимволов, исправление некорректных, повреждённых данных и тд.

# Тег <tr> используется для обозначения строк в таблице HTML
# Переменная rows будет списком объектов BeautifulSoup, каждый из которых представляет одну строку таблицы
rows = soup.find_all("tr")
data = []
for row in rows:
    # Тег <td> используется для обозначения ячеек в ряду таблицы
    cols = row.find_all("td")
    # strip без параметров удаляет только пробелы
    cleaned_cols = [col.text.strip() for col in cols]
    data.append(cleaned_cols)

pprint.pprint(data)

# 2 – преобразование данных — перевод строк в числа и тп

data = [['100', '200', '300'],
        ['400', '500', '600']]

numbers = []
for row in data:
    for text in row:
        number = int(text)
        numbers.append(number)
print(numbers)

# 3 – фильтрация данных — отбор только нужных данных

data = [[100, 110, 120],
        [400, 500, 600],
        [150, 130, 140]]

list1 = []
for row in data:
    for item in row:
        if item > 190:
            list1.append(item)
print(list1)
