from ..transaction import Transaction


class Commands:
    @staticmethod
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Hello, I'm a CryptoListentenerBot!\n"
                                      f"You're now in a list of listeners and can use me to listen "
                                      f"your btc transaction updates\n"
                                      f"For that purpose use command: /listen hash_of_your_transaction")

    @staticmethod
    def stop(transactions):
        def func(update, context):
            for transaction in transactions.values():
                if update.effective_chat.id in transaction.chats:
                    transaction.chats.remove(update.effective_chat.id)
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
                transactions[hash_].chats.add(update.effective_chat.id)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"Bot successfully started listening to {transaction}")
        return func

    @staticmethod
    def unlisten(transactions):
        def func(update, context):
            if len(context.args) != 1:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="/unlisten command takes exactly one argument")
            else:
                hash_ = hash(context.args[0])
                if hash_ in transactions:
                    transactions[hash_].chats.remove(update.effective_chat.id)
                    hash_ = transactions[hash_]
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=f"Bot successfully stopped listening to {hash_}")
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text="Bot isn't listening to that transaction.")
        return func
