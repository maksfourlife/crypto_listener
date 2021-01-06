from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
from os import path
import json

from .commands import Commands
from ..listener import Listener

CONFIG_PATH = path.join(path.dirname(__file__), "../config.json")


class Bot:
    def __init__(self, transactions, notification_rate=60, config_path=None):
        with open(config_path or CONFIG_PATH, "r") as file:
            self.config = json.loads(file.read())
        self.transactions = transactions
        self.updater = Updater(token=self.config["bot_token"], use_context=True)

        self.updater.dispatcher.add_handler(CommandHandler("start", Commands.start))
        self.updater.dispatcher.add_handler(CommandHandler("stop", Commands.stop(self.transactions)))
        self.updater.dispatcher.add_handler(CommandHandler("listen", Commands.listen(self.transactions)))

        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(self.notificate, "interval", seconds=notification_rate)

    def notificate(self):
        for transaction in self.transactions:
            notification = transaction.get_notification()
            if not notification:
                continue
            for chat in transaction.chats:
                self.updater.bot.send_message(chat_id=chat, message=notification)

    def start(self):
        self.updater.start_polling()
