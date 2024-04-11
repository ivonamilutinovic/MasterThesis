import math
import re
from enum import Enum
from typing import Optional, Union

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
