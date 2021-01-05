import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import json

temp_list = []

class JobsSpider(CrawlSpider):
    name = 'jobs'
    allowed_domains = ['www.concordia.ca']
    start_urls = ['http://www.concordia.ca/']

    def __init__(self, foo=None, *args, **kwargs):
        super(JobsSpider, self).__init__(*args, **kwargs)
        # Do something with foo
        self.i = 0
        self.temp_list = []

    # def parse(self, response):
    #     pass

    rules = [Rule(LinkExtractor(), callback='parse_item', follow=True)]

    def parse_item(self, response):
        self.temp_list.append(response.url)
        json.dump(self.temp_list, open("temp_list.json", "w", encoding="utf−8"))

        # f = open('filename.json', 'a')
        #
        # f.write(response.url+'\n')
        # f.close()

        self.i=self.i+1
        # page = response.url.split("/")[-1]
        # filename = f'{page}'
        with open(str(self.i)+".html", 'wb') as f:
            f.write(response.body)
        #return self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True)
        # for next_page in response.css('a::attr(href)'):
        # 
        #     yield response.follow(next_page, self.parse_item)





