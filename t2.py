import requests
header = {}
header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'


url = 'https://www.amazon.com/dp/B01MR2CKOT'
the_html = requests.get(url,headers=header).text
print(the_html)
