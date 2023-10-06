# HandyCurrencyBot
Бот предоставляет курс 20 валют в рублях на текущую дату. Данные берутся с сайта Цетрального Банка России (ЦБ РФ).

Токен бота нужно добавить в файл .env в корне прокета в виде BOT_TOKEN=YOU_BOT_TOKEN

Вы можете удалить ненужные валюты или добавить свои, указав их кодовые обозначения.

Логирование настроено в файл HandyCurrencyBot.log в корне проекта (файл нужно создать вручную).

Лог пишется вида:

2023-10-06 00:34:41,477 - INFO - User "tg username" sent message: 'Для получения курса выберите валюту или нажмите кнопку 'Выбрать валюту':'

2023-10-06 00:34:49,446 - INFO - User "tg username" sent message: 'Выбрана валюта: Японская иена (JPY)'

![image](https://github.com/LeoPadre/HandyCurrencyBot/assets/88144121/b44cced8-b2b3-44ea-96be-f6e771932a01)
