from lxml import html
import re

import requests




def get_page_url(the_html,page):
    next_page_url = html.fromstring(the_html).xpath('//*[@id="pagnNextLink"]/@href')[0]
    # url参数
    # fst = re.compile(r'fst=(.+)&page').search(next_page_url).group(1)  fst={fst}&
    keywords = re.compile(r'keywords=(.+)&ie').search(next_page_url).group(1)
    rh = re.compile(r'rh=(.+)&page').search(next_page_url).group(1)
    search_root = 'https://www.amazon.com/s/'
    page_url = search_root+'ref=sr_pg_{page}?rh={rh}&page={page}&keywords={keywords}&ie=UTF8'

    format_page = page_url.format(page=page,rh=rh,keywords=keywords)
    return format_page



def get_url_page_list(url):
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    web_html = requests.get(url,headers=header).text
    try:
        page_num = html.fromstring(web_html).xpath('//*[@id="pagn"]/span[last()-1]/text()')[0]
        print(page_num)
        url_page_list = [get_page_url(web_html,x) for x in range(1,int(page_num)+1)]
        print(url)
        print('获取页数成功')
    except:
        print(url)
        print('只有一页')
        url_page_list = [url]
    return url_page_list
# web_html = get_url_page_list('https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=funny+t+shirt')
# print(web_html)


