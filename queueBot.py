import telebot
from telebot import types

from bot import bot

import parser_subject
parser_subject.init_subject(bot)

setNameList = []
sendedMemberList = []
createQueueList = []

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    parser_subject.text_handler_subject(message)

    if message.from_user.id in setNameList:
        name = message.text
        bot.send_message(message.chat.id, "@" + message.from_user.username + " твое отоброжаемое имя " + name)
        setNameList.remove(message.from_user.id)
    # if message.from_user.id in createQueueList:
    #     name = message.text
    #     bot.send_message(message.chat.id, "Создана очередь по " + name)
    #     createQueueList.remove(message.from_user.id)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Возможности", callback_data="possibility")
    button2 = types.InlineKeyboardButton("Команды", callback_data="commands")
    markup.row(button1, button2)
    bot.send_message(message.chat.id,"Привет, я бот для составления очередей. \nТы можешь воспользоваться следующими командами, что бы более подробно узнать что я умею:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_message(message):
    commandsList(message)

@bot.message_handler(commands=['create'])
def create_message(message):
    createCommand(message)

@bot.message_handler(commands=['member'])
def member_message(message):
    memberCommand(message)



@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == "help_member":
        memberCommand(callback.message)
        # markup = types.InlineKeyboardMarkup()
        # button1 = types.InlineKeyboardButton("Ввод", callback_data="member_add")
        # button2 = types.InlineKeyboardButton("Отмена", callback_data="member_cancel")
        # markup.row(button1, button2)
        # bot.send_message(callback.message.chat.id, "Ты можешь ввести имя, которое будет отображаться при выводе очереди:",
        #                   reply_markup=markup)
    if callback.data == "help_create":
        createCommand(callback.message)
    if callback.data == "possibility":
        bot.send_message(callback.message.chat.id, "когда-нибудь мы это напишем")
    if callback.data == "commands":
        commandsList(callback.message)
    if callback.data == "member_cancel":
        bot.delete_message(callback.message.chat.id, callback.message.id)
    if callback.data == "create_cancel":
        bot.delete_message(callback.message.chat.id, callback.message.id)
    if callback.data == "member_add":
        setNameList.append(callback.message.from_user.id)

def commandsList(message):
    markup = types.InlineKeyboardMarkup()
    com1 = types.InlineKeyboardButton("/member", callback_data="help_member")
    com2 = types.InlineKeyboardButton("/create", callback_data="help_create")
    markup.row(com1, com2)
    bot.send_message(message.chat.id, "можно воспользоваться следующими командами:", reply_markup=markup)

def memberCommand(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Ввод", callback_data="member_add")
    button2 = types.InlineKeyboardButton("Отмена", callback_data="member_cancel")
    markup.row(button1, button2)
    bot.send_message(message.chat.id, "Ты можешь ввести имя, которое будет отображаться при выводе очереди:",
                     reply_markup=markup)

def createCommand(message):
    markup = types.InlineKeyboardMarkup()
    # button1 = types.InlineKeyboardButton("Ввод", callback_data="member_add")
    button2 = types.InlineKeyboardButton("Отмена", callback_data="create_cancel")
    markup.row(button2)
    bot.send_message(message.chat.id, "По какому предмету ты хочешь создать очередь?:", reply_markup=markup)
    createQueueList.append(message.from_user.id)

bot.infinity_polling()