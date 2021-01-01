class Transaction:
    def __init__(self, hash_):
        self.hash_ = hash_
        self.prev_state = None
        self.new_state = None
        self.error = {
            "loading": False,
            "tag": False
        }
        self._notification_queue = []
        self.chats = []

    def notification(self):
        if len(self._notification_queue):
            return self._notification_queue.pop(0)

    def update_state(self, state):
        self.prev_state, self.new_state = self.new_state, state
        if self.prev_state != self.new_state and self.prev_state and self.new_state:
            self._notification_queue.append(self.new_state)

    def __hash__(self):
        return hash(self.hash_)

    def __repr__(self):
        return self.hash_
