import telebot

from Requests.BaseHandler import BaseHandler
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from TgUtils.KeyboardMarkups import makeSubjectListMarkup
from utils import checkSubjectTitle, removeBlank
import TgUtils.KeyboardMarkups as km


class SubjectHandlers(BaseHandler):
    def subjectCommand(self, message: telebot.types.Message) -> None:
        chatMember: telebot.types.ChatMember = self.bot.get_chat_member(message.chat.id, message.from_user.id)
        if chatMember.status not in ['creator', 'administrator']:
            self.bot.reply_to(message, 'Эту команду могут выполнять только администраторы')
            return

        self.bot.reply_to(message, "Для продолжения нажми кнопку ввод", reply_markup=km.EnterCancel)
        self.runtimeInfoManager.sendBarrier.add('subject1', message.from_user.id)

    def removesubjectCommand(self, message: telebot.types.Message) -> None:
        chatMember: telebot.types.ChatMember = self.bot.get_chat_member(message.chat.id, message.from_user.id)
        if chatMember.status not in ['creator', 'administrator']:
            self.bot.reply_to(message, 'Эту команду могут выполнять только администраторы')
            return

        markup = makeSubjectListMarkup(SubjectService.getSubjects(self.database))
        self.bot.reply_to(message, 'Удалить предмет', reply_markup=markup)
        self.runtimeInfoManager.sendBarrier.add('removesubject', message.from_user.id)

    def subjectTextHandler(self, message: telebot.types.Message) -> None:
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('subject1', message.from_user.id):
            if message.text == "Ввод":
                self.bot.reply_to(message, 'Введи название предмета',
                                  reply_markup=km.Remove)
                self.runtimeInfoManager.sendBarrier.add('subject2', message.from_user.id)
            else:
                self.bot.reply_to(message, 'Ввод отображаемого названия отменен',
                                  reply_markup=km.Remove)
            return

        if self.runtimeInfoManager.sendBarrier.checkAndRemove('subject2', message.from_user.id):
            title: str = removeBlank(message.text)
            
            if not checkSubjectTitle(title):
                self.bot.reply_to(message,
                                      'Название предмета некорректно.\n'
                                      'Используйте не более 30 символов русского и английского алфавита.')
                return

            if SubjectService.isSubjectExist(self.database, title):
                self.bot.reply_to(message, f'Предмет {title} уже существует')
                return

            SubjectService.addSubject(self.database, title)
            self.bot.reply_to(message, f'Предмет {title} добавлен')

        if self.runtimeInfoManager.sendBarrier.checkAndRemove('removesubject', message.from_user.id):
            if message.text == '❌ Отмена':
                self.bot.reply_to(message, 'Команда отменена',
                                  reply_markup=km.Remove)
                return

            subjectTitle = message.text
            if not SubjectService.isSubjectExist(self.database, subjectTitle):
                self.bot.reply_to(message, 'Такого предмета и так не было. Зачем удалять то...',
                                  reply_markup=km.Remove)
                return

            subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)
            if QueueService.isQueueExist(self.database, subject.id):
                self.bot.reply_to(message, 'По этому предмету есть очередь. Для начала удалите ее',
                                  reply_markup=km.Remove)
                return

            SubjectService.removeSubject(self.database, subjectTitle)
            self.bot.reply_to(message, 'Предмет удален',
                                reply_markup=km.Remove)
