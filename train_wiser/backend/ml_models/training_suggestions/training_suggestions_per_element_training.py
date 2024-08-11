from datetime import timedelta
import pandas as pd
from train_wiser.backend.utils.run_info_utils import round_race_distance, is_race_distance_of_relevant_type
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Masking

from datetime import timedelta
import pandas as pd
import numpy as np

# Enumeracija za tipove aktivnosti
ACTIVITIES_OF_INTEREST = {'WeightTraining', 'Run', 'TrailRun', 'Ride', 'VirtualRide', 'Swim'}
ACTIVITY_DICT = {activity: idx for idx, activity in enumerate(ACTIVITIES_OF_INTEREST, start=1)}
ACTIVITY_DICT['RestDay'] = 0  # Dodajemo Rest day kao 0

def parse_date(date_str):
    # Try different date formats
    date_formats = [
        '%b %d, %Y, %I:%M:%S %p',  # Example: Sep 11, 2017, 8:05:09 PM
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

        # Convert the 'start_date' column to datetime format
        data['start_date'] = data['start_date'].apply(parse_date)

        # Sort data by date
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

                # Sort training data by date within the interval
                training_data = training_data.sort_values(by='start_date')

                sequence = []
                for single_date in pd.date_range(start=start_date, end=end_date - timedelta(days=1)):
                    daily_data = training_data[training_data['start_date'].dt.date == single_date.date()]
                    if not daily_data.empty:
                        # Uzmi samo prvi trening u danu
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
                        # If there is no training for that day, we are adding placeholder
                        sequence.append([ACTIVITY_DICT['RestDay'], 0, 0, 0])

                # # Ograničavanje sekvenci na 60 dana
                # sequence = sequence[:60]

                training_sequences.append(sequence)
                result_targets.append([race_distance, row['moving_time']])

    return training_sequences, result_targets

# List of CSV file paths
file_paths = [
    '/home/hp/Desktop/MasterThesis/train_wiser/backend/training_data/training_suggestions/ivona_training_data.csv',
    '/home/hp/Desktop/MasterThesis/train_wiser/backend/training_data/training_suggestions/ivona_training_data.csv',
    '/home/hp/Desktop/MasterThesis/train_wiser/backend/training_data/training_suggestions/ivona_training_data.csv',
    '/home/hp/Desktop/MasterThesis/train_wiser/backend/training_data/training_suggestions/ivona_training_data.csv',
    # '/home/hp/Desktop/MasterThesis/train_wiser/backend/training_data/training_suggestions/milos_training_data.csv'
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

print(padded_training_sequences.shape)  # Shape of training sequences

# Convert targets to numpy array
result_targets = np.array(result_targets, dtype='float32')

# Add time dimension to result_targets
result_targets = np.expand_dims(result_targets, axis=1)

print(f'Sample padded training sequence: {padded_training_sequences[0]}')
print(f'Sample result target: {result_targets[0]}')

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Attention

from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Attention, Input, concatenate

from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Embedding, Input, Flatten


def create_lstm_model(vocab_size, input_length, output_shape):
    inputs = Input(shape=(input_length,))

    # Embedding layer to map input indices to dense vectors
    embedding_out = Embedding(input_dim=vocab_size, output_dim=64, input_length=input_length)(inputs)

    # LSTM layers
    lstm_out = LSTM(64, return_sequences=True)(embedding_out)
    lstm_out_2 = LSTM(32)(lstm_out)

    # Dense layer to process the output
    dense_out = Dense(64, activation='relu')(lstm_out_2)

    # Output layer
    outputs = Dense(output_shape, activation='linear')(dense_out)

    model = Model(inputs, outputs)

    return model


# Primer vrednosti
vocab_size = 1000  # Broj različitih ulaznih vrednosti (veličina vokabulara)
input_length = 60  # Dužina sekvence
output_shape = 4  # Oblik izlaza

model = create_lstm_model(vocab_size, input_length, output_shape)
model.summary()

# Primer kodiranja ulaznih podataka
# input_indices bi bili indeksirani elementi iz ulaznog skupa
input_indices = np.random.randint(0, vocab_size, (1, input_length))

output = model.predict(input_indices)
print("Output:", output)

# input_shape = (60, 4)  # Primer ulaznog oblika
# output_shape = 4  # Oblik izlaza odgovara ulaznom
#
# model = create_lstm_model(input_shape, output_shape)
# model.summary()
##################
# # Defining input and output shapes
# input_shape = (result_targets.shape[1], result_targets.shape[2])  # Input shape: [timesteps, features]
# output_shape = padded_training_sequences.shape[1] * padded_training_sequences.shape[2]  # Output shape: flattened training sequence
#
# from sklearn.model_selection import train_test_split
#
# # Assuming you already have padded_training_sequences and result_targets ready
# X_train, X_test, y_train, y_test = train_test_split(result_targets, padded_training_sequences,test_size=0.2,
#                                                     random_state=42)
#
# # Now you can train your model with the training data and validate it with the test data.
#
# model.compile(optimizer='adam', loss='mse')
#
# # Training the model using only the training set
# history = model.fit(X_train, y_train.reshape((y_train.shape[0], -1)), epochs=50, batch_size=32, validation_data=(X_test, y_test.reshape((y_test.shape[0], -1))))
#
# # Plotting training and validation loss
# import matplotlib.pyplot as plt
#
# plt.plot(history.history['loss'], label='Train Loss')
# plt.plot(history.history['val_loss'], label='Validation Loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()
#
# # If you want to test a specific sample from your test set, you can:
# sample_index = 0  # Example index
# sample_input = X_train[sample_index]
# sample_output = y_train[sample_index]
#
# sample_prediction = model.predict(np.expand_dims(sample_input, axis=0))
# print(f'Real output: {sample_output}')
# print(f'Predicted output: {sample_prediction}')
