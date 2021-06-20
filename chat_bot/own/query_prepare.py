import re
from nltk.corpus import wordnet as wn
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class QueryPrepare:
    regular_language = "\#.*?\s"
    english_stopwords = stopwords.words('english')


    def __init__(self):
        # self.tokenizer = RegexpTokenizer(r'\w+')
        self.porter = nltk.PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.lemmatizer.lemmatize("start")

    def main_prepare_query(self, query):

        query=query.strip()
        query = re.sub(" +", " ", query)
        tokens = query.split(" ")
        tokens=self.remove_stopwords(tokens)
        tokens = self.normalize(tokens)
        return tokens



    def remove_stopwords(self, tokens):
        token_without = []
        for elem in tokens:
            if elem not in self.english_stopwords:
                token_without.append(elem)
        return token_without



    def normalize(self, tokens):
        #  нормализация токенов
        res = []
        for t in tokens:
            if t=="":
                continue
            try:
                res.append(self.lemmatizer.lemmatize(t))
            except WordNetError as e:
                print(e)
                res.append(t)
            except AttributeError as e:
                print(e)
                res.append(t)
            except:
                res.append(t)
        return res




