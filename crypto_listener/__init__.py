import threading

from .bot import Bot
from .listener import Listener


class CryptoListener:
    def __init__(self, config_path=None):
        self.bot = Bot(config_path)
        self.listener = Listener()

    def start(self):
        self.bot.start()

    def reply_updates(self):
        for btc_key, (s1, s2) in self.listener.items():
            if s1 != s2:
                pass
