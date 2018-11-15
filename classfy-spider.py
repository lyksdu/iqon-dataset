import json
from os import path,listdir
import requests
from bs4 import BeautifulSoup
import re
import threading


class Thread_cate_spider(threading.Thread):
    def __init__(self, filename):
        super(Thread_cate_spider, self).__init__()
        self.filename = filename
    
    def run(self):
        outfit = {}
        
        if self.filename in listdir(path.join('cate')):
            exit(0)
        re_num = re.compile(r"\d+")
        with open(path.join('new_sets',self.filename),'r') as fp:
            outfit = json.load(fp)
        print(outfit['setUrl'])
        for item in outfit['items']:
        # print(item['imgUrl'])
        
        # print(num.findall(item['imgUrl'][0]))
            new_item_url = item_url+re_num.findall(item['imgUrl'])[0]
        # print(new_item_url)
            test_tot = 0
            while True:
                try:
                    test_tot += 1
                    if test_tot > 100:
                        exit(0)
                    r = requests.get(new_item_url,headers={
                        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                        'Referer': outfit['setUrl']
                    })
                    break
                except Exception:
                    pass    
            page = BeautifulSoup(r.text,'html.parser')

            try:
                category_name = page.select(".category")[0]
                # print (category_name.text)
                category_name = category_name.text
                if '×' in category_name:
                    category_name = category_name.split('×')[1]
                item['category'] = category_name 
            except Exception:
                exit(0)

        with open(path.join('cate',self.filename),'w') as fp:
            json.dump(outfit,fp)

    



dir_name = "new_sets"
dir_list = listdir(path.join(dir_name))
# print(dirlist)
item_url = "https://item.iqon.jp/"
dir_list = ['2467725.json',
'2760867.json',
'2915420.json',
'2956852.json']
for i in dir_list:
    t = Thread_cate_spider(i)
    t.start()
    # outfit ={}
    # with open(path.join(dir_name,i),'r') as fp:
    #     outfit = json.load(fp)
    #     # print(outfit.keys())
    #     # dict_keys(['settId', 'setUrl', 'likeCount', 'items'])
    #     # if len(outfit['items'])<2:
    #     #     print('!!!')
    #                 # break
    #     # items_keys(['imgUrl','price'])
    #     for item in outfit['items']:
    #         # print(item['imgUrl'])
    #         num = re.compile("\d+")
    #         # print(num.findall(item['imgUrl'][0]))
    #         new_item_url = item_url+num.findall(item['imgUrl'])[0]
    #         print(new_item_url)
    #         r = requests.get(new_item_url,headers={
    #                 'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    #                 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    #                 'Referer': outfit['setUrl']
    #             })
    #         page = BeautifulSoup(r.text,'html.parser')
    #         try:
    #             category_name = page.select(".category")[0]
    #             print (category_name.text)
    #             category_name = category_name.text
    #             if '×' in category_name:
    #                 category_name = category_name.split('×')[1]
    #             item['category'] = category_name 
    #         except Exception:
    #             pass

    # with open(path.join('cate',i),'w') as fp:
    #     json.dump(outfit,fp)