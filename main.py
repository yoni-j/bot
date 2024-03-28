import telegram

BOT_TOKEN = "YOUR_BOT_TOKEN"


def handle_update(request):
    update = telegram.Update.de_json(request.get_json(), bot=telegram.Bot(token=BOT_TOKEN))

    # Extract the user message
    message = update.message.text

    # Handle the message (basic echo example)
    if message:
        reply_text = f"You said: {message}"
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=update.message.chat_id, text=reply_text)

    return "OK"
