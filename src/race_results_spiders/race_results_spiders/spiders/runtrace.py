import scrapy


class RuntraceSpider(scrapy.Spider):
    name = "runtrace"
    allowed_domains = ["runtrace.net"]
    start_urls = ["https://runtrace.net"]

    def parse(self, response):
        pass
