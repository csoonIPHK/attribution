import pandas as pd
from collections import OrderedDict
import csv
import numpy as np

testFile = "Q2Paths.csv"
df = pd.read_csv(testFile, header=0, usecols=["MCF Channel Grouping Path", "Conversions", "Conversion Value"])
total_conv = df['Conversions'].sum()

# Delimits path column to form column where values are lists of paths
df['d_list'] = [i.replace(' ','').split('>') for i in df['MCF Channel Grouping Path']]
# Counts delimit_list to determine the number of touchpoints for each conversion and adds column with touchpoint count as values
df['touchpoints'] = [len(i) for i in df['d_list']]
# Converts the first two channels in each conversion into a column where values are pair of tuples 
df['p_tuples'] = [(i[0],i[1]) for i in df['d_list']]

for i, j in df[df['touchpoints']==5]['p_tuples'].value_counts().iteritems():
    print(i,j/total_conv)