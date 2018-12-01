# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Repository, engine


class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.strptime(item['update_time'][:-1],'%Y-%m-%dT%H:%M:%S')
        # '1,000'转化为1000
        item['commits'] = int(item['commits'].replace(',',''))
        item['branches'] = int(item['branches'].replace(',',''))
        item['releases'] = int(item['releases'].replace(',',''))

        # 根据item构造Repository对象添加到数据库session中
        self.session.add(Repository(**item))
        return item

    def open_spider(self, spider):
        # 爬虫开启的时候，创建数据库的session
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        # 爬虫关闭的时间，提交数据库session, 然后关闭
        self.session.commit()
        self.session.close()
