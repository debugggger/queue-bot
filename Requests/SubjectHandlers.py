from typing import List

import telebot
from telebot import types

from Requests.BaseHandler import BaseHandler
from Services.SubjectService import SubjectService
from db import Database
from Entities.Subject import Subject
from Requests.RuntimeInfoManager import RuntimeInfoManager
from utils import checkSubjectTitle, removeBlank

class SubjectHandlers(BaseHandler):
    def subjectCommand(self, message: telebot.types.Message) -> None:
        self.bot.reply_to(message, 'Введи название нового предмета')
        self.runtimeInfoManager.sendBarrier.add('subject', message.from_user.id)

    def removesubjectCommand(self, message: telebot.types.Message) -> None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        for s in SubjectService.getSubjects(self.database):
            markup.add(s.title)

        self.bot.reply_to(message, 'Удалить предмет', reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('removesubject', message.from_user.id)

    def subjectTextHandler(self, message: telebot.types.Message) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('subject', message.from_user.id):
            title: str = removeBlank(message.text)
            
            if not checkSubjectTitle(title):
                self.bot.send_message(message.chat.id,
                                      'Название предмета некорректно.\n'
                                      'Используйте не более 30 символов русского и английского алфавита.')
                return

            if SubjectService.isSubjectExist(self.database, title):
                self.bot.send_message(message.chat.id, f'Предмет {title} уже существует')
                return

            SubjectService.addSubject(self.database, title)
            self.bot.send_message(message.chat.id, f'Предмет {title} добавлен')

        if self.runtimeInfoManager.sendBarrier.checkAndRemove('removesubject', message.from_user.id):
            if message.text in [s.title for s in SubjectService.getSubjects(self.database)]:
                SubjectService.removeSubject(self.database, message.text)
                self.bot.reply_to(message, 'Предмет удален',
                                  reply_markup=types.ReplyKeyboardRemove())
            else:
                self.bot.reply_to(message, 'Такого предмета и так не было. Зачем удалять то...',
                                  reply_markup=types.ReplyKeyboardRemove())
