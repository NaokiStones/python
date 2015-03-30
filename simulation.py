# coding:utf-8 

import random
import numpy as np
# param
num_of_user = 10000      # ユーザ数
num_of_page = 1000     # ページ数
num_of_category = 40   # カテゴリー数
num_of_category_each = 22 # それぞれのカテゴリーのコンテンツ数(user)
num_of_category_each_page = 152 # それぞれのカテゴリーのコンテンツ数(user)
num_of_view = 180

epsilon_each_category = 20 # それぞれのカテゴリーのコンテンツ数のブレ
epsilon_each_category_page = 152 # それぞれのカテゴリーのコンテンツ数のブレ
epsilon_view = 18
epsilon = 0.90

# User_attr生成
user_attr = np.array([]) 
for i in range(num_of_category):
    tmp_num_of_category_each = num_of_category_each + random.randint(0, epsilon_each_category) - (epsilon_each_category / 2)
    user_attr = np.append(user_attr, [i] * tmp_num_of_category_each)

for i in range(num_of_user - len(user_attr)):
    user_attr = np.append(user_attr, random.randint(0, epsilon_each_category))
    
random.shuffle(user_attr)
# Users生成 
users = []
for i in range(num_of_user):
    tmp_id = i
    tmp_attr = int(user_attr[i])
    users.append((tmp_id, tmp_attr))


## Page_attr, Page_attr_index生成

# page_attr
page_attr = np.array([])
for i in range(num_of_category):
    tmp_num_of_category_each = num_of_category_each_page + random.randint(0, epsilon_each_category_page) - (epsilon_each_category_page / 2)
    page_attr = np.append(page_attr, np.array([i] * tmp_num_of_category_each))

page_attr = np.append(page_attr, np.array([0]*(num_of_page - len(page_attr))))
random.shuffle(page_attr)

# page_attr_index
page_attr_index = []
for i in range(num_of_category):
    page_attr_index.append([])

for i in range(num_of_page):
    page_attr_index[int(page_attr[i])].append(i)

# pages作成
pages = []
cnt = 0
for i in range(num_of_page):
    pages.append((i, int(page_attr[i])))
    if(page_attr[i]==0):
        cnt+=1
# print pages
# print cnt

# print page_attr_index

# 見る
record = []
for i in range(num_of_user):
    tmp_num_of_view = num_of_view + random.randint(0, epsilon_view)
    for j in range(tmp_num_of_view):
        tmp_page = -1 
        if(random.random() < epsilon):
            tmp_index = random.randint(0, num_of_category-1)
            tmp_page = random.choice(page_attr_index[tmp_index])
        else:
            tmp_index = int(user_attr[i])
            tmp_page = random.choice(page_attr_index[tmp_index])
        tmp_record = (i, tmp_page)
        record.append(tmp_record)
#print record

user_vect = []
for i in range(num_of_user):
    user_vect.append(np.zeros(num_of_page))

for i in range(len(record)):
    user_vect[record[i][0]][record[i][1]] += 1


##                   Clustering                       ##
# print "Clustering!"

from sklearn.cluster import KMeans
kmeans_model = KMeans(n_clusters=num_of_category, max_iter=6000, random_state=10).fit(user_vect)
labels = kmeans_model.labels_

# generate network
for i in range(num_of_user):
    str1 = '[' + str(labels[i])+ ']'
    print '%d,%s' % (i, str1)

for i in range(num_of_user):
    str1 = '{' + str(int(user_attr[i]))+ '}'
    print '%d,%s' % (i, str1)

for i in range(num_of_category):
    str1 = '[' + str(i) + ']'
    print '%s,%s' % (str1, 'root')
    str1 = '{' + str(i) + '}'
    print '%s,%s' % (str1, 'root')
centers = kmeans_model.cluster_centers_
## show result 

sum = 0

