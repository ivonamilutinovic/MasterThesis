import pandas as pd
from datetime import timedelta
import numpy as np

file_path = '/mnt/data/output.csv'
data = pd.read_csv(file_path, parse_dates=['start_date'])

print(data.head())

data = data.sort_values(by='start_date')

data['type'] = data['is_race'].apply(lambda x: 'trka' if x else 'trening')


def prepare_data(df, days=90):
    sequences = []
    targets = []

    for i, row in df.iterrows():
        if row['type'] == 'trka':
            end_date = row['start_date']
            start_date = end_date - timedelta(days=days)
            training_data = df[
                (df['start_date'] >= start_date) & (df['start_date'] < end_date) & (df['type'] == 'trening')]

            if len(training_data) > 0:
                sequence = training_data[['activity_type', 'distance', 'moving_time', 'average_heartrate']].values
                sequences.append(sequence)
                targets.append(
                    [row['distance'], row['moving_time']])

    return sequences, targets


sequences, targets = prepare_data(data)

print(f'Number of sequences: {len(sequences)}')

max_len = max(len(seq) for seq in sequences)
print(f'Max sequence length: {max_len}')

def pad_sequences(sequences, max_len):
    padded_sequences = []
    for seq in sequences:
        # Ako je sekvenca kraća od max_len, popuni je sa -1 (kao maskirajuća vrednost)
        padded_seq = np.pad(seq, ((0, max_len - len(seq)), (0, 0)), 'constant', constant_values=-1)
        padded_sequences.append(padded_seq)
    return np.array(padded_sequences)

padded_sequences = pad_sequences(sequences, max_len)

print(padded_sequences.shape)  # Oblik sekvenci za treniranje

# Konvertovanje ciljeva u numpy array
targets = np.array(targets)
