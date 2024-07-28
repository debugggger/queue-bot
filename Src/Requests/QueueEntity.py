import datetime
import telebot
from telebot import types
from Entities.Subject import Subject

from Requests.BaseHandler import BaseHandler
from Requests.RuntimeInfoManager import RuntimeInfoManager
from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from utils import formQueueText, removeBlank, checkSubjectTitle
import TgUtil.KeyboardMarkups as km


class QueueEntity(BaseHandler):

    def createCommand(self, message: telebot.types.Message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        markup.add('❌ Отмена')
        for s in SubjectService.getSubjects(self.database):
            markup.add(s.title)
        self.bot.reply_to(message, "По какому предмету ты хочешь создать очередь?", reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('create', message.from_user.id)

    def deleteCommand(self, message: telebot.types.Message):
        chatMember: telebot.types.ChatMember = self.bot.get_chat_member(message.chat.id, message.from_user.id)
        if chatMember.status not in ['creator', 'administrator']:
            self.bot.reply_to(message, 'Эту команду могут выполнять только администраторы')
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        markup.add('❌ Отмена')
        for s in SubjectService.getSubjects(self.database):
            if QueueService.isQueueExist(self.database, s.id):
                markup.add(f'Очередь по {s.title}')
        self.bot.reply_to(message, "По какому предмету ты хочешь удалить очередь?", reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('delete', message.from_user.id)

    def showCommand(self, message: telebot.types.Message):
        if QueueService.isAnyQueueExist(self.database):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            subjects = SubjectService.getSubjects(self.database)
            markup.add('❌ Отмена')

            for i in range(len(subjects)):
                if QueueService.isQueueExist(self.database, subjects[i].id):
                    markup.add(str(subjects[i].title))

            self.bot.reply_to(message, 'По какому предмету ты хочешь просмотреть очередь?', reply_markup=markup)
            self.runtimeInfoManager.sendBarrier.add('show', message.from_user.id)
        else:
            self.bot.reply_to(message, 'Еще нет никаких очередей. Радуйся!',
                              reply_markup=types.ReplyKeyboardRemove(selective=True))

    def queueTextHandler(self, message: telebot.types.Message) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('create', message.from_user.id):
            if message.text == '❌ Отмена':
                self.bot.reply_to(message, 'Команда отменена',
                                  reply_markup=km.Remove)
                return

            if SubjectService.isSubjectExist(self.database, message.text):
                subject = SubjectService.getSubjectByTitle(self.database, message.text)
                if QueueService.isQueueExist(self.database, subject.id):
                    self.bot.reply_to(message, 'Очередь по этому предмету уже существует',
                                      reply_markup=km.Remove)
                else:
                    QueueService.createQueue(self.database, subject.id)
                    self.bot.reply_to(message, "Создана очередь по " + subject.title, reply_markup=km.Remove)
            else:
                self.bot.reply_to(message, 'Такого предмета нет',
                                  reply_markup=km.Remove)

        if self.runtimeInfoManager.sendBarrier.checkAndRemove('delete', message.from_user.id):
            if not message.text.startswith('Очередь по '):
                self.bot.reply_to(message, 'Команда отменена', reply_markup=km.Remove)
                return

            subjectTitle = message.text.removeprefix('Очередь по ')
            if not SubjectService.isSubjectExist(self.database, subjectTitle):
                self.bot.reply_to(message, 'Такого предмета не существует', reply_markup=km.Remove)
                return
            subject: Subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)

            if QueueService.isQueueExist(self.database, subject.id):
                queue = QueueService.getQueueBySubjectId(self.database, subject.id)
                QueueService.deleteQueue(self.database, queue.id)
                self.bot.reply_to(message, 'Очередь удалена', reply_markup=types.ReplyKeyboardRemove(selective=True))

                self.runtimeInfoManager.replaceRequests = [rr for rr in self.runtimeInfoManager.replaceRequests if rr.queueId != queue.id]

            else:
                self.bot.reply_to(message, "Очередь по " + subject.title + " не существует.", reply_markup=types.ReplyKeyboardRemove(selective=True))

        if self.runtimeInfoManager.sendBarrier.checkAndRemove('show', message.from_user.id):
            title: str = removeBlank(message.text)
            if title == "❌ Отмена":
                self.bot.reply_to(message, 'Команда отменена',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                return

            if SubjectService.isSubjectExist(self.database, title):

                if not self.runtimeInfoManager.timeoutManager.checkAndUpdate('show', title, datetime.datetime.now()):
                    self.bot.reply_to(message, 'Очереди можно смотреть не чаще, чем раз в ' +
                                      str(self.runtimeInfoManager.timeoutManager.getTimeout('show')) + ' секунд')
                    return

                subj = SubjectService.getSubjectByTitle(self.database, title)
                queue = QueueService.getQueueBySubjectId(self.database, subj.id)
                queueText = formQueueText(queue)

                msg = self.bot.reply_to(message, queueText)
                self.runtimeInfoManager.lastQueueMessages[title] = msg

            else:
                self.bot.reply_to(message, "Очереди по такому предмету нет")
