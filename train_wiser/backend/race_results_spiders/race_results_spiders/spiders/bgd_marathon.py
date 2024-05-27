import csv
import json
import os.path
import re
from typing import List, Dict, Union, TYPE_CHECKING, Optional, Tuple

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from train_wiser.backend.utils.file_operations import pdf_to_csv, remove_file
from train_wiser.backend.utils.log import get_logger
from train_wiser.backend.utils.run_info_utils import is_race_of_relevant_type, str_time_to_seconds, SUCCESS_RACE_STATUS, \
    translate_to_unidecode_and_remove_spaces, translate_to_unidecode

if TYPE_CHECKING:
    from scrapy.http.response import Response


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
        all_events_per_year_divs = response.xpath(
            '//div[contains(concat(" ", normalize-space(@class), " "), " results-tab ")]')

        for event_per_year_div in all_events_per_year_divs:
            event_year = event_per_year_div.css("::attr(id)").get()
            all_events_in_year_divs = event_per_year_div.xpath('.//div[@class="wp-block-file"]')
            for result in self.parse_all_events_in_year(response, event_year, all_events_in_year_divs):
                yield result

    def parse_all_events_in_year(self, response, event_year: str, all_events_in_year_divs):
        # Example:
        #  event_year: "2023"
        #  all_events_in_year_divs: ... <div class="wp-block-file">
        #    <a id="wp-block-file--media-046f4620-6f9d-4a8e-b03c-6f8498e434ad"
        #    href="https://bgdmarathon.org/wp-content/uploads/2023/04/Marathon2023.pdf" target="_blank"
        #    rel="noreferrernoopener">Belgrade Marathon 2023 &#8211; Marathon</a></div></div> ...

        race_date_dict = self._load_race_date_dict()
        for i, event in enumerate(all_events_in_year_divs):
            results_in_pdf = event.css("a::attr(href)").get()
            yield scrapy.Request(url=response.urljoin(results_in_pdf), callback=self.parse_pdf_race_results,
                                 cb_kwargs={'event_year': event_year, 'race_date_dict': race_date_dict})

    def parse_pdf_race_results(self, response: 'Response', event_year: str, race_date_dict: Dict[str, str]):
        if response.headers.get('Content-Type') != b'application/pdf':
            raise AttributeError(f"URL {response.url} is not pdf file.")
        pdf_name = os.path.basename(response.url).split('/')[-1].lower()
        if not is_race_of_relevant_type(pdf_name) or not self.is_resulting_pdf_relevant(pdf_name):
            return
        pdf_content = response.body
        csv_name = f'{os.path.splitext(pdf_name)[0]}.csv'

        results_path = os.path.join('../../../training_data', 'bgd_marathon_csv_results', event_year)
        local_pdf_path = os.path.join(results_path, pdf_name)
        csv_path = os.path.join(results_path, csv_name)

        # Making pdf with result
        os.makedirs(results_path, exist_ok=True)
        with open(local_pdf_path, 'wb+') as pdf_file:
            pdf_file.write(pdf_content)

        pdf_to_csv(local_pdf_path, csv_path)

        participants_results, best_time = self.parse_csv_results(csv_path)
        if not participants_results or not best_time:
            return
        race_name = os.path.splitext(csv_name)[0]
        race_distance = self.determine_race_distance_from_pdf_name_and_results(
            pdf_name, best_time)
        if not race_distance:
            return
        race_date = race_date_dict.get(race_name, f'{event_year}-mm-dd')
        if not race_date.startswith(event_year):
            raise AttributeError(f"Year of the race should be {event_year}, instead, date is {race_date}.")
        race_results_json = {'participants_results': participants_results,
                             'race_name': race_name,
                             'race_distance': race_distance,
                             'race_date': race_date}
        remove_file(local_pdf_path)
        remove_file(csv_path)
        return race_results_json

    def parse_csv_results(self, csv_filepath: str) -> Tuple[Optional[List[Dict[str, Union[str, int]]]], int]:
        final_result_list: List[Dict] = list()
        name_regex_op1 = re.compile('([a-z]+(\s[a-z]+){1,2})(,\s[a-z\d]*){0,2}')
        name_regex_op2 = re.compile('\d+\.\s+\d+\s+([a-z\s]+)')
        chip_time_regex = r'(?:\d{1,2}\s?:){1,2}\d{1,2}'
        best_time = float('inf')
        with open(csv_filepath, newline='', encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            for runner_result_row in reader:
                if any(isinstance(element, str) and
                       element.lower().strip() in ['dns', 'dnf', 'dsq'] for element in runner_result_row):
                    continue
                time_results = list()
                for element in runner_result_row:
                    time_results_per_column = [time_result.replace(' ', '')
                                               for time_result in re.findall(chip_time_regex, element)]
                    time_results.extend(time_results_per_column)
                if not time_results:
                    continue
                total_time_str = max(time_results, key=str_time_to_seconds)
                total_time = str_time_to_seconds(total_time_str)
                best_time = min(best_time, total_time)

                runner_name = next((translate_to_unidecode_and_remove_spaces(element).split(',')[0]
                                    for element in runner_result_row
                                    if name_regex_op1.fullmatch(translate_to_unidecode(element))), None)
                if not runner_name:
                    runner_name = next((translate_to_unidecode_and_remove_spaces(
                        name_regex_op2.search(translate_to_unidecode(element)).group(1))
                                        for element in runner_result_row
                                        if name_regex_op2.fullmatch(translate_to_unidecode(element))), None)
                    if not runner_name:
                        continue

                final_result_list.append({
                    'runner_name': runner_name,
                    'total_time': total_time,
                    # 'total_time_str': total_time_str,
                    'runner_status': SUCCESS_RACE_STATUS,
                    # 'full_row': runner_result_row
                })
        if best_time == float('inf'):
            best_time = None
        return final_result_list, best_time

    def determine_race_distance_from_pdf_name_and_results(self, pdf_name: str,
                                                          best_time_on_race: int) -> Optional[float]:
        if '5k' in pdf_name:
            return 5
        elif '10k' in pdf_name:
            return 10
        elif 'zenska-trka' in pdf_name or 'zenskatrka' in pdf_name:
            return 7.7
        elif best_time_on_race > 6300:
            # If best time is bigger than 1h45min, it is supposed that marathon distance is in the results
            return 42
        elif best_time_on_race > 3000:
            # If best time is bigger than 50min, it is supposed that half-marathon distance is in the results
            return 21
        else:
            return None

    def is_resulting_pdf_relevant(self, pdf_name: str) -> bool:
        not_relevant_race_types = ['kategorije', 'category', 'gender']
        return not any(race_type in pdf_name.lower().strip() for race_type in not_relevant_race_types)

    def _load_race_date_dict(self):
        with open('../../../race_data/bgd_marathon_race_name_to_date.json', 'r', encoding='utf-8') as f:
            race_date_dict = json.load(f)
        return race_date_dict


SCRAPY_LOG_FILE = 'scrapy_bgd_marathon_log.txt'
configure_logging({'LOG_FILE': SCRAPY_LOG_FILE,
                   "LOG_FORMAT": "%(levelname)s: %(message)s",
                   "LOG_LEVEL": 'WARNING'})
crawler_runner = CrawlerRunner(
    settings={
        "FEEDS": {
            "../../../training_data/bgd_marathon_race_results.json": {"format": "json"},
        },
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_EXPORT_INDENT": 4,
    }
)

d = crawler_runner.crawl(BgdMarathonSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the crawling is finished
