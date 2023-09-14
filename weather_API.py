import json
import telebot
import requests


bot = telebot.TeleBot('6310565927:AAEa9h0dSGrkWbGYEvRkNi2sKX9Xl-MkyyM')
# токен, выданный FatherBot
API = 'a45d70066eb39dc6ddf54811e7ec1172'
# апи-ключ с сайта погоды https://openweathermap.org/current

@bot.message_handler(commands=['start'])
# декоратор
def start(message):
    """кнопка старт вызывает приветствие и просьбу написать город"""
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    bot.send_message(message.chat.id, 'Напиши название города')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    """запрос на сервер по АПИ с названием города.
    Ответ в виде JSON из которого пользователь получает данные о температуре,
    влажности и давленнии в данный момент"""
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        bot.reply_to(message, f'''В данный момент в городе {city.title()} Температура = {temp} С 
                                                                Давление = {pressure} МПа  
                                                                Влажность = {humidity} %''' )
    else:
        bot.reply_to(message, f'Город указан не верно😔')
        # если город указан неверно или его нет в списке


bot.polling(none_stop=True)
