# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from seiya.db import engine, Session, JobModel
from seiya.spider.items import JobItem

class SeiyaPipeline(object):
    def open_spider(self, spider):
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()


    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            return self._process_job_item(item)
        else:
            return item


    def _process_job_item(self, item):
        city = item['city'].split('·')[0]
        m = re.search(r'(\d*)k-(\d*)k', item['salary'])
        if m:
            salary_lower, salary_upper = int(m.group(1)), int(m.group(2))
        else:
            salary_lower, salary_upper = 0, 0

        m = re.search(r'(\d+)-(\d+)', item['experience'])
        if m:
            experience_lower, experience_upper = int(m.group(1)), int(m.group(2))
        else:
            experience_lower, experience_upper = 0, 0

        tags = ' '.join(item['tags'])

        jobdata = JobModel(
            title=item['title'],
            city=city,
            salary_lower=salary_lower,
            salary_upper=salary_upper,
            experience_lower=experience_lower,
            experience_upper=experience_upper,
            education=item['education'],
            tags=tags,
            company=item['company']
            )

        self.session.add(jobdata)
        return item