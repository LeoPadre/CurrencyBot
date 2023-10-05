import requests
import xml.etree.ElementTree as ET
from datetime import date
import telebot
from telebot import types
from decouple import config

# Чтение токена из переменных окружения
BOT_TOKEN = config('BOT_TOKEN')


# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для получения курса валюты
def get_currency_rate(currency_code):
    current_date = date.today()
    current_date_str = current_date.strftime("%d/%m/%Y")
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={current_date_str}"
    response = requests.get(url)

    if response.status_code == 200:
        xml_content = response.content
        root = ET.fromstring(xml_content)

        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            if char_code == currency_code:
                name = valute.find('Name').text
                vunit_rate = valute.find('VunitRate').text
                vunit_rate = round(float(vunit_rate.replace(',', '.')), 2)
                return f'{vunit_rate} рублей за 1 {name}'
    else:
        return "Ошибка при загрузке данных"

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton("USD", callback_data='USD')
    item2 = types.InlineKeyboardButton("EUR", callback_data='EUR')
    item3 = types.InlineKeyboardButton("GBP", callback_data='GBP')
    item4 = types.InlineKeyboardButton("AUD", callback_data='AUD')
    item5 = types.InlineKeyboardButton("AZN", callback_data='AZN')
    item6 = types.InlineKeyboardButton("AMD", callback_data='AMD')
    item7 = types.InlineKeyboardButton("BYN", callback_data='BYN')
    item8 = types.InlineKeyboardButton("GEL", callback_data='GEL')
    item9 = types.InlineKeyboardButton("AED", callback_data='AED')
    item10 = types.InlineKeyboardButton("INR", callback_data='INR')
    item11 = types.InlineKeyboardButton("KZT", callback_data='KZT')
    item12 = types.InlineKeyboardButton("CNY", callback_data='CNY')
    item13 = types.InlineKeyboardButton("TJS", callback_data='TJS')
    item14 = types.InlineKeyboardButton("TRY", callback_data='TRY')
    item15 = types.InlineKeyboardButton("UZS", callback_data='UZS')
    item16 = types.InlineKeyboardButton("UAH", callback_data='UAH')
    item17 = types.InlineKeyboardButton("JPY", callback_data='JPY')
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13, item14, item15, item16, item17)
    bot.send_message(message.chat.id, "Привет! Я бот, который предоставляет курсы валют. Выберите валюту:", reply_markup=markup)

# Обработчик выбора валюты
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    currency_code = call.data
    currency_rate = get_currency_rate(currency_code)
    bot.send_message(call.message.chat.id, currency_rate)

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
