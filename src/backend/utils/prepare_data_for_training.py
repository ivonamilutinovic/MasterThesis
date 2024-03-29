import json
import os
from collections import defaultdict
from typing import List, Union, Dict

from unidecode import unidecode

from src.backend.utils.run_info_utils import FINISHED_RACE_STATUS

TRAINING_DATA_DIR = 'training_data'


def prepare_data_for_training():
    reorder_runtrace_results(os.path.join(TRAINING_DATA_DIR, 'runtrace_race_results.json'))


def reorder_runtrace_results(json_file: str) -> None:
    results_per_runner_dict = defaultdict(list)
    with open(json_file, 'r', encoding='utf-8') as f:
        results_per_race_dict = json.load(f)

    for race in results_per_race_dict:
        runners_results: List[Dict[str, Union[str, int]]] = race['participants_results']
        race_name: str = race['race_name']
        race_distance: float = race['race_distance']
        race_date: str = race['race_date']
        for runner_result_dict in runners_results:
            runner_name: str = unidecode(runner_result_dict['runner_name'])
            total_time: int = runner_result_dict['total_time']
            avg_pace: int = runner_result_dict['avg_pace']
            runner_status: str = runner_result_dict['runner_status'].strip().lower()
            if runner_status.lower() == 'racing':
                raise RuntimeError(f"Runner {runner_name} has 'racing' status. Race {race_name},"
                                   f" distance {race_distance}.")
            if runner_status != FINISHED_RACE_STATUS:
                raise ValueError(f"Runner status should be set to 'finished'. Instead it is {runner_status}.")
            results_per_runner_dict[runner_name].append({'race_name': race_name,
                                                         'race_date': race_date,
                                                         'race_distance': race_distance,
                                                         'total_time': total_time,
                                                         'avg_pace': avg_pace})

    output_json = os.path.join(TRAINING_DATA_DIR, 'runtrace_race_results_prepared.json')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results_per_runner_dict, f, indent=4, ensure_ascii=False)
