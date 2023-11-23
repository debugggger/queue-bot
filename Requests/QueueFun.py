
from telebot import types

from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService

class QueueFun():
    def __init__(self, bot, botDB):
        self.bot = bot
        self.botDB = botDB
        self.joinCertainList = {}
        self.joinList = {}


    def jointoCommand(self, message):
        members = [member.tgNum for member in MemberService.getMembers(self.botDB)]
        if str(message.from_user.id) in members:
            markup = types.InlineKeyboardMarkup(row_width=3)
            bt1 = types.InlineKeyboardButton("Отмена", callback_data="jointo_cancel")
            markup.row(bt1)

            subjects = SubjectService.getSubjects(self.botDB)
            for i in range(len(subjects)):
                if QueueService.isQueueExist(self.botDB, subjects[i].id):

                    btCur = types.InlineKeyboardButton("Очередь по " + subjects[i].title,
                                                       callback_data="jointoNum_" + str(subjects[i].id))
                    markup.row(btCur)
            self.bot.send_message(message.chat.id, "В какую очередь ты хочешь записаться?", reply_markup=markup)
        else:
            self.bot.send_message(message.chat.id, "Для использования этой команды тебе нужно записаться в списочек"
                                                   " членов закрытого клуба любителей очередей.")

    def joinCommand(self, message):
        members = [member.tgNum for member in MemberService.getMembers(self.botDB)]
        if str(message.from_user.id) in members:
            self.joinConnector(message, -1)
        else:
            self.bot.send_message(message.chat.id, "Для использования этой команды тебе нужно записаться в списочек"
                                                   " членов закрытого клуба любителей очередей.")

    def joinConnector(self, message, queueId):
        if queueId == -1:
            queueId = QueueService.getLastQueue(self.botDB).id

        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Назад", callback_data="join_back")
        bt2 = types.InlineKeyboardButton("Первое свободное", callback_data="join_first")
        bt3 = types.InlineKeyboardButton("Определенное", callback_data="join_certain")
        bt4 = types.InlineKeyboardButton("Последнее свободное", callback_data="join_last")
        markup.row(bt1, bt2)
        markup.row(bt3, bt4)
        self.bot.send_message(message.chat.id, "Выбери место для записи", reply_markup=markup)

        self.joinList[message.from_user.id] = queueId

    def joinTextHandler(self, message):
        if message.from_user.id in self.joinCertainList:
            try:
                entryNum = int(message.text)
                if entryNum <= 0:
                    self.bot.send_message(message.chat.id, "Введи корректное число")
                    return
            except:
                self.bot.send_message(message.chat.id, "Введи корректное число")
                return

            count = MemberService.getMembersCount(self.botDB)
            if (count < entryNum):
                num = count
            else:
                num = entryNum

            if QueueService.isPlaceEmpty(self.botDB, num, self.joinCertainList[message.from_user.id]) == False:
                if QueueService.getMemberInQueueByPlace(self.botDB, self.joinCertainList[message.from_user.id], num).memberId \
                        == MemberService.getMemberByTgNum(self.botDB, message.from_user.id).id:
                    self.bot.send_message(message.chat.id,
                                          "Ты уже записан на желаемое место")
                    self.joinList.pop(message.from_user.id)
                    self.joinCertainList.pop(message.from_user.id)
                    return

            while num <= count:

                if QueueService.isPlaceEmpty(self.botDB, num, self.joinCertainList[message.from_user.id]):

                    QueueService.addToQueue(self.botDB, self.joinCertainList[message.from_user.id], message.from_user.id, num, 1)
                    if num != entryNum:
                        self.bot.send_message(message.chat.id,
                                              "Желаемое место уже занято. Ты записан на " + str(num) + " место")
                    else:
                        self.bot.send_message(message.chat.id, "Ты записан на " + str(num) + " место")
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
                    if QueueService.isPlaceEmpty(self.botDB, num, self.joinCertainList[message.from_user.id]):
                        QueueService.addToQueue(self.botDB, self.joinCertainList[message.from_user.id], message.from_user.id, num, 1)
                        if num != entryNum:
                            self.bot.send_message(message.chat.id,
                                                  "Желаемое место уже занято. Ты записан на " + str(num) + " место")
                        else:
                            self.bot.send_message(message.chat.id, "Ты записан на " + str(num) + " место")

                        self.joinList.pop(message.from_user.id)
                        self.joinCertainList.pop(message.from_user.id)
                        break
                    else:
                        num -= 1
            if num == 0 and message.from_user.id in self.joinCertainList:
                self.bot.send_message(message.chat.id, "Слишком много желающих записаться, на тебя места не хватило:)")

    def jointoCallback(self, callback):
        numStr = callback.data.strip("jointoNum_")
        numSubj = int(numStr)

        subj = SubjectService.getSubjectById(self.botDB, numSubj)

        if QueueService.isQueueExist(self.botDB, subj.id):
            queue = QueueService.getQueueBySubjectId(self.botDB, subj.id)
            self.bot.send_message(callback.message.chat.id, "Выбрана очередь по " + subj.title + ":\n")
            callback.message.from_user = callback.from_user

            self.joinConnector(callback.message, queue.id)
        else:
            self.bot.send_message(callback.message.chat.id, "Очередь по " + subj.title + " не существует.")


    def joinLastCallback(self, callback):
        if callback.from_user.id in self.joinList:
            place = MemberService.getMembersCount(self.botDB)
            while place >= 1:

                if QueueService.isPlaceEmpty(self.botDB, place, self.joinList[callback.from_user.id]):
                    QueueService.addToQueue(self.botDB, self.joinList[callback.from_user.id], callback.from_user.id, place, 2)
                    self.bot.send_message(callback.message.chat.id, "Ты записан на " + str(place) + " место")
                    self.joinList.pop(callback.from_user.id)
                    break
                else:
                    place -= 1


    def joinCertainCallback(self, callback):
        if callback.from_user.id in self.joinList:
            self.bot.send_message(callback.message.chat.id, "Введи место для записи")
            self.joinCertainList[callback.from_user.id] = self.joinList[callback.from_user.id]

    def joinFirstCallback(self, callback):
        if callback.from_user.id in self.joinList:

            count = MemberService.getMembersCount(self.botDB)
            place = 1
            while place <= count:
                if QueueService.isPlaceEmpty(self.botDB, place, self.joinList[callback.from_user.id]):
                    QueueService.addToQueue(self.botDB, self.joinList[callback.from_user.id], callback.from_user.id, place, 0)
                    self.bot.send_message(callback.message.chat.id, "Ты записан на " + str(place) + " место")
                    self.joinList.pop(callback.from_user.id)
                    break
                else:
                    place += 1

    def joinBackCallback(self, callback):
        if callback.from_user.id in self.joinList:
            callback.message.from_user = callback.from_user
            self.joinList.pop(callback.from_user.id)
            self.jointoCommand(callback.message)
