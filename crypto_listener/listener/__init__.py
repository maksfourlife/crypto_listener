import time
import bs4
import requests
import threading


BASE_URL = "https://www.blockchain.com/btc/tx/"


class Listener:
    def __init__(self, update_rate=60):
        self.transactions = {}
        self.update_rate = update_rate

    @staticmethod
    def _transaction_expired(transaction):
        return len(transaction.chats) == 0 or \
               isinstance(transaction.new_state, str) and \
               transaction.new_state.startswith("Confirmed") and \
               transaction.count_notifications() == 0

    def _track_changes(self):
        while True:
            for hash_ in list(self.transactions.keys()):
                if self._transaction_expired(self.transactions[hash_]):
                    del self.transactions[hash_]
                    continue
                with requests.get(BASE_URL + self.transactions[hash_].hash_) as res:
                    try:
                        soup = bs4.BeautifulSoup(res.content.decode("utf-8"), features="html.parser")
                    except:
                        self.transactions[hash_].add_notification("[Error] can't load transaction")
                        continue
                try:
                    self.transactions[hash_].update_state(f"{soup.find(text='Status').next_element.text} "
                                                          f"{soup.find(text='Confirmations').next_element.text}")
                except:
                    self.transactions[hash_].add_notification("[Error] can't find tag")
            time.sleep(self.update_rate)

    def start(self):
        threading.Thread(target=self._track_changes, name="listener_tracker", daemon=True).start()
