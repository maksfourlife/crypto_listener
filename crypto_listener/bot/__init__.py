from telegram.ext import Updater, CommandHandler
from os import path
import json

from .commands import Commands
from ..listener import Listener

CONFIG_PATH = path.join(path.dirname(__file__), "../config.json")


class Bot:
    def __init__(self, transactions, config_path=None):
        with open(config_path or CONFIG_PATH, "r") as file:
            self.config = json.loads(file.read())
        self.transactions = transactions
        self.updater = Updater(token=self.config["bot_token"], use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler("start", Commands.start(self.chats)))
        self.updater.dispatcher.add_handler(CommandHandler("stop", Commands.stop(self.chats)))
        self.updater.dispatcher.add_handler(CommandHandler("listen", Commands.listen(self.transactions)))

    def notificate(self):
        for transaction in self.transactions:
            notification = transaction.notification()
            for chat in transaction.chats:
                self.updater.bot.send_message(chat_id=chat, message=notification)

    def start(self):
        self.updater.start_polling()
