import requests
import bs4


class Listener:
    def __init__(self):
        self.listen = {}
        self.states = {}

    def track_updates(self):
        for btc_key, btc in self.listen.items():
            with requests.get(btc) as res:
                if not res.ok:
                    state = "error loading"
                else:
                    soup = bs4.BeautifulSoup(res.content.decode("utf-8"))
                    state = soup.findAll(True, {"class": ["sc-45ldg2-0", "iA-DtFk"]})[0]
            if btc_key not in self.states:
                self.states[btc_key] = (None, None)
            self.states[btc_key] = self.states[btc_key][1], state
