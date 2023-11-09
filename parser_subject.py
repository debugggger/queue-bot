from bot import bot
from telebot import types

c_callback_prefix_removesubject = 'removesubject_'

subjects = [] # TODO connect DB

subject_user_list = []
removesubject_user_list = []


def command_subject(message):
    bot.send_message(message.chat.id, 'Введите название нового предмета')
    subject_user_list.append(message.from_user.id)

def command_removesubject(message):
    buttons = []
    for subject in subjects:
        buttons.append([types.InlineKeyboardButton(subject, callback_data=c_callback_prefix_removesubject+subject)])
    markup = types.InlineKeyboardMarkup(buttons)
    bot.send_message(message.chat.id, 'Удалить предмет', reply_markup=markup)

    removesubject_user_list.append(message.from_user.id)

def callback_removesubject(callback):
    if callback.from_user.id not in removesubject_user_list:
        return
    
    subject = callback.data.removeprefix(c_callback_prefix_removesubject)
    bot.send_message(callback.message.chat.id, 'Предмет ' + subject + ' удален')
    subjects.remove(subject)
    removesubject_user_list.remove(callback.from_user.id)

def text_handler_subject(message):
    if message.from_user.id not in subject_user_list:
        return 
    bot.send_message(message.chat.id, 'Предмет ' + message.text + ' добавлен')
    subjects.append(message.text)
    subject_user_list.remove(message.from_user.id)

def init_subject(bot):
    bot.message_handler(commands=['subject']) (command_subject)
    bot.message_handler(commands=['removesubject']) (command_removesubject)
    bot.callback_query_handler(func = lambda callback: callback.data.startswith(c_callback_prefix_removesubject)) (callback_removesubject)
