import mysql.connector
import pandas as pd
import numpy as np

import ratings_module
import model_module 
import dataprep_module
import views_module
import league_module
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
        password="PLACEHOLDER",
        database="ekstrabet"
    )
    return conn

##
# Funkcja odpowiadająca za pobranie informacji z bazy danych
def get_values():
    conn = db_connect()
    query = "SELECT * FROM matches where game_date < '2024-04-11' order by game_date"
    matches_df = pd.read_sql(query, conn)
    query = "SELECT id, name FROM teams"
    teams_df = pd.read_sql(query, conn)
    #teams_df.set_index('id', inplace=True)
    matches_df['result'] = matches_df['result'].replace({'X': 0, '1' : 1, '2' : -1})
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
    #Wygenerowanie cech + rankingow dla modelu
    rating_factory = ratings_module.RatingFactory()
    # Tworzenie obiektu klasy EloRating
    elo_rating = rating_factory.create_rating("Elo", matches_df, teams_df)
    # Wywołanie funkcji rating_wrapper
    elo_rating.rating_wrapper()
    matches_df, _, teams_dict , _ = elo_rating.get_data()

    #Filtrowanie zbioru względem danej drużyny
    #filtered_matches_df = matches_df.loc[(matches_df['home_team'] == 154) | (matches_df['away_team'] == 154)]
    #Wypisywanie drużyn oraz ich rankingów
    #elo_rating.print_ratings()


    #Przygotowanie danych
    #Jakiego typu predykcji dokonujemy? Mozliwosci:
    # goals_total - Liczba bramek w meczu
    # team_goals - Liczba bramek danego zespołu
    # winnter - predyckaj 1X2
    # corner_total - Liczba rzutow roznych w meczu
    # team_goals - Liczba rzutow roznych danego zespolu
    # fouls_total - Liczba fauli w danym meczu
    # team_fouls - Liczba fauli danej druzyny
    # offsides_total - Liczba spalonych w meczu
    # offsides_team - Liczba spalonych danej drużyny
    model_type = 'goals_total'
    data = dataprep_module.DataPrep(matches_df, teams_df, upcoming_df)
    data.prepare_predict()

    schedule = [[15,16],[6,17],[11,12],[14,3],[4,5],[18,10],[2,13],[1,7],[9,8]]
    external_tests = data.generate_external_test(schedule)
    external_tests_np = np.array(external_tests)
    real_results = [1,5,0,3,2,5,4,2,2]
    #Wypisywanie ostatnich 4 spotkan zespolu o id 7
    #data.return_last_matches(4,7)
    #Generowanie meczów do przewidzenia:
    #league = league_module.League(matches_df, teams_df)

    _, _, _, model_columns_df = data.get_data() 

    #Generowanie lub trenowanie modelu
    predict_model = model_module.Model(model_columns_df, 9, 3, 'new')
    predict_model.create_window()
    predict_model.window_to_numpy()
    predict_model.divide_set()
    predict_model.train_goals_total_model()
    predictions = predict_model.make_predictions(external_tests_np)
    for i in range(len(predictions)):
        print("Spotkanie: {} - {}".format(teams_dict[external_tests[i][0]], teams_dict[external_tests[i][1]]))
        print("Wygenerowana liczba bramek w spotkaniu: {}".format(predictions[i]))
        print("Prawdziwy wynik spotkania: {}".format(real_results[i]))

if __name__ == '__main__':
    main()