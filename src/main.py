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
    bot = telegram.Bot(token=BOT_TOKEN)
    request_body = request.get_json()

    # Handle llm message
    if "chat_id" in request_body:
        text = request_body["text"]
        message = text.replace(LLM_MESSAGE_PREFIX, '')
        asyncio.run(bot.send_message(chat_id=request_body["chat_id"], text=message))
        return "OK"

    # Handle user message
    else:
        update = telegram.Update.de_json(request_body, bot=bot)
        message = update.message.text
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
