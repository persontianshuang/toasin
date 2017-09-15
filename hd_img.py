from concurrent import futures
import os
import requests
from lxml import html

import settings


MONGO_URI = '108.61.203.110'
name = settings.NAME

import pymongo
def pymg(highest,collections,port=MONGO_URI):
    client = pymongo.MongoClient(port, 27017)
    zhihu = client[highest]
    collections = zhihu[collections]
    return collections

MAX_WORKER = 30

def down_one(asin):
    url = 'https://www.amazon.com/dp/'+asin
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    the_html = requests.get(url,headers=header).text
    response = html.fromstring(the_html)
    img = response.xpath('//div[contains(@id, "imgTagWrapperId")]//img/@src')[0]
    img = img.strip().replace('data:image/jpeg;base64,','')
    client = pymongo.MongoClient(MONGO_URI,27017)
    db = client['amazon_asin']
    coll = db[name]
    print('开始修改数据库')
    coll.update({'asin': asin},{'$set':{'img': img,'status':1}})

    client.close()

    print('成功:',url)
# down_one('https://www.amazon.com/Loved-Blanket-Star-Mermaid-Girls/dp/B01MR2CKOT/ref=sr_1_795?s=home-garden&ie=UTF8&qid=1501816261&sr=1-795-spons&keywords=mermaid+blanket+for+kids&psc=1')


def download_many(cc_list):
    print('download_many')
    workers = min(MAX_WORKER,len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        executor.map(down_one,cc_list)

def asin_to_mongo():
    from time import time
    start = time()


    all_urls = []

    # from_db = list(pymg('amazon_asin',name).find({'status':0},{'_id':0}))
    # print('待采集',len(from_db))
    # all_to_urls = [x['asin'] for x in from_db]
    download_many(all_to_urls)
    end = time()
    print ('Cost {} seconds'.format((end - start)))
asin_to_mongo()
