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
    return cv2.approxPolyDP(pts, tolerance, True)
    anchor = 0
    floater = len(pts) - 1
    stack = []
    keep = set()

    stack.append((anchor, floater))
    while stack:
        anchor, floater = stack.pop()

        if pts[floater] != pts[anchor]:
            anchorX = float(pts[floater][0] - pts[anchor][0])
            anchorY = float(pts[floater][1] - pts[anchor][1])
            seg_len = math.sqrt(anchorX ** 2 + anchorY ** 2)
            anchorX /= seg_len
            anchorY /= seg_len
        else:
            anchorX = anchorY = seg_len = 0.0

        # внутренний цикл:
        max_dist = 0.0
        farthest = anchor + 1
        for i in range(anchor + 1, floater):
            dist_to_seg = 0.0
            # compare to anchor
            vecX = float(pts[i][0] - pts[anchor][0])
            vecY = float(pts[i][1] - pts[anchor][1])
            seg_len = math.sqrt(vecX ** 2 + vecY ** 2)
            # dot product:
            proj = vecX * anchorX + vecY * anchorY
            if proj < 0.0:
                dist_to_seg = seg_len
            else:
                # compare to floater
                vecX = float(pts[i][0] - pts[floater][0])
                vecY = float(pts[i][1] - pts[floater][1])
                seg_len = math.sqrt(vecX ** 2 + vecY ** 2)
                # dot product:
                proj = vecX * (-anchorX) + vecY * (-anchorY)
                if proj < 0.0:
                    dist_to_seg = seg_len
                else:  # расстояние от до прямой по теореме Пифагора:
                    dist_to_seg = math.sqrt(abs(seg_len ** 2 - proj ** 2))
                if max_dist < dist_to_seg:
                    max_dist = dist_to_seg
                    farthest = i

        if tol1 <= max_dist <= tolerance:  # использование отрезка
            keep.add(anchor)
            keep.add(floater)
        else:
            stack.append((anchor, farthest))
            stack.append((farthest, floater))

    keep = list(keep)
    keep.sort()
    return [pts[i] for i in keep]


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
        a=list(simplify_points(pts, 15)[:, 0, :])

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



