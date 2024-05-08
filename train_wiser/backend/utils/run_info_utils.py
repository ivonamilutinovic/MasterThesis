import json
import math
import re
from enum import Enum
from typing import Optional, Union, Dict

from transliterate import translit
from unidecode import unidecode


class RaceInfoEnum(Enum):
    PACE = "tempo"
    TIME = "vreme"


FINISHED_RACE_STATUS = 'finished'
SUCCESS_RACE_STATUS = 'ok'


def is_race_of_relevant_type(race_name: str) -> bool:
    # Race name should be unidecoded
    not_relevant_race_types = ['trail', 'trejl', 'vertical', 'ocr', 'plivanje', 'swimming', 'tribalion', 'stafeta',
                               'stafetni', 'relay', 'nordijsko', 'hodanje', 'kros']
    return not any(race_type in race_name.lower() for race_type in not_relevant_race_types)


def round_race_distance(race_distance: float) -> Union[int, float]:
    if math.floor(race_distance) == 7:
        difference_to_7 = abs(race_distance - 7)
        difference_to_7_7 = abs(race_distance - 7.7)
        if difference_to_7 <= difference_to_7_7:
            race_distance = 7
        elif difference_to_7 > difference_to_7_7:
            race_distance = 7.7
    else:
        race_distance = math.floor(race_distance)

    return race_distance


def is_race_distance_of_relevant_type(race_distance: float) -> bool:
    relevant_distances = [5, 7, 7.7, 10, 21, 42]
    return round_race_distance(race_distance) in relevant_distances


def str_time_to_seconds(time_str: str) -> Optional[int]:
    time_str = time_str.strip()

    if not time_str:
        return None

    if re.fullmatch("(\d{1,2}:){1,2}\d{1,2}(.\d{1,2})?", time_str) is None:
        raise ValueError(f"{time_str} is in unexpected format.")

    time_tokens = time_str.split(":")

    seconds = 0
    multiply = 1
    for token in reversed(time_tokens):
        seconds += float(token) * multiply
        multiply *= 60

    return round(seconds)


def translate_to_unidecode(text: str):
    return unidecode(translit(text, 'sr', reversed=True).lower())


def translate_to_unidecode_and_remove_spaces(text: str):
    return unidecode(translit(text, 'sr', reversed=True).lower().replace(' ', ''))


def count_number_of_data() -> Dict[str, int]:
    json_bgd_path = 'training_data/bgd_marathon_race_results.json'
    json_trka_rs_path = 'training_data/trka_rs_race_results.json'
    json_runtrace_path = 'training_data/runtrace_race_results.json'
    race_results_grouped_per_race = 'training_data/race_results_grouped_per_race.json'

    with open(json_bgd_path, 'r', encoding='utf-8') as f:
        list_data_bgd = json.load(f)

    with open(json_trka_rs_path, 'r', encoding='utf-8') as f:
        list_data_trka_rs = json.load(f)

    with open(json_runtrace_path, 'r', encoding='utf-8') as f:
        list_data_runtrace = json.load(f)

    with open(race_results_grouped_per_race, 'r', encoding='utf-8') as f:
        all_results_per_runner = json.load(f)

    participants_results_len_bgd = 0
    participants_results_len_trka_rs = 0
    participants_results_len_runtrace = 0

    for race_data in list_data_bgd:
        participants_results_len_bgd += len(race_data['participants_results'])

    for race_data in list_data_trka_rs:
        participants_results_len_trka_rs += (len(race_data['participants_results'])
                                             if race_data['participants_results'] else 0)

    for race_data in list_data_runtrace:
        participants_results_len_runtrace += len(race_data['participants_results'])

    total_number_of_runner_race_results = (participants_results_len_bgd +
                                           participants_results_len_trka_rs +
                                           participants_results_len_runtrace)

    total_number_of_runners_with_race_results = len(all_results_per_runner.keys())

    avg_num_of_5k_per_runner = 0
    avg_num_of_7k_per_runner = 0
    avg_num_of_7_7k_per_runner = 0
    avg_num_of_10k_per_runner = 0
    avg_num_of_21k_per_runner = 0
    avg_num_of_42k_per_runner = 0

    num_of_runners_with_5k_races = 0
    num_of_runners_with_7k_races = 0
    num_of_runners_with_7_7k_races = 0
    num_of_runners_with_10k_races = 0
    num_of_runners_with_21k_races = 0
    num_of_runners_with_42k_races = 0

    for races in all_results_per_runner.values():
        if races.get('5', None):
            avg_num_of_5k_per_runner += len(races['5'])
            num_of_runners_with_5k_races += 1

        if races.get('7', None):
            avg_num_of_7k_per_runner += len(races['7'])
            num_of_runners_with_7k_races += 1

        if races.get('7.7', None):
            avg_num_of_7_7k_per_runner += len(races['7.7'])
            num_of_runners_with_7_7k_races += 1

        if races.get('10', None):
            avg_num_of_10k_per_runner += len(races['10'])
            num_of_runners_with_10k_races += 1

        if races.get('21', None):
            avg_num_of_21k_per_runner += len(races['21'])
            num_of_runners_with_21k_races += 1

        if races.get('42', None):
            avg_num_of_42k_per_runner += len(races['42'])
            num_of_runners_with_42k_races += 1

    avg_num_of_5k_per_runner = avg_num_of_5k_per_runner / num_of_runners_with_5k_races
    avg_num_of_7k_per_runner = avg_num_of_7k_per_runner / num_of_runners_with_7k_races
    avg_num_of_7_7k_per_runner = avg_num_of_7_7k_per_runner / num_of_runners_with_7_7k_races
    avg_num_of_10k_per_runner = avg_num_of_10k_per_runner / num_of_runners_with_10k_races
    avg_num_of_21k_per_runner = avg_num_of_21k_per_runner / num_of_runners_with_21k_races
    avg_num_of_42k_per_runner = avg_num_of_42k_per_runner / num_of_runners_with_42k_races

    return {'bgd_marathon_data_len': participants_results_len_bgd,
            'trka_rs_data_len': participants_results_len_trka_rs,
            'runtrace_data_len': participants_results_len_runtrace,
            'total_number_of_runner_race_results': total_number_of_runner_race_results,
            'total_number_of_runners_with_race_results': total_number_of_runners_with_race_results,
            'avg_num_of_5k_per_runner': avg_num_of_5k_per_runner,
            'avg_num_of_7k_per_runner': avg_num_of_7k_per_runner,
            'avg_num_of_7_7k_per_runner': avg_num_of_7_7k_per_runner,
            'avg_num_of_10k_per_runner': avg_num_of_10k_per_runner,
            'avg_num_of_21k_per_runner': avg_num_of_21k_per_runner,
            'avg_num_of_42k_per_runner': avg_num_of_42k_per_runner,
            'avg_number_of_races_per_runner': total_number_of_runner_race_results /
            total_number_of_runners_with_race_results}
