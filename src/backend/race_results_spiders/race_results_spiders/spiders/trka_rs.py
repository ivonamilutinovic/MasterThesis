import os
import zipfile
from typing import Optional, TYPE_CHECKING

import scrapy
from django.http import FileResponse
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from src.backend.utils.log import get_logger
from src.backend.utils.run_info_utils import str_time_to_seconds, RaceInfoEnum

if TYPE_CHECKING:
    from scrapy.http.response import Response

LOGGER = get_logger(__name__)


class TrkaRsSpider(scrapy.Spider):
    name = "trka_rs"
    allowed_domains = ["trka.rs"]

    def start_requests(self):
        urls = [
            "https://trka.rs/events/past/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_event_list)

    def parse_event_list(self, response: 'Response'):
        for event in response.css('.event-item'):
            self.parse_event(event, response)

    def parse_event(self, event, response: 'Response'):
        event_id = self.parse_event_id(event)
        date = response.css('.event-item-date::text').get()
        race_name = response.css('.event-item-name::text').get()

        # Finding the dropdown menu associated with the current event-item div
        dropdown_menu = event.xpath(
            './following-sibling::div[@class="event-list-item-results"]/p/div[@class="btn-group"]/ul[@class="dropdown-menu"]')

        # Extracting the first href attribute from the dropdown menu
        first_results_link = dropdown_menu.css('li:first-child a::attr(href)').get()
        if first_results_link:
            yield scrapy.Request(url=response.urljoin(first_results_link), callback=self.get_event_results)
        else:
            raise ValueError(f"URL with results cannot be found for the race {race_name}")

    def get_event_results(self, response: 'Response'):
        self.download_event_results(response)

    def download_event_results(self, response: 'Response'):
        download_link = response.css('a[href*="/_download-detailed-results/"]::attr(href)').get()
        if download_link:
            download_url = response.urljoin(download_link)
            yield scrapy.Request(url=download_url, callback=self.save_and_parse_zip_results)

    def save_and_parse_zip_results(self, event_id: int, response: 'Response'):
        if isinstance(response, FileResponse) and response.headers.get('Content-Type') == b'application/zip':
            results_path = os.path.join('training_data', f'results_{event_id}')
            results_zip_path = f'{results_path}.zip'
            with open(results_zip_path, 'wb') as f:
                f.write(response.body)
            with zipfile.ZipFile(results_zip_path, 'r') as zip_ref:
                zip_ref.extractall(results_path)
            csv_files = [csv_file for csv_file in os.listdir(results_path) if csv_file.endswith('.csv')]
            for csv_file in csv_files:
                race_name = os.path.splitext(csv_file)
        else:
            raise AttributeError(f"Response is not a ZIP file: {response.url}")

    def parse_csv_results(self, csv_filename):
        # TODO: Implementation
        pass


# SCRAPY_LOG_FILE = 'scrapy_runtrace_log.txt'
# configure_logging({'LOG_FILE': SCRAPY_LOG_FILE})

configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
crawler_runner = CrawlerRunner(
    settings={
        "FEEDS": {
            "trka_rs_race_results.json": {"format": "json"},
        },
    }
)

d = crawler_runner.crawl(TrkaRsSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the crawling is finished

