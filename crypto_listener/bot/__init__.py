from telegram.ext import Updater
import json

from .commands import Commands


class CryptoListenerBot:
    def __init__(self, config_path="../config.json"):
        with open(config_path, "r") as file:
            self.config = json.loads(file.read())
        self.listen2_dict = {}
        self.updater = Updater(token=self.config["bot_token"], use_context=True)
        self.updater.dispatcher.add_handler("start", Commands.start)
        self.updater.dispatcher.add_handler("listen", Commands.listen(self.listen2_dict))

    def start(self):
        self.updater.start_polling()
