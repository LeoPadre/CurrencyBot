import requests
import xml.etree.ElementTree as ET
import datetime

# Загрузить XML-содержимое по ссылке
current_date = datetime.date.today()
current_date_str = current_date.strftime("%d.%m.%Y")
url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + current_date_str.replace('.', '/')

response = requests.get(url)

# Проверить, что запрос прошел успешно
if response.status_code == 200:
    # Разобрать XML-содержимое
    xml_content = response.content
    root = ET.fromstring(xml_content)

    # Создать пустой список для данных
    data = []

    # Пройти по элементам XML и извлечь нужные данные
    for valute in root.findall('Valute'):
        name = valute.find('Name').text>
        vunit_rate = valute.find('VunitRate').text
        # Преобразовать строку в число с двумя знаками после запятой в меньшую сторону
        vunit_rate = round(float(vunit_rate.replace(',', '.')), 2)
        data.append((name, vunit_rate))

    # Теперь переменная 'data' содержит данные в виде списка кортежей
    for name, vunit_rate in data:
        print(f'{vunit_rate} рублей за 1 {name}')
else:
    print("Ошибка при загрузке данных:", response.status_code)
