from typing import Dict, Callable, List
import os
import time

import telebot
from telebot import types
from dotenv import load_dotenv
from Requests.RemoveHandlers import RemoveHandlers
from Requests.ReplaceHandlers import ReplaceHandlers
from Services.MemberService import MemberService
from Services.QueueService import QueueService

from db import Database

from Requests.QueueEntity import QueueEntity
from Requests.QueueFun import QueueFun
from Requests.SubjectHandlers import SubjectHandlers
from Requests.UserHandlers import UserHandlers
from Requests.RuntimeInfoManager import RuntimeInfoManager
from utils import checkMessage, updateLastQueueText

load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
botDB = Database()

chatId = None if os.getenv('chat_id') is None else int(os.getenv('chat_id'))

runtimeInfoManager = RuntimeInfoManager()

subjectHandlers = SubjectHandlers(bot, botDB, runtimeInfoManager)
userHandlers = UserHandlers(bot, botDB, runtimeInfoManager)
removeHandlers = RemoveHandlers(bot, botDB, runtimeInfoManager)
replaceHandlers = ReplaceHandlers(bot, botDB, runtimeInfoManager)

qFun = QueueFun(bot, botDB, runtimeInfoManager)
qEntity = QueueEntity(bot, botDB, runtimeInfoManager)

def possibilityCommand(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     "Бот, который поможет тебе не потеряться в бесконечных "
                     "очередях.🤡\n С его помощью ты можешь создать очередь и "
                     "добавиться в нее, вывести список добавленных пользователей."
                     " Бот позволяет не только выйти из очереди, если ты захотел "
                     "пойти на допсу, но и поменяться с другим человеком, если, "
                     "конечно, он будет на это согласен😈"
                     )

# member - добавление в список пользователей
# subject - добавление предмета
# create - создание очереди
# delete - удаление очереди
# show - вывод очереди
# join - запись в последнюю очередь
# jointo - запись в любую из очередей
# replaceto - смена мест
# replace - смена места в последней очереди
# removefrom - выход из очереди
# reject - отклонение запроса смены мест
# confirm - подтверждение запроса смены мест

def commandsList(message):
    bot.send_message(message.chat.id,
                     "можно воспользоваться следующими командами:\n"
                     "/member - добавление в список пользователей\n"
                     "/subject - добавление предмета\n"
                     "/create - создание очереди\n"
                     "/delete - удаление очереди\n"
                     "/show - вывод очереди\n"
                     "/join - запись в последнюю очередь\n"
                     "/jointo - запись в любую из очередей\n"                     
                     "/replaceto - смена мест c выбором очереди\n"
                     "/replace - смена места в последней очереди\n"
                     "/removefrom - выход из очереди\n"
                     "/reject - отклонение запроса смены мест\n"
                     "/confirm - подтверждение запроса смены мест\n")

def startCommand(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Возможности", callback_data="possibility")
    button2 = types.InlineKeyboardButton("Команды", callback_data="commands")
    markup.row(button1, button2)
    bot.send_message(message.chat.id,
                     "Привет! Я бот для составления очередей.\nТы можешь воспользоваться следующими "
                     "командами, чтобы более подробно узнать что я умею:",
                     reply_markup=markup)

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
    '/removefrom': removeHandlers.removefromCommand,
    '/replaceto': replaceHandlers.replacetoCommand,
    '/replace': replaceHandlers.replaceCommand,
    '/reject': replaceHandlers.rejectCommand,
    '/confirm': replaceHandlers.confirmCommand,

    '/start@queeeeueeee_bot': startCommand,
    '/help@queeeeueeee_bot': commandsList,
    '/create@queeeeueeee_bot': qEntity.createCommand,
    '/delete@queeeeueeee_bot': qEntity.deleteCommand,
    '/member@queeeeueeee_bot': userHandlers.memberCommand,
    '/show@queeeeueeee_bot': qEntity.showCommand,
    '/jointo@queeeeueeee_bot': qFun.jointoCommand,
    '/join@queeeeueeee_bot': qFun.joinCommand,
    '/subject@queeeeueeee_bot': subjectHandlers.subjectCommand,
    '/removesubject@queeeeueeee_bot': subjectHandlers.removesubjectCommand,
    '/removefrom@queeeeueeee_bot': removeHandlers.removefromCommand,
    '/replaceto@queeeeueeee_bot': replaceHandlers.replacetoCommand,
    '/replace@queeeeueeee_bot': replaceHandlers.replaceCommand,
    '/reject@queeeeueeee_bot': replaceHandlers.rejectCommand,
    '/confirm@queeeeueeee_bot': replaceHandlers.confirmCommand,
}

callbackHandlers: Dict[str, Callable[[telebot.types.CallbackQuery], None]] = {
    'help_member': lambda c: userHandlers.memberCommand(c.message),
    'help_show': lambda c: qEntity.showCommand(c.message),
    'help_delete': lambda c: qEntity.deleteCommand(c.message),
    'help_create': lambda c: qEntity.createCommand(c.message),
    'help_join': lambda c: qFun.joinCommand(c.message),
    'help_jointo': lambda c: qFun.jointoCommand(c.message),
    'commands': lambda c: commandsList(c.message),
    'possibility': lambda c: possibilityCommand(c.message),
}

textHandlers: List[Callable[[telebot.types.Message], None]] = {
    subjectHandlers.subjectTextHandler,
    userHandlers.setNameTextHandler,
    qFun.joinTextHandler,
    qEntity.queueTextHandler,
    removeHandlers.removefromTextHandler,
    replaceHandlers.replaceTextHandler,
}

@bot.message_handler(commands=['debug_chatid'])
def commandsHandler(message: telebot.types.Message):
    if not checkMessage(message):
        return

    bot.send_message(message.chat.id, f'chat_id = {message.chat.id}')


@bot.message_handler(func=lambda message: message.text.startswith('/'))
def commandsHandler(message: telebot.types.Message):
    if not checkMessage(message, chatId):
        return

    if message.text in commandHandlers.keys():
        commandHandlers[message.text](message)

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback: telebot.types.CallbackQuery):
    if not checkMessage(callback.message, chatId):
        return

    for key, handler in callbackHandlers.items():
        if callback.data.startswith(key):
            handler(callback)

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message: telebot.types.Message):
    if not checkMessage(message, chatId):
        return

    for textHandler in textHandlers:
        textHandler(message)

@bot.message_handler(content_types=['left_chat_member'])
def handle_left_chat_member(message: telebot.types.Message):
    if not checkMessage(message, chatId):
        return

    #bot.send_message(message.chat.id, f"Пользователь с ID {message.left_chat_member.id} покинул чат.")

    if not MemberService.isMemberExistByTgNum(botDB, message.left_chat_member.id):
        return

    member = MemberService.getMemberByTgNum(botDB, message.left_chat_member.id)
    for q in QueueService.getQueues(botDB):
        if QueueService.isMemberInQueue(botDB, q.id, member.id):
            place = QueueService.getPlaceByMemberId(botDB, q.id, member.id)
            removeHandlers.updateQueue(message, place, q)

    QueueService.deleteMemberFromAllQueues(botDB, member.id)
    for q in QueueService.getQueues(botDB):
        updateLastQueueText(bot, botDB, q.id, runtimeInfoManager)

    # TODO: отклонить все запросы на смену мест
    MemberService.deleteMember(botDB, str(message.left_chat_member.id))

bot.infinity_polling()
