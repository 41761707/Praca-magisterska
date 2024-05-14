import mysql.connector
import pandas as pd

import ratings_module
import model_module 
import dataprep_module
## @package main
# Moduł main zawiera funkcje i procedury odpowiedzialne za interakcję z użytkownikiem 
# oraz inicjalizację jak i poprawny przepływ działania programu.

##
#   Funkcja odpowiadająca za połączenie z bazą danych
def db_connect():
    # Połączenie z bazą danych MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radikey",
        database="ekstrabet"
    )
    return conn

##
# Funkcja odpowiadająca za pobranie informacji z bazy danych
def get_values():
    conn = db_connect()
    query = "SELECT * FROM matches where game_date < '2024-04-11' order by game_date"
    matches_df = pd.read_sql(query, conn)
    query = "SELECT id, name FROM teams "
    teams_df = pd.read_sql(query, conn)
    teams_df.set_index('id', inplace=True)
    matches_df['result'] = matches_df['result'].replace({'X': 0, '1' : 1, '2' : 2})
    matches_df = matches_df.drop(columns=['game_date'])
    matches_df.set_index('id', inplace=True)
    query = "SELECT id, home_team, away_team, game_date, result FROM matches where game_date >= '2024-04-11' order by game_date"
    upcoming_df = pd.read_sql(query, conn)
    upcoming_df = upcoming_df.drop(columns=['game_date'])
    upcoming_df.set_index('id', inplace=True)
    conn.close()
    return matches_df, teams_df, upcoming_df

##
# Funkcja odpowiedzialna za rozruch oraz kontrolowanie przepływu programu
def main():
    #Pobierz dane z bazy danych
    matches_df, teams_df, upcoming_df = get_values()
    #Przygotowanie danych
    data = dataprep_module.DataPrep(matches_df, teams_df, upcoming_df)
    data.prepare_predict()
    _, _, _, model_columns_df = data.get_data() 
    #Wygenerowanie cech + rankingow dla modelu
    #team_ratings = ratings(matches_df, teams_df)
    #Generowanie lub trenowanie modelu
    predict_model = model_module.Model(model_columns_df, 4, '1')
    predict_model.create_window()
    predict_model.window_to_numpy()
    predict_model.divide_set()
    predict_model.train_model()
    #Przewidywania
    #Dump do pliku / wykresy
    #print(matches_df.head)
    #print(teams_df.head)
    #print(upcoming_df.head)
    #print(model_columns_df.head)

if __name__ == '__main__':
    main()