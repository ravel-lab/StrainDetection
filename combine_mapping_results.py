#!/usr/bin/python3

import os
import pandas as pd 
import numpy as np

data_combo = pd.DataFrame()

for filename in os.listdir('.'):
    if filename.endswith(".depth"): 
        prefix = filename.split("_pred")[0]

        data=pd.read_csv(filename,header=None,sep="\t")

        data.columns = ['contig','locus',prefix]
        data = data.drop(['locus'],axis=1)
        data = data.groupby(np.arange(len(data))//100).mean()
        print(data.head())
        data_combo[prefix] = data[prefix]

        continue
    else:
        continue

print(data_combo.head())
