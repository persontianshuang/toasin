from concurrent import futures
import os
import requests,time,random
from lxml import html

# import settings


MONGO_URI = '108.61.203.110'
# name = settings.NAME
name = 't1'

import pymongo
def pymg(highest,collections,port=MONGO_URI):
    client = pymongo.MongoClient(port, 27017)
    zhihu = client[highest]
    collections = zhihu[collections]
    return collections

MAX_WORKER = 8

def down_one(asin):
    url = 'https://www.amazon.com/dp/'+asin
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    the_html = requests.get(url,headers=header).text
    response = html.fromstring(the_html)

    price = ''
    try:
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()')[0].strip()
    except:
        price = response.xpath('//*[@id="priceblock_saleprice"]/text()')[0].strip()


    client = pymongo.MongoClient(MONGO_URI,27017)
    db = client['haha']
    coll = db[name]
    print('开始修改数据库',price)
    coll.update({'asin': asin},{'$set':{'price': price,'status':-1}})

    client.close()

    print('成功:',url)
    time.sleep(random.randint(0,5))
# down_one('https://www.amazon.com/Loved-Blanket-Star-Mermaid-Girls/dp/B01MR2CKOT/ref=sr_1_795?s=home-garden&ie=UTF8&qid=1501816261&sr=1-795-spons&keywords=mermaid+blanket+for+kids&psc=1')


def download_many(cc_list):
    print('download_many')
    workers = min(MAX_WORKER,len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        executor.map(down_one,cc_list)

def asin_to_mongo():
    from time import time
    start = time()
    from_db = list(pymg('haha',name).find({'status':4},{'_id':0}))
    print('待采集',len(from_db))
    all_to_urls = [x['asin'] for x in from_db]
    download_many(all_to_urls)
    end = time()
    print ('Cost {} seconds'.format((end - start)))
asin_to_mongo()
