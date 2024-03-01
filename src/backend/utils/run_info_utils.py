import re
from enum import Enum
from typing import Optional


def str_time_to_seconds(time_str: str) -> Optional[int]:
    time_str = time_str.strip()

    if re.fullmatch("([0-9]{1,2}:){1,2}[0-9]{1,2}", time_str) is None:
        return None

    time_tokens = time_str.split(":")

    seconds = 0
    multiply = 1
    for token in reversed(time_tokens):
        seconds += int(token) * multiply
        multiply *= 60

    return seconds


class RaceInfoEnum(Enum):
    PACE = "tempo"
    TIME = "vreme"
