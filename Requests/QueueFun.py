
from telebot import types

class QueueFun():
    def __init__(self, bot, botDB):
        self.bot = bot
        self.botDB = botDB
        self.joinCertainList = {}
        self.joinList = {}


    def jointoCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="jointo_cancel")
        markup.row(bt1)

        subjects = [subject.title for subject in self.botDB.getSubjects()]

        for i in range(len(subjects)):
            btCur = types.InlineKeyboardButton("Очередь по " + str(subjects[i]),
                                               callback_data="jointoNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "В какую очередь ты хочешь записаться?", reply_markup=markup)

    def joinCommand(self, message):
        self.joinConnector(message, -1)

    def joinConnector(self, message, queueId):
        if queueId == -1:
            queueId = self.botDB.getLastQueue()

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

            if self.botDB.getMemberInQueueByPlace(self.joinCertainList[message.from_user.id], entryNum) == self.botDB.getMemberByTgNum(message.from_user.id).id:
                self.bot.send_message(message.chat.id,
                                      "Ты уже записан на место " + str(entryNum))
                self.joinList.pop(message.from_user.id)
                self.joinCertainList.pop(message.from_user.id)
                return

            count = self.botDB.getMembersCount()
            if (count < entryNum):
                num = count
            else:
                num = entryNum

            while num >= 1:
                if (self.botDB.checkPlace(num, self.joinCertainList[message.from_user.id])):
                    self.botDB.addToQueue(self.joinCertainList[message.from_user.id], message.from_user.id, num, 1)
                    if num != entryNum:
                        self.bot.send_message(message.chat.id, "Место №" + str(entryNum) + " уже занято. Ты записан на " + str(num) + " место")
                    else:
                        self.bot.send_message(message.chat.id, "Ты записан на " + str(num) + " место")

                    self.joinList.pop(message.from_user.id)
                    self.joinCertainList.pop(message.from_user.id)
                    break
                else:
                    num -= 1

            if num == 0 and message.from_user.id in self.joinCertainList:
                num = entryNum
                while num <= count:
                    if (self.botDB.checkPlace(num, self.joinCertainList[message.from_user.id])):
                        self.botDB.addToQueue(self.joinCertainList[message.from_user.id], message.from_user.id, num, 1)
                        if num != entryNum:
                            self.bot.send_message(message.chat.id, "Место №" + str(entryNum) + " уже занято. Ты записан на " + str(num) + " место")
                        else:
                            self.bot.send_message(message.chat.id, "Ты записан на " + str(num) + " место")
                        self.joinList.pop(message.from_user.id)
                        self.joinCertainList.pop(message.from_user.id)
                        break
                    else:
                        num += 1


    def jointoCallback(self, callback):
        numStr = callback.data.strip("jointoNum_")
        numSubj = int(numStr)
        subjects = [subject.title for subject in self.botDB.getSubjects()]
        id = self.botDB.getQueueIdBySubj(subjects[numSubj])
        if id == -1:
            self.bot.send_message(callback.message.chat.id, "Очередь по " + subjects[numSubj] + " не существует.")
            return

        self.bot.send_message(callback.message.chat.id, "Выбрана очередь по " + subjects[numSubj] + ":\n")
        callback.message.from_user = callback.from_user

        self.joinConnector(callback.message, id)


    def joinLastCallback(self, callback):
        if callback.from_user.id in self.joinList:
            place = self.botDB.getMembersCount()
            while place >= 1:
                if (self.botDB.checkPlace(place, self.joinList[callback.from_user.id])):
                    self.botDB.addToQueue(self.joinList[callback.from_user.id], callback.from_user.id, place, 2)
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

            count = self.botDB.getMembersCount()
            place = 1
            while place <= count:
                if (self.botDB.checkPlace(place, self.joinList[callback.from_user.id])):
                    self.botDB.addToQueue(self.joinList[callback.from_user.id], callback.from_user.id, place, 0)
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
