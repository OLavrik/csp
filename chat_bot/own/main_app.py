import logging
from own.message import send_message
from flask import request
from flask_restplus import Resource, fields, Namespace
import random
from flask import request
from own.restplus import api
from own.locat import Locations
from own.paper import PaperArxiv
from own.towns import TownDetect
from own.start_end import check_greeting,check_farewell, greeting_words, farewell_words

l = Locations()
paper = PaperArxiv()
towns = TownDetect()

log = logging.getLogger(__name__)

ns = api.namespace('chat_bot_hse',
                   description='Operations to get documentation'
                   )

# ты + positive -> thank
# спасибо -> thank
# ты + negativ -> no thank

stickers={
    "positive": ["CAACAgIAAxkBAAOqYMns-0CraXExcqLyyLsoXuvxhZ4AAjETAALo1uISzKKcP0Iv5wgfBA",
                 "CAACAgIAAxkBAAOwYMnudS829Gae1wqwJsLzUG-AV2gAAmESAALo1uISUlEXDAjMAAExHwQ",
                 "CAACAgIAAxkBAAOyYMnumeaf9bivqT3BdEFJIdrL5qoAAmMSAALo1uIS72wB9JWXwDgfBA",
                 "CAACAgIAAxkBAAO0YMnu38mfDPsmLm1-UJ_8YqJEk3sAAskSAALo1uISY63Nf2THxFUfBA"],
    "negative": ["CAACAgIAAxkBAAO2YMnu_PgdrUufzqg_9UjSQHsMw9YAAt0TAALo1uISjXlm36x8hmcfBA",
                 "CAACAgIAAxkBAAO4YMnvDC3OtskFpr0738a15zN414IAAi8TAALo1uISfYQ9YRAg0t0fBA",
                 "CAACAgIAAxkBAAO6YMnvHlZjMV99b03Au-g0gMKDGy8AAiUTAALo1uISbTLNQ_p-VHofBA",
                 "CAACAgIAAxkBAAO8YMnvMVuBzep9PCL5SU5yU648tvwAAjoTAALo1uISwun-QDmkq_4fBA"],
    "thank":["CAACAgIAAxkBAAOcYMniiHUPYpiQHhBPM2Mw2pM9nBgAAigTAALo1uISAW3oGlJon4kfBA",
            "CAACAgIAAxkBAAOsYMntRzHKqdnqSU7prHHltu-dbFwAAm0SAALo1uISK5x6STjv-VgfBA",
            "CAACAgIAAxkBAAOuYMnuQGv9X7j86_K4v3n6TOfthD8AAngSAALo1uISk8d5hpdGJ9YfBA"],
    "no_thank":["CAACAgIAAxkBAAO-YMnviu0Gt4mIgc5iofDDT9kh6c4AAnASAALo1uISyvLm19ltZy8fBA"],
    "neutral":['CAACAgIAAxkBAAIBbmDKKD060OoImzjH3M7ljM2TX_mMAAIgEwAC6NbiEjV-fzc3FjGxHwQ', 'CAACAgIAAxkBAAIBcGDKKMr-xK76tFrDUQx4Mx4vj5xoAAIwEwAC6NbiEgjvqY4J1s5LHwQ']
}

import requests
import json

def detect_tonal(text):
    body = {"text": text}
    doc_url = 'http://127.0.0.1:5000/tonal/'
    r = requests.post(doc_url, json=body)
    d = json.loads(r.content)

    return d["res"]


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

def get_answer(text):
    body = {"text": text}
    doc_url = 'http://127.0.0.1:5000/wiki/'
    r = requests.post(doc_url, json=body)
    d = json.loads(r.content)
    if "Not Found" in d["res"]:
        return ""
    return d["res"]



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
                    return "OK"

                if check_farewell(text):
                    t=random.choice(farewell_words)
                    t=t+", "+name
                    a=t[0]
                    t=a.upper()+t[1:]
                    send_message(chat_id, t)
                    return "OK"

                if paper.check_need_paper(text) :

                    answer= paper.get_papers(text)

                    send_message(chat_id, answer)
                    l.set_w(chat_id, False)
                    l.set_d(chat_id, False)
                    return "OK"

                # погода
                if towns.weather_check(text) or l.get_w(chat_id):
                    answer=towns.create_weather(l.get_town_string(chat_id), text)
                    if answer=="":
                        l.set_w(chat_id, False)
                        l.set_d(chat_id, False)
                    else:
                        send_message(chat_id, answer)
                        l.set_d(chat_id, False)
                        l.set_w(chat_id)
                        return "OK"




                # города
                if towns.dist_check(text) or l.get_d(chat_id):
                    answer=str(towns.create_dist(l.get_town_string(chat_id), text))
                    if answer=="":
                        l.set_w(chat_id, False)
                        l.set_d(chat_id, False)
                    else:
                        send_message(chat_id, answer)
                        l.set_d(chat_id)
                        l.set_w(chat_id, False)
                        return "OK"

                # реакция
                tonal=detect_tonal(text)


                if tonal=="positive":
                    stick=choose_sticker(text, True)
                    l.set_w(chat_id, False)
                    l.set_d(chat_id, False)

                    send_message(chat_id, stick, False)
                    return "OK"
                if tonal == "negative":
                    stick=choose_sticker(text, False)

                    l.set_w(chat_id, False)
                    l.set_d(chat_id, False)


                    send_message(chat_id, stick, False)
                    return "OK"
                if tonal == "neutral":
                    stick=get_answer(text)
                    if stick!="":
                        a = stick[0]
                        stick = a.upper() + stick[1:]
                        l.set_w(chat_id, False)
                        l.set_d(chat_id, False)
                        send_message(chat_id, stick)
                        return "OK"

            except:
                send_message(chat_id, "Что-то где-то ошибочка ;)")
                return "OK"

            send_message(chat_id, "Не хочу об этом ;)")
            return "OK"




