import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

def make_result(seq):
    dict_itog={"id":[], "time":[],  "x":[], "y":[]}
    for key in seq.keys():

        time=seq[key]["time"]


        dict_itog["id"].extend([key for i in range(len(time))])
        dict_itog["time"].extend(seq[key]["time"])
        dict_itog["y"].extend(seq[key]["trg"])
        dict_itog["x"].extend(seq[key]["src"])

    df=pd.DataFrame(dict_itog)
    df.to_csv("./gts_ra.csv",index=False)
    return df


def simplify_points(pts, tolerance):
    new_pts = [pts[0]]

    for i in range(1, len(pts) - 1):
        vector_1 = pts[i] - pts[i - 1]
        vector_2 = pts[i + 1] - pts[i]
        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle = np.arccos(dot_product)

        #print(angle * 180 / np.pi)
        EPS = 0.0001
        if EPS < angle:
            new_pts.append(pts[i])

    new_pts.append(pts[-1])
    return pts
# cv2.approxPolyDP(pts, tolerance, True)



import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
def score(true_y, pred_y):
    return f1_score(true_y, pred_y, average='weighted')

def center_padding(arr, left_pad, right_pad, val=0):
    res = [val for i in range(left_pad)]
    res.extend(arr)
    res.extend([val for i in range(right_pad)])
    return res


def plot_gr_test(arr_src, time):
#     arr_src=clean_external(arr_src, np.mean(arr_src))
#     arr_src=covert_quanlt(arr_src)
    plt.plot(time, arr_src)
    plt.xlabel("Time (s)")
    plt.ylabel("Src")
    plt.show()
    return arr_src




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

    for key in seq.keys():
        line=[]
        new_v=[]
        new_t=[]
        for v,t in  zip(seq[key]["src"], seq[key]["time"]):
            line.append((v,t))
        pts = np.array(line)
        a=simplify_points(pts, 10)

        for elem in a:
            new_v.append(elem[0])
            new_t.append(elem[1])
        seq[key]["src"]=new_v
        seq[key]["time"]=new_t
        seq[key]["trg"] = [0 for elem in range(len(new_t))]




    return seq

df = pd.read_csv('gts.csv')
seq=convert_to_dict(df)
make_result(seq)


# df_test = pd.read_csv('/Users/Olga.Lavrichenko/Documents/Olga/Untitled Folder/cardio_spike/olya_res.csv')
# seq_test=convert_to_dict(df_test)
# make_result(seq_test)



