import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.models import load_model
from tensorflow.keras import layers
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class Model:
    def __init__(self, model_columns_df, entries, create_model):
        self.model_columns_df = model_columns_df
        self.entries = entries
        self.create_model = create_model
        self.trainX = []
        self.trainY = []
        self.n_future = 1
        self.n_past = 5
        self.scaled_df = []
        '''self.window_helper = []
        self.window_df = []
        self.indexes = []
        self.X = []
        self.y = []
        self.indexes_train = []
        self.X_train = []
        self.y_train = []
        self.indexes_val = []
        self.X_val = []
        self.y_val = []
        self.indexes_test = []
        self.X_test = []
        self.y_test = []'''

    def create_window(self):
        self.model_columns_df = self.model_columns_df.astype(float)
        scaler = StandardScaler()
        scaler = scaler.fit(self.model_columns_df)
        self.scaled_df = scaler.transform(self.model_columns_df)
        for i in range(self.n_past, len(self.scaled_df) - self.n_future + 1):
            self.trainX.append(self.scaled_df[i-self.n_past:i, 0:self.model_columns_df.shape[1]])
            self.trainY.append(self.scaled_df[i+self.n_future - 1:i + self.n_future, 0])
        print(self.trainX[:5])
        print(self.trainY[:5])
        self.trainX, self.trainY = np.array(self.trainX), np.array(self.trainY)

    def window_to_numpy(self):

        df_as_np = self.window_df.to_numpy()
        self.indexes = list(range(1, len(df_as_np) + 1))
        #self.indexes = df_as_np[:, 0]
        mid = df_as_np[:, 1:-1]
        self.X = mid.reshape((len(self.indexes), mid.shape[1], 1))
        tmp_y = df_as_np[:, -1]
        #self.y = df_as_np[:, -1]
        #self.X = self.X.astype(np.float32)
        #self.y = self.y.astype(np.float32)
        for element in tmp_y:
            self.y.append(element[1])
        print(self.indexes[:5])
        print(self.X[:5])
        print(self.y[:5])
        self.X = self.X.astype(np.float32)
        self.y = self.y.astype(np.float32)

    def divide_set(self):
        first = int(len(self.indexes) * 0.8)
        second = int(len(self.indexes) * 0.9)
        self.indexes_train, self.X_train, self.y_train = self.indexes[:first], self.X[:first], self.y[:first]
        self.indexes_val, self.X_val, self.y_val = self.indexes[first:second], self.X[first:second], self.y[first:second]
        self.indexes_test, self.X_test, self.y_test = self.indexes[second:], self.X[second:], self.y[second:]

    def train_model(self):
        #model = ''
        #print(self.create_model)
        if self.create_model == '1':
            model = Sequential([
                    layers.Input((self.trainX.shape[1], self.trainX.shape[2])),
                    layers.LSTM(64),
                    layers.Dense(64, activation='relu'),
                    layers.Dense(32, activation='relu'),
                    layers.Dropout(0.2),
                    layers.Dense(self.trainY.shape[1])
                ])
            cp = ModelCheckpoint('model/', save_best_only = True)
            model.compile(loss='mse', 
                optimizer=SGD(learning_rate=0.001),
                metrics=['accuracy'])
            print(model.summary())
            history = model.fit(self.trainX, self.trainY, epochs=10, batch_size = 16, validation_split = 0.1)#, callbacks = [cp])
        else:
            model = load_model('model/')

        '''test_predictions = model.predict(self.X_test).flatten().astype(int)
        accuracy = accuracy_score(self.y_test, test_predictions)
        print("Accuracy:", accuracy)
        plt.plot(self.indexes_test, test_predictions)
        plt.plot(self.indexes_test, self.y_test)
        plt.legend(['Testing Predictions', 'Testing Observations'])
        plt.show()'''



    