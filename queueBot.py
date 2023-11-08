import telebot
from telebot import types

with open('token.txt') as file:
    lines = [line.rstrip() for line in file]
    token = lines[0]

bot=telebot.TeleBot(token)

setNameList = []
createQueueList = []

sendedMemberList = []

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    if message.from_user.id in setNameList:
        name = message.text
        bot.send_message(message.chat.id, "@" + message.from_user.username + " твое отоброжаемое имя " + name)
        setNameList.remove(message.from_user.id)
    # if message.from_user.id in createQueueList:
    #     name = message.text
    #     bot.send_message(message.chat.id, "Создана очередь по " + name)
    #     createQueueList.remove(message.from_user.id)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Возможности", callback_data="possibility")
    button2 = types.InlineKeyboardButton("Команды", callback_data="commands")
    markup.row(button1, button2)
    bot.send_message(message.chat.id,"Привет, я бот для составления очередей. \nТы можешь воспользоваться следующими командами, что бы более подробно узнать что я умею:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_message(message):
    commandsList(message)

@bot.message_handler(commands=['create'])
def create_message(message):
    createCommand(message)

@bot.message_handler(commands=['delete'])
def delete_message(message):
    deleteCommand(message)

@bot.message_handler(commands=['member'])
def member_message(message):
    memberCommand(message)

@bot.message_handler(commands=['show'])
def show_message(message):
    showCommand(message)

subjList = ["предмет 1", "предмет 2", "предмет 3"]

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == "help_member":
        callback.message.from_user = callback.from_user
        memberCommand(callback.message)

    if "createNum_" in callback.data:
        numStr = callback.data.strip("createNum_")
        numSubj = int(numStr)
        bot.send_message(callback.message.chat.id, "Создана очередь по " + subjList[numSubj])

    if "deleteNum_" in callback.data:
        numStr = callback.data.strip("deleteNum_")
        numSubj = int(numStr)
        bot.send_message(callback.message.chat.id, "Удалена очередь по " + subjList[numSubj])

    if "showNum_" in callback.data:
        numStr = callback.data.strip("showNum_")
        numSubj = int(numStr)
        bot.send_message(callback.message.chat.id, "Очередь по " + subjList[numSubj] + ":")

    if callback.data == "help_delete":
        deleteCommand(callback.message)
    if callback.data == "help_create":
        createCommand(callback.message)
    if callback.data == "help_show":
        showCommand(callback.message)

    if callback.data == "possibility":
        bot.send_message(callback.message.chat.id, "Бот, который поможет тебе не потеряться в бесконечных очередях.🤡\n"
                                                   "С его помощью ты можешь создать очередь и добавиться в нее, вывести "
                                                   "список добавленных пользователей. Бот позволяет не только выйти из "
                                                   "очереди, если ты захотел пойти на допсу, но и поменяться с другим человеком, "
                                                   "если, конечно, он будет на это согласен😈")
    if callback.data == "commands":
        commandsList(callback.message)


    #ToDo сделать кнопки неактивными
    if callback.data == "member_cancel":
        bot.delete_message(callback.message.chat.id, callback.message.id)
    if callback.data == "show_cancel":
        bot.delete_message(callback.message.chat.id, callback.message.id)
    if callback.data == "create_cancel":
        bot.delete_message(callback.message.chat.id, callback.message.id)
    if callback.data == "delete_cancel":
        bot.delete_message(callback.message.chat.id, callback.message.id)

    if callback.data == "member_add":
        if callback.message.from_user.id != 6872610637:
            if callback.message.from_user.id in sendedMemberList:
                bot.send_message(callback.message.chat.id, "Введи имя. которое будет отображаться при выводе сообщений:")
                setNameList.append(callback.message.from_user.id)
                sendedMemberList.remove(callback.message.from_user.id)
        else:
            if callback.from_user.id in sendedMemberList:
                bot.send_message(callback.message.chat.id, "Введи имя. которое будет отображаться при выводе сообщений:")
                setNameList.append(callback.from_user.id)
                sendedMemberList.remove(callback.from_user.id)

def commandsList(message):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton("/member", callback_data="help_member")
    bt2 = types.InlineKeyboardButton("/delete", callback_data="help_delete")
    bt3 = types.InlineKeyboardButton("/create", callback_data="help_create")
    bt4 = types.InlineKeyboardButton("/show", callback_data="help_show")
    markup.row(bt1, bt2, bt3, bt4)
    bot.send_message(message.chat.id, "можно воспользоваться следующими командами:", reply_markup=markup)

def memberCommand(message):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton("Ввод", callback_data="member_add")
    bt2 = types.InlineKeyboardButton("Отмена", callback_data="member_cancel")
    markup.row(bt1, bt2)
    bot.send_message(message.chat.id, "Для продолжения нажми кнопку ввод",
                     reply_markup=markup)
    sendedMemberList.append(message.from_user.id)


def createCommand(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    bt1 = types.InlineKeyboardButton("Отмена", callback_data="create_cancel")
    markup.row(bt1)
    for i in range(len(subjList)):
        btCur = types.InlineKeyboardButton(str(subjList[i]), callback_data="createNum_" + str(i))
        markup.row(btCur)
    bot.send_message(message.chat.id, "По какому предмету ты хочешь создать очередь?", reply_markup=markup)

def showCommand(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    bt1 = types.InlineKeyboardButton("Отмена", callback_data="show_cancel")
    markup.row(bt1)
    for i in range(len(subjList)):
        btCur = types.InlineKeyboardButton(str(subjList[i]), callback_data="showNum_" + str(i))
        markup.row(btCur)
    bot.send_message(message.chat.id, "По какому предмету ты хочешь просмотреть очередь?", reply_markup=markup)

def deleteCommand(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    bt1 = types.InlineKeyboardButton("Отмена", callback_data="delete_cancel")
    markup.row(bt1)
    for i in range(len(subjList)):
        btCur = types.InlineKeyboardButton(str(subjList[i]), callback_data="deleteNum_" + str(i))
        markup.row(btCur)
    bot.send_message(message.chat.id, "По какому предмету ты хочешь удалить очередь?", reply_markup=markup)

bot.infinity_polling()