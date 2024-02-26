from telebot import types
from typing import List
from Entities.Subject import Subject


EnterCancel = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True).add("Ввод", "❌ Отмена")
Remove = types.ReplyKeyboardRemove(selective=True)

def makeSubjectListMarkup(subjects: List[Subject]) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
    markup.add('❌ Отмена')
    for s in subjects:
        markup.add(s.title)
    return markup

def makeQueueListMarkup(subjects: List[Subject]) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
    markup.add('❌ Отмена')
    for s in subjects:
        markup.add(f'Очередь по {s.title}')
    return markup
