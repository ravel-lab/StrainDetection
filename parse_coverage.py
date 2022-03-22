#!/usr/bin/env python3
import pandas as pd
import sys

filename = sys.argv[1].split(".")[0]

data = pd.read_csv(sys.argv[1],sep="\t")

data[['Strain','Gene']] = data['contig'].str.split('|',expand=True)
data = data.drop(['Gene','pos'],axis=1)

data_sum = data.groupby('Strain').median()
data_sum.to_csv("%s_sum_cov.csv" %(filename),sep=",")
