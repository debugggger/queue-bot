import telebot
from telebot import types

from Requests.BaseHandler import BaseHandler
from Requests.RuntimeInfoManager import RuntimeInfoManager
from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from utils import removeBlank, checkSubjectTitle


class QueueEntity(BaseHandler):

    def createCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="create_cancel")
        markup.row(bt1)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.database)]
        
        for i in range(len(subjects)):
            btCur = types.InlineKeyboardButton(str(subjects[i]), callback_data="createNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь создать очередь?", reply_markup=markup)

    def deleteCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="delete_cancel")
        markup.row(bt1)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.database)]

        for i in range(len(subjects)):
            btCur = types.InlineKeyboardButton(str(subjects[i]), callback_data="deleteNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь удалить очередь?", reply_markup=markup)


    def createCallback(self, callback):
        numStr = callback.data.strip("createNum_")
        numSubj = int(numStr)
        self.database.createQueue(numSubj)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.database)]
        self.bot.send_message(callback.message.chat.id, "Создана очередь по " + subjects[numSubj])

    def deleteCallback(self, callback):
        numStr = callback.data.strip("deleteNum_")
        numSubj = int(numStr)
        self.database.deleteQueue(numSubj)
        subjects = [subject.title for subject in SubjectService.getSubjects(self.database)]
        self.bot.send_message(callback.message.chat.id, "Удалена очередь по " + subjects[numSubj])

    def showCallback(self, callback):
        numStr = callback.data.strip("showNum_")
        numSubj = int(numStr)
        subjects = SubjectService.getSubjectById(self.database, numSubj)
        self.bot.send_message(callback.message.chat.id, "Очередь по " + subjects.title + ":\n")

    def showCommand(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        subjects = SubjectService.getSubjects(self.database)

        for i in range(len(subjects)):
            if QueueService.isQueueExist(self.database, subjects[i].id):
                markup.add(str(subjects[i].title))

        markup.add("Отмена")
        self.bot.reply_to(message, 'По какому предмету ты хочешь просмотреть очередь?', reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('show', message.from_user.id)

    def queueTextHandler(self, message: telebot.types.Message) -> None:

        if self.runtimeInfoManager.sendBarrier.check('show', message.from_user.id):
            title: str = removeBlank(message.text)

            if SubjectService.isSubjectExist(self.database, title):

                qList = {}
                subj = SubjectService.getSubjectByTitle(self.database, title)
                queue = QueueService.getQueueBySubjectId(self.database, subj.id)
                for member in queue.members:
                    val =  " - " + str(MemberService.getMemberById(self.database, member.memberId).name) + "\n"

                    qList [member.placeNumber] = val

                sortedQ = {k: v for k, v in sorted(qList.items())}
                resStr = ''
                for q in sortedQ:
                    resStr += str(q) + sortedQ[q]

                self.bot.send_message(message.chat.id, "Очередь по " + title + ":\n" + resStr)
            elif title != "Отмена":
                self.bot.send_message(message.chat.id, "Очереди по такому предмету нет")
