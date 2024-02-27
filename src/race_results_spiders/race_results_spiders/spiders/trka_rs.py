import scrapy


class TrkaRsSpider(scrapy.Spider):
    name = "trka_rs"
    allowed_domains = ["trka.rs"]
    start_urls = ["https://trka.rs"]

    def parse(self, response):
        pass
