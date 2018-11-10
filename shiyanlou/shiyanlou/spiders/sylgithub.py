# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlouItem

class SylgithubSpider(scrapy.Spider):
    name = 'sylgithub'

    @property
    def start_urls(self):
        url_tmpl = [
                'https://github.com/shiyanlou?tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoxOTo1NyswODowMM4FkpYw&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yNVQxMTozMTowNyswODowMM4Bxrsx&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yMFQxMzowMzo1MiswODowMM4BjkvL&tab=repositories'
                ]
        return url_tmpl

    def parse(self, response):
        for repos in response.css('div#user-repositories-list li'):
            item = ShiyanlouItem({
                'name': repos.css('div.d-inline-block.mb-1 h3 a::text').    re_first('\S+'),
                'update_time': repos.xpath('.//div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first()
                })
            yield item
