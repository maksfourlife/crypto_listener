import requests
import bs4


class Listener:
    def __init__(self):
        self.transactions = {}

    def track_changes(self):
        for hash_, transaction in self.listen.items():
            with requests.get(transaction.hash_) as res:
                if not res.ok:
                    transaction.error["loading"] = True
                else:
                    transaction.error["loading"] = False
                    soup = bs4.BeautifulSoup(res.content.decode("utf-8"))
                    state = soup.findAll(True, {"class": ["sc-45ldg2-0", "iA-DtFk"]})[0]
            transaction.update_state(state)
