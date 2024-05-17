import pandas as pd
import numpy as np

class EloRating:
    def __init__(self, matches_df, teams_df):
        # implementacja obliczania rankingu Elo
            self.matches_df = matches_df
            self.teams_df = teams_df
            self.teams_dict = {}
            self.ratings = {}

    def e_step(self, r_i, r_j):
        return 1 / (1 + 10 ** (-(r_i - r_j) / 400))

    def u_step(self, r, p, a, k):
        return r + k * (a - p)
    
    def relax_coef(self):
        pass
    
    def shape_coef(self):
        pass

    def cards_coef(self):
        pass

    def evaluate_k(self, goal_diff):
        constant = 128 #Podrasowana stała
        if goal_diff == 2:
            constant = constant * 3/2
        elif goal_diff == 3:
            constant = constant * 7/4 
        elif goal_diff > 3:
            constant = constant * (7/4 + (goal_diff-3)/8)
        return constant

    def print_ratings(self):
        ratings_list = [(self.teams_dict[k],v) for k,v in self.ratings.items()]
        ratings_list.sort(key=lambda x: x[1], reverse= True)
        for item in ratings_list:
            print(item[0],": ", item[1])

    def elo_rating(self, ratings, home_team_id, away_team_id, result, goal_diff):
        k_factor = self.evaluate_k(goal_diff)
        home_team_rating = ratings[home_team_id]
        away_team_rating = ratings[away_team_id]
        home_team_ppb = self.e_step(home_team_rating, away_team_rating)
        away_team_ppb = self.e_step(away_team_rating, home_team_rating)
        #assert home_team_ppb + away_team_ppb = 1
        home_team_result = 0
        away_team_result = 0
        if result == 0:
            home_team_result = 0.5
            away_team_result = 0.5
        elif result == 1:
            home_team_result = 1
        else: 
            away_team_result = 1
        home_team_update = self.u_step(home_team_rating, home_team_ppb, home_team_result, k_factor)
        away_team_update = self.u_step(away_team_rating, away_team_ppb, away_team_result, k_factor)
        ratings[home_team_id] = home_team_update
        ratings[away_team_id] = away_team_update
        return home_team_update, away_team_update
    
    def rating_wrapper(self):
        starting_rating = 1500
        for team in self.teams_df.values:
            if team[0] not in self.ratings:
                self.ratings[team[0]] = starting_rating
            if team[1] not in self.teams_dict:
                self.teams_dict[team[0]] = team[1]
        for index, match in self.matches_df.iterrows():
            '''print(self.matches_df.loc[index, 'home_team_goals'], 
                  self.matches_df.loc[index, 'away_team_goals'], 
                  self.matches_df.loc[index, 'home_team'], 
                  self.matches_df.loc[index, 'away_team'], 
                  self.matches_df.loc[index, 'result'])'''
            goal_diff = abs(self.matches_df.loc[index, 'home_team_goals'] - self.matches_df.loc[index, 'away_team_goals'])
            home_rating, away_rating = self.elo_rating(self.ratings, 
                                                       self.matches_df.loc[index, 'home_team'], self.matches_df.loc[index, 'away_team'], self.matches_df.loc[index, 'result'], goal_diff)

            self.matches_df.at[index, 'home_rating'] = home_rating
            self.matches_df.at[index, 'away_rating'] = away_rating
            self.matches_df.at[index, 'home__home_rating'] = home_rating
            self.matches_df.at[index, 'away_away_rating'] = away_rating
    
    def get_data(self):
         return self.matches_df, self.teams_df, self.teams_dict, self.ratings
    
    def print_ratings(self):
        ratings_list = [(self.teams_dict[k],v) for k,v in self.ratings.items()]
        ratings_list.sort(key=lambda x: x[1], reverse= True)
        for item in ratings_list:
            print(item[0],": ", item[1])

