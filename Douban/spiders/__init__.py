# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import json

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["https://book.douban.com/"]
    start_urls = [
        "https://book.douban.com/latest/"
    ]

    def parse(self, response):
        book_list = []

        list = response.xpath('//*[@id="content"]/div/div[1]/ul/li')
        for li in list:
            book = {}
            book['pic'] = li.xpath('.//div[@class="media__img"]/a/img/@src').extract_first()
            book['title'] = li.xpath('.//div[@class="media__body"]/h2/a/text()').extract_first()
            book['abstract'] = li.xpath('.//div[@class="media__body"]/p[@class="subject-abstract color-gray"]/text()').extract_first()
            abs = li.xpath('.//div[@class="media__body"]/p[@class="subject-abstract color-gray"]/text()').extract_first()
            book['abstract'] = abs.replace('\n', '').replace('\r', '').replace(' ', '').split(r'/')
            book['ranking'] = li.xpath('.//div[@class="media__body"]/p[@class="clearfix w250"]/span[@class="font-small color-red fleft"]/text()').extract_first()
            book['price'] = li.xpath('.//div[@class="media__body"]/div[@class="clearfix w250 color-gray fleft"]/span[@class="buy-info"]/a/text()').extract_first().replace('\n', '').replace('\r', '').replace(' ', '').replace('纸质版', '')
            book_list.append(book)
        
        result = json.dumps(book_list, ensure_ascii=False)
        filename = "booklist.json"
        with open(filename, 'w') as f:
            # [f.write(str(book)) for book in book_list]
            f.write(str(result))