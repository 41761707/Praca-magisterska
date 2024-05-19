import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.metrics import accuracy_score
from tensorflow.keras.optimizers import Adagrad
from tensorflow.keras.models import load_model
from tensorflow.keras import layers
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

class Model:
    def __init__(self, model_type, model_columns_df, entries, features, create_model):
        self.model_columns_df = model_columns_df
        self.model_type = model_type
        self.model = ''
        self.entries = entries
        self.features = features
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
        self.test_predictions = []
        self.mean_y = 0
        self.mean_rank = 0
        self.norm_y = 0
        self.norm_rank = 0
    
    def normalize_rank(self, data):
        data_np = np.array(data)

        # Znalezienie minimalnej i maksymalnej wartości w całej tablicy
        min_val = np.min(data_np)
        max_val = np.max(data_np)

        # Normalizacja tablicy
        normalized_data = (data_np - min_val) / (max_val - min_val)

        # Konwersja znormalizowanej tablicy z powrotem do listy (opcjonalnie)
        normalized_data_list = normalized_data.tolist()

        return normalized_data_list
    
    def ranked_probability_score(y_true, y_pred):
        N = len(y_true)  # liczba obserwacji
        M = len(y_pred[0])  # liczba możliwych wyników

        # Inicjalizacja tablicy dla RPS
        rps_array = np.zeros(N)

        # Obliczanie RPS dla każdej obserwacji
        for i in range(N):
            rps = 0
            for j in range(M - 1):
                rps += (np.sum(y_pred[i][:j+1]) - np.sum(y_true[i][:j+1]))**2
            rps_array[i] = rps / (M - 1)

        # Obliczanie średniego RPS
        mean_rps = np.mean(rps_array)
        
        return mean_rps

    def create_window(self):
        model_tolist = self.model_columns_df.values.tolist()
        iter = 0
        for index, match in self.model_columns_df.iterrows():
            self.window_helper.append({'id' : index, 
                                       'Match-8' : model_tolist[iter], 
                                       'Match-7' : model_tolist[iter+1], 
                                       'Match-6' : model_tolist[iter+2], 
                                       'Match-5' : model_tolist[iter+3], 
                                       'Match-4' : model_tolist[iter+4], 
                                       'Match-3' : model_tolist[iter+5], 
                                       'Match-2' : model_tolist[iter+6],
                                       'Match-1' : model_tolist[iter+7],
                                       'Match-CURR' : model_tolist[iter+8]})
            iter = iter + 1
            if iter > len(self.model_columns_df)-self.entries:
                break
        self.window_df = pd.DataFrame(self.window_helper)
        self.window_df = self.window_df.drop(columns=['id'])

    def remade(self, labels):
        new_self_x = []
        for list in self.X:
            row = []
            for inner_list in list:
                for inner_inner in inner_list:
                    row.append(inner_inner[0:-1 * labels])
            new_self_x.append(row)
        return new_self_x

        
    def window_to_numpy(self, labels):
        df_as_np = self.window_df.to_numpy()
        self.indexes = list(range(1, len(df_as_np) + 1))
        mid = df_as_np[:, 0:-1]
        tmp_y = df_as_np[:, -1]
        for element in tmp_y:
            self.y.append(element[(-1) * labels :])
        self.X = mid.reshape((len(self.indexes), mid.shape[1], 1))
        self.X = self.remade(labels)
        #Normalizacja
        #self.X = self.normalize_rank(self.X)
        #print(self.X[:5])



    def divide_set(self):
        first = int(len(self.indexes) * 0.7)
        second = int(len(self.indexes) * 0.8)
        self.indexes_train, self.X_train, self.y_train = self.indexes[:first], self.X[:first], self.y[:first]
        self.indexes_val, self.X_val, self.y_val = self.indexes[first:second], self.X[first:second], self.y[first:second]
        self.indexes_test, self.X_test, self.y_test = self.indexes[second:], self.X[second:], self.y[second:]

    def train_goals_total_model(self):
        if self.create_model == 'new':
            self.model = Sequential([layers.Input((int(self.entries-1), self.features)),
                    layers.LSTM(64, activation = 'relu'),
                    layers.Dense(32, activation = 'relu'),
                    layers.Dense(16, activation = 'relu'),
                    layers.Dense(1)])
            cp = ModelCheckpoint('model_goals/', save_best_only = True)
            self.model.compile(loss='mse', 
                optimizer=Adagrad(learning_rate=0.001),
                metrics=['accuracy'])
            self.model.fit(self.X_train, self.y_train, validation_data=(self.X_val, self.y_val), epochs=30, batch_size = 32, callbacks = [cp])
            #print(self.model.summary())
        else:
            self.model = load_model('model_goals/')

    def train_goals_per_team(self):
        if self.create_model == 'new':
            self.model = Sequential([layers.Input((int(self.entries-1), self.features)),
                    layers.LSTM(64, activation = 'relu'),
                    layers.Dense(32, activation = 'relu'),
                    layers.Dense(16, activation = 'relu'),
                    layers.Dense(3)])
            cp = ModelCheckpoint('model_team_goals/', save_best_only = True)
            self.model.compile(loss='mse', 
                optimizer=Adagrad(learning_rate=0.001),
                metrics=['accuracy'])

            self.model.fit(self.X_train, self.y_train, validation_data=(self.X_val, self.y_val), epochs=25, batch_size = 32, callbacks = [cp])
            #print(self.model.summary())
        else:
            self.model = load_model('model_team_goals/')

        #test_predictions = model.predict(self.X_test).flatten().astype(int)
        #accuracy = accuracy_score(test_predictions, self.y_test)
        #print("Accuracy:", accuracy)
        #plt.plot(self.indexes_test[:50], test_predictions[:50])
        #plt.plot(self.indexes_test[:50], self.y_test[:50])
        #plt.legend(['Testing Predictions', 'Testing Observations'])
        #plt.show()

    def make_predictions(self, tests):
        test_prediction = self.model.predict(tests).flatten().astype(int)
        test_prediction = np.clip(test_prediction, 0, 6)
        return test_prediction

    def train_goals_teams_model(self):
        if self.create_model == 'new':
            self.model = Sequential([layers.Input((int(self.entries-1), self.features)),
                    layers.LSTM(64, activation = 'relu'),
                    layers.Dense(32, activation = 'relu'),
                    layers.Dense(3)])
            cp = ModelCheckpoint('model_goals_teams/', save_best_only = True)
            self.model.compile(loss='mse', 
                optimizer=Adagrad(learning_rate=0.001),
                metrics=['accuracy'])

            self.model.fit(self.X_train, self.y_train, validation_data=(self.X_val, self.y_val), epochs=50, callbacks = [cp])
            #print(self.model.summary())
        else:
            self.model = load_model('model_goals_teams/')
    
    def predict_external_graphs(self, team_name):
        test_predictions = self.model.predict(self.X_test).flatten().astype(int)
        test_predictions = np.clip(test_predictions, 0, 6)
        plt.plot(self.indexes_test, test_predictions)
        plt.plot(self.indexes_test, self.y_test)
        plt.legend(['Predykcje', 'Obserwacje'])
        plt.savefig('graphs/goals/{}_goals_total.png'.format(team_name))
        plt.close()
        ou_accuracy = 0
        exact_accuracy = 0
        for i in range(len(test_predictions)):
            generated_ou = "U" if test_predictions[i] < 2.5 else "O"
            real_ou = "U" if self.y_test[i][0] < 2.5 else "O"
            if generated_ou == real_ou:
                ou_accuracy = ou_accuracy + 1
            if test_predictions[i] == self.y_test[i][0]:
                exact_accuracy = exact_accuracy + 1
        return exact_accuracy / len(test_predictions), ou_accuracy / len(test_predictions), exact_accuracy, ou_accuracy, len(test_predictions)
    
    def predict_test(self):
        test_predictions = self.model.predict(self.X_test).flatten().astype(int)
        print(test_predictions)
        accuracy = accuracy_score(test_predictions, self.y_test)
        test_predictions = np.clip(test_predictions, 0, 6)
        ou_predictions = 0
        for i in range(len(test_predictions)):
            if (self.y_test[i][0] < 2.5 and test_predictions[i] < 2.5) or (self.y_test[i][0] > 2.5 and test_predictions[i] > 2.5):
                ou_predictions += 1
        print("Accuracy:", accuracy)
        print("OU: ", ou_predictions / len(test_predictions))
        plt.plot(self.indexes_test[:50], test_predictions[:50])
        plt.plot(self.indexes_test[:50], self.y_test[:50])
        plt.legend(['Testing Predictions', 'Testing Observations'])
        plt.show()

'''class Model:
    def __init__(self, data):
        self.data = data
    
    def preprocess_data(self):
        # Implementacja ogólnej metody preprocess_data
        pass
    
    def train(self):
        # Implementacja ogólnej metody trenowania modelu
        pass
    
    def evaluate(self):
        # Implementacja ogólnej metody oceny wydajności modelu
        pass

class WinnerModel(Model):
    def __init__(self, data):
        super().__init__(data)
    
    def preprocess_data(self):
        # Implementacja specyficznej metody preprocess_data dla WinnerModel
        pass
    
    def train(self):
        # Implementacja specyficznej metody trenowania modelu dla WinnerModel
        pass
    
    def evaluate(self):
        # Implementacja specyficznej metody oceny wydajności modelu dla WinnerModel
        pass

class GoalTotalModel(Model):
    def __init__(self, data):
        super().__init__(data)
    
    def preprocess_data(self):
        # Implementacja specyficznej metody preprocess_data dla GoalTotalModel
        pass
    
    def train(self):
        # Implementacja specyficznej metody trenowania modelu dla GoalTotalModel
        pass
    
    def evaluate(self):
        # Implementacja specyficznej metody oceny wydajności modelu dla GoalTotalModel
        pass'''



