import requests
from lxml import html

class Bianti:

    def make_req(self,url):
        header = {}
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

        the_html = requests.get(url,headers=header).text
        response = html.fromstring(the_html)
        return response
    def parse(self, response):
        # img = response.xpath('//div[contains(@id, "imgTagWrapperId")]//img/@src')[0]
        # img = img.strip().replace('data:image/jpeg;base64,','')
        price = ''
        try:
            price = response.xpath('//*[@id="priceblock_ourprice"]/text()')[0]
        except:
            price = response.xpath('//*[@id="priceblock_saleprice"]/text()')[0]
        print(price)

    def new_page(self):
        try:
            select_bianti = response.xpath('//select/option/@value').extract()
            select_bianti_baseurl = 'https://www.amazon.com/dp/{}?th=1&psc=1'
            select_bianti_url = [select_bianti_baseurl.format(x.split(',')[1]) for x in select_bianti if len(x.split(','))==2 and int(x.split(',')[0]) in range(20)]
            for x in select_bianti_url:
                yield Request(x,meta={'price':price}
                              ,callback=self.page_bianti)
        except:
            print('-'*20)
            print('本页无select')


    def single(self,url):
        self.parse(self.make_req(url))

Bianti().single('https://www.amazon.com/dp/B01MR2CKOT')
