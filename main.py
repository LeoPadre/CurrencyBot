import xml.etree.ElementTree as ET
from datetime import date
import telebot
from telebot import types
from decouple import config
import aiohttp
import asyncio
import logging

# Настройка логгирования
logging.basicConfig(filename='HandyCurrencyBot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Чтение токена из переменных окружения
BOT_TOKEN = config('BOT_TOKEN')

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения полных названий валют
currency_names = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "GBP": "Фунт стерлингов",
    "AUD": "Австралийский доллар",
    "AZN": "Азербайджанский манат",
    "AMD": "Армянский драм",
    "BYN": "Белорусский рубль",
    "GEL": "Грузинский лари",
    "AED": "Дирхам ОАЭ",
    "INR": "Индийская рупия",
    "KZT": "Казахстанский тенге",
    "CNY": "Китайский юань",
    "TJS": "Таджикский сомони",
    "TRY": "Турецкая лира",
    "UZS": "Узбекский сум",
    "UAH": "Украинская гривна",
    "JPY": "Японская иена",
    "KRW": "Вон Республики Корея",
    "CHF": "Швейцарский франк",
    "SEK": "Шведская крона"
}

# Функция для получения курса валюты
async def get_currency_rate(currency_code):
    current_date = date.today()
    current_date_str = current_date.strftime("%d/%m/%Y")
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={current_date_str}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            if response.status == 200:
                xml_content = await response.text()
                root = ET.fromstring(xml_content)

                for valute in root.findall('Valute'):
                    char_code = valute.find('CharCode').text
                    if char_code == currency_code:
                        name = valute.find('Name').text
                        vunit_rate = valute.find('VunitRate').text
                        vunit_rate = round(float(vunit_rate.replace(',', '.')), 2)
                        return f'<b>🇷🇺 {vunit_rate} рублей за 1 {currency_names[currency_code]}</b>'
            else:
                return "Ошибка при загрузке данных"

# Функция для отправки кнопки "Выбрать валюту"
def send_choose_currency_button(chat_id):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Выбрать валюту", callback_data="choose_currency")
    markup.add(button)
    bot.send_message(chat_id, "Для получения курса выберите валюту или нажмите кнопку 'Выбрать валюту':", reply_markup=markup, parse_mode='HTML')

# Функция для отправки клавиатуры с выбором валюты
def send_currency_selection_keyboard(chat_id):
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

    bot.send_message(chat_id, "Выберите валюту:", reply_markup=markup)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username  # Получаем имя пользователя
    log_activity(message, username)  # Логгирование активности с именем пользователя
    send_choose_currency_button(message.chat.id)  # Отправляем кнопку "Выбрать валюту"

# Обработчик выбора валюты или кнопки "Выбрать валюту"
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "choose_currency":
        username = call.from_user.username  # Получаем имя пользователя
        log_activity(call.message, username)  # Логгирование активности с именем пользователя
        send_currency_selection_keyboard(call.message.chat.id)  # Отправляем клавиатуру с выбором валюты
    else:
        currency_code = call.data
        username = call.from_user.username
        user_message = f"Выбрана валюта: {currency_names[currency_code]} ({currency_code})"

        async def send_currency_rate():
            currency_rate = await get_currency_rate(currency_code)
            bot.send_message(call.message.chat.id, currency_rate, parse_mode='HTML')  # Выделяем текст жирным
            send_choose_currency_button(call.message.chat.id)  # После вывода курса, предлагаем выбрать другую валюту
            log_activity(call.message, username, user_message)  # Логгирование активности с выбранной валютой

        asyncio.run(send_currency_rate())

# Функция для логгирования активности
def log_activity(message, username=None, user_message=None):
    username = username or message.from_user.username
    activity = f"User {username} sent message: '{user_message or message.text}'"

    logging.info(activity)

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
