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
                return f'🇷🇺 {vunit_rate} рублей за 1 {name}'
    else:
        return "Ошибка при загрузке данных"

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    currencies = [
        ("USD", "🇺🇸"), ("EUR", "🇪🇺"), ("GBP", "🇬🇧"), ("AUD", "🇦🇺"), ("AZN", "🇦🇿"),
        ("AMD", "🇦🇲"), ("BYN", "🇧🇾"), ("GEL", "🇬🇪"), ("AED", "🇦🇪"), ("INR", "🇮🇳"),
        ("KZT", "🇰🇿"), ("CNY", "🇨🇳"), ("TJS", "🇹🇯"), ("TRY", "🇹🇷"), ("UZS", "🇺🇿"),
        ("UAH", "🇺🇦"), ("JPY", "🇯🇵"), ("KRW", "🇰🇷"), ("CHF", "🇨🇭"), ("SEK", "🇸🇪")
    ]

    row_width = 4
    for i in range(0, len(currencies), row_width):
        row = currencies[i:i+row_width]
        buttons = [types.InlineKeyboardButton(f"{flag} {currency}", callback_data=currency) for currency, flag in row]
        markup.row(*buttons)

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
