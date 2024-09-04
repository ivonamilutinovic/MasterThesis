import json
import os.path
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.models import Sequential


class RacePredictionModel:
    def __init__(self, sequence_length=3, start_date_str="1990-01-01"):
        self.sequence_length = sequence_length
        self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        self.model = self.build_model()
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()

    def prepare_data(self, runner_results_dict):
        X = []
        y = []
        dates = []
        distances = []

        for results_per_runner_list in runner_results_dict.values():
            if len(results_per_runner_list) >= self.sequence_length + 1:
                for i in range(len(results_per_runner_list) - self.sequence_length):
                    sequence = []
                    for j in range(self.sequence_length):
                        race = results_per_runner_list[i + j]
                        sequence.append([race["race_date_int"], race["race_distance"], race["total_time"]])

                    next_race = results_per_runner_list[i + self.sequence_length]
                    X.append(sequence)
                    y.append(next_race["total_time"])
                    dates.append(next_race["race_date"])
                    distances.append(next_race["race_distance"])

        X = np.array(X, dtype=np.float32)
        y = np.array(y, dtype=np.float32).reshape(-1, 1)

        print("Before scaling:")
        print("X sample:", X[0])
        print("y sample:", y[0])

        X_scaled = self.scaler_X.fit_transform(X.reshape(-1, 3)).reshape(X.shape)
        y_scaled = self.scaler_y.fit_transform(y)

        print("After scaling:")
        print("X sample:", X_scaled[0])
        print("y sample:", y_scaled[0])

        # Verification if denormalization is correct
        y_denorm = self.scaler_y.inverse_transform(y_scaled)
        if np.allclose(y, y_denorm):
            print("Scaling and denormalization are correct.")
        else:
            print("There is an issue with scaling and denormalization.")

        return X_scaled, y_scaled, dates, distances

    def build_model(self):
        model = Sequential()
        model.add(Bidirectional(LSTM(50, return_sequences=True), input_shape=(self.sequence_length, 3)))
        model.add(Dropout(0.2))
        model.add(Bidirectional(LSTM(50, return_sequences=True)))
        model.add(Dropout(0.2))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        return model

    def train(self, X_train, y_train, epochs=50):
        physical_devices = tf.config.list_physical_devices('GPU')
        if len(physical_devices) > 0:
            print(f'Using GPU: {physical_devices[0]}')
            tf.config.experimental.set_memory_growth(physical_devices[0], True)
        else:
            print('GPU not available, using CPU.')
        self.model.fit(X_train, y_train, epochs=epochs, verbose=1, validation_split=0.2)

    def evaluate(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test, verbose=1)

    def predict(self, X_test):
        predictions = self.model.predict(X_test)
        return self.scaler_y.inverse_transform(predictions)

    def evaluate_and_visualize(self, model, X_test, y_test, dates_test, distances_test):
        predicted_time = model.predict(X_test)

        predicted_time_denorm = self.scaler_y.inverse_transform(predicted_time)
        actual_time_denorm = self.scaler_y.inverse_transform(y_test.reshape(-1, 1))

        mse_denorm = mean_squared_error(actual_time_denorm, predicted_time_denorm)
        print(f'Mean Squared Error on Test Set (de-normalized): {mse_denorm}')

        plt.figure(figsize=(12, 6))
        plt.plot(range(len(actual_time_denorm)), actual_time_denorm, label='Actual Time', marker='o')
        plt.plot(range(len(predicted_time_denorm)), predicted_time_denorm.flatten(), label='Predicted Time', marker='x')
        plt.xlabel('Sample')
        plt.ylabel('Total Time')
        plt.title('Actual vs Predicted Total Time')
        plt.legend()
        plt.show()

        for i in range(len(predicted_time_denorm)):
            print(
                f'Date: {dates_test[i]}, Distance: {distances_test[i]}, Predicted Time: {predicted_time_denorm[i][0]}, Actual Time: {actual_time_denorm[i][0]}')

        with open('predicted_results.txt', 'w') as f:
            for i in range(len(predicted_time_denorm)):
                f.write(
                    f'Date: {dates_test[i]}, Distance: {distances_test[i]}, '
                    f'Predicted Time: {predicted_time_denorm[i][0]}, Actual Time: {actual_time_denorm[i][0]}\n'
                )
                f.write('\n')

        with open('normalized_predicted_results.txt', 'w') as f:
            for i in range(len(predicted_time_denorm)):
                f.write(
                    f'Date: {dates_test[i]}, Distance: {distances_test[i]}, '
                    f'Predicted Time: {predicted_time[i][0]}, Actual Time: {y_test[i][0]}\n'
                )
                f.write('\n')

def train_model_for_race_result_prediction():
    json_file = os.path.abspath('../training_data/race_results.json')
    with open(json_file, 'r', encoding='utf-8') as f:
        runners_data = json.load(f)
    model = RacePredictionModel(sequence_length=3)
    X, y, dates, distances = model.prepare_data(runners_data)
    X_train, X_test, y_train, y_test, dates_train, dates_test, distances_train, distances_test = train_test_split(
        X, y, dates, distances, test_size=0.2, random_state=42)
    model.train(X_train, y_train, epochs=50)
    loss = model.evaluate(X_test, y_test)
    print(f'Mean Squared Error: {loss}')
    model.evaluate_and_visualize(model, X_test, y_test, dates_test, distances_test)


train_model_for_race_result_prediction()
