import scrapy

from seiya.spider.items import JobItem
class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ['www.lagou.com']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'user_trace_token=20181231143504-d303b028-5061-42c4-ad25-a29ad0a49c70; _ga=GA1.2.1669566407.1546238105; LGUID=20181231143504-35510f2f-0cc6-11e9-b484-525400f775ce; JSESSIONID=ABAAABAAAGFABEFC71F7B91CD4721367739E61616A8A63D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221682dc68606f1-047e2123dd27cf-b78173e-2073600-1682dc6860711e7%22%2C%22%24device_id%22%3A%221682dc68606f1-047e2123dd27cf-b78173e-2073600-1682dc6860711e7%22%7D; ab_test_random_num=0; _putrc=A638626F8A57886B123F89F2B170EADC; login=true; hasDeliver=0; _gat=1; LGSID=20190109185031-6233f2e2-13fc-11e9-b2ce-5254005c3644; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dmmjgx8Iyf5YTRFiHUsIoP1eCWqDkOTPoaeJ0ajv6bie%26ck%3D6685.1.148.384.149.384.141.229%26shh%3Dwww.baidu.com%26sht%3D50000022_hao_pg%26wd%3D%26eqid%3De545858000030ce1000000065c35d1f4; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1546238105,1546600835,1547031029; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B70807; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; gate_login_token=fd922efc6a849be6bfe5846638db6c6c33a1454c8935e66668ecb387c011c75f; _gid=GA1.2.1993530238.1547031036; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_recjob; SEARCH_ID=a9f03ae0a05c4a6ea4c837a45d7fbab0; LGRID=20190109185136-891a6642-13fc-11e9-b2ce-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1547031094',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
    

    def start_requests(self):
        #urls = ['https://www.lagou.com/zhaopin/{}/'.format(i) for i in range(1,16)]
        urls = ['https://www.lagou.com/zhaopin/{}/'.format(i) for i in range(16,31)]
        for i, url in enumerate(urls):
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers,)

    def parse(self, response):
        for job in response.css('ul.item_con_list li'):
            title = job.css('div.list_item_top div.p_top h3::text').extract_first()
            city = job.css('div.list_item_top div.p_top em::text').extract_first()
            salary = job.css('div.list_item_top div.p_bot span::text').extract_first()
            experience, education = job.css('div.list_item_top div.p_bot div.li_b_l::text').re(r'(.+)\s/\s(.+)\s')
            tags = job.css('div.list_item_bot div.li_b_l span::text').extract()
            company = job.css('div.list_item_top div.company_name a::text').extract_first()
            yield JobItem({
                'title': title,
                'city': city,
                'salary': salary,
                'experience': experience,
                'education': education,
                'tags': tags,
                'company': company
                })
