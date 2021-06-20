import pandas as pd
import numpy as np

def detect_extr(arr):
    q25=np.quantile(arr, 0.25)
    q50=np.quantile(arr, 0.50)
    q75=np.quantile(arr, 0.75)
    IQR=q75-q25
    min_extr=q25-1.5*IQR
    max_extr=q75+1.5*IQR
    r=[0 if (elem>min_extr and elem<max_extr) else 1 for elem in arr]
    return r

def clean_external(arr, val):
    extr=detect_extr(arr)
    res=[]
    for i, elem in enumerate(arr):
        if extr[i]==1:
            res.append(val)
        else:
            res.append(elem)
    return arr

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

def empty(arr, a):
    return arr

def prepocess(arr, mean):
    return [elem -mean for elem in arr]

def create_data_window_for_seq(data_dict, window_size=3, prepcess=clean_external):
    s = ["f" + str(i) for i in range(window_size)]
    fs=["s"+str(i) for i in range(window_size)]
    dict_frame = {}
    for elem in s:
        dict_frame[elem] = []
    for elem in fs:
        dict_frame[elem] = []

    for key in data_dict.keys():
        val = data_dict[key]["src"]
        med = np.mean(val)
        val=clean_external(val, med)
        trg = data_dict[key]["trg"]

        for i in range(len(val)-window_size):
            res = val[i:i+window_size]
            tr_=trg[i:i+window_size]




            for j, elem in enumerate(s):
                dict_frame[elem].append(res[j])

            for j, elem in enumerate(fs):
                dict_frame[elem].append(tr_[j])

    return dict_frame


def create_data_window(data_dict, window_size=3, prepcess=prepocess):
    s = ["f" + str(i) for i in range(window_size)]
    dict_frame = {"y": []}
    for elem in s:
        dict_frame[elem] = []

    for key in data_dict.keys():
        val = data_dict[key]["src"]
        trg = data_dict[key]["trg"]
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
            dict_frame["y"].append(trg[i])

    return dict_frame

if __name__ == "__main__":
    df = pd.read_csv('/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/CardioSpike/data/train.csv')
    seq=convert_to_dict(df)
    data_f=create_data_window(seq, 3)
    print("meow")
    df_new = pd.DataFrame(data_f)
    df_new.to_csv("./w=3_p=m.csv",index=False)









