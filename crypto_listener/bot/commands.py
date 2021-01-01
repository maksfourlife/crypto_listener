from ..transaction import Transaction


class Commands:
    @staticmethod
    def start(chats):
        def func(update, context):
            chats[update.effective_chat.id] = Chat(update.effective_chat.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Hello, I'm a CryptoListentenerBot!\n"
                                          f"You're now in a list of listeners and can use me to listen "
                                          f"your btc transaction updates\n"
                                          f"For that purpose use command: /listen [url/you/want/to/listen/from]")
        return func

    @staticmethod
    def stop(chats):
        def func(update, context):
            del chats[update.effective_chat.id]
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Thank you for usage.\n"
                                          f"You're now excluded from the list of receivers.\n"
                                          f"Return any time you want.")
        return func

    @staticmethod
    def listen(transactions):
        def func(update, context):
            if len(context.args) != 1:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="/listen command takes exactly one argument")
            else:
                transaction = Transaction(context.args[0])
                if (hash_ := hash(transaction)) not in transactions:
                    transactions[hash_] = transaction
                transactions[hash_].chats.append(update.effective_chat.id)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"Bot successfully started listening to {transaction}")
        return func
