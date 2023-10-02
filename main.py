import requests
import xml.etree.ElementTree as ET
import datetime

# Загрузка XML-содержимого по ссылке
current_date = datetime.date.today()
current_date_str = current_date.strftime("%d.%m.%Y")
url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + current_date_str.replace('.', '/')

response = requests.get(url)

# Проверка успешного выполнения запроса
if response.status_code == 200:
    # Разбор XML-содержимого
    xml_content = response.content
    root = ET.fromstring(xml_content)

    # Создание пустого списка для данных
    data = []

    # Проход по элементам XML и извлечение нужных данных
    for valute in root.findall('Valute'):
        name = valute.find('Name').text
        vunit_rate = valute.find('VunitRate').text
        # Преобразование строки в число с двумя знаками после запятой в меньшую сторону
        vunit_rate = round(float(vunit_rate.replace(',', '.')), 2)
        data.append((name, vunit_rate))

    # Теперь переменная 'data' содержит данные в виде списка кортежей
    for name, vunit_rate in data:
        print(f'{vunit_rate} рублей за 1 {name}')
else:
    print("Ошибка при загрузке данных:", response.status_code)
