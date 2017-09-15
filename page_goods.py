from lxml import html
import requests

from bson.objectid import ObjectId

import settings

MONGO_URI = '108.61.203.110'
name = settings.NAME

import pymongo

def pymg(highest,collections,port=MONGO_URI):
    client = pymongo.MongoClient(port, 29999)
    zhihu = client[highest]
    collections = zhihu[collections]
    return collections

def get_price_img(xhtml1):
    title = 'title'
    store_name = 'store_name'
    price = ''
    # try:
    #     title = xhtml1.xpath('.//a/h2/text()')[0]
    #     # store_name = xhtml1.xpath('.//div[@class="a-row a-spacing-small"]/div[@class="a-row a-spacing-none"]/span[2]/text()')[0]
    #     price = [x for x in xhtml1.xpath('.//a/span/text()') if '$' in x][0]
    # except:
    #     pass
    img = xhtml1.xpath('.//div/a/img/@src')[0]

    asin = xhtml1.xpath('.//@data-asin')[0]
    data = {
        'asin': asin,
        'price': price,
        'img': img,
        'title': title,
        'store_name': store_name,
        'brand': 'false',
        'status': -2
    }
    if store_name.lower() in title.lower():
        data['brand'] = 'true'
    return data
def get_singel_page_goods(html1):
    result_list = html.fromstring(html1).xpath('//li[starts-with(@id,"result_")]')
    return result_list


# def get_list_url(url):

def down_one(data):
    url = data['urls']
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    the_html = requests.get(url,headers=header).text
    asins = [get_price_img(each) for each in get_singel_page_goods(the_html)]

    client = pymongo.MongoClient(MONGO_URI,29999)
    db = client['amazon_asin']
    coll = db[name]
    # print('开始插入数据库')
    # for x in asins:
    #     coll.update({'asin': x['asin']}, x, True)
    coll.insert_many(asins)

    url_coll = client['amazon_results_url'][name]
    url_coll.update({'_id': ObjectId(data['_id'])}, {'$set':{'status':4}})
    client.close()

    print('成功:',data['_id'])
# down_one('https://www.amazon.com/s/ref=sr_pg_2?rh=n%3A1055398%2Ck%3Amermaid+tail+blanket&page=2&keywords=mermaid+tail+blanket&ie=UTF8')
