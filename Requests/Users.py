from telebot import types

class Users():
    def __init__(self, bot, botDB):
        self.bot = bot
        self.botDB = botDB
        self.setNameList = []
        self.sendedMemberList = []

    def memberCommand(self, message):
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton("Ввод", callback_data="member_add")
        bt2 = types.InlineKeyboardButton("Отмена", callback_data="member_cancel")
        markup.row(bt1, bt2)
        self.bot.send_message(message.chat.id, "Для продолжения нажми кнопку ввод",
                         reply_markup=markup)
        self.sendedMemberList.append(message.from_user.id)

    def memberAddCallback(self, callback):
        if callback.from_user.id in self.sendedMemberList:
            self.bot.send_message(callback.message.chat.id,
                                  "Введи имя, которое будет отображаться при выводе сообщений:")
            self.setNameList.append(callback.from_user.id)
            self.sendedMemberList.remove(callback.from_user.id)

    def setNameTextHandler(self, message):
        if message.from_user.id in self.setNameList:
            name = message.text
            self.bot.reply_to(message, "Отображаемое имя установлено")
            self.botDB.add_member(message.from_user.username, message.from_user.id)
            self.setNameList.remove(message.from_user.id)
