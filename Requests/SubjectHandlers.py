from typing import List

import telebot
from telebot import types

from db import Database
from Entities.Subject import Subject
from Requests.RuntimeInfoManager import RuntimeInfoManager

class SubjectHandlers:
    def __init__(self, bot: telebot.TeleBot, database: Database, runtimeInfoManager: RuntimeInfoManager):
        self.bot: telebot.TeleBot = bot
        self.database: Database = database
        self.runtimeInfoManager: RuntimeInfoManager = runtimeInfoManager

        self.c_callbackPrefixRemovesubject: str = 'removesubject_'

    def subjectCommand(self, message: telebot.types.Message) -> None:
        self.bot.send_message(message.chat.id, 'Введите название нового предмета')
        self.runtimeInfoManager.sendBarrier.add('subject', message.from_user.id)

    def removesubjectCommand(self, message: telebot.types.Message) -> None:
        subjects: List[Subject] = self.database.getSubjects()

        buttons = []
        for subject in subjects:
            buttons.append(
                [types.InlineKeyboardButton(subject.title, callback_data=self.c_callbackPrefixRemovesubject + subject.title)])
        markup = types.InlineKeyboardMarkup(buttons)
        self.bot.send_message(message.chat.id, 'Удалить предмет', reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('removesubject', message.from_user.id)

    def subjectTextHandler(self, message: telebot.types.Message) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('subject', message.from_user.id):
            if self.database.isSubjectExist(message.text):
                self.bot.send_message(message.chat.id, 'Предмет ' + message.text + ' уже существует')
                return
            self.database.addSubject(message.text)
            self.bot.send_message(message.chat.id, 'Предмет ' + message.text + ' добавлен')

    def removesubjectCallback(self, callback: telebot.types.CallbackQuery) -> None:
        subject = callback.data.removeprefix(self.c_callbackPrefixRemovesubject)
        self.database.removeSubject(subject)
        self.bot.send_message(callback.message.chat.id, 'Предмет ' + subject + ' удален')

        self.runtimeInfoManager.sendBarrier.remove('removesubject', callback.from_user.id)
