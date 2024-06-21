import numpy as np
import db_module
import pandas as pd
import sys

def ranked_probability_score(pred, true):
    pred = np.array(pred)
    true = np.array(true)
    
    n_samples, n_categories = pred.shape
    
    rps = 0.0
    for i in range(n_samples):
        cum_pred = np.cumsum(pred[i])
        cum_true = np.cumsum(true[i])
        rps += np.sum((cum_pred - cum_true) ** 2)
    
    rps /= n_samples
    return rps

def read_data(winner_txt):
    winner_results = []
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

    
    return winner_results

def main():
    conn = db_module.db_connect()
    pred = []
    true = []
    winner_txt = sys.argv[1]
    query = "SELECT m.id, m.result FROM matches m join teams t1 on m.home_team = t1.id join teams t2 on m.away_team = t2.id where game_date  order by game_date"
    upcoming_df = pd.read_sql(query, conn)
    upcoming_np = upcoming_df.to_numpy()
    winner_results = read_data(winner_txt)
    #pred = [[0.6, 0.3, 0.1], [0.2, 0.3, 0.5]]
    #true = [[1, 0, 0], [0, 0, 1]]
    for i in range(1000): #range(len(winner_results)):
        for j in range(len(upcoming_df)):
            if int(winner_results[i][0]) == int(upcoming_np[j][0]):
                pred.append([winner_results[i][1] / 100, winner_results[i][2] / 100, winner_results[i][3] / 100])
                if upcoming_np[j][1] == "1":
                    true.append([1, 0, 0])
                if upcoming_np[j][1] == "X":
                    true.append([0, 1, 0])
                else:
                    true.append([0, 0, 1])
    print(winner_results[:5])
    print(pred[:5])
    print(true[:5])   


    rps_value = ranked_probability_score(pred, true)
    print(f"Ranked Probability Score: {rps_value}")

if __name__ == '__main__':
    main()