import re
import math
from enum import Enum
from typing import Optional


class RaceInfoEnum(Enum):
    PACE = "tempo"
    TIME = "vreme"


FINISHED_RACE_STATUS = 'finished'
SUCCESS_RACE_STATUS = 'ok'


def is_race_of_relevant_type(race_name: str) -> bool:
    not_relevant_race_types = ['trail', 'vertical', 'ocr', 'plivanje', 'swimming', 'tribalion', 'štafeta']
    return not any(race_type in race_name.lower() for race_type in not_relevant_race_types)


def is_race_distance_of_relevant_type(race_distance: float) -> bool:
    relevant_distances = [5, 7, 7.7, 10, 21, 42]  # TODO: See runtrace for 7.7 and trka zadovoljstva on Ada
    return math.floor(race_distance) in relevant_distances


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
