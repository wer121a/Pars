from time import sleep
import pandas as pd
import numpy as np
from multiprocessing import Process, Queue

base_nwe = pd.DataFrame(columns=["Name", "p1", "x", 'p2', 'f1', 'f2', 'totm', 'totb'])


def obrbotka(travel, p, queue, ):

    p = p

    while True:
        base = base_nwe.copy()
        base = travel.get()
        #создание одного df из двух баз
        # df = pd.merge(base, base2, on="Name")
        base.loc[:, base.columns !="Name"] = base.loc[:, base.columns != "Name"].replace("—", 0)
        base["p1"] = pd.to_numeric(base["p1"],errors='coerce')
        base["p2"] = pd.to_numeric(base["p2"],errors='coerce')
        
        base["Исход"] = 100 - (((1/base["p1"])+(1/base["p2"]))*100)

        base = base.loc[base["Исход"] > 0]
        base = base.loc[base["Исход"] < p]

        if base.empty:
            print("Нет")
        else:
            print(base)
            queue.put(base.copy())


# 10 000 - б
# формула (1/п1)+(1/п2)=x*100 и 100-x = доход
# 1 панас п1 = 1.6 ; п2 = 2.7
# 2 панас п1 = 1.4 ; п2 = 2.9

# 1 фрик п1 1.6 п2.9 - вилка

# бк1 6400 на п1 = 10311
# бк2 3556 на п2 = 10311