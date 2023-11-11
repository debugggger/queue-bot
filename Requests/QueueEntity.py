from telebot import types

class QueueEntity():
    def __init__(self, bot, botDB):
        self.bot = bot
        self.botDB = botDB

    def createCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="create_cancel")
        markup.row(bt1)
        for i in range(len(self.subj.getSubj())):
            btCur = types.InlineKeyboardButton(str(self.subj.getSubj()[i]), callback_data="createNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь создать очередь?", reply_markup=markup)

    def deleteCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="delete_cancel")
        markup.row(bt1)
        for i in range(len(self.subj.getSubj())):
            btCur = types.InlineKeyboardButton(str(self.subj.getSubj()[i]), callback_data="deleteNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь удалить очередь?", reply_markup=markup)


    def createCallback(self, callback):
        numStr = callback.data.strip("createNum_")
        numSubj = int(numStr)
        self.bot.send_message(callback.message.chat.id, "Создана очередь по " + self.subj.getSubj()[numSubj])

    def deleteCallback(self, callback):
        numStr = callback.data.strip("deleteNum_")
        numSubj = int(numStr)
        self.bot.send_message(callback.message.chat.id, "Удалена очередь по " + self.subj.getSubj()[numSubj])

    def showCallback(self, callback):
        numStr = callback.data.strip("showNum_")
        numSubj = int(numStr)
        self.bot.send_message(callback.message.chat.id, "Очередь по " + self.subj.getSubj()[numSubj] + ":\n")

    def showCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="show_cancel")
        markup.row(bt1)
        for i in range(len(self.subj.getSubj())):
            btCur = types.InlineKeyboardButton(str(self.subj.getSubj()[i]), callback_data="showNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь просмотреть очередь?", reply_markup=markup)