class MyRating:
    def __init__(self, matches_df, teams_df):
        # implementacja obliczania rankingu PI
            self.matches_df = matches_df
            self.teams_df = teams_df
            self.teams_dict = {}
            self.ratings = {}

    def outcome_probability(self, team_a, team_b):
        return 1 / (1 + 10 ** (-(team_a - team_b) / 400))
    
    def update_rating(self, team_rating, win_ppb, team_result, const):
        return team_rating + const * (team_result - win_ppb) #(1-card)
    
    def evaluate_const(self, goal_diff):
        constant = 128 #Podrasowana stała
        if goal_diff == 2:
            constant = constant * 3/2
        elif goal_diff == 3:
            constant = constant * 7/4 
        elif goal_diff > 3:
            constant = constant * (7/4 + (goal_diff-3)/8)
        return constant
    
    def main_rating(self, 
                    ratings, 
                    home_team_id, 
                    away_team_id, 
                    result, goal_diff, 
                    home_team_cards, 
                    away_team_cards,  
                    round):
        const = self.evaluate_const(goal_diff)
        home_team_rating = ratings[home_team_id]
        away_team_rating = ratings[away_team_id]
        home_team_ppb = self.outcome_probability(home_team_rating, away_team_rating)
        away_team_ppb = self.outcome_probability(away_team_rating, home_team_rating)
        #assert home_team_ppb + away_team_ppb = 1
        home_team_result = 0
        away_team_result = 0
        if result == 0:
            home_team_result = 0.5
            away_team_result = 0.5
        elif result == 1:
            home_team_result = 1
        else: 
            away_team_result = 1
        home_team_update = self.update_rating(home_team_rating, home_team_ppb, home_team_result, const)
        away_team_update = self.update_rating(away_team_rating, away_team_ppb, away_team_result, const)
        ratings[home_team_id] = home_team_update
        ratings[away_team_id] = away_team_update
        return home_team_update, away_team_update
    
    def update_home_team(h_att_i, h_def_i, a_att_i, a_def_j, a_att_j, s_h, s_a, l, phi_1):
        h_att_i = max((h_att_i + l * phi_1 * (s_h - ((h_att_i + a_def_j) / 2))), 0)
        a_att_i = max((a_att_i + l * (1 - phi_1) * (s_h - ((h_att_i + a_def_j) / 2))), 0)
        h_def_i = max((h_def_i + l * phi_1 * (s_a - ((a_att_j + h_def_i) / 2))), 0)
        a_def_i = max((a_def_i + l * (1 - phi_1) * (s_a - ((a_att_j + h_def_i) / 2))), 0)

        return h_att_i, a_att_i, h_def_i, a_def_i 
    def update_away_team(a_att_j, h_att_j, a_def_j, h_def_j, h_def_i, h_att_i, s_h, s_a, l,phi_2):
        a_att_j = max((a_att_j + l * phi_2 * (s_a - ((a_att_j + h_def_i) / 2))), 0)
        h_att_j = max((h_att_j + l * (1 - phi_2) * (s_a - ((a_att_j + h_def_i) / 2))), 0)
        a_def_j = max((a_def_j + l * phi_2 * (s_h - ((h_att_i + a_def_j) / 2))), 0)
        h_def_j = max((h_def_j + l * (1 - phi_2) * (s_h - ((h_att_i + a_def_j) / 2))), 0)
    
    def rating_wrapper(self):
        starting_rating = 1500
        for team in self.teams_df.values:
            if team[0] not in self.ratings:
                self.ratings[team[0]] = starting_rating
            if team[1] not in self.teams_dict:
                self.teams_dict[team[0]] = team[1]
        for index, _ in self.matches_df.iterrows():
            goal_diff = abs(self.matches_df.loc[index, 'home_team_goals'] - self.matches_df.loc[index, 'away_team_goals'])
            home_rating, away_rating = self.main_rating(self.ratings, 
                                                       self.matches_df.loc[index, 'home_team'], 
                                                       self.matches_df.loc[index, 'away_team'], 
                                                       self.matches_df.loc[index, 'result'], 
                                                       goal_diff,
                                                       self.matches_df.loc[index, 'home_team_rc'],
                                                       self.matches_df.loc[index, 'away_team_rc'],
                                                       0)

            self.matches_df.at[index, 'home_rating'] = home_rating
            self.matches_df.at[index, 'away_rating'] = away_rating
            self.matches_df.at[index, 'home__home_rating'] = home_rating
            self.matches_df.at[index, 'away_away_rating'] = away_rating
            self.matches_df.at[index, 'home_att_power'] = home_rating
            self.matches_df.at[index, 'home_def_power'] = away_rating
            self.matches_df.at[index, 'away_att_power'] = home_rating
            self.matches_df.at[index, 'away_def_power'] = away_rating

    def get_data(self):
        return self.matches_df, self.teams_df, self.teams_dict, self.ratings
    
    def print_ratings(self):
        ratings_list = [(self.teams_dict[k],v) for k,v in self.ratings.items()]
        ratings_list.sort(key=lambda x: x[1], reverse= True)
        for item in ratings_list:
            print(item[0],": ", item[1])

    

class RatingFactory:
    @staticmethod
    def create_rating(method, matches_df, teams_df):
        if method == "MyRating":
            return MyRating(matches_df, teams_df)
        elif method == "Elo":
            return EloRating(matches_df, teams_df)
        else:
            raise ValueError("Nieznana metoda obliczania rankingu")

# Użycie fabryki do tworzenia instancji różnych metod obliczania rankingu
#elo_calculator = RatingFactory.create_rating("Elo", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)
#berrar_calculator = RatingFactory.create_rating("Berrar", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)
#gap_calculator = RatingFactory.create_rating("GAP", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)
#pi_calculator = RatingFactory.create_rating("PI", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)