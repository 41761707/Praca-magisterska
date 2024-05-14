import numpy as np
import pandas as pd

## @package dataprep
# Moduł DataPrep zawiera funkcje i klasy służące do przygotowania danych do dalszych operacji w programie.
# Wymagane zależności: 
# Moduł 'pandas'
# Moduł 'numpy'

##
# Klasa Data odpowiedzialna za przetwarzanie danych i przygotowanie ich do dalszych operacji.
class DataPrep:
    ##
    # Konstruktor klasy DataPrep
    # @param matches_df Lista rozegranych meczów
    # @param teams_df Lista wszystkich drużyn w bazie danych
    # @param upcoming_df Lista przyszłych meczów do rozpatrzenia
    def __init__(self, matches_df, teams_df, upcoming_df):
        self.matches_df = matches_df
        self.teams_df = teams_df
        self.upcoming_df = upcoming_df
        self.model_columns = []
        self.model_columns_df = []
        

    def prepare_predict(self):
        for index, match in self.matches_df.iterrows():
            #self.model_columns.append({'id' : index, 'home_rating' : 0, 'away_rating' : 0, 'goals' : self.matches_df.loc[index, 'home_team_goals'] + self.matches_df.loc[index, 'away_team_goals']})
            self.model_columns.append({'id' : index, 'goals' : self.matches_df.loc[index, 'home_team_goals'] + self.matches_df.loc[index, 'away_team_goals']})
        self.model_columns_df = pd.DataFrame(self.model_columns)
        self.model_columns_df.set_index('id', inplace=True)
    
    ##
    # Funkcja odpowiadająca za zwrócenie przygotowanych danych do dalszych operacji
    # @return matches_df Lista rozegranych meczów
    # @return teams_df Lista wszystkich drużyn w bazie danych
    # @return upcoming_df Lista przyszłych meczów do rozpatrzenia
    def get_data(self):
        return self.matches_df, self.teams_df, self.upcoming_df, self.model_columns_df