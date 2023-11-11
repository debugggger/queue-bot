import telebot

from Requests.Common import CommonReq
from Requests.QueueEntity import QueueEntity
from Requests.QueueFun import QueueFun
from Requests.Subjects import Subjects
from Requests.Users import Users
from telebot import types
import time
from dotenv import load_dotenv
import os
from db import BotDB


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))
BotDB = BotDB()
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

@bot.message_handler(commands=['member'])
def handle_add_user(message):
    bot.reply_to(message, 'добавление в БД')
    BotDB.add_member(message.from_user.username, message.from_user.id)

@bot.message_handler(content_types=['left_chat_member'])
def handle_left_chat_member(message):
    user_id = message.left_chat_member.id
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Пользователь с ID {user_id} покинул чат.")


bot.infinity_polling()
