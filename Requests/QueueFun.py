from telebot import types



class QueueFun():
    def __init__(self, bot, subj):
        self.bot = bot
        self.joinCertainList = []
        self.joinList = []
        self.subj = subj

    def jointoCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="jointo_cancel")
        markup.row(bt1)
        for i in range(len(self.subj.getSubj())):
            btCur = types.InlineKeyboardButton("Очередь по " + str(self.subj.getSubj()[i]),
                                               callback_data="jointoNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "В какую очередь ты хочешь записаться?", reply_markup=markup)

    def joinCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Назад", callback_data="join_back")
        bt2 = types.InlineKeyboardButton("Первое свободное", callback_data="join_first")
        bt3 = types.InlineKeyboardButton("Определенное", callback_data="join_certain")
        bt4 = types.InlineKeyboardButton("Последнее", callback_data="join_last")
        markup.row(bt1, bt2)
        markup.row(bt3, bt4)
        self.bot.send_message(message.chat.id, "Выбери место для записи", reply_markup=markup)
        self.joinList.append(message.from_user.id)

    def joinTextHandler(self, message):
        if message.from_user.id in self.joinCertainList:
            num = message.text
            self.bot.reply_to(message, "Ты записан на место " + str(num))
            self.joinCertainList.remove(message.from_user.id)

    def jointoCallback(self, callback):
        numStr = callback.data.strip("jointoNum_")
        numSubj = int(numStr)
        self.bot.send_message(callback.message.chat.id, "Выбрана очередь по " + self.subj.getSubj()[numSubj] + ":\n")
        callback.message.from_user = callback.from_user
        self.joinCommand(callback.message)

    def joinLastCallback(self, callback):
        if callback.from_user.id in self.joinList:
            num = 10
            self.bot.send_message(callback.message.chat.id, "Ты записан на " + str(num) + " место")
            self.joinList.remove(callback.from_user.id)

    def joinCertainCallback(self, callback):
        if callback.from_user.id in self.joinList:
            self.bot.send_message(callback.message.chat.id, "Введи место для записи")
            self.joinCertainList.append(callback.from_user.id)
            self.joinList.remove(callback.from_user.id)

    def joinFirstCallback(self, callback):
        if callback.from_user.id in self.joinList:
            num = 1
            self.bot.send_message(callback.message.chat.id, "Ты записан на " + str(num) + " место")
            self.joinList.remove(callback.from_user.id)

    def joinBackCallback(self, callback):
        if callback.from_user.id in self.joinList:
            callback.message.from_user = callback.from_user
            self.joinList.remove(callback.from_user.id)
            self.jointoCommand(callback.message)
