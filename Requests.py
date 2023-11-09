from telebot import types

class ReqParser():
    def __init__(self, bot):
        self.bot = bot
        self.setNameList = []
        self.sendedMemberList = []
        self.joinCertainList = []
        self.joinList = []
        self.subjList = ["предмет 1", "предмет 2", "предмет 3"]

    def commandsList(self, message):
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton("/member", callback_data="help_member")
        bt2 = types.InlineKeyboardButton("/show", callback_data="help_show")
        bt3 = types.InlineKeyboardButton("/create", callback_data="help_create")
        bt4 = types.InlineKeyboardButton("/join", callback_data="help_join")
        bt5 = types.InlineKeyboardButton("/jointo", callback_data="help_jointo")
        bt6 = types.InlineKeyboardButton("/delete", callback_data="help_delete")
        markup.row(bt1, bt2)
        markup.row(bt3, bt4)
        markup.row(bt5, bt6)
        self.bot.send_message(message.chat.id, "можно воспользоваться следующими командами:\n"
                                               "/member - добавление в список пользователей\n"
                                               "/show - вывод очерди\n"
                                               "/create - создание очереди\n"
                                               "/join - запись в последнюю очередь\n"
                                               "/jointo - запись в любую из очередей\n"
                                               "/delete - удаление очереди", reply_markup=markup)

    def memberCommand(self, message):
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton("Ввод", callback_data="member_add")
        bt2 = types.InlineKeyboardButton("Отмена", callback_data="member_cancel")
        markup.row(bt1, bt2)
        self.bot.send_message(message.chat.id, "Для продолжения нажми кнопку ввод",
                         reply_markup=markup)
        self.sendedMemberList.append(message.from_user.id)

    def createCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="create_cancel")
        markup.row(bt1)
        for i in range(len(self.subjList)):
            btCur = types.InlineKeyboardButton(str(self.subjList[i]), callback_data="createNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь создать очередь?", reply_markup=markup)

    def showCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="show_cancel")
        markup.row(bt1)
        for i in range(len(self.subjList)):
            btCur = types.InlineKeyboardButton(str(self.subjList[i]), callback_data="showNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь просмотреть очередь?", reply_markup=markup)

    def jointoCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="jointo_cancel")
        markup.row(bt1)
        for i in range(len(self.subjList)):
            btCur = types.InlineKeyboardButton("Очередь по " + str(self.subjList[i]),
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

    def deleteCommand(self, message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        bt1 = types.InlineKeyboardButton("Отмена", callback_data="delete_cancel")
        markup.row(bt1)
        for i in range(len(self.subjList)):
            btCur = types.InlineKeyboardButton(str(self.subjList[i]), callback_data="deleteNum_" + str(i))
            markup.row(btCur)
        self.bot.send_message(message.chat.id, "По какому предмету ты хочешь удалить очередь?", reply_markup=markup)
