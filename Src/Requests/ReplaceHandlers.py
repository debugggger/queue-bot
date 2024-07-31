import datetime

import telebot
from telebot import types
from utils import formReplaceRequest

import utils
from Entities import Subject
from Requests.RuntimeInfoManager import RuntimeInfoManager, ReplaceRequest
from Requests.BaseHandler import BaseHandler
from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from DbUtils.db import Database
from Requests.QueueFun import updateLastQueueText


class ReplaceHandlers(BaseHandler):
    def __init__(self, bot: telebot.TeleBot, database: Database, runtimeInfoManager: RuntimeInfoManager):
        BaseHandler.__init__(self, bot, database, runtimeInfoManager)
        self.replaceCertainList = {}
        self.replaceList = {}

    def replacetoCommand(self, message: telebot.types.Message):
        self.runtimeInfoManager.removeOldReplaceRequest()
        if not MemberService.isMemberExistByTgNum(self.database, message.from_user.id):
            self.bot.reply_to(message, 'Для использования этой команды тебе нужно записаться в списочек member-ов')
            return
        curMember = MemberService.getMemberByTgNum(self.database, message.from_user.id)
        if not self.runtimeInfoManager.checkReplace(curMember.id):
            self.bot.reply_to(message, "Извините, у вас уже есть запрос на смену места",
                              reply_markup=types.ReplyKeyboardRemove(selective=True))
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

    def replaceCommand(self, message):
        self.runtimeInfoManager.removeOldReplaceRequest()
        members = [member.tgNum for member in MemberService.getMembers(self.database)]
        if str(message.from_user.id) in members:
            curMember = MemberService.getMemberByTgNum(self.database, message.from_user.id)
            if not self.runtimeInfoManager.checkReplace(curMember.id):
                self.bot.reply_to(message, "Извините, у вас уже есть запрос на смену места",
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                return
            self.replaceConnector(message, -1)
        else:
            self.bot.reply_to(message, "Для использования этой команды тебе нужно записаться в списочек"
                                       " членов закрытого клуба любителей очередей.")

    def rejectCommand(self, message):
        self.runtimeInfoManager.removeOldReplaceRequest()
        if not MemberService.isMemberExistByTgNum(self.database, message.from_user.id):
            self.bot.reply_to(message, 'Для использования этой команды тебе нужно записаться в списочек member-ов')
            return
        curMember = MemberService.getMemberByTgNum(self.database, message.from_user.id)
        if not QueueService.isMemberInAnyQueue(self.database, curMember.id):
            self.bot.reply_to(message, 'Ты еще не записан ни в одну очередь. Ух, ты!')
            return
        if self.runtimeInfoManager.checkAndRemove(curMember.id):
            self.bot.reply_to(message, "Смена мест отменена")
        else:
            self.bot.reply_to(message, 'Вы не начинали смену мест')

    def confirmCommand(self, message):
        self.runtimeInfoManager.removeOldReplaceRequest()
        if not MemberService.isMemberExistByTgNum(self.database, message.from_user.id):
            self.bot.reply_to(message, 'Для использования этой команды тебе нужно записаться в списочек member-ов')
            return
        curMember = MemberService.getMemberByTgNum(self.database, message.from_user.id)
        if self.runtimeInfoManager.checkReplace(curMember.id):
            self.bot.reply_to(message, "Извините, у вас еще нет запросов на смену места",
                              reply_markup=types.ReplyKeyboardRemove(selective=True))
            return
        rR = self.runtimeInfoManager.getAndRemoveReplaceRequest(curMember.id)
        if self.runtimeInfoManager.timeoutManager.checkAndUpdate('replaceto', rR, datetime.datetime.now()):
            self.bot.reply_to(message, 'Подтверждение смены мест активно только ' +
                              str(self.runtimeInfoManager.timeoutManager.getTimeout('replaceto')) + ' секунд')
            return
        fromQueueMem = QueueService.getMemberInQueueByMemberId(self.database, rR.queueId, rR.fromId)
        toQueueMem = QueueService.getMemberInQueueByMemberId(self.database, rR.queueId, rR.toId)
        QueueService.setPlaceByMemberId(self.database, rR.queueId, rR.fromId, toQueueMem.placeNumber)
        QueueService.setPlaceByMemberId(self.database, rR.queueId, rR.toId, fromQueueMem.placeNumber)
        updateLastQueueText(self.bot, self.database, rR.queueId, self.runtimeInfoManager)
        self.bot.reply_to(message, "Смена мест произошла успешно!",
                          reply_markup=types.ReplyKeyboardRemove(selective=True))

    def replaceConnector(self, message, queueId):
        if len(QueueService.getQueues(self.database)) == 0:
            self.bot.reply_to(message, "Нет ни одной очереди, как так то....")
            return
        if queueId == -1:
            queueId = QueueService.getLastQueue(self.database).id

        self.runtimeInfoManager.sendBarrier.add('replaceCertain', message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        subjectTitle = QueueService.getQueueById(self.database, queueId).subject.title
        subject: Subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)
        self.bot.reply_to(message,
                          "Выбрана очередь по " + subject.title + ":\n" + "Введи место с которым хочешь поменяться",
                          reply_markup=markup)

        self.replaceList[message.from_user.id] = queueId

    # def checkNum(self, message):
    #     try:
    #         entryNum = int(message)
    #         if entryNum <= 0:
    #             entryNum = -1
    #         return entryNum
    #     except:
    #         return -1

    def replaceTextHandler(self, message: telebot.types.Message):
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('replaceCertain', message.from_user.id):

            entryNum = utils.checkNumPlace(message.text)
            if entryNum == -1:
                self.bot.reply_to(message, "Введи корректное число")
                return
            # try:
            #     entryNum = int(message.text)
            #     if entryNum <= 0:
            #         self.bot.reply_to(message, "Введи корректное число")
            #         return
            # except:
            #     self.bot.reply_to(message, "Введи корректное число")
            #     return

            qId = self.replaceList[message.from_user.id]
            maxPlace = QueueService.getMaxPlaceNumber(self.database, qId)
            # Ввели число, которое больше кол-ва чел в очереди
            if maxPlace < entryNum:
                self.bot.reply_to(message, "Место превышает количество человек в этой очереди")
            else:
                curMember = MemberService.getMemberByTgNum(self.database, message.from_user.id)
                chatCurMem = self.bot.get_chat_member(message.chat.id, curMember.tgNum)
                oldPlace = QueueService.getPlaceByMemberId(self.database, qId, curMember.id)
                oldEntryType = QueueService.getMemberInQueueByPlace(self.database, qId, oldPlace).entryType
                # Если на желамом месте никого - просто запись
                if QueueService.isPlaceEmpty(self.database, entryNum, qId, curMember.id):
                    QueueService.deleteQueueMember(self.database, qId, curMember.id)
                    QueueService.addToQueue(self.database, qId, message.from_user.id, entryNum, int(oldEntryType))
                    self.bot.reply_to(message, "Успешно перезаписан на " + str(entryNum) + " место",
                                      reply_markup=types.ReplyKeyboardRemove(selective=True))
                else:
                    # Иначе проверяем человека
                    replaceQueueMem = QueueService.getMemberInQueueByPlace(self.database, qId, entryNum)
                    chatRepMem = self.bot.get_chat_member(message.chat.id, replaceQueueMem.member.tgNum)
                    if not self.runtimeInfoManager.checkReplace(replaceQueueMem.member.id):
                        self.bot.reply_to(message, "Извините, этого человека уже есть запрос на смену места",
                                          reply_markup=types.ReplyKeyboardRemove(selective=True))
                    else:
                        rR = ReplaceRequest(curMember.id, replaceQueueMem.member.id, qId)
                        self.runtimeInfoManager.replaceRequests.append(rR)
                        self.runtimeInfoManager.timeoutManager.checkAndUpdate('replaceto', rR, datetime.datetime.now())

                        queue = QueueService.getQueueById(self.database, qId)
                        replaceRequestText = formReplaceRequest(chatRepMem.user.username, chatCurMem.user.username, queue.subject.title, replaceQueueMem.placeNumber, oldPlace)

                        self.bot.send_message(message.chat.id, replaceRequestText)

            self.replaceList.pop(message.from_user.id)

            return

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
                    self.replaceConnector(message, queue.id)
                    # self.runtimeInfoManager.sendBarrier.add('replaceCertain', message.from_user.id)

            else:
                self.bot.reply_to(message, 'Очереди по этому предмету еще нет. Самое время создать ее!',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
        #
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('replace', message.from_user.id):

            return
