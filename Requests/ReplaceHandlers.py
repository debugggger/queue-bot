import telebot
from telebot import types

from Entities import Subject
from Requests.RuntimeInfoManager import RuntimeInfoManager, ReplaceRequest
from Requests.BaseHandler import BaseHandler
from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from db import Database


class ReplaceHandlers(BaseHandler):
    def __init__(self, bot: telebot.TeleBot, database: Database, runtimeInfoManager: RuntimeInfoManager):
        BaseHandler.__init__(self, bot, database, runtimeInfoManager)
        self.replaceCertainList = {}
        self.replaceList = {}

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

    def replaceCommand(self, message):
        members = [member.tgNum for member in MemberService.getMembers(self.database)]
        if str(message.from_user.id) in members:
            self.replaceConnector(message, -1)
        else:
            self.bot.reply_to(message, "Для использования этой команды тебе нужно записаться в списочек"
                                       " членов закрытого клуба любителей очередей.")

    def rejectCommand(self, message):
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

    def replaceTextHandler(self, message: telebot.types.Message):
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('replaceCertain', message.from_user.id):
            try:
                entryNum = int(message.text)
                if entryNum <= 0:
                    self.bot.reply_to(message, "Введи корректное число")
                    return
            except:
                self.bot.reply_to(message, "Введи корректное число")
                return

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
                    # if self.runtimeInfoManager.sendBarrier.check('replaceto', replaceQueueMem.member.tgNum):
                    if not self.runtimeInfoManager.checkReplace(replaceQueueMem.member.id, qId):
                        self.bot.reply_to(message, "Извините, этого человека уже есть запрос на смену места",
                                          reply_markup=types.ReplyKeyboardRemove(selective=True))
                    else:
                        self.runtimeInfoManager.replaceRequests.append(ReplaceRequest(curMember.id, replaceQueueMem.member.id, qId))
                        self.bot.send_message(message.chat.id, '@' + chatRepMem.user.username
                                              + ' вам предлагают поменяться в очереди\n'
                                                ' от кого: ' + ' @' + chatCurMem.user.username + '\n'
                                              + ' очередь: ' + str(
                            QueueService.getQueueById(self.database, qId).subject.title) + '\n'
                                              + ' ваше место: ' + str(replaceQueueMem.placeNumber) + '\n'
                                              + ' предлагаемое место: ' + str(oldPlace))

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

