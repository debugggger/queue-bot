import telebot
from telebot import types

from DbUtils.db import Database
from Requests.RuntimeInfoManager import RuntimeInfoManager

class BaseHandler:
    def __init__(self, bot: telebot.TeleBot, database: Database, runtimeInfoManager: RuntimeInfoManager):
        self.bot: telebot.TeleBot = bot
        self.database: Database = database
        self.runtimeInfoManager: RuntimeInfoManager = runtimeInfoManager
