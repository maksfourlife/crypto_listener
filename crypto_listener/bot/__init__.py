from telegram.ext import Updater, CommandHandler
from os import path
import json

from .commands import Commands
from ..listener import Listener

CONFIG_PATH = path.join(path.dirname(__file__), "../config.json")


class Bot:
    def __init__(self, config_path=None):
        with open(config_path or CONFIG_PATH, "r") as file:
            self.config = json.loads(file.read())
        self.listener = Listener()
        self.updater = Updater(token=self.config["bot_token"], use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler("start", Commands.start))
        self.updater.dispatcher.add_handler(CommandHandler("listen", Commands.listen(self.listener.listen)))

    def start(self):
        self.updater.start_polling()
