import csv
import os
import re
import zipfile
from datetime import datetime
from typing import List, Dict, Union, TYPE_CHECKING, Optional, Tuple

import requests
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from transliterate import translit
from twisted.internet import reactor
from unidecode import unidecode

from train_wiser.backend.utils.file_operations import remove_file
from train_wiser.backend.utils.log import get_logger
from train_wiser.backend.utils.run_info_utils import is_race_of_relevant_type, str_time_to_seconds, \
    is_race_distance_of_relevant_type, round_race_distance

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
        event_items = response.xpath('//div[@class="event-list-item"]')
        for event in event_items:
            parsed_event = self.parse_event(event, response)
            if parsed_event:
                yield parsed_event

    def parse_event(self, event, response: 'Response'):
        race_date = event.css('.event-item-date::text').get().strip()
        formatted_race_date = datetime.strptime(race_date, "%d.%m.%Y.").date()
        event_name = unidecode(event.css('.event-item-name::text').get().
                               replace('\r', '').replace('\n', '').replace('"', '').replace('?', '').strip())
        if not is_race_of_relevant_type(event_name):
            return

        results_ref = event.css(".event-list-item-results a::attr(href)").get()

        if results_ref:
            race_names_and_dist = self._parse_race_names_and_dist(response, event)
            return scrapy.Request(url=response.urljoin(results_ref), callback=self.download_event_results,
                                  cb_kwargs={'event_name': event_name,
                                             'race_date': formatted_race_date,
                                             'race_names_and_dist': race_names_and_dist})
        else:
            LOGGER.debug(f"URL with results cannot be found for the event {event_name}.")
            return

    def _parse_race_names_and_dist(self, response, event) -> Dict[str, float]:
        event_link = event.css('a[href^="/events/"]::attr(href)').get()
        response_with_event = requests.get(url=response.urljoin(event_link))
        html_string = response_with_event.content.decode('utf-8')
        meta_description_content = re.search(
            r'<meta\sproperty="og:description"\s+content="Догађај се састоји од следећих трка: ([^"]*)"\s*/?>',
            html_string)
        race_names_and_dist_list: List[Tuple[str, str]] = re.findall(r"([\w\s.]+) \(([\w.]+)\skm\)",
                                                                     meta_description_content.group(1))
        race_names_and_dist: Dict[str, float] = dict()
        for name_dest_tuple in race_names_and_dist_list:
            race_names_and_dist[name_dest_tuple[0].strip()] = float(name_dest_tuple[1])

        return race_names_and_dist

    def download_event_results(self, response: 'Response', event_name: str, race_date: str,
                               race_names_and_dist: Dict[str, float]):
        download_link = response.css('a[href*="/_download-detailed-results/"]::attr(href)').get()
        if download_link:
            download_url = response.urljoin(download_link)
            return scrapy.Request(url=download_url, callback=self.parse_zip_results,
                                  cb_kwargs={'event_name': event_name,
                                             'race_date': race_date,
                                             'race_names_and_dist': race_names_and_dist})

    def parse_zip_results(self, response: 'Response', event_name: str, race_date: str,
                          race_names_and_dist: Dict[str, float]):
        if response.headers.get('Content-Type') == b'application/zip':
            csv_files = self.extract_zip_files_with_results(response, event_name)
            for csv_file in csv_files:
                race_name = unidecode(os.path.splitext(os.path.basename(csv_file))[0])
                try:
                    race_distance = race_names_and_dist[race_name]  # self.determine_race_distance(csv_file)
                    if not is_race_distance_of_relevant_type(race_distance):
                        LOGGER.debug(f"Race {race_name} has distance {race_distance} that is not relevant "
                                     f"for ML training. Proceeding with excluding this race from results.")
                        return
                    if not is_race_of_relevant_type(race_name):
                        return
                    participants_results = self.parse_csv_results(csv_file)
                    race_name = f"{event_name}, {race_name}"
                    race_results_json = {'participants_results': participants_results,
                                         'race_name': race_name,
                                         'race_distance': round_race_distance(race_distance),
                                         'race_date': race_date}
                    remove_file(csv_file)
                    yield race_results_json
                except KeyError:
                    LOGGER.debug(f"Race with name '{race_name}' not available in the dictionary "
                                 f"(race_name -> race_distance): {race_names_and_dist}")
        else:
            raise AttributeError(f"Response is not a ZIP file: {response.url}")

    def extract_zip_files_with_results(self, response: 'Response', race_name: str):
        results_path = os.path.join('../../../training_data', 'trka_rs_csv_results', f'{race_name}')
        os.makedirs(results_path, exist_ok=True)
        results_zip_path = f'{results_path}.zip'

        with open(results_zip_path, 'wb+') as f:
            f.write(response.body)
        with zipfile.ZipFile(results_zip_path, 'r') as zip_ref:
            zip_ref.extractall(results_path)
        remove_file(results_zip_path)
        csv_files = [os.path.join(results_path, csv_file) for csv_file in os.listdir(results_path)
                     if csv_file.endswith('.csv')]

        return csv_files

    def parse_csv_results(self, csv_filepath: str) -> Optional[List[Dict[str, Union[str, float]]]]:
        expected_header = ['rank', 'number', 'first_name', 'last_name', 'gender', 'birth_year',
                           'club', 'city', 'country', 'chip_time', 'gun_time', 'status']

        # Columns to extract
        columns_to_extract = ['first_name', 'last_name', 'gun_time', 'status']

        final_result_list: List[Dict] = []
        with open(csv_filepath, newline='', encoding='UTF-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Header check
            if reader.fieldnames != expected_header:
                raise ValueError("The header of the CSV file is not in the expected format.")

            for runner_result_row in reader:
                # Extracting only the specified columns
                runner_result_dict = {k: runner_result_row[k] for k in columns_to_extract}
                runner_status = runner_result_dict['status'].strip().lower()
                if runner_status == 'ok':
                    gun_time = str_time_to_seconds(runner_result_dict['gun_time'])
                    if not gun_time:
                        return
                    runner_name = f"{runner_result_dict['first_name']}{runner_result_dict['last_name']}"
                    runner_name = translit(runner_name, 'sr', reversed=True).lower().replace(' ', '')

                    final_result_list.append({
                        'runner_name': runner_name,
                        'total_time': gun_time,
                        'runner_status': runner_status
                    })

        return final_result_list

    def determine_race_distance(self, csv_filename: str) -> float:
        # If race distance is None, race is of not relevant type or distance
        csv_filename = translit(csv_filename, 'sr', reversed=True).lower().replace(' ', '')
        race_distance = None
        if re.search(r'([^0-9]|\b)10km|frtalj', csv_filename):
            race_distance = 10
        elif re.search(r'([^0-9]|\b)7km', csv_filename):
            race_distance = 7
        elif re.search(r'halfmarathon|polumaraton|([^0-9]|\b)21km', csv_filename):
            race_distance = 21.1
        elif re.search(r'minimarathon|minimaraton|([^0-9]|\b)5km', csv_filename):
            race_distance = 5
        elif re.search(r'marathon|maraton|([^0-9]|\b)42km', csv_filename):
            race_distance = 42.2

        return race_distance


# SCRAPY_LOG_FILE = 'scrapy_trka_rs_log.txt'
# configure_logging({'LOG_FILE': SCRAPY_LOG_FILE})

configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
crawler_runner = CrawlerRunner(
    settings={
        "FEEDS": {
            "../../../training_data/trka_rs_race_results.json": {"format": "json"},
        },
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_EXPORT_INDENT": 4,
    }
)

d = crawler_runner.crawl(TrkaRsSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the crawling is finished
