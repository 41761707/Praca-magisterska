
import mysql.connector
import pandas as pd
#import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
#from keras.layers import Activation, Dense, Dropout, Embedding, LSTM
#from sklearn.preprocessing import StandardScaler
'''
    Główny program projektu predykcji meczów
    Autor: Radosław Wojtczak
    Data rozpoczęcia: 01.03.2024
    Ostatnia aktualizacja: 13.05.02024
    Wersja: 1.0.2
'''
# S4 - state space model
def db_connect():
    # Połączenie z bazą danych MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radikey",
        database="ekstrabet"
    )
    return conn

def e_step(r_i, r_j):
    return 1 / (1 + 10 ** (-(r_i - r_j) / 400))

def u_step(r, p, a, k):
    return r + k * (a - p)

def evaluate_k( goal_diff):
    constant = 32 #Z gory ustalone przez autora
    if goal_diff == 2:
        constant = constant * 1/2
    elif goal_diff == 3:
        constant = constant * 3/4 
    elif goal_diff > 3:
        constant = constant * 3/4 + (goal_diff-3)/8
    return constant

def pi_rating(ratings, home_team_id, away_team_id, result, goal_diff):
    home_team_rating = ratings[home_team_id]
    away_team_rating = ratings[away_team_id]

def berrar_rating(ratings, home_team_id, away_team_id, result, goal_diff):
    home_team_rating = ratings[home_team_id]
    away_team_rating = ratings[away_team_id]

def gap_rating(ratings, home_team_id, away_team_id, result, goal_diff):
    home_team_rating = ratings[home_team_id]
    away_team_rating = ratings[away_team_id]


def elo_rating(ratings, home_team_id, away_team_id, result, goal_diff):
    k_factor = evaluate_k(goal_diff)
    home_team_rating = ratings[home_team_id]
    away_team_rating = ratings[away_team_id]
    home_team_ppb = e_step(home_team_rating, away_team_rating)
    away_team_ppb = e_step(away_team_rating, home_team_rating)
    #assert home_team_ppb + away_team_ppb = 1
    home_team_result = 0
    away_team_result = 0
    if result == 0:
        home_team_result = 0.5
        away_team_result = 0.5
    elif result == 1:
        home_team_result = 1
    else: 
        away_team_result = 1
    home_team_update = u_step(home_team_rating, home_team_ppb, home_team_result, k_factor)
    away_team_update = u_step(away_team_rating, away_team_ppb, away_team_result, k_factor)
    ratings[home_team_id] = home_team_update
    ratings[away_team_id] = away_team_update
    return home_team_update, away_team_update


def rating_wrapper(matches_df, teams_df, rank_type):
    teams_dict = {}
    ratings = {}
    starting_rating = 1500
    for team in teams_df.values:
        if team[0] not in ratings:
            ratings[team[0]] = starting_rating
        if team[1] not in teams_dict:
            teams_dict[team[0]] = team[1]
    for index, match in matches_df.iterrows():
        goal_diff = abs(match[4] - match[5])
        if rank_type == 'ELO':
            home_rating, away_rating = elo_rating(ratings, match[2], match[3], match[-1], goal_diff)
        elif rank_type == 'PI':
            pass
        elif rank_type == 'BERRAR':
            pass
        elif rank_type == 'GAP': 
            pass

        matches_df.at[index, 'rating_home'] = home_rating
        matches_df.at[index, 'rating_away'] = away_rating

        #Over 2.5
        if match[4] + match[5] > 2.5:
            matches_df.at[index, 'OverG'] = 1
        else:
            matches_df.at[index, 'OverG'] = 0

        #BTTS
        if match[4] > 0 and match[5] > 0:
            matches_df.at[index, 'BTTS'] = 1
        else:
            matches_df.at[index, 'BTTS'] = 0
    ratings_list = [(teams_dict[k],v) for k,v in ratings.items()]
    ratings_list.sort(key=lambda x: x[1], reverse= True)
    #for item in ratings_list:
    #    print(item[0],": ", item[1])
    return ratings

def to_timeseries(train_data, window_size):
    df_as_np = train_data.to_numpy()
    X = []
    y = []
    for i in range(len(df_as_np)-window_size):
        match = [x for x in df_as_np[i:i+window_size]]
        X.append(match)
        result = df_as_np[i+window_size]
        y.append(result[0])
    return np.array(X), np.array(y)

