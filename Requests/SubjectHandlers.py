from typing import List

import telebot
from telebot import types

from Requests.BaseHandler import BaseHandler
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from TgUtil.KeyboardMarkups import makeSubjectListMarkup
from db import Database
from Entities.Subject import Subject
from Requests.RuntimeInfoManager import RuntimeInfoManager
from utils import checkSubjectTitle, removeBlank
import TgUtil.KeyboardMarkups as km


class SubjectHandlers(BaseHandler):
    def subjectCommand(self, message: telebot.types.Message) -> None:
        self.bot.reply_to(message, 'Введи название нового предмета')
        self.runtimeInfoManager.sendBarrier.add('subject', message.from_user.id)

    def removesubjectCommand(self, message: telebot.types.Message) -> None:
        markup = makeSubjectListMarkup(SubjectService.getSubjects(self.database))

        self.bot.reply_to(message, 'Удалить предмет', reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('removesubject', message.from_user.id)

    def subjectTextHandler(self, message: telebot.types.Message) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('subject', message.from_user.id):
            title: str = removeBlank(message.text)
            
            if not checkSubjectTitle(title):
                self.bot.reply_to(message,
                                      'Название предмета некорректно.\n'
                                      'Используйте не более 30 символов русского и английского алфавита.')
                return

            if SubjectService.isSubjectExist(self.database, title):
                self.bot.reply_to(message, f'Предмет {title} уже существует')
                return

            SubjectService.addSubject(self.database, title)
            self.bot.reply_to(message, f'Предмет {title} добавлен')

        if self.runtimeInfoManager.sendBarrier.checkAndRemove('removesubject', message.from_user.id):
            if message.text == '❌ Отмена':
                self.bot.reply_to(message, 'Команда отменена',
                                  reply_markup=km.Remove)
                return

            subjectTitle = message.text
            if not SubjectService.isSubjectExist(self.database, subjectTitle):
                self.bot.reply_to(message, 'Такого предмета и так не было. Зачем удалять то...',
                                  reply_markup=km.Remove)

            subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)
            if QueueService.isQueueExist(self.database, subject.id):
                q = QueueService.getQueueBySubjectId(self.database, subject.id)
                QueueService.deleteQueue(self.database, q.id)
                self.bot.reply_to(message, 'По этому предмету была очередь, она тоже удалена',
                                    reply_markup=km.Remove)


            SubjectService.removeSubject(self.database, subjectTitle)
            self.bot.reply_to(message, 'Предмет удален',
                                reply_markup=km.Remove)
