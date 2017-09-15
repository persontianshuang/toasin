import pymongo,os,re,random

import pymongo

def pymg(highest,collections,port='108.61.203.110'):
    client = pymongo.MongoClient(port, 27017)
    zhihu = client[highest]
    collections = zhihu[collections]
    return collections


client = pymongo.MongoClient('localhost', 27017)
zhihu = client['ls']
coll = zhihu['meirenyutan']


# img_path = "/Users/user/Desktop/美人鱼2"
# list_img = os.listdir(img_path)
# img_asin = [re.split(r'[_.]',str(it))[-2] for it in list_img]
#
#
# print(img_asin)
#
# coll.insert_many([{'asin':x,'price':''} for x in img_asin])
# print(len(img_asin))

# this = pymg('amazon','t1')
# for x in coll.find({'price': ''}):
#     the = this.find_one({'asin':x['asin']})
#     if the != None:
#         print('_'*20)
#         coll.update({'asin':x['asin']},{'$set':{'price':the['price']}})
#     else:print(the)

# for x in coll.find({'price': ''}):
#     coll.update({'asin':x['asin']},{'$set':{'status': random.randint(0,5)}})
# li = list(coll.find())

ha = pymg('haha','t1',port='108.61.203.110').find({'price': ''})
# print(len(list(ha)))
for x in ha:
    print(x['asin'])