def create(X_train, y_train, X_val, y_val):
    model = Sequential()
    model.add(InputLayer((5,1)))
    model.add(LSTM(64, input_shape = (5,1)))
    model.add(Dense(8,'relu'))
    model.add(Dense(1,'linear'))
    #model.add(Dense(10, activation='softmax'))
    #model.add(Dense(1,'linear'))
    model.summary()
    cp = ModelCheckpoint('model/', save_best_only = True)
    model.compile(loss=MeanSquaredError(), optimizer='adam', metrics = 'accuracy')
    model.fit(X_train, y_train, validation_data = (X_val, y_val), epochs = 15, callbacks = [cp])
    return model
def Model(matches_df, upcoming_df, create_model = False):
    selected_columns = ['home_team_sog']
    matches_df = matches_df[selected_columns].copy()
    X,y = to_timeseries(matches_df, 5)
    print(X)
    print(y)
    '''first = int(len(X) * 0.8)
    second = int(len(X) * 0.9)
    X_train, y_train = X[:first], y[:first]
    X_val, y_val = X[first:second], y[first:second]
    X_test, y_test = X[second:], y[second:]
    print(X_train.shape)
    print(y_train.shape)
    print(X_val.shape)
    print(y_val.shape)
    print(X_test.shape)
    print(y_test.shape)
    if create_model:
        model = create(X_train, y_train, X_val, y_val)
    else:
        model = load_model('model/')
    print(X_train[0])
    print(y_train[0])
    train_predictions = model.predict(X_train).flatten()
    y_train = y_train.flatten()
    #print(train_predictions)
    #print(y_train)
    #print(train_predictions.shape)
    #print(y_train.shape)
    train_results = pd.DataFrame(data = {'Train': train_predictions, 'Actual': y_train})
    print(train_results)
    plt.plot(train_results['Train'][:50])
    plt.plot(train_results['Actual'][:50])
    plt.show()'''





    #model.add(Dense(1, activation ='sigmoid'))

def add_aditional_data(matches_df, upcoming_df):
    #rating_home
    matches_df.insert(len(matches_df.columns) - 1, 'rating_home', 0)
    upcoming_df.insert(len(upcoming_df.columns) - 1, 'rating_home', 0)
    #rating_away
    matches_df.insert(len(matches_df.columns) - 1, 'rating_away', 0)
    upcoming_df.insert(len(upcoming_df.columns) - 1, 'rating_away', 0)
    #BTTS
    matches_df.insert(len(matches_df.columns) - 1, 'BTTS', 0)
    upcoming_df.insert(len(upcoming_df.columns) - 1, 'BTTS', 0)
    #Over_2.5G
    matches_df.insert(len(matches_df.columns) - 1, 'OverG', 0)
    upcoming_df.insert(len(upcoming_df.columns) - 1, 'OverG', 0)


    return matches_df, upcoming_df
def main():
    conn = db_connect()
    query = "SELECT * FROM matches where game_date < '2024-04-11' order by game_date"
    matches_df = pd.read_sql(query, conn)
    query = "SELECT id, name FROM teams "
    teams_df = pd.read_sql(query, conn)
    matches_df['result'] = matches_df['result'].replace({'X': 0, '1' : 1, '2' : 2})
    matches_df = matches_df.drop(columns=['game_date'])
    matches_df.set_index('id', inplace=True)
    query = "SELECT id, home_team, away_team, game_date, result FROM matches where game_date >= '2024-04-11' order by game_date"
    upcoming_df = pd.read_sql(query, conn)
    upcoming_df = upcoming_df.drop(columns=['game_date'])
    upcoming_df.set_index('id', inplace=True)
    conn.close()
    matches_df, upcoming_df = add_aditional_data(matches_df, upcoming_df)
    print(matches_df.columns)
    print(upcoming_df.columns)
    #print(matches_df)
    #print(upcoming_df)
    #print(matches_df.head)
    #print(teams_df.head)
    #print(teams_df[teams_df['id'] == 40]) - tak id druzyny
    #match[3] - home team
    #match[4] - away team
    #ratings = rating_wrapper(matches_df, teams_df, 'ELO') # Pierwsza implementacja rankingu ELO
    #Model(matches_df, upcoming_df, True)
    #print(matches_df)
if __name__ == '__main__':
    main()