# -*- coding: utf-8 -*-
import scrapy
from JD.items import JdItem
from scrapy.http import Request
import requests
import json
import re
class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['jd.com']
    # start_urls = ['https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&page=1']
    def start_requests(self):
        ua = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }
        yield Request("https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&page=1",headers=ua)

    def parse(self, response):
        item = JdItem()
        url = response.xpath("//div[@class='p-img']/a/@href").extract()
        # print(url)
        for this_url in url:
            if this_url.startswith("https",0,5):
                yield Request(this_url,callback=self.next_parse)
            else:
                yield Request("https:"+this_url,callback=self.next_parse)
        for i in range(3,200,2):
            next_url = "https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&page={}".format(i,i+55)
            yield Request(next_url,callback = self.parse)

    def next_parse(self,response):
        item = JdItem()
        try:
            item["url"] = response.url
            item["name"] = response.xpath('//div[@class="p-info lh"]/div[@class="p-name"]/text()').extract()
            item["store"] = response.xpath('//div[@class="name"]/a/text()').extract()
            pat = "//item.jd.com/(.*?).html"
            shop_id = re.compile(pat).findall(item["url"])[0]
            response1 = requests.get("https://p.3.cn/prices/mgets?callback=jQuery7879290&type=1&area=1_72_2799_0&pdtk=&pduid=719435848&pdpin=&pin=null&pdbp=0&skuIds=J_{}%2CJ_19659646005%2CJ_42646006588%2CJ_4741808%2CJ_33239063849%2CJ_33341525798%2CJ_3494451%2CJ_797802%2CJ_37652171093&ext=11100000&source=item-pc".format(shop_id))
            data1 = response1.text
            price = data1[data1.index("["):data1.rindex("]")+1]
            p = json.loads(price)
            item["price"] = p[0]["p"]
            response2 =requests.get("https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}&callback=jQuery2538049&_=1559982177443".format(shop_id))
            data2 = response2.text
            comment = data2[data2.find("["):data2.rfind("]")+1]
            c = json.loads(comment)
            item["comment"] = c[0]["CommentCountStr"]
            item["good_comment"] = c[0]["GoodRateShow"]
            yield item
        except Exception as e:
            print(e)


