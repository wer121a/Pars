from time import sleep
import pandas as pd
import numpy as np
from multiprocessing import Process, Queue

base_nwe = pd.DataFrame(columns=["Name", "p1", "x", 'p2', 'f1', 'f2', 'totm', 'totb'])


def obrbotka(travel, p):

    p = p

    while True:
        base = base_nwe.copy()
        base = travel.get()
        base.loc[:, base.columns !="Name"] = base.loc[:, base.columns != "Name"].replace("—", 0)
        base["p1"] = pd.to_numeric(base["p1"],errors='coerce')
        base["p2"] = pd.to_numeric(base["p2"],errors='coerce')
        base["Исход"] = 100 - (((1/base["p1"])+(1/base["p2"]))*100)
        
        # base = base.loc[base["Исход"] < p]

        
        print(base)
        # Queue.put(base.copy())
