class Commands:
    bot_greeting = f"Hello, I'm a CryptoListentenerBot!\n" \
                   f"You can use me to listen your btc transaction updates\n" \
                   f"For that purpose use command: /listen [url/you/want/to/listen/from]"

    @classmethod
    def start(cls, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=cls.bot_greeting)

    @staticmethod
    def listen(listen2_dict):
        def func(update, context):
            if len(content.args) > 1:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="/listen command takes exactly one argument")
            else:
                btc_hash = hash(content.args[0])
                listen2_dict[btc_hash] = content.args[0]
                if "listen" not in context.user_data:
                    context.user_data["listen"] = set()
                context.user_data["listen"].add(btc_hash)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"Bot successfully started listening to {content.args[0]}")
        return func
