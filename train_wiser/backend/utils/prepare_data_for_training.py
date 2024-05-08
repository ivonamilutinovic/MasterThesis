import json
import os
from datetime import datetime
from typing import List, Union, Dict

from unidecode import unidecode

from train_wiser.backend.utils.log import get_logger
from train_wiser.backend.utils.run_info_utils import FINISHED_RACE_STATUS, SUCCESS_RACE_STATUS

TRAINING_DATA_DIR = 'training_data'
MERGED_RESULTS = 'merged_results1.json'
GROUPED_RACE_RESULTS = 'race_results.json'
RACE_RESULTS = 'race_results.json'
RACE_RESULTS_GROUPED_PER_RACE = 'race_results_grouped_per_race.json'
RACE_RESULTS_FOR_21K = 'race_results_for_21k.json'



LOGGER = get_logger(__name__)


def merge_all_race_results():
    results_per_runner_dict = dict()
    results_per_runner_grouped_per_race_dict = dict()
    rearrange_results_per_runner(os.path.join(TRAINING_DATA_DIR, 'runtrace_race_results.json'),
                                 results_per_runner_dict, results_per_runner_grouped_per_race_dict)
    rearrange_results_per_runner(os.path.join(TRAINING_DATA_DIR, 'trka_rs_race_results.json'),
                                 results_per_runner_dict, results_per_runner_grouped_per_race_dict)
    rearrange_results_per_runner(os.path.join(TRAINING_DATA_DIR, 'bgd_marathon_race_results.json'),
                                 results_per_runner_dict, results_per_runner_grouped_per_race_dict)
    write_results_in_json(results_per_runner_dict, results_per_runner_grouped_per_race_dict)


def rearrange_results_per_runner_1(json_file: str, results_per_runner_dict: Dict) -> None:
    with open(json_file, 'r', encoding='utf-8') as f:
        results_per_race_dict = json.load(f)

    for race in results_per_race_dict:
        runners_results: List[Dict[str, Union[str, int]]] = race['participants_results']
        race_name: str = race['race_name']
        race_distance: float = race['race_distance']
        race_date: str = race['race_date']
        race_date_int = date_to_days(race_date)
        if not runners_results:
            LOGGER.debug(f"Race {race_name} did not have any participants.")
            continue
        for runner_result_dict in runners_results:
            runner_name: str = unidecode(runner_result_dict['runner_name']).replace(' ', '').lower()
            total_time: int = runner_result_dict['total_time']
            runner_status: str = runner_result_dict['runner_status'].strip().lower()
            if runner_status not in {FINISHED_RACE_STATUS, SUCCESS_RACE_STATUS}:
                raise ValueError(f"Runner status should be set to 'finished'. Instead it is {runner_status}.")
            runner = results_per_runner_dict.get(runner_name, None)
            if runner is None:
                results_per_runner_dict[runner_name] = {race_distance: [{'race_name': race_name,
                                                                         'race_date': race_date,
                                                                         'race_date_int': race_date_int,
                                                                         'race_distance': race_distance,
                                                                         'total_time': total_time}]}
            else:
                races_with_dist_for_runner = runner.get(race_distance, None)
                if races_with_dist_for_runner:
                    runner[race_distance].append({'race_name': race_name,
                                                  'race_date': race_date,
                                                  'race_date_int': race_date_int,
                                                  'race_distance': race_distance,
                                                  'total_time': total_time})
                else:
                    runner[race_distance] = [{'race_name': race_name,
                                              'race_date': race_date,
                                              'race_date_int': race_date_int,
                                              'race_distance': race_distance,
                                              'total_time': total_time}]


def rearrange_results_per_runner(json_file: str, results_per_runner_dict: Dict,
                                 results_per_runner_grouped_per_race_dict: Dict) -> None:
    with open(json_file, 'r', encoding='utf-8') as f:
        results_per_race_dict = json.load(f)

    for race in results_per_race_dict:
        runners_results: List[Dict[str, Union[str, int]]] = race['participants_results']
        race_name: str = race['race_name']
        race_distance: float = race['race_distance']
        race_date: str = race['race_date']
        race_date_int = date_to_days(race_date)
        if not runners_results:
            LOGGER.debug(f"Race {race_name} did not have any participants.")
            continue
        for runner_result_dict in runners_results:
            runner_name: str = unidecode(runner_result_dict['runner_name']).replace(' ', '').lower()
            total_time: int = runner_result_dict['total_time']
            runner_status: str = runner_result_dict['runner_status'].strip().lower()
            if runner_status not in {FINISHED_RACE_STATUS, SUCCESS_RACE_STATUS}:
                raise ValueError(f"Runner status should be set to 'finished'. Instead it is {runner_status}.")
            runner = results_per_runner_dict.get(runner_name, None)

            if runner is None:
                results_per_runner_dict[runner_name] = [{'race_name': race_name,
                                                         'race_date': race_date,
                                                         'race_date_int': race_date_int,
                                                         'race_distance': race_distance,
                                                         'total_time': total_time}]
            else:
                runner.append({'race_name': race_name,
                               'race_date': race_date,
                               'race_date_int': race_date_int,
                               'race_distance': race_distance,
                               'total_time': total_time})

            runner_with_grouped_races = results_per_runner_grouped_per_race_dict.get(runner_name, None)
            if runner_with_grouped_races is None:
                results_per_runner_grouped_per_race_dict[runner_name] = {race_distance: [{'race_name': race_name,
                                                                         'race_date': race_date,
                                                                         'race_date_int': race_date_int,
                                                                         'race_distance': race_distance,
                                                                         'total_time': total_time}]}
            else:
                races_with_dist_for_runner = runner_with_grouped_races.get(race_distance, None)
                if races_with_dist_for_runner:
                    runner_with_grouped_races[race_distance].append({'race_name': race_name,
                                                                     'race_date': race_date,
                                                                     'race_date_int': race_date_int,
                                                                     'race_distance': race_distance,
                                                                     'total_time': total_time})
                else:
                    runner_with_grouped_races[race_distance] = [{'race_name': race_name,
                                                                 'race_date': race_date,
                                                                 'race_date_int': race_date_int,
                                                                 'race_distance': race_distance,
                                                                 'total_time': total_time}]


def date_to_days(date_str: str, start_date_str: str = "1990-01-01") -> int:
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start_date_str, date_format)
    current_date = datetime.strptime(date_str, date_format)
    return (current_date - start_date).days


def write_results_in_json(results_per_runner_dict: Dict, results_per_runner_grouped_per_race_dict: Dict):
    for runner_name, runner_races in results_per_runner_dict.items():
        runner_races.sort(key=lambda x: x['race_date_int'])

    output_json = os.path.join(TRAINING_DATA_DIR, RACE_RESULTS)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results_per_runner_dict, f, indent=4, ensure_ascii=False)

    output_json = os.path.join(TRAINING_DATA_DIR, RACE_RESULTS_GROUPED_PER_RACE)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results_per_runner_grouped_per_race_dict, f, indent=4, ensure_ascii=False)

# def prepare_data_for_training():
#     merged_results = os.path.join(TRAINING_DATA_DIR, JSON_DATA_FOR_TRAINING)
#     with open(merged_results, 'r', encoding='utf-8') as f:
#         results_per_runner = json.load(f)
