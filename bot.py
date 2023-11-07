import telebot

with open('token.txt') as file:
    lines = [line.rstrip() for line in file]
    token = lines[0]

bot = telebot.TeleBot(token)
