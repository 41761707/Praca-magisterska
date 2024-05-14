import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

class Model:
    def __init__(self, model_columns_df, entries, create_model):
        self.model_columns_df = model_columns_df
        self.entries = entries
        self.create_model = create_model
        self.window_helper = []
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
        self.y_test = []

    def create_window(self):
        model_tolist = self.model_columns_df.values.tolist()
        iter = 0
        for index, match in self.model_columns_df.iterrows():
            self.window_helper.append({'id' : index, 'Match-3' : model_tolist[iter][0], 'Match-2' : model_tolist[iter+1][0], 'Match-1' : model_tolist[iter+2][0], 'Match-CURR' : model_tolist[iter+3][0]})
            '''self.window_helper.append({'id' : index, 'Match-7' : model_tolist[iter][0], 
                                                     'Match-6' : model_tolist[iter+1][0], 
                                                     'Match-5' : model_tolist[iter+2][0], 
                                                     'Match-4' : model_tolist[iter+3][0], 
                                                     'Match-3' : model_tolist[iter+4][0], 
                                                     'Match-2' : model_tolist[iter+5][0], 
                                                     'Match-1' : model_tolist[iter+6][0], 
                                                     'Match-CURR' : model_tolist[iter+7][0]})'''
            iter = iter + 1
            if iter > len(self.model_columns_df)-self.entries:
                break
        self.window_df = pd.DataFrame(self.window_helper)
        #self.window_df.set_index('id', inplace=True)
        
    def window_to_numpy(self):

        df_as_np = self.window_df.to_numpy()
        self.indexes = list(range(1, len(df_as_np) + 1))
        #self.indexes = df_as_np[:, 0]
        mid = df_as_np[:, 1:-1]
        self.X = mid.reshape((len(self.indexes), mid.shape[1], 1))
        self.y = df_as_np[:, -1]
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
            model = Sequential([layers.Input((int(self.entries-1), 1)),
                    layers.LSTM(64),
                    layers.Dense(64, activation='tanh'),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(16, activation='relu'),
                    layers.Dense(1)])
            cp = ModelCheckpoint('model/', save_best_only = True)
            model.compile(loss='mse', 
                optimizer=Adam(learning_rate=0.001),
                metrics=['mean_absolute_error'])

            model.fit(self.X_train, self.y_train, validation_data=(self.X_val, self.y_val), epochs=20, callbacks = [cp])
        else:
            model = load_model('model/')
        train_predictions = model.predict(self.X_train).flatten()
        #for i in range(len(train_predictions)):
        #    train_predictions[i] = round(train_predictions[i])
        plt.plot(self.indexes_train, train_predictions)
        plt.plot(self.indexes_train, self.y_train)
        plt.legend(['Training Predictions', 'Training Observations'])
        plt.yticks(range(0, int(max(max(train_predictions), max(self.y_train))) + 1))
        plt.savefig('train_4_Slask_tanh_relu_relu.png')
        plt.show()


        #val_predictions = model.predict(self.X_val).flatten()

        #plt.plot(self.indexes_val, val_predictions)
        #plt.plot(self.indexes_val, self.y_val)
        #plt.legend(['Validation Predictions', 'Validation Observations'])
        #plt.show()

        #test_predictions = model.predict(self.X_test).flatten().astype(int)
        #print(test_predictions[:5])
        #plt.plot(self.indexes_test, test_predictions)
        #plt.plot(self.indexes_test, self.y_test)
        #plt.legend(['Testing Predictions', 'Testing Observations'])
        #plt.show()



    