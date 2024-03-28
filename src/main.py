import os

import telegram
import functions_framework
import logging

logger = logging.getLogger()

BOT_TOKEN = os.getenv("BOT_TOKEN")


@functions_framework.http
def handle_update(request):
    update = telegram.Update.de_json(request.get_json(), bot=telegram.Bot(token=BOT_TOKEN))
    logger.info("started!!!!!!!")

    # Extract the user message
    message = update.message.text
    logger.info(message)

    # Handle the message (basic echo example)
    if message:
        reply_text = f"You said: {message}"
        logger.info(reply_text)
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=update.message.chat_id, text=reply_text)

    return "OK"
