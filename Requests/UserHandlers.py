import telebot
from telebot import types

from db import Database
from Requests.RuntimeInfoManager import RuntimeInfoManager
from utils import checkMemberName, removeBlank

class UserHandlers():
    def __init__(self, bot: telebot.TeleBot, database: Database, runtimeInfoManager: RuntimeInfoManager):
        self.bot: telebot.TeleBot = bot
        self.database: Database = database
        self.runtimeInfoManager: RuntimeInfoManager = runtimeInfoManager

    def memberCommand(self, message: telebot.types.Message) -> None:
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton("Ввод", callback_data="member_add")
        bt2 = types.InlineKeyboardButton("Отмена", callback_data="member_cancel")
        markup.row(bt1, bt2)
        self.bot.send_message(message.chat.id, "Для продолжения нажми кнопку ввод",
                              reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('member1', message.from_user.id)

    def memberAddCallback(self, callback: telebot.types.CallbackQuery) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('member1', callback.from_user.id):
            self.bot.send_message(callback.message.chat.id,
                                  "Введи имя, которое будет отображаться при выводе сообщений:")
            self.runtimeInfoManager.sendBarrier.add('member2', callback.from_user.id)

    def setNameTextHandler(self, message: telebot.types.Message) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('member2', message.from_user.id):
            name = removeBlank(message.text)

            if not checkMemberName(name):
                self.bot.send_message(message.chat.id,
                                      'Отображаемое имя некорректно.\n'
                                      'Используйте не более 30 символов русского и английского алфавита.'
                                      'Также дефис, апостроф, пробел (но не более одного такого символа подряд).')
                return

            self.database.add_member(name, message.from_user.id)
            self.bot.reply_to(message, "Отображаемое имя установлено")
