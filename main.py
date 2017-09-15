from concurrent import futures
import os
import requests

import settings
from goods_url import get_url_page_list
from page_goods import down_one

MONGO_URI = '108.61.203.110'
name = settings.NAME

import pymongo
def pymg(highest,collections,port=MONGO_URI):
    client = pymongo.MongoClient(port, 29999)
    zhihu = client[highest]
    collections = zhihu[collections]
    return collections

# pp = pymg('amazon_results_url',name)
# for x in pp.find():
#     pp.update({'_id':x['_id']},{'$set':{'status':0}})

MAX_WORKER =50

def download_many(cc_list):
    print('download_many')
    workers = min(MAX_WORKER,len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        executor.map(down_one,cc_list)

def asin_to_mongo():
    from_db = list(pymg('amazon_results_url',name).find({'status':2}))
    print('todo:',len(from_db))
    def kk(data):
        data['_id'] = str(data['_id'])
        return data

    all_to_urls = [kk(x) for x in from_db]
    download_many(all_to_urls)

asin_to_mongo()
# 14352 14334

# asin = [x['asin'] for x in list(pymg('amazon_asin',name).find({'status':0},{'_id':0}))]
# asin = [print(x['asin']) for x in list(pymg('amazon_asin',name).find({},{'_id':0}))]
# print(asin)
# import requests,json
# data = {
#     'tasks': asin,
#     'name': name
# }
# requests.post('http://'+MONGO_URI+':5000/product',json=json.dumps(data))
