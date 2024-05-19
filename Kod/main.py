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
        password="placeholder",
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

def accuracy_test(matches_df, teams_dict, teams_df, upcoming_df, key):
    filtered_matches_df = matches_df.loc[(matches_df['home_team'] == key) | (matches_df['away_team'] == key)]
    model_type = 'goals_total'
    data = dataprep_module.DataPrep(filtered_matches_df , teams_df, upcoming_df)
    data.prepare_predict_goals()
    #data.prepare_predict_winner()

    _, _, _, model_columns_df = data.get_data() 
    predict_model = model_module.Model(model_type, model_columns_df, 9, 10, 'old')
    predict_model.create_window()
    predict_model.window_to_numpy(1)
    predict_model.divide_set()
    predict_model.train_goals_total_model()
    exact_accuracy, ou_accuracy, exact, ou, predictions = predict_model.predict_external_graphs(teams_dict[key])
    print("{};{};{};{};{};{}".format(key,
                                     exact_accuracy,
                                     ou_accuracy,
                                     exact, 
                                     ou, 
                                     predictions))

def predict_chosen_matches(data, schedule, predict_model, teams_dict):
    external_tests = data.generate_external_test(schedule)
    external_tests_np = np.array(external_tests)
    #real_results = [0, 5, 2, 5, 3, 4, 1, 3, 2 ,2, 0, 2, 4]
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
    #league = league_module.League(matches_df, teams_df)



##
# Funkcja odpowiedzialna za rozruch oraz kontrolowanie przepływu programu
def main():
    matches_df, teams_df, upcoming_df = get_values()
    rating_factory = ratings_module.RatingFactory()
    my_rating = rating_factory.create_rating("MyRating", matches_df, teams_df)
    my_rating.rating_wrapper()
    matches_df, _, teams_dict , _ = my_rating.get_data()
    #Filtrowanie zbioru względem danej drużyny
    #filtered_matches_df = matches_df.loc[(matches_df['home_team'] == 154) | (matches_df['away_team'] == 154)]
    #Wypisywanie drużyn oraz ich rankingów
    #my_rating.print_ratings()
    #my_rating.print_powers()
    data = dataprep_module.DataPrep(matches_df, teams_df, upcoming_df)
    model_type = sys.argv[1]
    model_mode = sys.argv[2]
    #team_id = int(sys.argv[3])
    #accuracy_test(matches_df, teams_dict, teams_df, upcoming_df, int(sys.argv[3]))
    #print(matches_df.head)
    if model_type == 'goals_total':
        data.prepare_predict_goals()
        _, _, _, model_columns_df = data.get_data() 
        predict_model = model_module.Model(model_type, model_columns_df, 9, 10, model_mode)
        predict_model.create_window()
        predict_model.window_to_numpy(1)
        predict_model.divide_set()
        predict_model.train_goals_total_model()
        predict_model.predict_test()

    if model_type == 'goals_teams':
        data.prepare_predict_team_goals()
        _, _, _, model_columns_df = data.get_data() 
        predict_model = model_module.Model(model_type, model_columns_df, 9, 10, model_mode)
        predict_model.create_window()
        predict_model.window_to_numpy(3)
        predict_model.divide_set()
        predict_model.train_goals_teams_model()
        predict_model.predict_test()

    #Mock testing
    '''schedule = [[124, 147], [121, 321], [138, 129], [127, 140], [134, 143], [132, 133], [135, 142], [139, 125], [141, 122], [123, 144], [11, 6], [7, 14], [205, 198],
                [157, 158], [159, 168], [155, 180], [160, 156], [183, 164], [165, 154], [169, 163], [161, 162], [166, 167],
                [16, 17], [1, 10], [9, 2], [28, 21], [32, 23], [24, 30],
                [213, 202], [207, 201], [323,224],
                [280, 293], [282, 286], [327, 278], [291, 300], [288, 292]]''' #18.05.2024
    
    schedule = [[53, 66], [65, 58], [59, 56], [74, 67], [61, 63], [64, 54], [51, 60], [68, 62], [52, 57], [70, 55], #Premier League
                [136, 107], [106, 116], [109, 113], [114, 112], [111, 119], [126, 105], [110, 120], [115, 108], [117, 118], #Ligue 1
                [264, 268], [259, 263], [257, 267], [262, 260], [270, 284], [277, 269], [265, 273], [272, 266], [261, 258], #La Liga 
                [281, 290], [303, 274], [294, 326], #LaLiga 2
                [174, 188], [322, 186], [173, 170], [178, 177], [176, 182], [187, 181], [194, 171], [189, 175], [184, 185], #2. Bundesliga
                [13, 4], [15, 5], [12, 3], #Ekstraklasa 
                [319, 35], [22, 33], [20, 27], #1 Liga Fortuna
                [210, 218], [208, 226], [209, 211], [200, 199], [203, 219] #Serie A
                ]
    predict_chosen_matches(data, schedule, predict_model, teams_dict)

if __name__ == '__main__':
    main()