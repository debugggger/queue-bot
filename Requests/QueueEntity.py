from telebot import types

from Services.SubjectService import SubjectService

class QueueEntity():
    def __init__(self, bot, botDB):
        self.bot = bot
        self.botDB = botDB

    def createCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="create_cancel")
        markup.row(bt1)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.botDB)]
        
        for i in range(len(subjects)):
            btCur = types.InlineKeyboardButton(str(subjects[i]), callback_data="createNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь создать очередь?", reply_markup=markup)

    def deleteCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="delete_cancel")
        markup.row(bt1)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.botDB)]

        for i in range(len(subjects)):
            btCur = types.InlineKeyboardButton(str(subjects[i]), callback_data="deleteNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь удалить очередь?", reply_markup=markup)


    def createCallback(self, callback):
        numStr = callback.data.strip("createNum_")
        numSubj = int(numStr)
        self.botDB.createQueue(numSubj)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.botDB)]
        self.bot.send_message(callback.message.chat.id, "Создана очередь по " + subjects[numSubj])

    def deleteCallback(self, callback):
        numStr = callback.data.strip("deleteNum_")
        numSubj = int(numStr)
        self.botDB.deleteQueue(numSubj)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.botDB)]
        self.bot.send_message(callback.message.chat.id, "Удалена очередь по " + subjects[numSubj])

    def showCallback(self, callback):
        numStr = callback.data.strip("showNum_")
        numSubj = int(numStr)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.botDB)]
        self.bot.send_message(callback.message.chat.id, "Очередь по " + subjects[numSubj] + ":\n")

    def showCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="show_cancel")
        markup.row(bt1)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.botDB)]

        for i in range(len(subjects)):
            btCur = types.InlineKeyboardButton(str(subjects[i]), callback_data="showNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь просмотреть очередь?", reply_markup=markup)
