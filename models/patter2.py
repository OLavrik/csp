import numpy as np
import matplotlib.pyplot as plt


def detect_extr(arr):
    q25=np.quantile(arr, 0.25)
    q50=np.quantile(arr, 0.50)
    q75=np.quantile(arr, 0.75)
    IQR=q75-q25
    min_extr=q25-1.5*IQR
    max_extr=q75+1.5*IQR
    r=[0 if (elem>min_extr and elem<max_extr) else 1 for elem in arr]
    return r


def covert_quanlt(arr):
    q25 = np.quantile(arr, 0.25)
    q50 = np.quantile(arr, 0.50)
    q75 = np.quantile(arr, 0.75)
    IQR = q75 - q25
    min_extr = q25 - 1.5 * IQR
    max_extr = q75 + 1.5 * IQR
    res = []
    for elem in arr:
        if elem==q50:
            res.append(0)
            continue
        if elem > q25 and elem < q50:
            res.append(-1)
            continue
        if elem > q50 and elem < q75:
            res.append(1)
            continue
        if elem <= q25:
            res.append(-2)
            continue
        if elem >= q75:
            res.append(2)
            continue
    return res

def clean_external(arr, val):
    extr=detect_extr(arr)
    res=[]
    for i, elem in enumerate(arr):
        if extr[i]==1:
            res.append(val)
        else:
            res.append(elem)
    return res

def plot_gr(arr_src, arr_trg, time):
    arr_src=clean_external(arr_src, np.mean(arr_src))
    arr_src=covert_quanlt(arr_src)
    # plt.plot(time, arr_src)
    # plt.plot(time, [elem for elem in arr_trg])
    # plt.xlabel("Time (s)")
    # plt.ylabel("Src/Trg")
    # plt.show()
    return arr_src

def plot_gr_test(arr_src, time):
    arr_src=clean_external(arr_src, np.mean(arr_src))
    arr_src=covert_quanlt(arr_src)
    # plt.plot(time, arr_src)
    # plt.xlabel("Time (s)")
    # plt.ylabel("Src")
    # plt.show()
    return arr_src

import pandas as pd
import numpy as np
import json

def convert_to_dict(df):
    seq = {}
    for index, row in df.iterrows():
        id_ = row["id"]
        if id_ not in list(seq.keys()):
            seq[row["id"]] = {}
            seq[row["id"]]["src"] = []
            seq[row["id"]]["time"] = []
            seq[row["id"]]["trg"] = []
        seq[row["id"]]["src"].append(int(row["x"]))
        seq[row["id"]]["time"].append(int(row["time"]))
        seq[row["id"]]["trg"].append(int(row["y"]))
    return seq
def convert_to_dict_test(df):
    seq = {}
    for index, row in df.iterrows():
        id_ = row["id"]
        if id_ not in list(seq.keys()):
            seq[row["id"]] = {}
            seq[row["id"]]["src"] = []
            seq[row["id"]]["time"] = []
            seq[row["id"]]["y"] = []
        seq[row["id"]]["src"].append(int(row["x"]))
        seq[row["id"]]["time"].append(int(row["time"]))
    return seq
df = pd.read_csv('/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/CardioSpike/data/train.csv')
seq=convert_to_dict(df)


for key in seq.keys():
    seq[key]["src"]=plot_gr(seq[key]["src"], seq[key]["trg"], seq[key]["time"])


arr_mask=[]
for key in seq.keys():
    prev=0
    res=[]
    for val, elem in zip(seq[key]["src"], seq[key]["trg"]):
        if elem==1 and prev==0:
            res.append(val)
            prev=1
            continue

        if elem==1:
            res.append(val)
            continue

        if elem==0 and prev==1:
            arr_mask.append(res)
            res=[]
            prev=0
            continue

clean_arr=[]
for arr in arr_mask:
    flag=True
    found=0
    not_found=0
    for key in seq.keys():
        for i in range(0, len(seq[key]["src"])-len(arr)):
            if arr==seq[key]["src"][i:i+len(arr)]:

                if sum(seq[key]["trg"][i:i+len(arr)])>=len(seq[key]["trg"][i:i+len(arr)]):
                    print(seq[key]["trg"][i:i+len(arr)])
                    print("_________")
                    found+=1
                else:
                    not_found+=1
    if not_found==0:
        clean_arr.append(arr)

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
    df.to_csv("./pattern2_res.csv",index=False)
    return df

df_test = pd.read_csv('/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/models/test_cardio.csv')
seq_test=convert_to_dict_test(df_test)


for key in seq_test.keys():
    seq_test[key]["src"]=plot_gr_test(seq_test[key]["src"],  seq_test[key]["time"])

for key in seq_test.keys():
    # seq_test[key]["y"] = []
    seq_test[key]["y"].extend([int(0) for elem in range(len(seq_test[key]["src"]))])

for key in seq_test.keys():
    for arr in clean_arr:
        for i in range(0, len(seq_test[key]["src"])-len(arr)):
            if arr == seq_test[key]["src"][i:i + len(arr)]:
                seq_test[key]["y"][i:i+len(arr)]=[1 for k in range(len(arr))]
                print("meow")

make_result(seq_test, 2)





