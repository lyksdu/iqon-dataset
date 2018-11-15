import json
from os import path,listdir
import re
dir_list = listdir('cate')
trans_dict = {}
for file_name in dir_list:
    outfit = {}

    with open(path.join('cate',file_name), 'r') as fp:
        try:
            outfit = json.load(fp)
        except Exception:
            print(file_name)
            continue
    for item in outfit['items']:
        # try:
            # trans_set.add(item['category'])
        try:
            trans_dict[item['category']].append(outfit['settId'])
        except Exception:
            trans_dict[item['category']] = []
            trans_dict[item['category']].append(outfit['settId'])
            # print( )
            # print(item['imgUrl'])
print(len(trans_dict))
for a,b in trans_dict.items():
    if len(b) < 5:
        print(a,b)