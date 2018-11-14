import json
from os import path,listdir
import requests
from bs4 import BeautifulSoup
import re
dir_name = "new_sets"
dir_list = listdir(path.join(dir_name))
# print(dirlist)
item_url = "https://item.iqon.jp/"

for i in dir_list:
    outfit ={}
    with open(path.join(dir_name,i),'r') as fp:
        outfit = json.load(fp)
        # print(outfit.keys())
        # dict_keys(['settId', 'setUrl', 'likeCount', 'items'])
        # if len(outfit['items'])<2:
        #     print('!!!')
                    # break
        # items_keys(['imgUrl','price'])
        for item in outfit['items']:
            # print(item['imgUrl'])
            num = re.compile("\d+")
            # print(num.findall(item['imgUrl'][0]))
            new_item_url = item_url+num.findall(item['imgUrl'])[0]
            print(new_item_url)
            r = requests.get(new_item_url,headers={
                    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                    'Referer': outfit['setUrl']
                })
            page = BeautifulSoup(r.text,'html.parser')
            try:
                category_name = page.select(".category")[0]
                print (category_name.text)
                category_name = category_name.text
                if '×' in category_name:
                    category_name = category_name.split('×')[1]
                item['category'] = category_name 
            except Exception:
                pass

    with open(path.join('cate',i),'w') as fp:
        json.dump(outfit,fp)