import numpy as np
import pandas as pd
import sys
import db_module

## @package Bet
# Moduł main zawiera funkcje odpowiedzialne za wyszukiwanie odpowiednich zakładów bukmacherskich
class Bet:
    def __init__(self):
        pass
    
    def get_odds(self):
        pass
    def compare_odds(self):
        pass

def read_data(goals_txt, winner_txt):
    winner_results = []
    goals_results = []
    try:
        with open(goals_txt, 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                # Usunięcie białych znaków (np. nowych linii) z końca linii
                line = line.strip()
                # Podzielenie linii względem separatora ;
                parts = line.split(';')
                # Dodanie wyników do listy
                goals_results.append(parts)
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
                winner_results.append(parts)
    except FileNotFoundError:
        print(f"Plik {winner_txt} nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    
    return goals_results, winner_results

def main():
    goals_results = []
    winner_results = []
    goals_txt = sys.argv[1]
    winner_txt = sys.argv[2]
    goals_results, winner_results = read_data(goals_txt, winner_txt)
    print(goals_results[:5])
    print(winner_results[:5])
    conn = db_module.db_connect()
    query = "SELECT id, home_team, away_team, league, season, home_team_goals, away_team_goals FROM matches where game_date >= '2024-04-10' and league = 1 order by game_date"
    upcoming_df = pd.read_sql(query, conn)
    upcoming_df = 
    print(upcoming_df.head(10))
    conn.close()

if __name__ == '__main__':
    main()