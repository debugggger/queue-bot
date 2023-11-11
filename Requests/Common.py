from telebot import types

class CommonReq():
    def __init__(self, bot, botDB, user, qEntity, qFun, subj):
        self.bot = bot
        self.botDB = botDB
        self.user = user
        self.qFun = qFun
        self.qEntity = qEntity
        self.subj = subj

    def textHandler(self, message):
        self.subj.subjectTextHandler(message)
        self.user.setNameTextHandler(message)
        self.qFun.joinTextHandler(message)

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

    def startCommand(self, message):
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Возможности", callback_data="possibility")
        button2 = types.InlineKeyboardButton("Команды", callback_data="commands")
        markup.row(button1, button2)
        self.bot.send_message(message.chat.id,
                         "Привет! Я бот для составления очередей.\nТы можешь воспользоваться следующими "
                         "командами, что бы более подробно узнать что я умею:", reply_markup=markup)

    def callback(self, callback):
        callback.message.from_user = callback.from_user
        if callback.data.startswith(self.subj.c_callbackPrefixRemovesubject) and callback.from_user.id in self.subj.removesubjectUserList:
            self.subj.removesubjectCallback(callback)
        elif "createNum_" in callback.data:
            self.qEntity.createCallback(callback)
        elif "deleteNum_" in callback.data:
            self.qEntity.deleteCallback(callback)
        elif "showNum_" in callback.data:
            self.qEntity.showCallback(callback)
        elif "jointoNum_" in callback.data:
            self.qFun.jointoCallback(callback)
        else:
            match callback.data:
                case "help_member":
                    self.user.memberCommand(callback.message)
                case "help_show":
                    self.qEntity.showCommand(callback.message)
                case "help_delete":
                    self.qEntity.deleteCommand(callback.message)
                case "help_create":
                    self.qEntity.createCommand(callback.message)
                case "help_join":
                    self.qFun.joinCommand(callback.message)
                case "help_jointo":
                    self.qFun.jointoCommand(callback.message)
                case "commands":
                    self.commandsList(callback.message)
                case "possibility":
                    self.bot.send_message(callback.message.chat.id, "Бот, который поможет тебе не потеряться в бесконечных "
                                                               "очередях.🤡\n С его помощью ты можешь создать очередь и "
                                                               "добавиться в нее, вывести список добавленных пользователей."
                                                               " Бот позволяет не только выйти из очереди, если ты захотел "
                                                               "пойти на допсу, но и поменяться с другим человеком, если, "
                                                               "конечно, он будет на это согласен😈")
                case "member_cancel" | "show_cancel" | "create_cancel" | "delete_cancel" | "jointo_cancel":
                    self.bot.delete_message(callback.message.chat.id, callback.message.id)

                case "member_add":
                    self.user.memberAddCallback(callback)
                case "join_back":
                    self.qFun.joinBackCallback(callback)
                case "join_first":
                    self.qFun.joinFirstCallback(callback)
                case "join_certain":
                    self.qFun.joinCertainCallback(callback)
                case "join_last":
                    self.qFun.joinLastCallback(callback)

                case _:
                    return
