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
    #if eval(col_page) == []:
        #continue
del TestA_beh['userID']
del TestA_beh['artistID']
TestA_beh = TestA_beh.groupby(['name'],as_index = False).sum()
TestA_beh.to_csv(r"../result/task3_2.csv", index=False, encoding='gb18030')
#print(TestA_beh)

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

def create_C1(data_set):
    """
    Create frequent candidate 1-itemset C1 by scaning data set.
    Args:
        data_set: A list of transactions. Each transaction contains several items.
    Returns:
        C1: A set which contains all frequent candidate 1-itemsets
    """
    C1 = set()
    for t in data_set:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1

def is_apriori(Ck_item, Lksub1):
    """
    Judge whether a frequent candidate k-itemset satisfy Apriori property.
    Args:
        Ck_item: a frequent candidate k-itemset in Ck which contains all frequent
                 candidate k-itemsets.
        Lksub1: Lk-1, a set which contains all frequent candidate (k-1)-itemsets.
    Returns:
        True: satisfying Apriori property.
        False: Not satisfying Apriori property.
    """
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True

def create_Ck(Lksub1, k):
    """
    Create Ck, a set which contains all all frequent candidate k-itemsets
    by Lk-1's own connection operation.
    Args:
        Lksub1: Lk-1, a set which contains all frequent candidate (k-1)-itemsets.
        k: the item number of a frequent itemset.
    Return:
        Ck: a set which contains all all frequent candidate k-itemsets.
    """
    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k - 2] == l2[0:k - 2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                # pruning
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck

def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    """
    Generate Lk by executing a delete policy from Ck.
    Args:
        data_set: A list of transactions. Each transaction contains several items.
        Ck: A set which contains all all frequent candidate k-itemsets.
        min_support: The minimum support.
        support_data: A dictionary. The key is frequent itemset and the value is support.
    Returns:
        Lk: A set which contains all all frequent k-itemsets.
    """
    Lk = set()
    item_count = {}
    for t in data_set:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    t_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk

def generate_L(data_set, k, min_support):
    """
    Generate all frequent itemsets.
    Args:
        data_set: A list of transactions. Each transaction contains several items.
        k: Maximum number of items for all frequent itemsets.
        min_support: The minimum support.
    Returns:
        L: The list of Lk.
        support_data: A dictionary. The key is frequent itemset and the value is support.
    """
    support_data = {}
    C1 = create_C1(data_set)
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k + 1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data

def generate_big_rules(L, support_data, min_conf):
    """
    Generate big rules from frequent itemsets.
    Args:
        L: The list of Lk.
        support_data: A dictionary. The key is frequent itemset and the value is support.
        min_conf: Minimal confidence.
    Returns:
        big_rule_list: A list which contains all big rules. Each big rule is represented
                       as a 3-tuple.
    """
    big_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list

if __name__ == "__main__":
    """
    Test
    """
    data_set = load_data_set()
    L, support_data = generate_L(data_set, k=1, min_support=0.2)
    big_rules_list = generate_big_rules(L, support_data, min_conf=0.7)
    for Lk in L:
        print("=" * 50)
        print("frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
        print("=" * 50)
        for freq_set in Lk:
            print(freq_set, support_data[freq_set])
    print
    for item in big_rules_list:
        print(item[0], "=>", item[1], "conf: ", item[2])
    print("Big Rules")