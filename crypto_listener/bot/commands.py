from ..transaction import Transaction


class Commands:
    @staticmethod
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Hello, I'm a WhyBitListener_bot 🚀\n"
                                      f"You can use me to listen your btc transaction updates 💸\n\n"
                                      f"Commands:"
                                      f"\n/check hash_of_your_transaction"
                                      f"\n/uncheck hash_of_your_transaction"
                                      f"\n/stop")

    @staticmethod
    def stop(transactions):
        def func(update, context):
            for transaction in transactions.values():
                if update.effective_chat.id in transaction.chats:
                    transaction.chats.remove(update.effective_chat.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Thank you for usage!... return any time you wish 😕")
        return func

    @staticmethod
    def listen(transactions):
        def func(update, context):
            if len(context.args) != 1:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="/check command takes exactly one argument 🤌")
            else:
                transaction = Transaction(context.args[0])
                if (hash_ := hash(transaction)) not in transactions:
                    transactions[hash_] = transaction
                transactions[hash_].chats.add(update.effective_chat.id)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"Bot successfully started checking {transaction} 🤖")
        return func

    @staticmethod
    def unlisten(transactions):
        def func(update, context):
            if len(context.args) != 1:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="/uncheck command takes exactly one argument 🤌")
            else:
                hash_ = hash(context.args[0])
                if hash_ in transactions:
                    transactions[hash_].chats.remove(update.effective_chat.id)
                    hash_ = transactions[hash_]
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=f"Bot successfully stopped checking {hash_} 🤖")
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text="Bot isn't checking that transaction 😧")
        return func
