import re
import requests
import html
from own.query_prepare import QueryPrepare
class PaperArxiv:
    link_arxiv="https://arxiv.org/search/?query=QUESTION&searchtype=all&source=header"
    # link_arxiv = "https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=QUESTION&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first"

    def __init__(self):
        self.query_process=QueryPrepare()

    def numbers_in_text(self, text):
        from natasha import (
            Segmenter,
            MorphVocab,

            NewsEmbedding,
            NewsMorphTagger,

            Doc
        )

        if "1" in text:
            return 1
        if "2" in text:
            return 2
        if "3" in text:
            return 3
        if "4" in text:
            return 4
        if "5" in text:
            return 5
        if "6" in text:
            return 6
        if "7" in text:
            return 7




        segmenter = Segmenter()
        morph_vocab = MorphVocab()

        emb = NewsEmbedding()
        morph_tagger = NewsMorphTagger(emb)

        numbers_dict = {'один': 1, '1': 1,
                        'два': 2, '2': 2,
                        'три': 3, '3': 3,
                        'четыре': 4, '4': 4,
                        'пять': 5, '5': 5,
                        'шесть': 6, '6': 6,
                        'семь': 7, '7': 7,
                        'восемь': 8, '8': 8,
                        'девять': 9, '9': 9}
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
            if token.lemma in numbers_dict:
                return numbers_dict[token.lemma] if numbers_dict[token.lemma]!=None else 1





    def find_arxiv(self, web_text):
        link_reg = r'<a\shref=.*?>pdf<\/a>'
        value = re.findall(link_reg, web_text)
        return value

    def get_link(self, text):
        r = r'\".*?\"'
        value = re.findall(r, text)
        return [elem[1:-1] for elem in value]

    def check_need_paper(self, text):
        tokens = text.split(" ")
        if "погода" in text:
            return False
        if "тем" in text:
            return True
        if "стат" in text:
            return True
        if " про " in text:
            return True
        if " о " in text:
            return True
        if " об " in text:
            return True
        return False


    def get_papers(self, name):
        i=self.numbers_in_text(name)
        name = name.encode('ascii', 'ignore').decode('ascii')
        tokens = self.query_process.main_prepare_query(name)
        if tokens==[]:
            return "Я ищу в международных источниках, поэтому тему надо указать на англйиском!)"
        q = "+".join(tokens)
        l = self.link_arxiv.replace("QUESTION", q)
        r = requests.get(l)
        web_text = html.unescape(r.text)
        v = self.find_arxiv(web_text)
        res = []

        for elem in v:
            res.extend(self.get_link(elem))
        if res==[]:
            return "Что-то ничего не нашел:( Может другую тему выберешь?"
        if len(res)>5:
            res=res[:i]
        return "Вот ссылки на pdf статей, которые нам удалось найти по данной теме:\n"+" \n".join(res)

if __name__ == "__main__":
    d=PaperArxiv()
    print(d.numbers_in_text('пришли м статей'))
    print(d.get_papers("Хояу найти 3 статьи на тему nlp in biology"))


