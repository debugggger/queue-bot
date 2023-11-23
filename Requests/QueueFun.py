import telebot
from telebot import types
from Entities.Subject import Subject
from Requests.RuntimeInfoManager import RuntimeInfoManager

from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from Requests.BaseHandler import BaseHandler
from db import Database

class QueueFun(BaseHandler):
    def __init__(self, bot: telebot.TeleBot, database: Database, runtimeInfoManager: RuntimeInfoManager):
        BaseHandler.__init__(self, bot, database, runtimeInfoManager)
        self.joinCertainList = {}
        self.joinList = {}

    def jointoCommand(self, message):
        members = [member.tgNum for member in MemberService.getMembers(self.database)]
        if str(message.from_user.id) in members:

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            markup.add('Отмена')
            for s in SubjectService.getSubjects(self.database):
                if QueueService.isQueueExist(self.database, s.id):
                    markup.add(f'Очередь по {s.title}')

            self.bot.reply_to(message, "В какую очередь ты хочешь записаться?", reply_markup=markup)
            self.runtimeInfoManager.sendBarrier.add('jointo', message.from_user.id)
        else:
            self.bot.reply_to(message, "Для использования этой команды тебе нужно записаться в списочек"
                                                   " членов закрытого клуба любителей очередей.")

    def joinCommand(self, message):
        members = [member.tgNum for member in MemberService.getMembers(self.database)]
        if str(message.from_user.id) in members:
            self.joinConnector(message, -1)
        else:
            self.bot.reply_to(message, "Для использования этой команды тебе нужно записаться в списочек"
                                                   " членов закрытого клуба любителей очередей.")

    def joinConnector(self, message, queueId):
        if queueId == -1:
            queueId = QueueService.getLastQueue(self.database).id

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True).add(
            'Назад', 'Первое свободное', 'Определенное', 'Последнее свободное'
        )
        self.bot.reply_to(message, "Выбери место для записи", reply_markup=markup)

        self.joinList[message.from_user.id] = queueId

    def joinTextHandler(self, message: types.Message):

        # Обработака ввода определенного места
        if message.from_user.id in self.joinCertainList:
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

            if QueueService.isPlaceEmpty(self.database, num, self.joinCertainList[message.from_user.id]) == False:
                if QueueService.getMemberInQueueByPlace(self.database, self.joinCertainList[message.from_user.id], num).memberId \
                        == MemberService.getMemberByTgNum(self.database, message.from_user.id).id:
                    self.bot.reply_to(message,
                                          "Ты уже записан на желаемое место")
                    self.joinList.pop(message.from_user.id)
                    self.joinCertainList.pop(message.from_user.id)
                    return

            while num <= count:

                if QueueService.isPlaceEmpty(self.database, num, self.joinCertainList[message.from_user.id]):

                    QueueService.addToQueue(self.database, self.joinCertainList[message.from_user.id], message.from_user.id, num, 1)
                    if num != entryNum:
                        self.bot.reply_to(message,
                                              "Желаемое место уже занято. Ты записан на " + str(num) + " место")
                    else:
                        self.bot.reply_to(message, "Ты записан на " + str(num) + " место")
                    self.joinList.pop(message.from_user.id)
                    self.joinCertainList.pop(message.from_user.id)
                    break
                else:
                    num += 1

            if num >= count and message.from_user.id in self.joinCertainList:
                if (count < entryNum):
                    num = count
                else:
                    num = entryNum
                while num >= 1:
                    if QueueService.isPlaceEmpty(self.database, num, self.joinCertainList[message.from_user.id]):
                        QueueService.addToQueue(self.database, self.joinCertainList[message.from_user.id], message.from_user.id, num, 1)
                        if num != entryNum:
                            self.bot.reply_to(message,
                                                  "Желаемое место уже занято. Ты записан на " + str(num) + " место")
                        else:
                            self.bot.reply_to(message, "Ты записан на " + str(num) + " место")

                        self.joinList.pop(message.from_user.id)
                        self.joinCertainList.pop(message.from_user.id)
                        break
                    else:
                        num -= 1
            if num == 0 and message.from_user.id in self.joinCertainList:
                self.bot.reply_to(message, "Слишком много желающих записаться, на тебя места не хватило:)")

            return

        # Обработка выбора очереди по команде /jointo
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('jointo', message.from_user.id):
            if not message.text.startswith('Очередь по '):
                self.bot.reply_to(message, 'Команда отменена', reply_markup=types.ReplyKeyboardRemove())
                return

            subjectTitle = message.text.removeprefix('Очередь по ')

            if not SubjectService.isSubjectExist(self.database, subjectTitle):
                self.bot.reply_to(message, 'Такого предмета не сущесвует', reply_markup=types.ReplyKeyboardRemove())
                return

            subject: Subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)

            if QueueService.isQueueExist(self.database, subject.id):
                queue = QueueService.getQueueBySubjectId(self.database, subject.id)
                self.bot.reply_to(message, "Выбрана очередь по " + subject.title + ":\n", reply_markup=types.ReplyKeyboardRemove())
                self.joinConnector(message, queue.id)
            else:
                self.bot.reply_to(message, "Очередь по " + subject.title + " не существует.", reply_markup=types.ReplyKeyboardRemove())

            return

        # Выбор типа записи в очередь (первое свободное, и т.д.)
        if message.from_user.id in self.joinList:
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
            if QueueService.isPlaceEmpty(self.database, place, self.joinList[message.from_user.id]):
                QueueService.addToQueue(self.database, self.joinList[message.from_user.id], message.from_user.id, place, 2)
                self.bot.reply_to(message, "Ты записан на " + str(place) + " место", reply_markup=types.ReplyKeyboardRemove())
                self.joinList.pop(message.from_user.id)
                break
            else:
                place -= 1

    def joinCertain(self, message: types.Message):
        self.bot.reply_to(message, "Введи место для записи", reply_markup=types.ReplyKeyboardRemove())
        self.joinCertainList[message.from_user.id] = self.joinList[message.from_user.id]

    def joinFirst(self, message: types.Message):
        count = MemberService.getMembersCount(self.database)
        place = 1
        while place <= count:
            if QueueService.isPlaceEmpty(self.database, place, self.joinList[message.from_user.id]):
                QueueService.addToQueue(self.database, self.joinList[message.from_user.id], message.from_user.id, place, 0)
                self.bot.reply_to(message, "Ты записан на " + str(place) + " место", reply_markup=types.ReplyKeyboardRemove())
                self.joinList.pop(message.from_user.id)
                break
            else:
                place += 1
