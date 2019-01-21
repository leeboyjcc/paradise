import json

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


results = []

def parse(response):
    for comment in response.css('div.comment-list-item'):
        result = {}
        result['username'] = comment.xpath('.//div[@class="user-username"]/a/text()').re_first(r'\s*(\S*)\s*')
        result['content'] = comment.xpath('.//div[contains(@class,"comment-item-content")]/p/text()').extract_first()
        results.append(result)

def has_next_page(response):
    #next_page = response.xpath('//div[@id="question"]/div[@class="pagination-container"]/ul[@class="pagination"]/li[@class="disabled"]').extract()
    #print(len(response.xpath('//div[@id="questions"]/div[@class="pagination-container"]/ul[@class="pagination"]')))
    #print(response.xpath('//div[@id="questions"]/div[@class="pagination-container"]/ul[@class="pagination"]'))
    #print(response.xpath('//div[@id="questions"]/div[@class="pagination-container"]/ul[@class="pagination"]/li[7]').extract())
    #print(response.xpath('//div[@id="questions"]/div[@class="pagination-container"]/ul[@class="pagination"]/li[contains(@class,"disabled")]').extract())
    next_page = response.xpath('//div[@id="questions"]/div[@class="pagination-container"]/ul[@class="pagination"]/li[contains(@class,"disabled")]/a/text()').extract_first()
    if next_page == '下一页':
        return False
    else:
        return True

def goto_next_page(driver):
    #driver.find_element_by_xpath('//ul[@class="pagination"]/li[@class="next-page"]/a').click()
    driver.find_element_by_xpath('//*[@id="comments"]/div/div[4]/ul/li[7]/a').click()

def wait_page_return(driver, page):
    print(page)
    WebDriverWait(driver,30).until(EC.text_to_be_present_in_element(
        (By.XPATH, '//ul[@class="pagination"]/li[@class="active"]'),
        str(page)))

def spider():
    driver = webdriver.PhantomJS()
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:
        wait_page_return(driver, page)

        html = driver.page_source

        response = HtmlResponse(url=url, body=html.encode('utf8'))

        parse(response)

        if not has_next_page(response):
            break

        page += 1
        goto_next_page(driver)

    print(results)
    with open('/home/shiyanlou/comments.json','w') as f:
        f.write(json.dumps(results))


if __name__=='__main__':
    spider()
