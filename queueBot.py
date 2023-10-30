import telebot
from telebot import types

with open('token.txt') as file:
    lines = [line.rstrip() for line in file]
    token = lines[0]

bot=telebot.TeleBot(token)

setNameList = []


@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    if message.from_user.id in setNameList:
        name = message.text
        bot.send_message(message.chat.id, "@" + message.from_user.username + " твое отоброжаемое имя " + name)
        setNameList.remove(message.from_user.id)

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

@bot.message_handler(commands=['member'])
def member_message(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Ввод", callback_data="member_add")
    button2 = types.InlineKeyboardButton("Отмена", callback_data="member_cancel")
    markup.row(button1, button2)
    bot.send_message(message.chat.id,"Ты можешь ввести имя, которое будет отображаться при выводе очереди:", reply_markup=markup)
    setNameList.append(message.from_user.id)


@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == "help_member":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Ввод", callback_data="member_add")
        button2 = types.InlineKeyboardButton("Отмена", callback_data="member_cancel")
        markup.row(button1, button2)
        bot.send_message(callback.message.chat.id, "Ты можешь ввести имя, которое будет отображаться при выводе очереди:",
                          reply_markup=markup)

    if callback.data == "help_create":
        bot.send_message(callback.message.chat.id, "создание очереди")

    if callback.data == "possibility":
        bot.send_message(callback.message.chat.id, "когда-нибудь мы это напишем")
    if callback.data == "commands":
        commandsList(callback.message)
    if callback.data == "member_cancel":
        bot.delete_message(callback.message.chat.id, callback.message.id)

def commandsList(message):
    markup = types.InlineKeyboardMarkup()
    com1 = types.InlineKeyboardButton("/member", callback_data="help_member")
    com2 = types.InlineKeyboardButton("/create", callback_data="help_create")
    markup.row(com1, com2)
    bot.send_message(message.chat.id, "можно воспользоваться следующими командами:", reply_markup=markup)

bot.infinity_polling()