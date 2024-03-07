import os.path

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from src.backend.utils.file_operations import pdf_to_csv
from src.backend.utils.log import get_logger

LOGGER = get_logger(__name__)


class BgdMarathonSpider(scrapy.Spider):
    name = "bgd_marathon"
    allowed_domains = ["bgdmarathon.org"]

    def start_requests(self):
        urls = [
            "https://bgdmarathon.org/results/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_event_list)

    def parse_event_list(self, response):
        all_results_div = response.css(".results-tabs div").get()
        all_events_per_year_divs = all_results_div.css(".results-tab div").getall()

        for event_per_year_div in all_events_per_year_divs:
            event_year = event_per_year_div.css("::attr(id)")
            all_events_in_year_divs = event_per_year_div.css(".wp-block-file div").getall()
            self.parse_all_events_in_year(event_year, all_events_in_year_divs)

    def parse_all_events_in_year(self, event_year: str, all_events_in_year_divs):
        # Example:
        #  event_year: "2023"
        #  all_events_in_year_divs: ... <div class="wp-block-file">
        #    <a id="wp-block-file--media-046f4620-6f9d-4a8e-b03c-6f8498e434ad"
        #    href="https://bgdmarathon.org/wp-content/uploads/2023/04/Marathon2023.pdf" target="_blank"
        #    rel="noreferrernoopener">Belgrade Marathon 2023 &#8211; Marathon</a></div></div> ...
        for event in all_events_in_year_divs:
            results_in_pdf = event.css("a::attr(href)")
            self._check_name_of_pdf_results_file(event_year, results_in_pdf)
            yield scrapy.Request(url=results_in_pdf, callback=self.parse_pdf_race_results)

    def parse_pdf_race_results(self, response):
        if not response.headers['Content-Type'] == 'application/pdf':
            LOGGER.debug(f"Url {response.url} is not a link to pdf file.")
            return
        pdf_content = response.body
        pdf_name = os.path.basename(response.url)
        csv_name = f"{pdf_name.split('.')[:-1]}.csv"
        pdf_to_csv(pdf_content, csv_name)

    def _check_name_of_pdf_results_file(self, event_year, results_in_pdf):
        pdf_name = os.path.basename(results_in_pdf)
        if not pdf_name.endswith(".pdf"):
            LOGGER.debug("")
            return False
        if event_year not in pdf_name:
            LOGGER.debug("")
            return False


configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
crawler_runner = CrawlerRunner(
    settings={
        "FEEDS": {
            "runtrace_race_results.json": {"format": "json"},
        },
    }
)

d = crawler_runner.crawl(BgdMarathonSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the crawling is finished
