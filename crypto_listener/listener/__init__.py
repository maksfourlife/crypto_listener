import time
import bs4
import requests
import threading


BASE_URL = "https://www.blockchain.com/btc/tx/"


class Listener:
    def __init__(self, update_rate=60):
        self.transactions = {}
        self.update_rate = update_rate

    def _track_changes(self):
        while True:
            for transaction in self.transactions.values():
                with requests.get(BASE_URL + transaction.hash_) as res:
                    try:
                        soup = bs4.BeautifulSoup(res.content.decode("utf-8"))
                    except:
                        transaction.add_notification("Error: can't load transaction")
                        continue
                try:
                    transaction.update_state(soup.findAll(True, {"class": ["sc-45ldg2-0", "iA-DtFk"]})[0])
                except:
                    transaction.add_notification("Error: can't find state")
            time.sleep(self.update_rate)

    def start(self):
        threading.Thread(target=self._track_changes, name="listener_tracker", daemon=True).start()
