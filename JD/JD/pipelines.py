# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class JdPipeline(object):
    def __init__(self):
        self.count = 0
        self.db = pymysql.connect("localhost","root","123","python")
        self.cursor = self.db.cursor()




    def process_item(self, item, spider):
        try:
            self.count+=1
            sql = "insert into jdcomputer(name,store,price,comment,good_comment,url) values('{}','{}','{}','{}','{}','{}')".format(item["name"][0],item["store"][0],item["price"],item["comment"],item["good_comment"],item["url"])
            self.cursor.execute(sql)
            self.db.commit()
            print("------第{}次保存成功------".format(self.count))
        except Exception as e:
            print(e)
        # print(item["name"])
        # print(item["store"])
        # print(item["price"])
        # print(item["comment"])
        # print(item["good_comment"])
        # print(item["url"])


        return item

    def close_spider(self):
        self.cursor.close()
        self.db.close()

