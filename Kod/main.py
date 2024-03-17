import sys
import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
'''
    Główny program projektu predykcji meczów
    Autor: Radikey
    Data rozpoczęcia: 09.12.2023
    Wersja: 1.0.0

    Szkielet projektu:
        1. Baza danych do przechowywania informacji 
        2. Model, który w odpowiedni sposób będzie informacje wczytywał oraz wnioskował
        3. Wątek do generalnej obsługi programu
'''

def db_connect():
    # Połączenie z bazą danych MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="PLACEHOLDER",
        database="ekstrabet"
    )
    return conn

def elo_rating():
    pass
def main():
    conn = db_connect()
    query = "SELECT * FROM matches where league in (1,2)"
    matches_df = pd.read_sql(query, conn)
    query = "SELECT id, name FROM teams where country = 1"
    teams_df = pd.read_sql(query, conn)
    matches_df['result'] = matches_df['result'].replace({'X': 0, '1' : 1, '2' : 2})
    #print(matches_df.head)
    #print(teams_df.head)
    #print(teams_df[teams_df['id'] == 40]) - tak id druzyny
    conn.close()
if __name__ == '__main__':
    main()