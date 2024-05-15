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
        

    '''def prepare_predict(self):
        for index, match in self.matches_df.iterrows():
            #self.model_columns.append({'id' : index, 'home_rating' : 0, 'away_rating' : 0, 'goals' : self.matches_df.loc[index, 'home_team_goals'] + self.matches_df.loc[index, 'away_team_goals']})
            #self.model_columns.append({'id' : index, 'goals' : self.matches_df.loc[index, 'home_team_goals'] + self.matches_df.loc[index, 'away_team_goals']})
            self.model_columns.append({'id' : index, 
                                       'home_team' : self.matches_df.loc[index, 'home_team'],
                                       'away_team' : self.matches_df.loc[index, 'away_team'],
                                       'home_rating' : self.matches_df.loc[index, 'home_rating'],
                                       'away_rating' : self.matches_df.loc[index, 'away_rating'],
                                       'home_team_sc' : self.matches_df.loc[index, 'home_team_sc'],
                                       'away_team_sc' : self.matches_df.loc[index, 'away_team_sc'],
                                       'home_team_sog' : self.matches_df.loc[index, 'home_team_sog'],
                                       'away_team_sog' : self.matches_df.loc[index, 'away_team_sog'],
                                       'goals' : self.matches_df.loc[index, 'home_team_goals'] + self.matches_df.loc[index, 'away_team_goals']})
        self.model_columns_df = pd.DataFrame(self.model_columns)
        self.model_columns_df.set_index('id', inplace=True)'''
    
    def prepare_predict(self):
        for index, match in self.matches_df.iterrows():
            self.model_columns.append({'id' : index, 
                                       'home_rating' : self.matches_df.loc[index, 'home_rating'],
                                       'away_rating' : self.matches_df.loc[index, 'away_rating'],
                                       'goals' : self.matches_df.loc[index, 'home_team_goals'] + self.matches_df.loc[index, 'away_team_goals']})
        self.model_columns_df = pd.DataFrame(self.model_columns)
        self.model_columns_df.set_index('id', inplace=True)

    '''def turn_last_into_predictable(self, matches_df):
        for index, match in self.matches_df.iterrows():
            self.model_columns.append({'id' : index, 
                                       'home_rating' : self.matches_df.loc[index, 'home_rating'],
                                       'away_rating' : self.matches_df.loc[index, 'away_rating'],
                                       'goals' : self.matches_df.loc[index, 'home_team_goals'] + self.matches_df.loc[index, 'away_team_goals']})
        self.model_columns_df = pd.DataFrame(self.model_columns)
        self.model_columns_df.set_index('id', inplace=True)'''
    
    def turn_match_into_numpy(self, match):
        return [match['home_rating'], match['away_rating'], match['home_team_goals'] + match['away_team_goals']]
    
    def return_last_matches(self, amount, team_id):
        #filtered_rows = self.model_columns_df[(self.model_columns_df['home_team'] == int(team_id)) | (self.model_columns_df['away_team'] == int(team_id))].tail(int(amount))
        filtered_rows = self.matches_df[(self.matches_df['home_team'] == int(team_id)) | (self.matches_df['away_team'] == int(team_id))].tail(int(amount))
        return filtered_rows
    
    def generate_external_test(self, schedule):
        external_test = []
        for pair in schedule:
            match_schedule = []
            home_team_df = self.return_last_matches(4, pair[0])
            away_team_df = self.return_last_matches(4, pair[1])
            home_team_schedule = []
            away_team_schedule = []
            for _, match in home_team_df.iterrows():
                home_team_schedule.append(self.turn_match_into_numpy(match))
            for _, match in away_team_df.iterrows():
                away_team_schedule.append(self.turn_match_into_numpy(match))
            for i in range(len(home_team_schedule)):
                match_schedule.append(home_team_schedule[i])
                match_schedule.append(away_team_schedule[i])
            external_test.append(match_schedule)
        return external_test
    ##
    # Funkcja odpowiadająca za zwrócenie przygotowanych danych do dalszych operacji
    # @return matches_df Lista rozegranych meczów
    # @return teams_df Lista wszystkich drużyn w bazie danych
    # @return upcoming_df Lista przyszłych meczów do rozpatrzenia
    def get_data(self):
        return self.matches_df, self.teams_df, self.upcoming_df, self.model_columns_df