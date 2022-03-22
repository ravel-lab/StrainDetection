#!/usr/bin/python3

#loading in required python modules
from Bio import SeqIO
import sys
import matplotlib.pyplot as pyplot
from statistics import median
import pandas as pd

data = pd.read_csv("%s.depth" %(sys.argv[1]),sep="\t",header=None)

data.columns = ['contig','pos','cov']

data_mean = data.groupby('contig',sort=False).mean().reset_index()

data_mean.to_csv("%s.cov" %(sys.argv[1]), sep="\t",index=None)
