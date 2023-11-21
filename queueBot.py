from typing import Dict, Callable, List
import os
import time

import telebot
from telebot import types
from dotenv import load_dotenv

from db import Database

from Requests.QueueEntity import QueueEntity
from Requests.QueueFun import QueueFun
from Requests.SubjectHandlers import SubjectHandlers
from Requests.UserHandlers import UserHandlers
from Requests.RuntimeInfoManager import RuntimeInfoManager

load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
botDB = Database()

chatId = None if os.getenv('chat_id') is None else int(os.getenv('chat_id'))

runtimeInfoManager = RuntimeInfoManager()

subjectHandlers = SubjectHandlers(bot, botDB, runtimeInfoManager)
userHandlers = UserHandlers(bot, botDB, runtimeInfoManager)

qEntity = QueueEntity(bot, botDB)
qFun = QueueFun(bot, botDB)


def possibilityCommand(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     "Бот, который поможет тебе не потеряться в бесконечных "
                     "очередях.🤡\n С его помощью ты можешь создать очередь и "
                     "добавиться в нее, вывести список добавленных пользователей."
                     " Бот позволяет не только выйти из очереди, если ты захотел "
                     "пойти на допсу, но и поменяться с другим человеком, если, "
                     "конечно, он будет на это согласен😈"
                     )

def commandsList(message):
    bot.send_message(message.chat.id,
                     "можно воспользоваться следующими командами:\n"
                     "/member - добавление в список пользователей\n"
                     "/show - вывод очерди\n"
                     "/create - создание очереди\n"
                     "/join - запись в последнюю очередь\n"
                     "/jointo - запись в любую из очередей\n"
                     "/delete - удаление очереди")

def startCommand(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Возможности", callback_data="possibility")
    button2 = types.InlineKeyboardButton("Команды", callback_data="commands")
    markup.row(button1, button2)
    bot.send_message(message.chat.id,
                     "Привет! Я бот для составления очередей.\nТы можешь воспользоваться следующими "
                     "командами, чтобы более подробно узнать что я умею:",
                     reply_markup=markup)

def deleteMessage(message: telebot.types.Message):
    bot.delete_message(message.chat.id, message.id)


commandHandlers: Dict[str, Callable[[telebot.types.Message], None]] = {
    '/start': startCommand,
    '/help': commandsList,
    '/create': qEntity.createCommand,
    '/delete': qEntity.deleteCommand,
    '/member': userHandlers.memberCommand,
    '/show': qEntity.showCommand,
    '/jointo': qFun.jointoCommand,
    '/join': qFun.joinCommand,
    '/subject': subjectHandlers.subjectCommand,
    '/removesubject': subjectHandlers.removesubjectCommand,
}

callbackHandlers: Dict[str, Callable[[telebot.types.CallbackQuery], None]] = {
    'createNum_': qEntity.createCallback,
    'deleteNum_': qEntity.deleteCallback,
    'showNum_': qEntity.showCallback,
    'jointoNum_': qFun.jointoCallback,

    'help_member': lambda c: userHandlers.memberCommand(c.message),
    'help_show': lambda c: qEntity.showCommand(c.message),
    'help_delete': lambda c: qEntity.deleteCommand(c.message),
    'help_create': lambda c: qEntity.createCommand(c.message),
    'help_join': lambda c: qFun.joinCommand(c.message),
    'help_jointo': lambda c: qFun.jointoCommand(c.message),
    'commands': lambda c: commandsList(c.message),
    'possibility': lambda c: possibilityCommand(c.message),

    'member_cancel': lambda c: deleteMessage(c.message),
    'show_cancel': lambda c: deleteMessage(c.message),
    'create_cancel': lambda c: deleteMessage(c.message),
    'delete_cancel': lambda c: deleteMessage(c.message),
    'jointo_cancel': lambda c: deleteMessage(c.message),

    'join_back': qFun.joinBackCallback,
    'join_first': qFun.joinFirstCallback,
    'join_certain': qFun.joinCertainCallback,
    'join_last': qFun.joinLastCallback,
}

textHandlers: List[Callable[[telebot.types.Message], None]] = {
    subjectHandlers.subjectTextHandler,
    userHandlers.setNameTextHandler,
    qFun.joinTextHandler,
}

@bot.message_handler(commands=['debug_chatid'])
def commandsHandler(message: telebot.types.Message):
    if time.time() - message.date > 3:
        return

    bot.send_message(message.chat.id, f'chat_id = {message.chat.id}')


@bot.message_handler(func=lambda message: message.text.startswith('/'))
def commandsHandler(message: telebot.types.Message):
    if time.time() - message.date > 3:
        return
    if chatId and (message.chat.id != chatId):
        return
    if message.text in commandHandlers.keys():
        commandHandlers[message.text](message)

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback: telebot.types.CallbackQuery):
    if time.time() - callback.message.date > 3:
        return
    if chatId and (callback.chat.id != chatId):
        return
    for key, handler in callbackHandlers.items():
        if callback.data.startswith(key):
            handler(callback)

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message: telebot.types.Message):
    if time.time() - message.date > 3:
        return
    if chatId and (message.chat.id != chatId):
        return
    for textHandler in textHandlers:
        textHandler(message)

@bot.message_handler(content_types=['left_chat_member'])
def handle_left_chat_member(message: telebot.types.Message):
    if time.time() - message.date > 3:
        return
    if chatId and (message.chat.id != chatId):
        return
    user_id = message.left_chat_member.id
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Пользователь с ID {user_id} покинул чат.")


bot.infinity_polling()
