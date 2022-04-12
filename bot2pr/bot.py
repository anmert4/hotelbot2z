import telebot
import sqlite3
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bot = telebot.TeleBot('5196018446:AAF88bQCX7Fxg2UsH3D1MhwXs-sXsEGhQ1s')
conn = sqlite3.connect("db.db", check_same_thread = False)
cursor = conn.cursor()

def menu():
    kb = types.ReplyKeyboardMarkup(True,False)
    kb.add("Где мой номер?", "О гостинице")
    kb.add("Услуги гостиницы", "Обратная связь")
    return kb

def rooms_markup():
    room = InlineKeyboardMarkup()
    room.row_width = 17
    room.add(InlineKeyboardButton("1", callback_data="1"), 
    InlineKeyboardButton("2", callback_data="2"),
    InlineKeyboardButton("3", callback_data="3"),
    InlineKeyboardButton("4", callback_data="4"),
    InlineKeyboardButton("5", callback_data="5"),
    InlineKeyboardButton("6", callback_data="6"),
    InlineKeyboardButton("7", callback_data="7"),
    InlineKeyboardButton("8", callback_data="8"),
    InlineKeyboardButton("9", callback_data="9"),
    InlineKeyboardButton("10", callback_data="10"),
    InlineKeyboardButton("11", callback_data="11"),
    InlineKeyboardButton("12", callback_data="12"),
    InlineKeyboardButton("13", callback_data="13"),
    InlineKeyboardButton("14", callback_data="14"),
    InlineKeyboardButton("15", callback_data="15"),
    InlineKeyboardButton("16", callback_data="16"),
    InlineKeyboardButton("17", callback_data="17"))
    return room

def services_markup():
    service = InlineKeyboardMarkup()
    service.row_width = 2
    service.add(InlineKeyboardButton("SPA-центр", url="https://sunny-hotel-spa.ru/spa"), 
    InlineKeyboardButton("Барбекю площадки", url="https://sunny-hotel-spa.ru/uslugi"),
    InlineKeyboardButton("Рестораны и бары", url="https://sunny-hotel-spa.ru/restorani_i_bari"),
    InlineKeyboardButton("Детям", url="https://sunny-hotel-spa.ru/detyam"))
    return service

@bot.message_handler(commands=['start','help'])
def start(message):
    bot.send_message(message.chat.id, text='Выберите интересующую вас услугу', reply_markup = menu())

@bot.message_handler(regexp="О гостинице")
def about(message):
    cursor.execute('SELECT `info`,`photo` FROM `about` WHERE id = 1')
    rows = cursor.fetchall()
    photo = open(rows[0][1], 'rb')
    bot.send_photo(message.from_user.id, photo, caption = rows[0][0])
    bot.send_photo(message.from_user.id, "FILEID")
    bot.register_next_step_handler(message, start)

@bot.message_handler(regexp="Где мой номер?")
def rooms(message):
    bot.send_message(message.chat.id, text='Выберите комнату', reply_markup = rooms_markup())

@bot.callback_query_handler(func=lambda call: True)
def room_query(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    cursor.execute('SELECT `info`,`photo` FROM `room` WHERE id = (?)', (call.data,))
    rows = cursor.fetchall()
    photo = open(rows[0][1], 'rb')
    bot.send_photo(call.message.chat.id, photo, caption = rows[0][0])
    bot.send_photo(call.message.chat.id, "FILEID")

@bot.message_handler(regexp="Услуги гостиницы")
def services(message):
    bot.send_message(message.chat.id, text='Выберите услугу', reply_markup = services_markup())

def feedback_markup():
    feedback = InlineKeyboardMarkup()
    feedback.row_width = 1
    feedback.add(InlineKeyboardButton("У меня возникли вопросы", url="https://sunny-hotel-spa.ru/"))
    return feedback

@bot.message_handler(regexp="Обратная связь")
def feedback(message):
    bot.send_photo(message.from_user.id, open('photos/h.jpg','rb'), caption = 'Если у вас возникли вопросы нажмите на кнопку ниже', reply_markup = feedback_markup())
    bot.send_photo(message.from_user.id, "FILEID")

if __name__ == '__main__':
    bot.polling(none_stop=True,interval=0)