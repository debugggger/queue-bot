import re
import time

import telebot

def removeBlank(string: str) -> str:
    return ' '.join(string.split())

def checkSubjectTitle(title: str) -> bool:
    return bool(re.fullmatch('([A-Za-zА-Яа-яёЁ]+ ?)+', title)) and (len(title) <= 30)

def checkMemberName(name: str) -> bool:
    return bool(re.fullmatch('([A-Za-zА-Яа-яёЁ]+[ \-\']?)+', name)) and (len(name) <= 30)

def checkMessage(message: telebot.types.Message, chatId=None, timeout=3) -> bool:
    if timeout is not None and time.time() - message.date > timeout:
        return False
    if chatId is not None and (message.chat.id != chatId):
        return False
    return True
