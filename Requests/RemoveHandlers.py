import telebot
from telebot import types

from Requests.RuntimeInfoManager import RuntimeInfoManager
from Requests.BaseHandler import BaseHandler

class RemoveHandlers(BaseHandler):
    def removefromCommand(self, message: telebot.types.Message):
        if not self.database.isMemberExistByTgNum(message.from_user.id):
            self.bot.reply_to(message, 'Для использования этой команды тебе нужно записаться в списочек member-ов')
            return
        #markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        #for s in self.database.getSubjects():
        #    markup.add(s.title)
        #self.bot.reply_to(message, 'Из какой очереди ты хочешь выйти', reply_markup=markup)
        #self.runtimeInfoManager.sendBarrier.add('removefrom', message.from_user.id)

    def removeSubjectTextHandler(self, message: telebot.types.Message):
        #if self.runtimeInfoManager.sendBarrier.checkAndRemove('removefrom', message.from_user.id):
        #    if self.database.getQueueIdBySubj() == -1:
        #        self.bot.reply_to(message, 'Очереди по этому предмету еще нет. Самое время создать ее!',
        #                          reply_markup=types.ReplyKeyboardRemove())
                
            