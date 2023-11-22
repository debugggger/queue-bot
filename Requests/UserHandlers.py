import telebot
from telebot import types

from db import Database
from Requests.RuntimeInfoManager import RuntimeInfoManager
from utils import checkMemberName, removeBlank
from Requests.BaseHandler import BaseHandler

class UserHandlers(BaseHandler):
    def memberCommand(self, message: telebot.types.Message) -> None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True).add("Ввод", "Отмена")
        self.bot.reply_to(message, "Для продолжения нажми кнопку ввод", reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('member1', message.from_user.id)

    def setNameTextHandler(self, message: telebot.types.Message) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('member1', message.from_user.id):
            if message.text == "Ввод":
                self.bot.send_message(message.chat.id, 'Введи имя, которое будет отображаться при выводе сообщений',
                                      reply_markup=types.ReplyKeyboardRemove())
                self.runtimeInfoManager.sendBarrier.add('member2', message.from_user.id)
            else:
                self.bot.send_message(message.chat.id, 'Ввод отображаемого имени отменен',
                                      reply_markup=types.ReplyKeyboardRemove())
            return
        
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('member2', message.from_user.id):
            name = removeBlank(message.text)

            if not checkMemberName(name):
                self.bot.send_message(message.chat.id,
                                      'Отображаемое имя некорректно.\n'
                                      'Используйте не более 30 символов русского и английского алфавита.'
                                      'Также дефис, апостроф, пробел (но не более одного такого символа подряд).')
                return

            self.database.addMember(name, message.from_user.id)
            self.bot.reply_to(message, 'Отображаемое имя установлено')
