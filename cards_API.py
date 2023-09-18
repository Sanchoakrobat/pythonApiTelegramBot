import json
import time
import telebot
import requests
from telebot import types

bot = telebot.TeleBot('6630173318:AAERN7J8yhGM1XfDSyORXKnbNSAG6qEhH9c')


@bot.message_handler(commands=['start'])
def start(message):
    '''Запускает общение, открывает кнопки'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # создаем кнопки под строкой ввода сообщения
    btn1 = types.KeyboardButton("Показать случайную карту")
    btn2 = types.KeyboardButton("Закончить")
    markup.add(btn1, btn2)



    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    time.sleep(1)
    bot.send_message(message.chat.id, 'Я помогу тебе выбрать случайную карту')
    time.sleep(1)
    bot.send_message(message.chat.id, text=f"Используй кнопку ниже 👇".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    '''создает колоду карт на deckofcardsapi.com, берет оттуда карту, скидывает картинку в чат '''
    if (message.text == "Показать случайную карту"):
        deck = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
        # запрос на создание колоды
        data = json.loads(deck.text)
        # записывает данные из json
        deck_id = data["deck_id"]
        # записывает номер в переменную
        card = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1')
        # запрос карты
        data_2 = json.loads(card.text)
        # записывает данные из json
        card_img = data_2["cards"][0]["image"]
        # записывает url карты в переменную
        bot.send_photo(message.chat.id, card_img)
        # отправляет картинку в чат
    elif(message.text == "Закончить"):
        bot.send_message(message.chat.id,
                         f'{message.from_user.first_name}, пока! ✋')
    else:
        bot.send_message(message.chat.id, f'{message.from_user.last_name}, у тебя всё ОК? Просили же нажать на кнопку 🖕')


bot.polling(none_stop=True)
