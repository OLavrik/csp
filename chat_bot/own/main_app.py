import logging
from own.message import send_message
from flask import request
from flask_restplus import Resource, fields, Namespace
import random
from flask import request
from own.restplus import api
from own.locat import Locations
from own.paper import PaperArxiv
import telegram
from own.start_end import check_greeting,check_farewell, greeting_words, farewell_words

def sent_photo(chat_id, path):
    token = ""

    send_message(chat_id, "Отчет за последние 2 дня!" )
    bot = telegram.Bot(token=token)
    bot.send_photo(chat_id, photo=open(path, 'rb'))
    # send_message(chat_id, "Аномалий не было обнаружено.")
    send_message(chat_id, "Понервничали 7 раз.")
    return "OK"


l = Locations()
paper = PaperArxiv()

log = logging.getLogger(__name__)

ns = api.namespace('chat_bot',
                   description='Operations to get documentation'
                   )

# ты + positive -> thank
# спасибо -> thank
# ты + negativ -> no thank

stickers={
    "positive": ["CAACAgIAAxkBAAMEYM6ktxMTA-MgRDO-YBCc9tPgp6wAAsoBAAIq8joHfJVhJkmAgxQfBA"],
    "negative": ["CAACAgIAAxkBAAMGYM6k59kOMsr1xzWdS1AXU6ACIO8AAtkBAAIq8joH3sm6l-MJryofBA"],
    "thank":["CAACAgIAAxkBAAMUYM6nxr-AoQJqJ0tojdjFkF9dgZsAAsoBAAIq8joHfJVhJkmAgxQfBA",
            "CAACAgIAAxkBAAMWYM6n2ItZYfTrEZA_WPeHzjbZ5IcAAswBAAIq8joH1RQIBVa6zmUfBA"],
    "rong_sleep":["CAACAgIAAxkBAAMYYM6n9gYV6Apxbwvoo3CYmv1zwFYAAtsBAAIq8joHEQiyxczCZjUfBA"],
    "angry":["CAACAgIAAxkBAAMaYM6oCwo8Nj20wvk1pj0qN8HwKzoAAtsBAAIq8joHEQiyxczCZjUfBA"]
   }




def choose_sticker(text,positive=True):
    text=text.lower()
    if "спасибо" in text:
        return random.choice(stickers["thank"])

    if "ты" in text:
        if positive:
            return random.choice(stickers["thank"])
        else:
            return random.choice(stickers["no_thank"])
    if positive:
        return random.choice(stickers["positive"])
    else:
        return random.choice(stickers["negative"])




@ns.route('/messages/')
class RecommendationDoc(Resource):

    def post(self):
        r = request.json
        print(r)
        if "message" in r.keys():
            chat_id = r["message"]["chat"]["id"]
            name = r["message"]["from"]['first_name']
        else:
            chat_id = r["edited_message"]["chat"]["id"]
            name = r["edited_message"]["from"]['first_name']



        if not l.check_id(chat_id):
            if "location" in r["message"].keys():
                l.set_location(chat_id, r["message"]['location'])
                send_message(chat_id, "Теперь я знаю, что вы живете в " + l.get_town_string(
                    chat_id) + ". Может есть ко мне какие-то вопросы?")
                return "OK"

            else:
                send_message(chat_id,
                             "Добрый день, " + name + """! \nРады приветсвовать Вас! Для начала можете, пожалуйста с помощью telegramm поделиться своей локацией.\n Так я смогу лучше отвечать на Ваши вопросы и быть полезным:)""")
                return "OK"
        else:
            try:


                # в начале статьи
                if "message" in r.keys():
                    text = r["message"]["text"]
                else:
                    text = r["edited_message"]["text"]

                if check_greeting(text):
                    t=random.choice(greeting_words)
                    t=t+", "+name
                    a=t[0]
                    t=a.upper()+t[1:]
                    send_message(chat_id, t)
                    send_message(chat_id, stickers["positive"][0], False)
                    return "OK"

                if check_farewell(text):
                    t=random.choice(farewell_words)
                    t=t+", "+name
                    a=t[0]
                    t=a.upper()+t[1:]
                    send_message(chat_id, t)
                    return "OK"
                if "ты можешь" in text:
                    s="""\n1) Следить за твоим сердечком! \n2) Контролировать особенности! \n3) Ежемесячный отчет! \n4) Предупреждать о потенциальных сбоях/ пренапряжениях! \n5) Позвать кого-то на помощь!"""

                    send_message(chat_id,s)
                    send_message(chat_id, stickers["positive"][0], False)
                    return "OK"

                if "пасибо" in text:
                    send_message(chat_id, stickers["positive"][0], False)
                    send_message(chat_id, "Ну и чего ты не спишь?!")
                    send_message(chat_id, stickers["rong_sleep"][0], False)
                    return "OK"

                if "отчет":
                    sent_photo(chat_id, "./Screenshot 2021-06-20 at 05.34.26.png")
                    return "OK"


                if paper.check_need_paper(text) :

                    answer= paper.get_papers(text)

                    send_message(chat_id, answer)
                    l.set_w(chat_id, False)
                    l.set_d(chat_id, False)
                    return "OK"








            except:
                send_message(chat_id, "Что-то где-то ошибочка ;)")
                return "OK"

            send_message(chat_id, "Не хочу об этом ;)")
            return "OK"




