import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def task2_1():
    user_taggedartists_csv = pd.read_csv(r"../Data/user_taggedartists.csv", encoding='gbk')
    artists_csv = pd.read_csv(r"../Data/artists.csv", encoding='gb18030')
    #print(artists_csv.columns)
    #print("原始数据数量" + str(len(artists_csv)))
    print("user_artists表数据去重后")
    user_taggedartists_csv.drop_duplicates(subset=['userID', 'artistID'], keep='first', inplace=True)  # 删除重复数据
    #print(len(user_taggedartists_csv))
    #print("\n")
    merge_csv = pd.merge(user_taggedartists_csv, artists_csv ,left_on='artistID',right_on='id') #合并两表
    merge_csv['add'] = '1'
    merge_csv['add'] = pd.to_numeric(merge_csv['add'], errors='coerce')
    merge_csv = merge_csv.drop(['url', 'pictureURL','id','tagID','day','month','year'], axis=1)#删去多余列
    #print(merge_csv)
    merge_csv_sum = pd.pivot_table(data=merge_csv, index=["name"], values=["add"], fill_value=0,
                                       aggfunc=[np.sum, len])
    #print(merge_csv_sum)
    merge_csv_sum_all_sum = pd.DataFrame({"name": merge_csv_sum.index, "number": merge_csv_sum.iloc[:, 0]})
    merge_csv_sum_all_sum.to_csv(r"../result/task2_1.csv", index=False, encoding='gb18030')
    print("task2_1 completed")
    task2_1_csv = pd.read_csv(r"../result/task2_1.csv", encoding='gbk')
    df_obj = task2_1_csv.sort_values(by="number", ascending=False)
    df_obj = df_obj.head(20)
    df_obj = df_obj.name
    print(df_obj)

def task2_2():
    task2_1_csv = pd.read_csv(r"../result/task2_1.csv", encoding='gbk')
    artists_csv = pd.read_csv(r"../Data/artists.csv", encoding='gb18030')
    merge_csv = pd.merge(task2_1_csv, artists_csv, left_on='name', right_on='name')  # 合并两表
    merge_csv = merge_csv.drop(['url', 'pictureURL'], axis=1)
    df_obj = merge_csv.sort_values(by="number", ascending=False)
    df_obj = df_obj.head(20)
    #print(df_obj)
    df_obj.to_csv(r"../result/task2_2.csv", index=False, encoding='gb18030')
    task2_2_csv = pd.read_csv(r"../result/task2_2.csv", encoding='gbk')
    user_taggedartists_csv = pd.read_csv(r"../Data/user_taggedartists.csv", encoding='gbk')
    merge1_csv = pd.merge(user_taggedartists_csv, task2_2_csv, left_on='artistID', right_on='id')  # 合并两表
    merge1_csv = merge1_csv.drop(['userID','id','day', 'month', 'year'], axis=1)
    #print(merge1_csv)
    merge1_csv.to_csv(r"../result/task2_3.csv", index=False, encoding='gb18030')
    task2_3_csv = pd.read_csv(r"../result/task2_3.csv", encoding='gbk')
    task2_3_csv['add'] = '1'
    task2_3_csv['add'] = pd.to_numeric(task2_3_csv['add'], errors='coerce')
    task2_3_csv_sum = pd.pivot_table(data=task2_3_csv, index=["tagID"], values=["add"], fill_value=0,
                                       aggfunc=[np.sum, len])#计算
    merge_csv_sum_all_sum = pd.DataFrame({"tagID": task2_3_csv_sum.index, "number": task2_3_csv_sum.iloc[:, 0]})
    #print(task2_3_csv_sum)
    df_obj = merge_csv_sum_all_sum.sort_values(by="number", ascending=False)#排序
    #print(df_obj)
    df_obj.to_csv(r"../result/task2_4.csv", index=False, encoding='gb18030')
    print("task2_4 completed")
    task2_4_csv = pd.read_csv(r"../result/task2_4.csv", encoding='gbk')
    tage_csv = pd.read_csv(r"../Data/tage.csv", encoding='gb18030')
    merge2_csv = pd.merge(task2_4_csv, tage_csv, left_on='tagID', right_on='tagID')  # 合并两表
    merge2_csv = merge2_csv.drop(['number', 'tagID'], axis=1)#删除
    print(merge2_csv)

def task2_3():
    user_artists_csv = pd.read_csv(r"../Data/user_artists.csv", encoding='gb18030')
    print(user_artists_csv.columns)
    print("原始数据数量" + str(len(user_artists_csv)))
    user_artists_sum = pd.pivot_table(data=user_artists_csv, index=["artistID"], values=["weight"], fill_value=0,
                                 aggfunc=[np.sum, len])
    user_artists_all_sum = pd.DataFrame({"artistID": user_artists_sum.index, "weight_sum": user_artists_sum.iloc[:, 0]})
    user_artists_all_sum.to_csv(r"../result/task2_5.csv", index=False, encoding='gbk')
    print("task2_5 completed")
    task2_5_csv = pd.read_csv(r"../result/task2_5.csv", encoding='gbk')
    task2_5_len = str(len(task2_5_csv))
    #print("原始数据数量" + task2_5_len)
    task2_5_len = pd.to_numeric(task2_5_len, errors='coerce')#强制转换
    print("原始数据数量")
    print(task2_5_len)
    people_two=int(task2_5_len*0.2) #20%歌手数
    print("20%歌手数",people_two)
    people_eight=int(task2_5_len*0.8) #80%歌手数
    print("80%歌手数",people_eight)
    weight_sum=task2_5_csv['weight_sum'].sum()
    print("时长总数",weight_sum)
    sing_two=int(weight_sum*0.2) #20%歌手数
    print("20%时长",sing_two)
    sing_eight=int(weight_sum*0.8) #80%歌手数
    print("80%时长",sing_eight)
    df_obj = task2_5_csv.sort_values(by="weight_sum", ascending=False)
    df_obj_sum8 = df_obj['weight_sum'].head(people_two).sum()
    print("前%20歌手播放时长总数",df_obj_sum8)#前%20歌手播放时长总数
    df_obj_sum2 = df_obj['weight_sum'].tail(people_eight).sum()
    print("后80%歌手播放时长总数",df_obj_sum2)#后80%歌手播放时长总数
    df_obj_sum=df_obj_sum8+df_obj_sum2#验证
    print("验证",df_obj_sum)  # 歌手播放时长总数


if __name__ == '__main__':
    task2_1()
    task2_2()
    task2_3()