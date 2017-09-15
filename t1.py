name = "img_list"
allowed_domains = ["amazon.com"]
da  = list(pymg('amazon_asin','meirenyutan').find({'brand':'false'},{'_id':0}))
start_urls = ['https://www.amazon.com/dp/'+x['asin'] for x in da]
# start_urls = ['https://www.amazon.com/dp/B01MD0J84J']


def parse(self, response):
    # with open('/Users/user/Desktop/222.html','a') as f:
    #     f.write(response.body.decode())
    img = response.xpath('//div[contains(@id, "imgTagWrapperId")]//img/@src')[0].extract()
    img = img.strip().replace('data:image/jpeg;base64,','')
    asin = response.url.replace('https://www.amazon.com/dp/','')
    price = ''
    try:
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()')[0].extract().strip()
    except:
        price = response.xpath('//*[@id="priceblock_saleprice"]/text()')[0].extract().strip()



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

    def page_bianti(self,response,price):
        bianti_asin_list = response.xpath('//li[@class="swatchAvailable"]/@data-defaultasin')
        for each in bianti_asin_list:
            asin = each
            base = '//li[@data-defaultasin="{}"]//div[@class="tooltip"]//img/@src'
            img = response.xpath(base.format(asin))[0]
            img = img.strip().replace('data:image/jpeg;base64,','')
            print(asin)
