from telegram.ext import Updater, CommandHandler
from os import path
import json

from .commands import Commands

CONFIG_PATH = path.join(path.dirname(__file__), "../config.json")


class CryptoListenerBot:
    def __init__(self, config_path=CONFIG_PATH):
        with open(config_path, "r") as file:
            self.config = json.loads(file.read())
        self.listen2_dict = {}
        self.updater = Updater(token=self.config["bot_token"], use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler("start", Commands.start))
        self.updater.dispatcher.add_handler(CommandHandler("listen", Commands.listen(self.listen2_dict)))

    def start(self):
        self.updater.start_polling()
