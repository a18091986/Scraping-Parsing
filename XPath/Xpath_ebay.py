from lxml import html
import requests
from pprint import pprint

url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=iphone&_sacat=0'
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

items = dom.xpath("//li[contains(@class,'s-item')]")

list_items = []
for item in items[1:]:
    item_info = {}
    name = item.xpath(".//h3[@class='s-item__title']/text()")
    link = item.xpath(".//h3[@class='s-item__title']/../@href")
    price = item.xpath(".//span[@class='s-item__price']//text()")
    review = item.xpath(".//div[@class='s-item__reviews']/a/@href")


    item_info['name'] = name
    item_info['link'] = link
    item_info['price'] = price
    item_info['review'] = review
    list_items.append(item_info)

pprint(list_items)