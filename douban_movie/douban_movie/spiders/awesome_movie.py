# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban_movie.items import MovieItem


class AwesomeMovieSpider(CrawlSpider):
    name = 'awesome-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091/']


    links = LinkExtractor(allow=r'https://movie.douban.com/subject/\d+/.*subject-page')
    rules = (
        Rule(links, callback='parse_movie_item', follow=True),
    )

    def parse_movie_item(self, response):
        item = MovieItem()
        item['url'] = response.url
        item['name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first() 
        item['summary'] = ' '.join(response.xpath('//span[@property="v:summary"]/text()').extract())
        item['score'] = response.xpath('//strong[@property="v:average"]/text()').extract_first() 

        return item

    def parse_start_url(self, response):
        yield self.parse_movie_item(response)
