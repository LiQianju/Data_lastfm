import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from csv import DictReader
from itertools import groupby #itertool还包含有其他很多函数，比如将多个list联合起来。。http://www.cocoachina.com/articles/97971

import csv

result = {}

with open(r"../Data/user_artists.csv", 'rb') as user_artists_csv:
    #user_artists_csv = user_artists_csv.drop(['weight'], axis=1)
    csvreader = csv.reader(user_artists_csv, delimiter=',', quotechar='"')
    for row in csvreader:
        if row[0] in result:
            result[row[0]].append(row[1])
        else:
            result[row[0]] = [row[1]]

print (result)

#user_artists_csv = pd.read_csv(r"../Data/user_artists.csv", encoding='gbk')
#user_artists_csv = user_artists_csv.drop(['weight'], axis=1)
#print(user_artists_csv)

