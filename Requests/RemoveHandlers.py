import telebot
from telebot import types

from Requests.RuntimeInfoManager import RuntimeInfoManager
from Requests.BaseHandler import BaseHandler
from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService

class RemoveHandlers(BaseHandler):
    def removefromCommand(self, message: telebot.types.Message):
        if not MemberService.isMemberExistByTgNum(self.database, message.from_user.id):
            self.bot.reply_to(message, 'Для использования этой команды тебе нужно записаться в списочек member-ов')
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        markup.add('Отмена')
        for s in SubjectService.getSubjects(self.database):
            if QueueService.isQueueExist(self.database, s.id):
                markup.add(f'Очередь по {s.title}')

        self.bot.reply_to(message, 'Из какой очереди ты хочешь выйти', reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('removefrom', message.from_user.id)

    def removeSubjectTextHandler(self, message: telebot.types.Message):
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('removefrom', message.from_user.id):
            if not message.text.startswith('Очередь по '):
                self.bot.send_message(message.chat.id, 'Команда отменена', reply_markup=types.ReplyKeyboardRemove())
                return

            subjectTitle = message.text.removeprefix('Очередь по ')

            if not SubjectService.isSubjectExist(self.database, subjectTitle):
                self.bot.send_message(message.chat.id, 'Такого предмета не сущесвует', reply_markup=types.ReplyKeyboardRemove())
                return

            subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)
            if QueueService.isQueueExist(self.database, subject.id):
                queue = QueueService.getQueueBySubjectId(self.database, subject.id)
                member = MemberService.getMemberByTgNum(self.database, message.from_user.id)
                if not QueueService.isMemberInQueue(self.database, queue.id, member.id):
                    self.bot.reply_to(message, 'Тебя еще нет в этой очереди. Как так то?!',
                                      reply_markup=types.ReplyKeyboardRemove())
                else:
                    QueueService.deleteQueueMember(self.database, queue.id, member.id)
                    self.bot.reply_to(message, 'Ты вышел из этой очереди',
                                      reply_markup=types.ReplyKeyboardRemove())
            else:
                self.bot.reply_to(message, 'Очереди по этому предмету еще нет. Самое время создать ее!',
                                  reply_markup=types.ReplyKeyboardRemove())

            