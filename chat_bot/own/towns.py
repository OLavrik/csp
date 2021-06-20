from natasha import Segmenter, NewsEmbedding, NewsNERTagger,Doc, MorphVocab, NewsEmbedding,NewsMorphTagger,NewsSyntaxParser,NewsNERTagger

import re
from own.query_prepare import QueryPrepare
import html
import requests
import requests
import time
from geopy.geocoders import Nominatim
from geopy.distance import distance
from ip2geotools.databases.noncommercial import DbIpCity

class TownDetect:
    dict_day={
        "сегодня":0,
        "завтра":1,
        "послезавтра":2
    }
    def __init__(self):
        self.query_process = QueryPrepare()

    def cities_in_text(self, text):
        tokens=text.split(" ")
        res=[]
        for elem in tokens:
            res.append(elem.capitalize())
        text=" ".join(res)

        segmenter = Segmenter()
        emb = NewsEmbedding()
        morph_tagger = NewsMorphTagger(emb)
        ner_tagger = NewsNERTagger(emb)
        morph_vocab = MorphVocab()
        syntax_parser = NewsSyntaxParser(emb)

        doc = Doc(text)

        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)

        cities = []
        for name in doc.spans:
            if name.type == 'LOC':
                name.normalize(morph_vocab)
                cities.append(name.normal)

        return cities



    def dist_check(self, text):
        text=text.lower()
        if "погода" in text:
            return False
        if "расстоян" in text:
            return True
        if "сколько до" in text:
            return True
        return False

    def weather_check(self, text):
        text = text.lower()
        if "погод" in text:
            return True
        return False

    def create_weather(self,town_local, text):
        towns = self.cities_in_text(text)

        if not self.weather_check(text) :


            found=False
            for elem in self.dict_day.keys():
                if elem in text:
                    found=True
            if not found:
                return ""

        towns=self.cities_in_text(text)
        day=0
        for elem in self.dict_day.keys():
            if elem in text:
                day=self.dict_day[elem]
                break
        if towns==[]:
            return self.geotemp(town_local.split(" ")[-1], day)
        else:
            return self.geotemp(towns[0], day)

    def create_dist(self,town_local, text):
        towns = self.cities_in_text(text)
        if not self.dist_check(text):
            if "до" not in text and towns==[]:
                return ""






        if towns==[]:
            return "Что я совсем глупенький. Но такого города не нашел:("
        else:
            if len(towns)>=2:
                return self.dist(towns[0], towns[1])
            else:
                return self.dist(town_local.split(" ")[-1], towns[0])




    api_key = '21fded5c420eb4293b75b691f8e19f95'
    ip = '91.108.0.192'

    def geotemp(self, name=None, day=None):
        geolocator = Nominatim(user_agent="geotemperatur")
        if name:
            location = geolocator.geocode(name)
            full_address = location.address
        else:
            location = DbIpCity.get(self.ip, api_key='free')
            full_address = geolocator.geocode(location.city).address
        lat = str(location.latitude)
        lon = str(location.longitude)

        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric&lang=ru" % (
        lat, lon, self.api_key)

        response = requests.get(url)
        data = response.json()
        if day is not None:
            i = data['daily'][day]

            return str(i['temp']['day']) + " градусов, " + i['weather'][0]['description']

        else:
            for i in data['daily']:

                return str(i['temp']['day'])+" градусов, "+i['weather'][0]['description']


    def dist(self, p2, p1=None):
        geolocator = Nominatim(user_agent="geodist")
        if p1:
            location = geolocator.geocode(p1)
            lat_1 = location.latitude
            lon_1 = location.longitude
        else:
            location = DbIpCity.get(ip, api_key='free')
            lat_1 = location.latitude
            lon_1 = location.longitude
        location = geolocator.geocode(p2)
        lat_2 = location.latitude
        lon_2 = location.longitude
        return distance((lat_1, lon_1), (lat_2, lon_2))



    def find_weather(self, web_text):
        link_reg = r'el=noopener aria-label=(.*?)data-log-node'
        value = re.findall(link_reg, web_text)
        return value[0]

    link_yandex = 'https://yandex.ru/search/?lr=2&text='

    def get_weather(self, question):
        tokens = self.query_process.main_prepare_query(question)
        q = "%20".join(tokens)
        l = self.link_yandex + q
        r = requests.get(l)
        web_text = html.unescape(r.text)
        return self.find_weather(web_text)[1:-2]

    def find_dist(self, web_text):
        link_reg = r'<div class="fact-answer fact-answer_size_xl typo typo_type_bold fact__answer">(.*?) \(по\xa0прямой\)</div>'
        value = re.findall(link_reg, web_text)
        return value

    def get_dist(self, question):
        tokens = self.query_process.main_prepare_query(question)
        q = "%20".join(tokens)
        l = self.link_yandex + q
        r = requests.get(l)
        web_text = html.unescape(r.text)
        return self.find_dist(web_text)






if __name__ == "__main__":
    d=TownDetect()
    print(d.create_weather("cc","какая погода в москве ?"))
    print(d.create_dist("Са", "Расстояние от москвы до екатеринбурга?"))


