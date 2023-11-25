import telebot
from telebot import types

from Requests.RuntimeInfoManager import RuntimeInfoManager
from Requests.BaseHandler import BaseHandler
from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from db import Database


class ReplaceHandlers(BaseHandler):
    def __init__(self, bot: telebot.TeleBot, database: Database, runtimeInfoManager: RuntimeInfoManager):
        BaseHandler.__init__(self, bot, database, runtimeInfoManager)
        self.joinCertainList = {}
        self.joinList = {}

    def replacetoCommand(self, message: telebot.types.Message):
        if not MemberService.isMemberExistByTgNum(self.database, message.from_user.id):
            self.bot.reply_to(message, 'Для использования этой команды тебе нужно записаться в списочек member-ов')
            return

        if QueueService.isAnyQueueExist(self.database):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            markup.add('❌ Отмена')
            for s in SubjectService.getSubjects(self.database):
                if QueueService.isQueueExist(self.database, s.id):
                    markup.add(f'Очередь по {s.title}')

            self.bot.reply_to(message, 'В какой очереди ты хочешь поменяться местами', reply_markup=markup)
            self.runtimeInfoManager.sendBarrier.add('replaceto', message.from_user.id)
        else:
            self.bot.reply_to(message, 'Еще нет никаких очередей. Радуйся!',
                              reply_markup=types.ReplyKeyboardRemove(selective=True))

    def replaceTextHandler(self, message: telebot.types.Message):
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('replaceto', message.from_user.id):
            if not message.text.startswith('Очередь по '):
                self.bot.reply_to(message, 'Команда отменена', reply_markup=types.ReplyKeyboardRemove(selective=True))
                return

            subjectTitle = message.text.removeprefix('Очередь по ')

            if not SubjectService.isSubjectExist(self.database, subjectTitle):
                self.bot.reply_to(message, 'Такого предмета не существует',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                return

            subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)
            if QueueService.isQueueExist(self.database, subject.id):
                queue = QueueService.getQueueBySubjectId(self.database, subject.id)
                member = MemberService.getMemberByTgNum(self.database, message.from_user.id)
                if not QueueService.isMemberInQueue(self.database, queue.id, member.id):
                    self.bot.reply_to(message, 'Тебя же нет в этой очереди. Ты чево пытаешься?!',
                                      reply_markup=types.ReplyKeyboardRemove(selective=True))
                else:
                    self.replaceCertain(message)

            else:
                self.bot.reply_to(message, 'Очереди по этому предмету еще нет. Самое время создать ее!',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))

    def replaceCertain(self, message: types.Message):
        self.bot.reply_to(message, "Введи место с которым хочешь поменяться",
                          reply_markup=types.ReplyKeyboardRemove(selective=True))
        self.joinCertainList[message.from_user.id] = self.joinList[message.from_user.id]