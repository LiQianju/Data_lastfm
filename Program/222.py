import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from csv import DictReader

user_taggedartists_csv = pd.read_csv(r"../Data/user_taggedartists.csv", encoding='gbk')

userID_number = user_taggedartists_csv.drop_duplicates(subset=['userID'], keep='first', inplace=False)  # 删除userID一行的重复数据

user_taggedartists_csv = user_taggedartists_csv.drop_duplicates(subset=['userID', 'artistID'], keep='first', inplace=False)  # 删除重复数据
artists_csv = pd.read_csv(r"../Data/artists.csv", encoding='gb18030')
merge_csv = pd.merge(user_taggedartists_csv, artists_csv, left_on='artistID', right_on='id')  # 合并两表
merge_csv = merge_csv.drop(['tagID','id', 'day', 'month', 'year','url', 'pictureURL'], axis=1)
merge_csv.to_csv(r"../result/task3_1.csv", index=False, encoding='gb18030')
task3_1_csv = pd.read_csv(r"../result/task3_1.csv", encoding='gbk')
print(task3_1_csv)


df = pd.get_dummies(task3_1_csv['userID'])
TestA_beh = pd.concat([task3_1_csv,df],axis=1)

col_page=pd.DataFrame(userID_number['userID'])

print(col_page)

for page in col_page:
    TestA_beh[page] = TestA_beh[page]*TestA_beh['artistID']
#    if eval(col_page) == []:
 #       continue
del TestA_beh['userID']
del TestA_beh['artistID']
TestA_beh = TestA_beh.groupby(['name'],as_index = False).sum()
print(TestA_beh)

'''
df = pd.get_dummies(task3_1_csv['userID'])
TestA_beh = pd.concat([task3_1_csv,df],axis=1)
df4 = tuple(userID_number['userID'])
col_page = str(df4) #将userID一列内容赋值给col_page
print(col_page)
col_page = col_page.strip(',').split(',')#改为列表形式
col_page = col_page[0:-1]#删去最后一个元素
col_page = col_page[1:0]
print(col_page)

for page in col_page:
    TestA_beh[page] = TestA_beh[page]*TestA_beh['artistID']
    if eval(col_page) == []:
        continue
del TestA_beh['userID']
del TestA_beh['artistID']
TestA_beh = TestA_beh.groupby(['artistID'],as_index = False).sum()
TestA_beh.to_csv(r"../result/task3_2.csv", index=False, encoding='gb18030')
print(TestA_beh)
'''
def zerofilter(listArr):
    ans = []
    for i in listArr:
        if i!=0:
            ans.append(i)
    return ans

def load_data_set():
    """
    Load a sample data set (From Data Mining: Concepts and Techniques, 3th Edition)
    Returns:
        A data set: A list of transactions. Each transaction contains several items.
    """
    data_set1 = pd.read_csv(r"../result/task3_1.csv", encoding='gbk')
    data_set =[]
    for i in data_set1.columns:
        dataRow = list(data_set1[i])
        dataRow = zerofilter(dataRow)
        data_set.append(dataRow)
    print(data_set)
    return data_set

if __name__ == '__main__':
    load_data_set()