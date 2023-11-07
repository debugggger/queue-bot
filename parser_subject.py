from bot import bot
from telebot import types

user_list = []

def command_subject(message):
    bot.send_message(message.chat.id, 'Введите название нового предмета')
    user_list.append(message.from_user.id)

def text_handler_subject(message):
    if message.from_user.id in user_list:
        bot.reply_to(message, 'Предмет ' + message.text + ' добавлен')
        user_list.remove(message.from_user.id)

def init_subject(bot):
    bot.message_handler(commands=['subject']) (command_subject)
