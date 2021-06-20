from numpy import loadtxt
from xgboost import XGBClassifier
model = XGBClassifier()
model.load_model("xgb_model.json")

import pandas as pd

df = pd.read_csv('sb.csv')

df_res = df.copy(deep=True)

Y = df["y"]
del df["y"]
del df["id"]
X = df

y = model.predict_proba(X)

res_col = []
for _Y, _y in zip(Y, y):
    res_col.append(1 if _y[1] > 0.07 else _Y)

df_res['y'] = res_col
df_res.to_csv('xg.csv', index=False)


