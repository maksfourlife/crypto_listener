import time
import bs4
import requests


class Listener:
    def __init__(self, update_rate=60):
        self.transactions = {}
        self.update_rate = update_rate

    def _track_changes(self):
        while 1:
            for hash_, transaction in self.listen.items():
                with requests.get(transaction.hash_) as res:
                    if not res.ok:
                        transaction.error["loading"] = True
                        continue
                    transaction.error["loading"] = False
                    soup = bs4.BeautifulSoup(res.content.decode("utf-8"))
                try:
                    transaction.update_state(soup.findAll(True, {"class": ["sc-45ldg2-0", "iA-DtFk"]})[0])
                    transaction.error["loading"] = False
                except:
                    transaction.error["loading"] = True
            time.sleep(self.update_rate)

    def start(self):
        threading.Thread(target=self._track_changes, name="listener_tracker", daemon=True).start()
