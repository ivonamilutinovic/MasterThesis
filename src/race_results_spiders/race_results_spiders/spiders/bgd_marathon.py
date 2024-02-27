import scrapy


class BgdMarathonSpider(scrapy.Spider):
    name = "bgd_marathon"
    allowed_domains = ["bgdmarathon.org"]
    start_urls = ["https://bgdmarathon.org"]

    def parse(self, response):
        pass
