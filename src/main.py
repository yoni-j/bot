import os

import telegram
import functions_framework
import logging
import asyncio

logger = logging.getLogger()

BOT_TOKEN = os.getenv("BOT_TOKEN")


@functions_framework.http
def handle_update(request):
    update = telegram.Update.de_json(request.get_json(), bot=telegram.Bot(token=BOT_TOKEN))
    message = update.message.text

    if message:
        reply_text = f"You said: {message}"
        bot = telegram.Bot(token=BOT_TOKEN)
        asyncio.run(bot.send_message(chat_id=update.message.chat_id, text=reply_text))

    return "OK"
