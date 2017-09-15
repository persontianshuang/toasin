from goods_url import get_url_page_list
import pymongo
import settings
from bson.objectid import ObjectId

MONGO_URI = '108.61.203.110'

def pymg(highest,collections,port=MONGO_URI):
    client = pymongo.MongoClient(port, 29999)
    zhihu = client[highest]
    collections = zhihu[collections]
    return collections
def path_url():
    path = "/Users/user/work/链接/2.txt"
    with open(path,'r') as f:
        fr = f.readlines()
        # [print(x.strip()) for x in fr]
        return [x.strip() for x in fr if x.strip()!='']

name = settings.NAME

urls = path_url()


amazon_results_url = pymg('amazon_results_url',name)
first_urls = pymg('first_urls',name)


if len(list(first_urls.find({},{'_id':0})))==0:
    first_urls_lists = [{'url':x,'status':0} for x in urls]
    first_urls.insert_many(first_urls_lists)

def down_one(data):
    x = data['url']
    to_url_lists = get_url_page_list(x)
    url_lists = [{'type':'results_url','urls':x,'status':0} for x in to_url_lists]
    amazon_results_url.insert_many(url_lists)
    first_urls.update({'_id':ObjectId(data['_id'])},{'$set':{'status':1}})


from concurrent import futures
MAX_WORKER = 20

def download_many(cc_list):
    print('download_many')
    print(len(cc_list))
    workers = min(MAX_WORKER,len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        executor.map(down_one,cc_list)

def kk(data):
    data['_id'] = str(data['_id'])
    return data


d_urls = [kk(x) for x in list(first_urls.find({'status':0}))]

download_many(d_urls)

# 队列
#
# 客户端
# workflow
# 一样的url  读取 设置 返回id

