from .bot import Bot
from .listener import Listener


class CryptoListener:
    def __init__(self, config_path=None):
        self.listener = Listener(10)
        self.bot = Bot(self.listener.transactions, config_path, 10)

    def start(self):
        self.listener.start()
        self.bot.start()
