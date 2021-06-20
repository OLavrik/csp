from sklearn.metrics import f1_score
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
import matplotlib.pyplot as plt


def convert_to_dict(df):
    seq = {}
    for index, row in df.iterrows():
        id_ = row["id"]
        if id_ not in list(seq.keys()):
            seq[row["id"]] = {}
            seq[row["id"]]["src"] = []
            seq[row["id"]]["time"] = []
            seq[row["id"]]["trg"] = []
        seq[row["id"]]["src"].append(row["x"])
        seq[row["id"]]["time"].append(row["time"])
        seq[row["id"]]["trg"].append(row["y"])
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


def create_data_window(data_dict, window_size=3, prepcess=empty):
    s = ["f" + str(i) for i in range(window_size)]
    dict_frame = {"y": []}
    for elem in s:
        dict_frame[elem] = []

    for key in data_dict.keys():
        val = data_dict[key]["src"]
        trg = data_dict[key]["trg"]
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

            res=prepcess(res)
            for j, elem in enumerate(s):
                dict_frame[elem].append(res[j])
            dict_frame["y"].append(trg[i])

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
    df = pd.read_csv('/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/data/train.csv')
    # for ind in df.id.unique():
    #     clear_serie(df, ind)

    seq = convert_to_dict(df)
    data_f = create_data_window(seq, window_size=13)
    print("meow")
    df_new = pd.DataFrame(data_f)
    return df_new


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
    if a - da  <= b <= a + da:
        return True
    return False


def get_pattern_from_sequence(seq, eps_p=0.01):
    n =  len(seq)
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
        random_int = random.randint(0, self.tokens-1)
        index = 0
        list_of_keys = self.keys()
        # вывести 'случайный индекс:', random_int
        for i in range(0, self.types):
            index += self[list_of_keys[i]]
            # вывести индекс
            if(index > random_int):
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






def train_model(df):

    for col in df.columns:
        df[col] = df[col].astype(int)

    train, test = train_test_split(df, random_state=33, test_size=0.25)

    X, y = train.iloc[:, 1:], train.iloc[:, 0]
    X_val, y_val = test.iloc[:, 1:], test.iloc[:, 0]
    print(X)

    model = CatBoostClassifier(
        iterations=10,
        learning_rate=0.1,

        max_depth=10,
        loss_function='Logloss',
        class_weights=[0.85, 0.15],

    )

    cat_features = list(range(0, X.shape[1]))
    model.fit(X, y, cat_features=cat_features, eval_set=(X_val, y_val), verbose=True, plot=True)
    print(model.is_fitted())
    print(model.get_params())
    print(model.get_feature_importance())

    pred = model.predict(X_val)
    print(set(pred))
    print('score:', score(y_val, pred))


if __name__ == "__main__":
    df = pd.read_csv('/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/models/boost/w=13_p=med.csv')
    df_new=create_data()
    train_model(df_new)