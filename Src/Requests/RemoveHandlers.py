import telebot
from telebot import types

from Requests.RuntimeInfoManager import RuntimeInfoManager
from Requests.BaseHandler import BaseHandler
from Services.MemberService import MemberService
from Services.QueueService import QueueService
from Services.SubjectService import SubjectService
from Requests.QueueFun import updateLastQueueText


class RemoveHandlers(BaseHandler):
    def removefromCommand(self, message: telebot.types.Message):
        if not MemberService.isMemberExistByTgNum(self.database, message.from_user.id):
            self.bot.reply_to(message, 'Для использования этой команды тебе нужно записаться в списочек member-ов')
            return
        curMember = MemberService.getMemberByTgNum(self.database, message.from_user.id)
        if not self.runtimeInfoManager.checkReplace(curMember.id):
            self.bot.reply_to(message, "Извините, у вас есть запрос на смену места",
                              reply_markup=types.ReplyKeyboardRemove(selective=True))
            return
        if QueueService.isAnyQueueExist(self.database):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            markup.add('❌ Отмена')
            for s in SubjectService.getSubjects(self.database):
                if QueueService.isQueueExist(self.database, s.id):
                    markup.add(f'Очередь по {s.title}')

            self.bot.reply_to(message, 'Из какой очереди ты хочешь выйти', reply_markup=markup)
            self.runtimeInfoManager.sendBarrier.add('removefrom', message.from_user.id)
        else:
            self.bot.reply_to(message, 'Еще нет никаких очередей. Радуйся!',
                              reply_markup=types.ReplyKeyboardRemove(selective=True))

    def removefromTextHandler(self, message: telebot.types.Message):
        if self.runtimeInfoManager.sendBarrier.checkAndRemove('removefrom', message.from_user.id):
            if not message.text.startswith('Очередь по '):
                self.bot.reply_to(message, 'Команда отменена', reply_markup=types.ReplyKeyboardRemove(selective=True))
                return

            subjectTitle = message.text.removeprefix('Очередь по ')

            if not SubjectService.isSubjectExist(self.database, subjectTitle):
                self.bot.reply_to(message, 'Такого предмета не существует',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))
                return

            subject = SubjectService.getSubjectByTitle(self.database, subjectTitle)
            if QueueService.isQueueExist(self.database, subject.id):
                queue = QueueService.getQueueBySubjectId(self.database, subject.id)
                member = MemberService.getMemberByTgNum(self.database, message.from_user.id)
                if not QueueService.isMemberInQueue(self.database, queue.id, member.id):
                    self.bot.reply_to(message, 'Тебя еще нет в этой очереди. Как так то?!',
                                      reply_markup=types.ReplyKeyboardRemove(selective=True))
                else:

                    place = QueueService.getPlaceByMemberId(self.database, queue.id, member.id)
                    QueueService.deleteQueueMember(self.database, queue.id, member.id)
                    self.bot.reply_to(message, 'Ты вышел из этой очереди',
                                      reply_markup=types.ReplyKeyboardRemove(selective=True))

                    self.updateQueue(message, place, queue)
                    updateLastQueueText(self.bot, self.database, queue.id, self.runtimeInfoManager)


            else:
                self.bot.reply_to(message, 'Очереди по этому предмету еще нет. Самое время создать ее!',
                                  reply_markup=types.ReplyKeyboardRemove(selective=True))

    def updateQueue(self, message: telebot.types.Message, place, queue):
        members = QueueService.getMembersInQueue(self.database, queue.id)
        count = 0
        m = {}
        for mem in members:
            m[mem.member.tgNum] = mem.placeNumber
        m = {k: v for k, v in sorted(m.items(), key=lambda item: item[1])}

        for tgId in m.keys():
            if m[tgId] > place:
                m[tgId] -= 1
                if count == 0:
                    chatMember = self.bot.get_chat_member(message.chat.id, tgId)
                    self.bot.send_message(message.chat.id, '@' + chatMember.user.username + ' твоя очередь сдавать')
                    count = 1

                QueueService.addToQueue(self.database, queue.id, int(tgId), int(m[tgId]), int(QueueService.getMemberInQueueByPlace(self.database, queue.id, int(m[tgId])+1).entryType))
            else:
                count = 1