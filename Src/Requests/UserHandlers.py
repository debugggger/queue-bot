import telebot
from Services.MemberService import MemberService

from utils import checkMemberName, removeBlank
from Requests.BaseHandler import BaseHandler
import TgUtils.KeyboardMarkups as km

class UserHandlers(BaseHandler):
    def memberCommand(self, message: telebot.types.Message) -> None:
        self.bot.reply_to(message, "Для продолжения нажми кнопку ввод", reply_markup=km.EnterCancel)
        self.runtimeInfoManager.sendBarrier.add('member1', message.from_user.id)

    def setNameTextHandler(self, message: telebot.types.Message) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('member1', message.from_user.id):
            if message.text == "Ввод":
                self.bot.reply_to(message, 'Введи имя, которое будет отображаться при выводе сообщений',
                                  reply_markup=km.Remove)
                self.runtimeInfoManager.sendBarrier.add('member2', message.from_user.id)
            else:
                self.bot.reply_to(message, 'Ввод отображаемого имени отменен',
                                  reply_markup=km.Remove)
            return
        
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('member2', message.from_user.id):
            name = removeBlank(message.text)

            if not checkMemberName(name):
                self.bot.reply_to(message,
                                      'Отображаемое имя некорректно.\n'
                                      'Используйте не более 30 символов русского и английского алфавита.'
                                      'Также дефис, апостроф, пробел (но не более одного такого символа подряд).')
                return

            MemberService.addMember(self.database, name, message.from_user.id)
            self.bot.reply_to(message, 'Отображаемое имя установлено')
