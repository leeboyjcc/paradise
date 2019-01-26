# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlouItem

class SylgithubSpider(scrapy.Spider):
    name = 'sylgithub'
    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for repos in response.css('div#user-repositories-list li'):
            item = ShiyanlouItem()
            item['name'] = repos.css('div.d-inline-block.mb-1 h3 a::text').re_first('\S+')
            item['update_time'] = repos.xpath('.//div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first()

            # 构造每个仓库自己的页面,获取提交、分支、发布版本的数量
            request = response.follow(repos.css('div.d-inline-block.mb-1 h3 a::attr(href)')[0], callback=self.parse_info)
            # 将未完成的item通过meta传入parse_info
            request.meta['item'] = item

            # 继续产生新的请求
            yield request


        # process next link
        next_page = None
        next_url = response.css('div.pagination a::attr(href)').extract()
        next_text = response.css('div.pagination a::text').extract()
        for l, t in zip(next_url, next_text):
            if t == 'Next':
                next_page = l
        # next_page为当前页面链接的下一个的页面，如果是最后一个页面则节点有链接且为Next
        # 的节点没有，也即next_page为None
        if next_page:
            # 产生新的Request，回调parse来处理
            yield response.follow(next_page, callback=self.parse)

    def parse_info(self, response):
        # 获取未构造完成的item
        item = response.meta['item']
        
        item['commits'] = response.xpath('//ul[@class="numbers-summary"]/li[1]').xpath('.//span/text()').re_first('[^\d]*(\d*)[^\d]*')
        item['branches'] = response.xpath('//ul[@class="numbers-summary"]/li[2]').xpath('.//span/text()').re_first('[^\d]*(\d*)[^\d]*')
        item['releases'] = response.xpath('//ul[@class="numbers-summary"]/li[3]').xpath('.//span/text()').re_first('[^\d]*(\d*)[^\d]*')

        # 返回构造完整的item 给pipeline处理
        yield item

