import requests
import telegram


def send_message(chat_id, text, flagText=True):
    method = "sendMessage"
    token = ""
    url = f"https://api.telegram.org/bot{token}/{method}"
    if flagText:
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)
    else:

        bot = telegram.Bot(token=token)
        bot.send_sticker(chat_id=chat_id, sticker=text)


