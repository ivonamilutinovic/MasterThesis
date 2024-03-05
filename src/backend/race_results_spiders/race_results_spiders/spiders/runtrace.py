from typing import Optional

import scrapy

from src.backend.utils.log import get_logger
from src.backend.utils.run_info_utils import str_time_to_seconds, RaceInfoEnum

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


LOGGER = get_logger(__name__)


class RuntraceSpider(scrapy.Spider):
    name = "runtrace"
    allowed_domains = ["runtrace.net"]

    def start_requests(self):
        urls = [
            "https://runtrace.net/?filters%5Bid_countries%5D=&filters%5Bstatus%5D=passed&filters%5Btype%5D="
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_event_list)

    def parse_event_list(self, response):
        # Extracts all href attributes from each 'a' element that has the title attribute;
        # These are references to race events
        all_events_references = response.css("a[title=Participants]::attr(href)").getall()

        for event_reference in all_events_references:
            yield scrapy.Request(response.urljoin(event_reference), self.parse_race_disciplines_per_event)

    def parse_race_disciplines_per_event(self, response):
        # Extracts all value attributes from option elements with dd-race-select class
        # These are race references within one event
        race_references = response.css(".dd-race-select option::attr(value)").getall()

        for race_reference in race_references:
            yield scrapy.Request(f"{response.url}?race_id={race_reference}&race_info=true", self.parse_race)

    def parse_race(self, response):
        # response.url example: 'https://runtrace.net/zemun2023?race_id=664&race_info=true'
        race_name = response.css("title::text").get()

        result_table = response.css("#results-table")

        # Race info field positions in the table
        avg_pace_field_pos = None
        total_time_field_pos = None
        # Selects <th> elements that are inside <tr> elements which are inside a <thead> element
        for i, column_name in enumerate(result_table.css("thead>tr>th")):
            column_name = column_name.css("::text").get()
            if column_name:
                column_name = column_name.strip().lower()

            if column_name == RaceInfoEnum.PACE.value:
                avg_pace_field_pos = i + 1
            elif column_name == RaceInfoEnum.TIME.value:
                total_time_field_pos = i + 1

        if avg_pace_field_pos is None or total_time_field_pos is None:
            LOGGER.debug(f"Pace or time not found for {race_name}. ")
            return None

        race_obj = {"participants": list()}

        race_distance = None
        for runner in result_table.css("tbody>tr"):
            runner_name = runner.css(".td-name::text").get().strip()  # todo: cyrillic, latin
            total_time = str_time_to_seconds(runner.css("td:nth-child({timePos})::text"
                                                        .format(timePos=total_time_field_pos)).get().strip())
            avg_pace = str_time_to_seconds(runner.css("td:nth-child({pacePos})::text"
                                                      .format(pacePos=avg_pace_field_pos)).get().strip())
            runner_status = runner.css(".js-status>.status::text").get().strip()

            if race_distance is None:
                race_distance = self.calculate_race_distance(runner_status, total_time, avg_pace)

            race_obj["participants"].append({"runner_name": runner_name,
                                             "total_time": total_time,
                                             "avg_pace": avg_pace,
                                             "runner_status": runner_status})

        race_obj["race_name"] = race_name
        race_obj["race_distance"] = race_distance

        return race_obj

    @staticmethod
    def calculate_race_distance(runner_status: str, total_time: int, avg_pace: int) -> Optional[float]:
        race_distance = None
        if runner_status.lower() == "finished" and total_time and avg_pace:
            race_distance = round(total_time / avg_pace, 3)
        return race_distance


# SCRAPY_LOG_FILE = 'scrapy_runtrace_log.txt'
# configure_logging({'LOG_FILE': SCRAPY_LOG_FILE})

configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
crawler_runner = CrawlerRunner(
    settings={
        "FEEDS": {
            "race_results.json": {"format": "json"},
        },
    }
)

d = crawler_runner.crawl(RuntraceSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the crawling is finished
