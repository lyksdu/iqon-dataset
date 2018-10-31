#coding = utf-8


'''
    setId:
    setUrl:
    item

'''


import requests, sqlite3, re, json
import asyncio
import threading
from bs4 import BeautifulSoup

orm = sqlite3.connect("iqon.db",timeout=10)
cursor = orm.cursor()
# try:
cursor.execute('''
    create table if not exists iqon (
        url char(80),
        likecount int
    );''')
# except Exception:
#     print("create database error")
re_price = re.compile(r"¥[\d,]+")
class test_UrlThread(threading.Thread):
    def __init__(self,url:str, setId:int):
        super(test_UrlThread,self).__init__()
        self.testurl = url
        self.Id = setId
    def run(self):
        while True:
            try:
                r = requests.get(self.testurl,headers={
                    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                })
                break
            except Exception:
                pass
        
        if r.status_code == 200:
            
            # orm = sqlite3.connect("iqon.db")
            page = BeautifulSoup(r.text,"html.parser")
            likecount = page.select(".like-count")   
            likecount = likecount[0].text
            if not page.select(".price"):
                exit(0)
            if int(likecount) < 10:
                exit(0)
            print(self.testurl,':',likecount)
            items = page.select(".item-box")
            if not items:
                exit(0)
            set_dictionary = {}
            set_dictionary['settId'] = self.Id
            set_dictionary['setUrl'] = self.testurl
            set_dictionary['likeCount'] = likecount
            set_dictionary['items'] = []
            for i in items:
                if not i.select(".price"):
                    continue
                global re_price
                
                try:
                    temp_price =  str(re_price.findall(str(i.select(".price")))[0])
                    set_dictionary['items'].append({
                        'imgUrl': i.img['src'],
                        'price': temp_price
                    })
                except Exception:
                    print("there exists another price form:",i.select(".price"))
                    print( i.img['src'])
            # cursor = orm.cursor()
            # cursor.execute(f'''
            #     insert into iqon values("{self.testurl}",{likecount});
            # ''')
            # orm.commit()
            # orm.close()
            with open(f"sets\{ self.Id }.json",'w') as fp:
                json.dump(set_dictionary,fp)

url = 'https://www.iqon.jp/sets/'
def all_numbers():
    i = 16981
    while i>0:
        yield i
        i+=1
for i in all_numbers():
    t = test_UrlThread(url+str(i),i)
    t.start()