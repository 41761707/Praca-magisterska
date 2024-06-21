import numpy as np
import pandas as pd
import sys
import db_module
from sklearn.metrics import confusion_matrix

def read_data(goals_txt, winner_txt, btts_txt):
    winner_results = []
    goals_results = []
    btts_results = []
    try:
        with open(goals_txt, 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                # Usunięcie białych znaków (np. nowych linii) z końca linii
                line = line.strip()
                # Podzielenie linii względem separatora ;
                parts = line.split(';')
                array = [parts[0], int(parts[1]), parts[2]]
                # Dodanie wyników do listy
                goals_results.append(array)
    except FileNotFoundError:
        print(f"Plik {goals_txt} nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    try:
        with open(winner_txt, 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                # Usunięcie białych znaków (np. nowych linii) z końca linii
                line = line.strip()
                # Podzielenie linii względem separatora ;
                parts = line.split(';')
                # Dodanie wyników do listy
                array = [parts[0], float(parts[1]), float(parts[2]), float(parts[3])]
                winner_results.append(array)
    except FileNotFoundError:
        print(f"Plik {winner_txt} nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    try:
        with open(btts_txt, 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                # Usunięcie białych znaków (np. nowych linii) z końca linii
                line = line.strip()
                # Podzielenie linii względem separatora ;
                parts = line.split(';')
                # Dodanie wyników do listy
                array = [int(parts[0]), float(parts[1]), float(parts[2])]
                btts_results.append(array)
    except FileNotFoundError:
        print(f"Plik {winner_txt} nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    
    return goals_results, winner_results, btts_results

def main():
    goals_results = []
    winner_results = []
    btts_results = []
    goals_txt = sys.argv[1]
    winner_txt = sys.argv[2]
    btts_txt = sys.argv[3]
    goals_results, winner_results, btts_results = read_data(goals_txt, winner_txt, btts_txt)
    conn = db_module.db_connect()
    #POL1 - 1
    #POL2 - 21
    #ENG1 - 2
    #ENG2 - 8
    #FRA1 - 3
    #FRA2 - 13
    #ITA1 - 5
    #ITA2 - 26
    #ESP1 - 6
    #ESP2 - 14
    #GER1 - 4
    #GER2 - 20
    query = "SELECT m.id, t1.name, t2.name, m.league, m.season, m.home_team_goals, m.away_team_goals, m.result FROM matches m join teams t1 on m.home_team = t1.id join teams t2 on m.away_team = t2.id where game_date and season in (1,2) order by game_date"
    upcoming_df = pd.read_sql(query, conn)
    upcoming_np = upcoming_df.to_numpy()
    goals_results = sorted(goals_results, key=lambda x: x[0])
    winner_results = sorted(winner_results, key=lambda x: x[0])
    btts_results = sorted(btts_results, key=lambda x: x[0])
    print(goals_results[:5])
    print(winner_results[:5])
    print(btts_results[:5])
    predicted_goals = []
    predicted_ou = []
    predicted_winner = []
    predicted_btts = []

    actual_goals = []
    actual_ou = []
    actual_winner = []
    actual_btts = []
    max_iter = min(5589, len(goals_results))
    for i in range(max_iter):
        for j in range(len(upcoming_np)):
            if int(goals_results[i][0]) == int(upcoming_np[j][0]):
                # L.GOLI
                #print("HALO")
                predicted_goals.append(int(goals_results[i][1]))
                sum_goals = int(upcoming_np[j][5]) + int(upcoming_np[j][6])
                actual_goals.append(sum_goals)

                #OU

                local_pred_ou = 'U' if int(goals_results[i][1]) < 2.5 else 'O'
                local_actual_ou = 'U' if sum_goals < 2.5 else 'O'

                predicted_ou.append(local_pred_ou)
                actual_ou.append(local_actual_ou)
            if int(winner_results[i][0]) == int(upcoming_np[j][0]):
                results = [winner_results[i][1], winner_results[i][2], winner_results[i][3]]
                max_value = np.max(results) 
                max_index = results.index(max_value) 
                predicted_winner.append(max_index)

                if upcoming_np[j][7] == '1':
                    actual_winner.append(0)
                elif upcoming_np[j][7] == '2':
                    actual_winner.append(2)
                else:
                    actual_winner.append(1)
            if int(btts_results[i][0]) == int(upcoming_np[j][0]):
                results = [btts_results[i][1], btts_results[i][2]]
                max_value = np.max(results) 
                max_index = results.index(max_value) 
                observed_btts = 0 if int(upcoming_np[j][5]) > 0 and int(upcoming_np[j][6]) > 0 else 1
                predicted_btts.append(max_index)
                actual_btts.append(observed_btts)

    print(actual_goals[:5])
    print(predicted_goals[:5])
    print("GOLE")
    print(confusion_matrix(actual_goals, predicted_goals))
    print("OU")
    print(confusion_matrix(actual_ou, predicted_ou, labels=["U", "O"]))
    print("WINNER")
    print(confusion_matrix(actual_winner, predicted_winner))
    print("BTTS")
    print(confusion_matrix(actual_btts, predicted_btts))

if __name__ == '__main__':
    main()