import pymongo

def pymg(highest,collections,port='108.61.203.110'):
    client = pymongo.MongoClient(port, 27017)
    zhihu = client[highest]
    collections = zhihu[collections]
    return collections

for x in pymg('amazon_asin','meirenyutan').find():
    pymg('amazon_asin','meirenyutan').update({'asin':x['asin']},{'$set':{'price':''}})
    the = pymg('amazon','t1').find_one({'asin':x['asin']})
    if the!=None:
        pymg('amazon_asin','meirenyutan').update({'asin':x['asin']},{'$set':{'price':the['price']}})
