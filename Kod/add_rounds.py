import mysql.connector
import pandas as pd
import numpy as np

def db_connect():
    # Połączenie z bazą danych MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radikey",
        database="ekstrabet"
    )
    return conn

def get_values():
    conn = db_connect()
    query = "SELECT * FROM matches order by game_date"
    matches_df = pd.read_sql(query, conn)
    conn.close()
    return matches_df

def update_rounds(matches_df):
    team_ids = []
    season_ids = [x for x in range(1,9)]
    #Z jakiegos powodu nie ma teamu o id = 25
    for i in range(1, 328):
        if i != 25:
            team_ids.append(i)
    for team in team_ids:
        for season in season_ids: 
            current_round = 1
            team_matches_df = matches_df.loc[(matches_df['home_team'] == team) | (matches_df['away_team'] == team)]
            team_season_matches_df = team_matches_df.loc[(team_matches_df['season'] == season)]
            for index, _ in team_season_matches_df.iterrows():
                true_index = matches_df.loc[index, 'id']
                sql_statement = 'UPDATE MATCHES SET ROUND = {} WHERE ID = {};'.format(current_round, true_index)
                print(sql_statement)
                current_round = current_round + 1
    #for index, _ in matches_df.iterrows():
    #    season = matches_df.loc[index, 'season']


def main():
    matches_df = get_values()
    update_rounds(matches_df)

if __name__ == '__main__':
    main()