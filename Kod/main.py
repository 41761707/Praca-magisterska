import mysql.connector
import pandas as pd
import numpy as np
import sys

#Moduły
import ratings_module
import model_module 
import dataprep_module
import views_module
import league_module
import bet_module
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
    matches_df['result'] = matches_df['result'].replace({'X': 0, '1' : 1, '2' : -1}) # 0 - remis, 1 - zwyciestwo gosp. -1 - zwyciestwo goscia
    #matches_df = matches_df.drop(columns=['game_date'])
    matches_df.set_index('id', inplace=True)
    query = "SELECT id, home_team, away_team, game_date, result FROM matches where game_date >= '2024-04-11' order by game_date"
    upcoming_df = pd.read_sql(query, conn)
    upcoming_df = upcoming_df.drop(columns=['game_date'])
    upcoming_df.set_index('id', inplace=True)
    conn.close()
    return matches_df, teams_df, upcoming_df

'''def tmp_test(matches_df, teams_dict, teams_df, upcoming_df, key):
    filtered_matches_df = matches_df.loc[(matches_df['home_team'] == key) | (matches_df['away_team'] == key)]
    model_type = 'goals_total'
    data = dataprep_module.DataPrep(filtered_matches_df , teams_df, upcoming_df)
    data.prepare_predict_goals()
    #data.prepare_predict_winner()

    _, _, _, model_columns_df = data.get_data() 
    predict_model = model_module.Model(model_type, model_columns_df, 9, 3, 'old')
    predict_model.create_window()
    predict_model.window_to_numpy()
    predict_model.divide_set()
    predict_model.train_goals_total_model()
    exact_accuracy, ou_accuracy, exact, ou, predictions = predict_model.predict_external_graphs(teams_dict[key])
    print("{};{};{};{};{};{}".format(key,
                                     exact_accuracy,
                                     ou_accuracy,
                                     exact, 
                                     ou, 
                                     predictions))'''



##
# Funkcja odpowiedzialna za rozruch oraz kontrolowanie przepływu programu
def main():
    #Pobierz dane z bazy danych
    matches_df, teams_df, upcoming_df = get_values()
    #print(upcoming_df.head)
    #Wygenerowanie cech + rankingow dla modelu
    rating_factory = ratings_module.RatingFactory()
    # Tworzenie obiektu klasy EloRating
    my_rating = rating_factory.create_rating("MyRating", matches_df, teams_df)
    # Wywołanie funkcji rating_wrapper
    my_rating.rating_wrapper()
    matches_df, _, teams_dict , _ = my_rating.get_data()

    #tmp_test(matches_df, teams_dict, teams_df, upcoming_df, int(sys.argv[1]))
    #Filtrowanie zbioru względem danej drużyny
    #filtered_matches_df = matches_df.loc[(matches_df['home_team'] == 154) | (matches_df['away_team'] == 154)]
    #Wypisywanie drużyn oraz ich rankingów
    #my_rating.print_ratings()

    #Przygotowanie danych
    #Jakiego typu predykcji dokonujemy? Mozliwosci:
    # goals_total - Liczba bramek w meczu
    # team_goals - Liczba bramek danego zespołu
    # winnter - predykcja 1X2
    # corner_total - Liczba rzutow roznych w meczu
    # team_goals - Liczba rzutow roznych danego zespolu
    # fouls_total - Liczba fauli w danym meczu
    # team_fouls - Liczba fauli danej druzyny
    # offsides_total - Liczba spalonych w meczu
    # offsides_team - Liczba spalonych danej drużyny
    model_type = 'goals_total'
    data = dataprep_module.DataPrep(matches_df, teams_df, upcoming_df)
    data.prepare_predict_goals()
    #data.prepare_predict_winner()

    _, _, _, model_columns_df = data.get_data() 
    #Generowanie lub trenowanie modelu
    predict_model = model_module.Model(model_type, model_columns_df, 9, 3, 'old')
    predict_model.create_window()
    predict_model.window_to_numpy()
    predict_model.divide_set()
    predict_model.train_goals_total_model()
    #predict_model.train_winner_model()
    #predict_model.predict_test()

    #Mock testing
    
    schedule = [[48,19]]
    external_tests = data.generate_external_test(schedule)
    external_tests_np = np.array(external_tests)
    #real_results = [1,5,0,3,2,5,4,2,2]
    predictions = predict_model.make_predictions(external_tests_np)
    #ou_accuracy = 0
    #exact_accuracy = 0
    for i in range(len(predictions)):
        generated_ou = "U" if predictions[i] < 2.5 else "O"
        #real_ou = "U" if real_results[i] < 2.5 else "O"
        print("Spotkanie: {} - {}".format(teams_dict[schedule[i][0]], teams_dict[schedule[i][1]]))
        print("Wygenerowana liczba bramek w spotkaniu: {} - O/U: {}".format(predictions[i], generated_ou))
        #print("Prawdziwy wynik spotkania: {} - O/U: {}".format(real_results[i], real_ou))
        #if generated_ou == real_ou:
        #    ou_accuracy = ou_accuracy + 1
        #if predictions[i] == real_results[i]:
        #    exact_accuracy = exact_accuracy + 1
    #print("Dokładność predykcji dokładnych wyników: {:.2f}%".format((exact_accuracy / len(predictions)) * 100))
    #print("Dokładność predykcji Over/Under: {:.2f}%".format((ou_accuracy / len(predictions)) * 100))
    #Wypisywanie ostatnich 4 spotkan zespolu o id 7
    #data.return_last_matches(4,7)
    #Generowanie meczów do przewidzenia
    #league = league_module.League(matches_df, teams_df)'''

if __name__ == '__main__':
    main()