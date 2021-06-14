import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import scipy.stats as st

def task1_1():
    user_friends_csv = pd.read_csv(r"../Data/user_friends.csv", encoding='gbk')
    print(user_friends_csv.columns)
    print("原始数据数量" + str(len(user_friends_csv)))
    print("\n")
    user_artists_csv = pd.read_csv(r"../Data/user_artists.csv", encoding='gbk')
    print(user_artists_csv.columns)
    print("原始数据数量" + str(len(user_artists_csv)))
    print("\n")
    print("user_friends表数据去重后")
    user_friends_csv.drop_duplicates(subset=['userID'],keep='first',inplace=True)  # 删除重复数据
    print(len(user_friends_csv))
    print("\n")
    print("user_artists表数据去重后")
    user_friends_csv.drop_duplicates(subset=['userID'], keep='first', inplace=True)  # 删除重复数据
    print(len(user_friends_csv))
    print("\n")

def task1_2():
    user_friends_csv = pd.read_csv(r"../Data/user_friends.csv", encoding='gbk')
    user_friends_csv['add'] = '1'
    user_friends_csv['add'] = pd.to_numeric(user_friends_csv['add'], errors ='coerce')#强制转换为int
    print(user_friends_csv)
    friends_sum = pd.pivot_table(data=user_friends_csv, index=["userID"], values=["add"], fill_value=0, aggfunc=[np.sum, len])
    friends_sum_all_sum = pd.DataFrame({"userID": friends_sum.index, "number": friends_sum.iloc[:, 0]})
    friends_sum_all_sum.to_csv(r"../result/task1_2.csv", index=False, encoding='gbk')
    print("task1_2 completed")
    task1_2_csv = pd.read_csv(r"../result/task1_2.csv", encoding='gbk')
    print(task1_2_csv['number'].mean())

def task1_3():
    task1_2_csv = pd.read_csv(r"../result/task1_2.csv", encoding='gbk')
    x=task1_2_csv.number
    y=st.norm.cdf(x)
    plt.figure(figsize=(10,10))
    plt.plot(x,y, '-', linewidth=1)
    plt.show()

if __name__ == '__main__':
    task1_1()
    task1_2()
    task1_3()