import json
import os
from collections import defaultdict
from typing import List, Union, Dict

from unidecode import unidecode

from src.backend.utils.log import get_logger
from src.backend.utils.run_info_utils import FINISHED_RACE_STATUS, SUCCESS_RACE_STATUS

TRAINING_DATA_DIR = 'training_data'
JSON_DATA_FOR_TRAINING = 'prepared_race_results.json'

LOGGER = get_logger(__name__)


def prepare_data_for_training():
    results_per_runner_dict = defaultdict(list)
    rearrange_results_per_runner(os.path.join(TRAINING_DATA_DIR, 'runtrace_race_results.json'), results_per_runner_dict)
    rearrange_results_per_runner(os.path.join(TRAINING_DATA_DIR, 'trka_rs_race_results.json'), results_per_runner_dict)
    rearrange_results_per_runner(os.path.join(TRAINING_DATA_DIR, 'bgd_marathon_race_results.json'),
                                 results_per_runner_dict)
    write_results_in_json(results_per_runner_dict)


def rearrange_results_per_runner(json_file: str, results_per_runner_dict: Dict) -> None:
    with open(json_file, 'r', encoding='utf-8') as f:
        results_per_race_dict = json.load(f)

    for race in results_per_race_dict:
        runners_results: List[Dict[str, Union[str, int]]] = race['participants_results']
        race_name: str = race['race_name']
        race_distance: float = race['race_distance']
        race_date: str = race['race_date']
        if not runners_results:
            LOGGER.debug(f"Race {race_name} did not have any participants.")
            continue
        for runner_result_dict in runners_results:
            runner_name: str = unidecode(runner_result_dict['runner_name']).replace(' ', '').lower()
            total_time: int = runner_result_dict['total_time']
            runner_status: str = runner_result_dict['runner_status'].strip().lower()
            if runner_status not in {FINISHED_RACE_STATUS, SUCCESS_RACE_STATUS}:
                raise ValueError(f"Runner status should be set to 'finished'. Instead it is {runner_status}.")
            results_per_runner_dict[runner_name].append({'race_name': race_name,
                                                         'race_date': race_date,
                                                         'race_distance': race_distance,
                                                         'total_time': total_time})


def write_results_in_json(results_per_runner_dict):
    output_json = os.path.join(TRAINING_DATA_DIR, JSON_DATA_FOR_TRAINING)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results_per_runner_dict, f, indent=4, ensure_ascii=False)
