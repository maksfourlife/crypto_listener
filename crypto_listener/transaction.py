class Transaction:
    def __init__(self, hash_):
        self.hash_ = hash_.replace("https://www.blockchain.com/btc/tx/", "")
        self.prev_state = None
        self.new_state = None
        self._notification_queue = []
        self.chats = set()

    def count_notifications(self):
        return len(self._notification_queue)

    def add_notification(self, message):
        self._notification_queue.append(message)

    def get_notification(self):
        if len(self._notification_queue):
            return f"Transaction {self.hash_} 👀\n{self._notification_queue.pop(0)}"

    def update_state(self, state):
        self.prev_state, self.new_state = self.new_state, state
        if self.prev_state != self.new_state:
            self._notification_queue.append(f"[State] {self.new_state}")

    def __hash__(self):
        return hash(self.hash_)

    def __repr__(self):
        return self.hash_
