import json
import os

import telegram
import functions_framework
import logging
import asyncio

from google.cloud import pubsub_v1

logger = logging.getLogger()

BOT_TOKEN = os.getenv("BOT_TOKEN")

project_id = "yonidev"
topic_name = "llm-topic"


@functions_framework.http
def handle_update(request):
    update = telegram.Update.de_json(request.get_json(), bot=telegram.Bot(token=BOT_TOKEN))
    message = update.message.text

    if message:
        reply_text = f"You said: {message}"
        bot = telegram.Bot(token=BOT_TOKEN)
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)
        message_bytes = reply_text.encode("utf-8")
        try:
            publish_future = publisher.publish(topic_path, data=message_bytes)
            publish_future.result()
        except Exception as e:
            print(f"Error publishing message: {e}")
        asyncio.run(bot.send_message(chat_id=update.message.chat_id, text=reply_text))

    return "OK"
