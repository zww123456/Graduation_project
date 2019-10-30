# -*- encoding=utf-8 -*-
import pandas as pd

pd.set_option('display.max_columns', None)

head = ['village', 'place', 'layout', 'price', 'area', 'year',
        'orientation', 'floor', 'trim', 'elevator', 'north', 'east']
data = pd.read_csv('House_Info.csv', delimiter=',', names=head)

place_list = data['place'].unique()
place_dict = {}
for i in range(len(place_list)):
    place_dict[place_list[i]] = i

print(place_dict)


def clean_place(x):
    return place_dict[x]


def clean_layout(x):
    if '室' in x and '厅' in x and '卫' in x:
        x = x.replace('室', '').replace('厅', '').replace('卫', '').replace(' ', ',')
    return x


def clean_price(x):
    return eval(x.replace(' 元/m²', ''))


def clean_area(x):
    return eval(x.replace('平方米', ''))


def clean_year(x):
    return eval(x.replace('年', ''))


ori_list = data['orientation'].unique()

ori_dict = {}
for i in range(len(ori_list)):
    ori_dict[ori_list[i]] = i

print(ori_dict)

def clean_ori(x):
    return ori_dict[x]


def clean_floor(x):
    if x[:2] == '低层':
        return -1
    elif x[:2] == '中层':
        return 0
    else:
        return 1


# trim_list = data['trim'].unique()
# print(trim_list)

def clean_trim(x):
    if x == '精装修':
        return 1
    elif x == '豪华装修':
        return 2
    elif x == '简单装修':
        return 0
    else:
        return -1


def clean_elevator(x):
    if x == '有':
        return 1
    else:
        return 0


data['place'] = data['place'].apply(clean_place)
data['layout'] = data['layout'].apply(clean_layout)
data['price'] = data['price'].apply(clean_price)
data['area'] = data['area'].apply(clean_area)
data['year'] = data['year'].apply(clean_year)
data['orientation'] = data['orientation'].apply(clean_ori)
data['floor'] = data['floor'].apply(clean_floor)
data['trim'] = data['trim'].apply(clean_trim)
data['elevator'] = data['elevator'].apply(clean_elevator)


def get_s(x):
    return eval(x.split(',')[0])


def get_f(x):
    return eval(x.split(',')[1])


def get_t(x):
    return eval(x.split(',')[2])


data['s'] = data['layout'].apply(get_s)
data['f'] = data['layout'].apply(get_f)
data['t'] = data['layout'].apply(get_t)

data = data.drop(['village','layout'], axis=1)

data['count_price'] = data['price'] * data['area']

qx = data[data['place'] == 0]
xxt = data[data['place'] == 1]
jn = data[data['place'] == 2]
xn = data[data['place'] == 3]
lq = data[data['place'] == 4]
yn = data[data['place'] == 5]
wm = data[data['place'] == 6]

print(data[:20])