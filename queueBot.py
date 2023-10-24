import telebot
from telebot import types

with open('token.txt') as file:
    lines = [line.rstrip() for line in file]
    token = lines[0]

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Возможности", callback_data="possibility")
    button2 = types.InlineKeyboardButton("Команды", callback_data="commands")
    markup.row(button1, button2)
    bot.send_message(message.chat.id,"Привет, я бот для составления очередей. \nТы можешь воспользоваться следующими командами, что бы более подробно узнать что я умею:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def start_message(message):
    commandsList(message)

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == "com_member":
        bot.send_message(callback.message.chat.id, "добавление в БД")
    if callback.data == "com_create":
        bot.send_message(callback.message.chat.id, "создание очереди")

    if callback.data == "possibility":
        bot.send_message(callback.message.chat.id, "когда-нибудь мы это напишем")
    if callback.data == "commands":
        commandsList(callback.message)

def commandsList(message):
    markup = types.InlineKeyboardMarkup()
    com1 = types.InlineKeyboardButton("/member", callback_data="com_member")
    com2 = types.InlineKeyboardButton("/create", callback_data="com_create")
    markup.row(com1, com2)
    bot.send_message(message.chat.id, "можно воспользоваться следующими командами:", reply_markup=markup)

bot.infinity_polling()