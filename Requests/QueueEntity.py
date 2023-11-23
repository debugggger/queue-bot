import telebot
from telebot import types
from Entities.Subject import Subject

from Requests.BaseHandler import BaseHandler
from Requests.RuntimeInfoManager import RuntimeInfoManager
from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from utils import removeBlank, checkSubjectTitle


class QueueEntity(BaseHandler):

    def createCommand(self, message: telebot.types.Message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        markup.add('❌ Отмена')
        for s in SubjectService.getSubjects(self.database):
            markup.add(s.title)
        self.bot.reply_to(message, "По какому предмету ты хочешь создать очередь?", reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('create', message.from_user.id)

    def deleteCommand(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        markup.add('❌ Отмена')
        for s in SubjectService.getSubjects(self.database):
            if QueueService.isQueueExist(self.database, s.id):
                markup.add(f'Очередь по {s.title}')
        self.bot.reply_to(message, "По какому предмету ты хочешь удалить очередь?", reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('delete', message.from_user.id)

    def showCallback(self, callback):
        numStr = callback.data.strip("showNum_")
        numSubj = int(numStr)
        subjects = SubjectService.getSubjectById(self.database, numSubj)
        self.bot.send_message(callback.message.chat.id, "Очередь по " + subjects.title + ":\n")

    def showCommand(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        subjects = SubjectService.getSubjects(self.database)
        markup.add('❌ Отмена')

        for i in range(len(subjects)):
            if QueueService.isQueueExist(self.database, subjects[i].id):
                markup.add(str(subjects[i].title))

        self.bot.reply_to(message, 'По какому предмету ты хочешь просмотреть очередь?', reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('show', message.from_user.id)

    def queueTextHandler(self, message: telebot.types.Message) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('create', message.from_user.id):
            if message.text == '❌ Отмена':
                self.bot.reply_to(message, 'Команда отменена',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                return

            if SubjectService.isSubjectExist(self.database, message.text):
                subject = SubjectService.getSubjectByTitle(self.database, message.text)
                if QueueService.isQueueExist(self.database, subject.id):
                    self.bot.reply_to(message, 'Очередь по этому предмету уже существует',
                                      reply_markup=types.ReplyKeyboardRemove(selective=True))
                else:
                    QueueService.createQueue(self.database, subject.id)
                    self.bot.reply_to(message, "Создана очередь по " + subject.title)
            else:
                self.bot.reply_to(message, 'Такого предмета нет',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))

        if self.runtimeInfoManager.sendBarrier.checkAndRemove('delete', message.from_user.id):
            if not message.text.startswith('Очередь по '):
                self.bot.reply_to(message, 'Команда отменена', reply_markup=types.ReplyKeyboardRemove(selective=True))
                return

            subjectTitle = message.text.removeprefix('Очередь по ')
            if not SubjectService.isSubjectExist(self.database, subjectTitle):
                self.bot.reply_to(message, 'Такого предмета не сущесвует', reply_markup=types.ReplyKeyboardRemove(selective=True))
                return
            subject: Subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)

            if QueueService.isQueueExist(self.database, subject.id):
                queue = QueueService.getQueueBySubjectId(self.database, subject.id)
                QueueService.deleteQueue(self.database, queue.id)
                self.bot.reply_to(message, 'Очередь удалена', reply_markup=types.ReplyKeyboardRemove(selective=True))
            else:
                self.bot.reply_to(message, "Очередь по " + subject.title + " не существует.", reply_markup=types.ReplyKeyboardRemove(selective=True))

        if self.runtimeInfoManager.sendBarrier.check('show', message.from_user.id):
            title: str = removeBlank(message.text)
            if title == "Отмена":
                self.bot.reply_to(message, 'Команда отменена',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                return

            if SubjectService.isSubjectExist(self.database, title):

                qList = {}
                subj = SubjectService.getSubjectByTitle(self.database, title)
                queue = QueueService.getQueueBySubjectId(self.database, subj.id)
                for member in queue.members:
                    val =  " - " + str(MemberService.getMemberById(self.database, member.memberId).name) + "\n"

                    qList [member.placeNumber] = val

                sortedQ = {k: v for k, v in sorted(qList.items())}
                resStr = ''
                for q in sortedQ:
                    resStr += str(q) + sortedQ[q]

                self.bot.reply_to(message, "Очередь по " + title + ":\n" + resStr)
            else:
                self.bot.reply_to(message, "Очереди по такому предмету нет")
