# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        # client = MongoClient('localhost', 27017)
        # self.mongobase = client.vacancy3105
        pass

    def process_item(self, item, spider):
        print()
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary(item['salary'])
        ...
        ...

        ...

        # collection = self.mongobase[spider.name]
        # collection.insert_one(item)
        return item

    def process_salary(self, salary):
        print(salary)
        minv = 0
        maxv = 100
        cur = 'test'
        return minv, maxv, cur
