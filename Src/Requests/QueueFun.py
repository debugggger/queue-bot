import telebot
from telebot import types
from Entities.Subject import Subject
from Requests.RuntimeInfoManager import RuntimeInfoManager

from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from Requests.BaseHandler import BaseHandler
from DbUtils.db import Database
from utils import formQueueText

def updateLastQueueText(bot: telebot.TeleBot, database, queueId: int, runtimeInfoManager: RuntimeInfoManager):
    queue = QueueService.getQueueById(database, queueId)
    if queue.subject.title not in runtimeInfoManager.lastQueueMessages:
        return
    msg = runtimeInfoManager.lastQueueMessages[queue.subject.title]
    msgNewText = formQueueText(queue)
    if msgNewText == msg.text:
        return
    bot.edit_message_text(msgNewText, msg.chat.id, msg.id)

class QueueFun(BaseHandler):
    def __init__(self, bot: telebot.TeleBot, database: Database, runtimeInfoManager: RuntimeInfoManager):
        BaseHandler.__init__(self, bot, database, runtimeInfoManager)
        self.joinList = {}

    def jointoCommand(self, message):
        members = [member.tgNum for member in MemberService.getMembers(self.database)]
        if str(message.from_user.id) in members:
            curMember = MemberService.getMemberByTgNum(self.database, message.from_user.id)
            if not self.runtimeInfoManager.checkReplace(curMember.id):
                self.bot.reply_to(message, "Извините, у вас есть запрос на смену места",
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                return
            if QueueService.isAnyQueueExist(self.database):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
                markup.add('❌ Отмена')
                for s in SubjectService.getSubjects(self.database):
                    if QueueService.isQueueExist(self.database, s.id):
                        markup.add(f'Очередь по {s.title}')

                self.bot.reply_to(message, "В какую очередь ты хочешь записаться?", reply_markup=markup)
                self.runtimeInfoManager.sendBarrier.add('jointo', message.from_user.id)
            else:
                self.bot.reply_to(message, 'Еще нет никаких очередей. Радуйся!',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
        else:
            self.bot.reply_to(message, "Для использования этой команды тебе нужно записаться в списочек"
                                       " членов закрытого клуба любителей очередей.")

    def joinCommand(self, message):
        members = [member.tgNum for member in MemberService.getMembers(self.database)]
        if str(message.from_user.id) in members:
            curMember = MemberService.getMemberByTgNum(self.database, message.from_user.id)
            if not self.runtimeInfoManager.checkReplace(curMember.id):
                self.bot.reply_to(message, "Извините, у вас есть запрос на смену места",
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                return
            self.joinConnector(message, -1)
        else:
            self.bot.reply_to(message, "Для использования этой команды тебе нужно записаться в списочек"
                                       " членов закрытого клуба любителей очередей.")

    def joinConnector(self, message, queueId):
        if len(QueueService.getQueues(self.database)) == 0:
            self.bot.reply_to(message, "Нет ни одной очереди, как так то....")
            return
        if queueId == -1:
            queueId = QueueService.getLastQueue(self.database).id

        self.runtimeInfoManager.sendBarrier.add('join', message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True).add(
            'Назад', 'Первое свободное', 'Определенное', 'Последнее свободное'
        )
        subjectTitle = QueueService.getQueueById(self.database, queueId).subject.title
        subject: Subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)
        self.bot.reply_to(message, "Выбрана очередь по " + subject.title + ":\n" + "Выбери место для записи",
                          reply_markup=markup)

        self.joinList[message.from_user.id] = queueId

    def joinTextHandler(self, message: types.Message):

        # Обработака ввода определенного места
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('joinCertain', message.from_user.id):
            try:
                entryNum = int(message.text)
                if entryNum <= 0:
                    self.bot.reply_to(message, "Введи корректное число")
                    return
            except:
                self.bot.reply_to(message, "Введи корректное число")
                return

            count = MemberService.getMembersCount(self.database)
            if (count < entryNum):
                num = count
            else:
                num = entryNum

            while num <= count:

                if QueueService.isPlaceEmpty(self.database, num, self.joinList[message.from_user.id],
                                             MemberService.getMemberByTgNum(self.database, message.from_user.id).id):
                    QueueService.addToQueue(self.database, self.joinList[message.from_user.id], message.from_user.id,
                                            num, 1)
                    if num != entryNum:
                        self.bot.reply_to(message, "Желаемое место уже занято или превышает количество человек, "
                                                   "которые живут очередями. Ты записан на " + str(num) + " место")
                    else:
                        self.bot.reply_to(message, "Ты записан на " + str(num) + " место")
                    updateLastQueueText(self.bot, self.database, self.joinList[message.from_user.id],
                                        self.runtimeInfoManager)
                    self.joinList.pop(message.from_user.id)
                    break
                else:
                    num += 1

            if num >= count and message.from_user.id in self.joinList:
                if (count < entryNum):
                    num = count
                else:
                    num = entryNum
                while num >= 1:
                    if QueueService.isPlaceEmpty(self.database, num, self.joinList[message.from_user.id],
                                                 MemberService.getMemberByTgNum(self.database,
                                                                                message.from_user.id).id):
                        QueueService.addToQueue(self.database, self.joinList[message.from_user.id],
                                                message.from_user.id, num, 1)
                        if num != entryNum:
                            self.bot.reply_to(message,
                                              "Желаемое место уже занято. Ты записан на " + str(num) + " место")
                        else:
                            self.bot.reply_to(message, "Ты записан на " + str(num) + " место")
                        updateLastQueueText(self.bot, self.database, self.joinList[message.from_user.id],
                                            self.runtimeInfoManager)
                        self.joinList.pop(message.from_user.id)
                        break
                    else:
                        num -= 1
            if num == 0 and message.from_user.id in self.joinList:
                self.joinList.pop(message.from_user.id)
                self.bot.reply_to(message, "Ты уже записан в эту очередь, свободных мест для записи нет. "
                                           "Для смены места воспользуйся командой /replace")
            return

        # Обработка выбора очереди по команде /jointo
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('jointo', message.from_user.id):
            if not message.text.startswith('Очередь по '):
                self.bot.reply_to(message, 'Команда отменена', reply_markup=types.ReplyKeyboardRemove(selective=True))
                return
            subjectTitle = message.text.removeprefix('Очередь по ')

            if not SubjectService.isSubjectExist(self.database, subjectTitle):
                self.bot.reply_to(message, 'Такого предмета не существует',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                return

            subject: Subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)

            if QueueService.isQueueExist(self.database, subject.id):
                queue = QueueService.getQueueBySubjectId(self.database, subject.id)
                self.joinConnector(message, queue.id)
                # self.bot.reply_to(message, " ", reply_markup=types.ReplyKeyboardRemove(selective=True))
            else:
                self.bot.reply_to(message, "Очередь по " + subject.title + " не существует.",
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))

            return

        # Выбор типа записи в очередь (первое свободное, и т.д.)
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('join', message.from_user.id):
            match message.text:
                case 'Первое свободное':
                    self.joinFirst(message)
                case 'Определенное':
                    self.joinCertain(message)
                case 'Последнее свободное':
                    self.joinLast(message)
                case _:
                    self.joinList.pop(message.from_user.id)
                    self.jointoCommand(message)

            return

    def joinLast(self, message: types.Message):
        place = MemberService.getMembersCount(self.database)
        while place >= 1:

            if QueueService.isPlaceEmpty(self.database, place, self.joinList[message.from_user.id],
                                         MemberService.getMemberByTgNum(self.database, message.from_user.id).id):
                QueueService.addToQueue(self.database, self.joinList[message.from_user.id], message.from_user.id, place,
                                        2)
                self.bot.reply_to(message, "Ты записан на " + str(place) + " место",
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                updateLastQueueText(self.bot, self.database, self.joinList[message.from_user.id],
                                    self.runtimeInfoManager)
                self.joinList.pop(message.from_user.id)
                break
            else:
                place -= 1
        if place == 0 and message.from_user.id in self.joinList:
            self.joinList.pop(message.from_user.id)
            self.bot.reply_to(message, "Ты уже записан в эту очередь, свободных мест для записи нет. "
                                       "Для смены места воспользуйся командой /replace")

    def joinCertain(self, message: types.Message):
        self.bot.reply_to(message, "Введи место для записи", reply_markup=types.ReplyKeyboardRemove(selective=True))
        self.runtimeInfoManager.sendBarrier.add('joinCertain', message.from_user.id)

    def joinFirst(self, message: types.Message):
        count = MemberService.getMembersCount(self.database)
        place = 1
        while place <= count:

            if QueueService.isPlaceEmpty(self.database, place, self.joinList[message.from_user.id],
                                         MemberService.getMemberByTgNum(self.database, message.from_user.id).id):
                QueueService.addToQueue(self.database, self.joinList[message.from_user.id], message.from_user.id, place,
                                        0)
                self.bot.reply_to(message, "Ты записан на " + str(place) + " место",
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                updateLastQueueText(self.bot, self.database, self.joinList[message.from_user.id],
                                    self.runtimeInfoManager)
                self.joinList.pop(message.from_user.id)
                break
            else:
                place += 1
        if place > count and message.from_user.id in self.joinList:
            self.joinList.pop(message.from_user.id)
            self.bot.reply_to(message, "Ты уже записан в эту очередь, свободных мест для записи нет. "
                                       "Для смены места воспользуйся командой /replace")
