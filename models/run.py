from sklearn.metrics import f1_score
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
import matplotlib.pyplot as plt


def convert_to_dict_test(df):
    seq = {}
    for index, row in df.iterrows():
        id_ = row["id"]
        if id_ not in list(seq.keys()):
            seq[row["id"]] = {}
            seq[row["id"]]["src"] = []
            seq[row["id"]]["time"] = []
        seq[row["id"]]["src"].append(row["x"])
        seq[row["id"]]["time"].append(row["time"])

    return seq


def padding(arr, window_size, val=0):
    res = [val for i in range(window_size - len(arr))]
    res.extend(arr)
    return res


def center_padding(arr, left_pad, right_pad, val=0):
    res = [val for i in range(left_pad)]
    res.extend(arr)
    res.extend([val for i in range(right_pad)])
    return res


def empty(arr):
    return arr


def create_data_window_test(data_dict, window_size=3, prepcess=empty):
    s = ["f" + str(i) for i in range(window_size)]
    dict_frame = {"id":[], "time":[]}
    for elem in s:
        dict_frame[elem] = []

    for key in data_dict.keys():
        val = data_dict[key]["src"]

        mean = np.median(val)
        for i in range(len(val)):
            l, r = 0, 0
            if i < (window_size - 1) // 2:
                l = (window_size - 1) // 2 - i
            if i > len(val) - 1 - (window_size - 1) // 2:
                r = (window_size - 1) // 2 - (len(val) - 1 - i)

            start = max(0, i - (window_size - 1) // 2)
            end = i + (window_size - 1) // 2 + 1
            res = center_padding(val[start: end], l, r, mean)

            res = prepcess(res)
            for j, elem in enumerate(s):
                dict_frame[elem].append(res[j])
            dict_frame["time"].append(data_dict[key]["time"][i])
            dict_frame["id"].append(key)


    return dict_frame


def score(true_y, pred_y):
    return f1_score(true_y, pred_y, average='weighted')


# def clean_answer():

def find_main_median(df, ind, min_x=450, max_x=1050):
    sub = df[df['id'] == ind]
    sub = sub[sub.x >= min_x]
    sub = sub[sub.x <= max_x]
    median = sub.x.median()
    return median


def find_sub_median(df, ind, main_median, dx=180):
    sub = df[df['id'] == ind]
    sub = sub[sub.x >= main_median - dx]
    sub = sub[sub.x <= main_median + dx]
    median = sub.x.median()
    return median


def clear_serie(df, ind, dx=180):
    median = find_main_median(df, ind)
    sub_median = find_sub_median(df, ind, median)
    df.loc[df['id'] == ind, 'x'] = df.loc[df['id'] == ind, 'x'].apply(
        lambda x: x if median - dx <= x <= median + dx else sub_median
    )


def create_data():
    df = pd.read_csv('/home/pavel/Projects/Work/CardioSpike/data/train.csv')
    # for ind in df.id.unique():
    #     clear_serie(df, ind)

    seq = convert_to_dict_test(df)
    data_f = create_data_window_test(seq, window_size=13)
    print("meow")
    df_new = pd.DataFrame(data_f)
    df_new.to_csv("./w=13_p=med.csv", index=False)


def get_anomaly_seq(df):
    sequences = []
    sequence = []
    for i, row in df.iterrows():
        y = row['y']
        if y == 1:
            sequence.append(row['x'])
        else:
            if len(sequence) > 0:
                sequences.append(sequence)
                sequence = []

    if len(sequence) > 0:
        sequences.append(sequence)

    return sequences


def equals(a, b, eps_p):
    da = abs(a) * eps_p
    if a - da <= b <= a + da:
        return True
    return False


def get_pattern_from_sequence(seq, eps_p=0.01):
    n = len(seq)
    matr = np.zeros((n, n))
    print(seq)
    print(matr.shape)

    for i in range(n):
        for j in range(n):
            if equals(seq[i], seq[j], eps_p):
                matr[i, j] = 1

    print(matr)


import random


class Dictogram(dict):
    def __init__(self, iterable=None):
        # Инициализируем наше распределение как новый объект класса,
        # добавляем имеющиеся элементы
        super(Dictogram, self).__init__()
        self.types = 0  # число уникальных ключей в распределении
        self.tokens = 0  # общее количество всех слов в распределении
        if iterable:
            self.update(iterable)

    def update(self, iterable):
        # Обновляем распределение элементами из имеющегося
        # итерируемого набора данных
        for item in iterable:
            if item in self:
                self[item] += 1
                self.tokens += 1
            else:
                self[item] = 1
                self.types += 1
                self.tokens += 1

    def count(self, item):
        # Возвращаем значение счетчика элемента, или 0
        if item in self:
            return self[item]
        return 0

    def return_random_word(self):
        random_key = random.sample(self, 1)
        # Другой способ:
        # random.choice(histogram.keys())
        return random_key[0]

    def return_weighted_random_word(self):
        # Сгенерировать псевдослучайное число между 0 и (n-1),
        # где n - общее число слов
        random_int = random.randint(0, self.tokens - 1)
        index = 0
        list_of_keys = self.keys()
        # вывести 'случайный индекс:', random_int
        for i in range(0, self.types):
            index += self[list_of_keys[i]]
            # вывести индекс
            if (index > random_int):
                # вывести list_of_keys[i]
                return list_of_keys[i]


def clean_dataset(df):
    df[df.x > 1300] = df.x.median()


def get_quantization(df):
    df['x_group']


def find_main_median(df, ind, min_x=450, max_x=1050):
    sub = df[df['id'] == ind]
    sub = sub[sub.x >= min_x]
    sub = sub[sub.x <= max_x]
    median = sub.x.median()
    return median


def find_sub_median(df, ind, main_median, dx=180):
    sub = df[df['id'] == ind]
    sub = sub[sub.x >= main_median - dx]
    sub = sub[sub.x <= main_median + dx]
    median = sub.x.median()
    return median


def clear_serie(df, ind, dx=180):
    median = find_main_median(df, ind)
    sub_median = find_sub_median(df, ind, median)
    df.loc[df['id'] == ind, 'x'] = df.loc[df['id'] == ind, 'x'].apply(
        lambda x: x if median - dx <= x <= median + dx else sub_median
    )


def save_model(model, path="./model"):
    model.save_mode(path)


def load_model(path):
    model = CatBoostClassifier()
    model.load_model(path)
    return model

def post_process(arr, window_size):
    wd=window_size*2
    return arr

def make_result(seq, window_size):
    dict_itog={"id":[], "time":[], "y":[]}
    for key in seq.keys():

        time=seq[key]["time"]
        y=seq[key]["y"]
        for t,y_ in zip(time, y):
            dict_itog["id"].append(int(key))
            dict_itog["time"].append(int(t))
            dict_itog["y"].append(int(y_))
    df=pd.DataFrame(dict_itog)
    df.to_csv("./2_res.csv",index=False)
    return df






def run_model(data_path='/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/models/test_cardio.csv', model_path="/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/models/boost/CATMax5CrossWindow13.uu", window_size=13):
    model = load_model(model_path)
    df = pd.read_csv(data_path)
    seq = convert_to_dict_test(df)
    df_new = pd.DataFrame(create_data_window_test(seq, window_size))
    ser={}

    for i, row in df_new.iterrows():
        id_ = row["id"]
        time= row["time"]
        # d=row.copy()
        # del d["id"]
        # del d["time"]

        if id_ not in ser.keys():
            ser[id_]={}
            ser[id_]["time"]=[]
            ser[id_]["y"]=[]
        ser[id_]["time"].append(time)
        d=[int(elem) for elem in list(row[2:])]

        res=model.predict([d])
        ser[id_]["y"].append(res[0])

    make_result(ser, window_size)

def prepocess(arr, mean):
    return [elem -mean for elem in arr]

def create_data_window_l(data_dict, window_size=3, prepcess=prepocess):
    s = ["f" + str(i) for i in range(window_size)]
    dict_frame = {"id":[], "time":[]}
    for elem in s:
        dict_frame[elem] = []

    for key in data_dict.keys():
        val = data_dict[key]["src"]

        mean=np.mean(val)
        med=np.mean(val)
        for i in range(len(val)):
            if i < window_size-1:
                k=max(0,i-window_size)
                res = padding(val[k:i + 1], window_size, mean)
            else:
                res = val[i - window_size+1:i + 1]
            res=prepcess(res, med)
            for j, elem in enumerate(s):
                dict_frame[elem].append(res[j])
            dict_frame["time"].append(data_dict[key]["time"][i])
            dict_frame["id"].append(key)


    return dict_frame

def run_linear(data_path='/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/models/test_cardio.csv', model_path="/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/models/boost/CATMax5CrossWindow13.uu", window_size=3):
    df = pd.read_csv('/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/models/w=3_p=m.csv')
    y = df["y"]
    del df["y"]
    X = df
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=33)
    from sklearn.linear_model import SGDClassifier
    clf = SGDClassifier()
    # fit (train) the classifier
    clf.fit(X_train, y_train)
    print(score(y_test, clf.predict(X_test)))

    df = pd.read_csv(data_path)
    seq = convert_to_dict_test(df)
    df_new = pd.DataFrame(create_data_window_l(seq, window_size))
    ser = {}

    for i, row in df_new.iterrows():
        id_ = row["id"]
        time = row["time"]
        # d=row.copy()
        # del d["id"]
        # del d["time"]

        if id_ not in ser.keys():
            ser[id_] = {}
            ser[id_]["time"] = []
            ser[id_]["y"] = []
        ser[id_]["time"].append(time)
        d = [int(elem) for elem in list(row[2:])]

        res = clf.predict([d])
        ser[id_]["y"].append(res[0])

    make_result(ser, window_size)



if __name__ == "__main__":
    df = pd.read_csv('/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/data/train.csv')
    run_linear()
