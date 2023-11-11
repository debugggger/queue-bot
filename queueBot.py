import telebot

from Requests.Common import CommonReq
from Requests.QueueEntity import QueueEntity
from Requests.QueueFun import QueueFun
from Requests.Subjects import Subjects
from Requests.Users import Users

with open('token.txt') as file:
    lines = [line.rstrip() for line in file]
    token = lines[0]

bot=telebot.TeleBot(token)
user = Users(bot)
subj = Subjects(bot)
qEntity = QueueEntity(bot, subj)
qFun = QueueFun(bot, subj)
commonReq = CommonReq(bot, user, qEntity, qFun, subj)

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    commonReq.textHandler(message)

@bot.message_handler(commands=['start'])
def start_message(message):
    commonReq.startCommand(message)

@bot.message_handler(commands=['help'])
def help_message(message):
    commonReq.commandsList(message)

@bot.message_handler(commands=['create'])
def create_message(message):
    qEntity.createCommand(message)

@bot.message_handler(commands=['delete'])
def delete_message(message):
    qEntity.deleteCommand(message)

@bot.message_handler(commands=['member'])
def member_message(message):
    user.memberCommand(message)

@bot.message_handler(commands=['show'])
def show_message(message):
    qEntity.showCommand(message)

@bot.message_handler(commands=['jointo'])
def jointo_message(message):
    qFun.jointoCommand(message)

@bot.message_handler(commands=['join'])
def join_message(message):
    qFun.joinCommand(message)

@bot.message_handler(commands=['subject'])
def subject_message(message):
    subj.subjectCommand(message)

@bot.message_handler(commands=['removesubject'])
def removesubject_message(message):
    subj.removesubjectCommand(message)

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    commonReq.callback(callback)

bot.infinity_polling()
