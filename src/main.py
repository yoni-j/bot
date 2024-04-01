import json
import os

import telegram
import functions_framework
import logging
import asyncio

from google.cloud import pubsub_v1

logger = logging.getLogger()

BOT_TOKEN = os.getenv("BOT_TOKEN")
LLM_MESSAGE_PREFIX = "#from_llm#"

project_id = "yonidev"
topic_name = "llm-topic"


@functions_framework.http
def handle_update(request):
    update = telegram.Update.de_json(request.get_json(), bot=telegram.Bot(token=BOT_TOKEN))
    message = update.message.text

    if message:
        if LLM_MESSAGE_PREFIX in message:
            message = message.replace(LLM_MESSAGE_PREFIX, '')
            bot = telegram.Bot(token=BOT_TOKEN)
            asyncio.run(bot.send_message(chat_id=update.message.chat_id, text=message))
            return "OK"

        else:
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, topic_name)
            message_bytes = json.dumps(
                {"chat_id": update.message.chat_id,
                 "message": message}
            ).encode("utf-8")
            try:
                publish_future = publisher.publish(topic_path, data=message_bytes)
                publish_future.result()
            except Exception as e:
                print(f"Error publishing message: {e}")

    return "OK"
