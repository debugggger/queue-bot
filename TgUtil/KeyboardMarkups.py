from telebot import types

EnterCancel = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True).add("Ввод", "❌ Отмена")
Remove = types.ReplyKeyboardRemove(selective=True)