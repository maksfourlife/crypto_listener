from telegram.ext import Updater, CommandHandler
from threading import Thread
from os import path
import json
import time

from .commands import Commands
from ..listener import Listener

CONFIG_PATH = path.join(path.dirname(__file__), "../config.json")


class Bot:
    def __init__(self, transactions, config_path=None, notification_rate=60):
        with open(config_path or CONFIG_PATH, "r") as file:
            self.config = json.loads(file.read())
        self.transactions = transactions
        self.notification_rate = notification_rate
        self.updater = Updater(token=self.config["bot_token"], use_context=True)

        self.updater.dispatcher.add_handler(CommandHandler("start", Commands.start))
        self.updater.dispatcher.add_handler(CommandHandler("stop", Commands.stop(self.transactions)))
        self.updater.dispatcher.add_handler(CommandHandler("listen", Commands.listen(self.transactions)))
        self.updater.dispatcher.add_handler(CommandHandler("unlisten", Commands.unlisten(self.transactions)))

        Thread(target=self.notificate, name="bot_notificator", daemon=True).start()

    def notificate(self):
        while True:
            for transaction in self.transactions.values():
                notification = transaction.get_notification()
                if not notification:
                    continue
                for chat in transaction.chats:
                    self.updater.bot.send_message(chat_id=chat, text=notification)
            time.sleep(self.notification_rate)

    def start(self):
        self.updater.start_polling()
