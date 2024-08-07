from typing import Optional

import pandas as pd
import json


class NoRunnerNameInRaceResultsSet(RuntimeError):
    pass



class NoRunnerDataInRaceResultsSet(RuntimeError):
    pass



def predict_next_race_time(runner_name: str, race_distance: float) -> Optional[str]:
    file_path = '/home/hp/Desktop/MasterThesis/train_wiser/backend/training_data/race_results_grouped_per_race.json'

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    runner_name = data.get(runner_name, {})

    if not runner_name:
        raise NoRunnerNameInRaceResultsSet

    runner_data = runner_name.get(str(race_distance), [])
    if not runner_data:
        raise NoRunnerDataInRaceResultsSet

    df = pd.DataFrame(runner_data)
    df = df.sort_values(by='race_date_int')

    alpha = 0.9
    df['EWMA_total_time'] = df['total_time'].ewm(alpha=alpha).mean()

    df['EWMA_prediction'] = df['EWMA_total_time'].shift(1)

    df['error'] = df['total_time'] - df['EWMA_prediction']

    next_race_prediction = df['EWMA_total_time'].iloc[-1]
    hours = int(next_race_prediction // 3600)
    minutes = int((next_race_prediction % 3600) // 60)
    seconds = int(next_race_prediction % 60)
    next_race_prediction_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return next_race_prediction_str
