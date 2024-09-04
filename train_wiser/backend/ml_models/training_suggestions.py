from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tensorflow.keras.layers import LSTM, Dense, Masking
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences

from train_wiser.backend.utils.run_info_utils import round_race_distance, is_race_distance_of_relevant_type

ACTIVITIES_OF_INTEREST = {'WeightTraining', 'Run', 'TrailRun', 'Ride', 'VirtualRide', 'Swim'}
ACTIVITY_DICT = {activity: idx for idx, activity in enumerate(ACTIVITIES_OF_INTEREST, start=1)}
ACTIVITY_DICT['RestDay'] = 0

def parse_date(date_str):
    date_formats = [
        '%b %d, %Y, %I:%M:%S %p',  # For zero-padded days (e.g., Sep 11, 2017, 8:05:09 PM)
        '%b %-d, %Y, %I:%M:%S %p',  # For non-zero-padded days (e.g., Jun 1, 2017, 7:07:02 PM) on Unix systems
        '%Y-%m-%d %H:%M:%S',        # Example: 2017-09-11 20:05:09
    ]
    for fmt in date_formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format for {date_str} not recognized")


def prepare_data(file_paths, days=56):
    training_sequences = []
    result_targets = []

    for file_path in file_paths:
        # Read data from CSV file
        data = pd.read_csv(file_path, low_memory=False, dtype={
            'start_date': str,
            'activity_type': str,
            'distance': float,
            'moving_time': float,
            'average_heartrate_zone': float,
            'is_race': bool,
            'name': str
        })

        data['start_date'] = data['start_date'].apply(parse_date)

        data = data.sort_values(by='start_date')

        for i, row in data.iterrows():
            if row['is_race']:
                race_distance = row['distance']
                if is_race_distance_of_relevant_type(race_distance):
                    race_distance = round_race_distance(row['distance'])
                else:
                    print(f"Race distance {race_distance} is not relevant. Race name: {row['name']}.")
                    continue

                end_date = row['start_date']
                start_date = end_date - timedelta(days=days)
                training_data = data[(data['start_date'] >= start_date) & (data['start_date'] < end_date)]

                sequence = []
                for single_date in pd.date_range(start=start_date, end=end_date - timedelta(days=1)):
                    daily_data = training_data[training_data['start_date'].dt.date == single_date.date()]
                    if not daily_data.empty:
                        # Taking only first training in the day
                        training = daily_data.iloc[0]
                        if training['activity_type'] in ACTIVITIES_OF_INTEREST:
                            activity_type = ACTIVITY_DICT[training['activity_type']]
                            sequence.append([
                                activity_type,
                                training['distance'],
                                training['moving_time'],
                                training['average_heartrate_zone'] if not pd.isna(training['average_heartrate_zone']) else 0
                            ])
                        else:
                            sequence.append([ACTIVITY_DICT['RestDay'], 0, 0, 0])
                    else:
                        # If there is no training for that day, placeholder is added
                        sequence.append([ACTIVITY_DICT['RestDay'], 0, 0, 0])

                training_sequences.append(sequence)
                result_targets.append([race_distance, row['moving_time']])

    return training_sequences, result_targets

file_paths = [
    '../training_data/training_suggestions/training_set_0.csv',
    '../training_data/training_suggestions/training_set_1.csv'
]

# Obtain training sequences and targets
training_sequences, result_targets = prepare_data(file_paths)

# Check the number of sequences
print(f'Number of sequences: {len(training_sequences)}')

# Find the maximum sequence length
max_len_seq = max(training_sequences, key=len)
print(f'Max sequence length: {len(max_len_seq)}')
print(f'Max sequence: {max_len_seq}')

# Optional: Print some sequences and targets to verify correctness
print(f'Sample training sequence: {training_sequences[0]}')
print(f'Sample result target: {result_targets[0]}')

print(f'\nData: {training_sequences}')
print(f"Targets: {result_targets}")

with open('sequences.txt', 'a+') as file:
    file.write(f'\n\nSequence (): {training_sequences}')
    file.write(f"\nTargets: {result_targets}")
    file.write(f"\n\nMax len seq: {max_len_seq}")


def prepare_sequences(training_sequences):
    # Maximum sequence length
    max_len = max(len(seq) for seq in training_sequences)

    # Convert sequences to a list of lists with uniform structure
    sequences_array = []
    for seq in training_sequences:
        structured_seq = [
            [int(x[0]), float(x[1]), float(x[2]), int(x[3])] for x in seq
        ]
        sequences_array.append(structured_seq)

    # Use pad_sequences from Keras to pad sequences
    padded_training_sequences = pad_sequences(sequences_array, maxlen=max_len, dtype='float32', padding='post', value=-1)

    return padded_training_sequences, max_len

# Prepare sequences
padded_training_sequences, max_len = prepare_sequences(training_sequences)

print(padded_training_sequences.shape)

result_targets = np.array(result_targets, dtype='float32')

result_targets = np.expand_dims(result_targets, axis=1)

print(f'Sample padded training sequence: {padded_training_sequences[0]}')
print(f'Sample result target: {result_targets[0]}')

# Function to create LSTM model
def create_lstm_model(input_shape, output_shape):
    model = Sequential()
    # Masking layer to ignore -1 values
    model.add(Masking(mask_value=-1, input_shape=input_shape))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(output_shape, activation='relu'))
    return model

input_shape = (result_targets.shape[1], result_targets.shape[2])  # Input shape: [timesteps, features]
output_shape = padded_training_sequences.shape[1] * padded_training_sequences.shape[2]  # Output shape: flattened training sequence

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(result_targets, padded_training_sequences,test_size=0.2,
                                                    random_state=42)

model = create_lstm_model((X_train.shape[1], X_train.shape[2]), y_train.shape[1] * y_train.shape[2])

model.compile(optimizer='adam', loss='mse')

history = model.fit(X_train, y_train.reshape((y_train.shape[0], -1)), epochs=50, batch_size=32, validation_data=(X_test, y_test.reshape((y_test.shape[0], -1))))

# Plotting training and validation loss
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()


sample_index = 0
sample_input = X_train[sample_index]
sample_output = y_train[sample_index]

sample_prediction = model.predict(np.expand_dims(sample_input, axis=0))
print(f'Real output: {sample_output}')
print(f'Predicted output: {sample_prediction}')
