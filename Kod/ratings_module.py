import pandas as pd
import numpy as np
class MyRating:
    def __init__(self, matches_df, teams_df):
        # implementacja obliczania rankingu PI
            self.matches_df = matches_df
            self.teams_df = teams_df
            self.teams_dict = {}
            self.ratings = {}
            self.powers = {}

    def outcome_probability(self, team_a, team_b):
        return 1 / (1 + 10 ** (-(team_a - team_b) / 400))
    
    def update_rating(self, team_rating, win_ppb, team_result, const):
        return team_rating + const * (team_result - win_ppb) #(1-card)
    
    def evaluate_const(self, goal_diff):
        constant = 32 #Podrasowana stała
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
    
    def update_home_team(self, i_h_att, i_h_def, i_a_att, j_a_def, j_a_att, i_a_def, s_h, s_a, l, phi_1):
        i_h_att = max((i_h_att + l * phi_1 * (s_h - ((i_h_att + j_a_def) / 2))), 0)
        i_a_att = max((i_a_att + l * (1 - phi_1) * (s_h - ((i_h_att + j_a_def) / 2))), 0)
        i_h_def = max((i_h_def + l * phi_1 * (s_a - ((j_a_att + i_h_def) / 2))), 0)
        i_a_def = max((i_a_def + l * (1 - phi_1) * (s_a - ((j_a_att + i_h_def) / 2))), 0)

        return i_h_att, i_a_att, i_h_def, i_a_def 
    
    def update_away_team(self, j_a_att, j_h_att, j_a_def, j_h_def, i_h_def, i_h_att, s_h, s_a, l,phi_2):
        j_a_att = max((j_a_att + l * phi_2 * (s_a - ((j_a_att + i_h_def) / 2))), 0)
        j_h_att = max((j_h_att + l * (1 - phi_2) * (s_a - ((j_a_att + i_h_def) / 2))), 0)
        j_a_def = max((j_a_def + l * phi_2 * (s_h - ((i_h_att + j_a_def) / 2))), 0)
        j_h_def = max((j_h_def + l * (1 - phi_2) * (s_h - ((i_h_att + j_a_def) / 2))), 0)

        return j_a_att, j_h_att, j_a_def, j_h_def
    
    def rating_wrapper(self):
        starting_rating = 800
        for team in self.teams_df.values:
            if team[0] not in self.ratings:
                self.ratings[team[0]] = starting_rating
                self.powers["{}h_att".format(team[0])] = 0
                self.powers["{}h_def".format(team[0])] = 0
                self.powers["{}a_att".format(team[0])] = 0
                self.powers["{}a_def".format(team[0])] = 0
            if team[1] not in self.teams_dict:
                self.teams_dict[team[0]] = team[1]
        for index, _ in self.matches_df.iterrows():
            s_h = int(self.matches_df.loc[index, 'home_team_goals']) / (int(self.matches_df.loc[index, 'home_team_sc']) + 1) * 1.0
            s_a = int(self.matches_df.loc[index, 'away_team_goals']) / (int(self.matches_df.loc[index, 'away_team_sc']) + 1) * 1.0
            i_h_att = float(self.powers["{}h_att".format(self.matches_df.loc[index, 'home_team'])])
            i_h_def = float(self.powers["{}h_def".format(self.matches_df.loc[index, 'home_team'])])
            i_a_att = float(self.powers["{}a_att".format(self.matches_df.loc[index, 'home_team'])])
            i_a_def = float(self.powers["{}a_def".format(self.matches_df.loc[index, 'home_team'])])
            j_h_att = float(self.powers["{}h_att".format(self.matches_df.loc[index, 'away_team'])])
            j_h_def = float(self.powers["{}h_def".format(self.matches_df.loc[index, 'away_team'])])
            j_a_att = float(self.powers["{}a_att".format(self.matches_df.loc[index, 'away_team'])])
            j_a_def = float(self.powers["{}a_def".format(self.matches_df.loc[index, 'away_team'])])
            goal_diff = abs(self.matches_df.loc[index, 'home_team_goals'] - self.matches_df.loc[index, 'away_team_goals'])
            home_rating, away_rating = self.main_rating(self.ratings, 
                                                       self.matches_df.loc[index, 'home_team'], 
                                                       self.matches_df.loc[index, 'away_team'], 
                                                       self.matches_df.loc[index, 'result'], 
                                                       goal_diff,
                                                       self.matches_df.loc[index, 'home_team_rc'],
                                                       self.matches_df.loc[index, 'away_team_rc'],
                                                       0)
            
            i_h_att, i_a_att, i_h_def, i_a_def = self.update_home_team(i_h_att, i_h_def, i_a_att, j_a_def, j_a_att, i_a_def, s_h, s_a, 0.5, 0.5)
            j_a_att, j_h_att, j_a_def, j_h_def = self.update_away_team(j_a_att, j_h_att, j_a_def, j_h_def, i_h_def, i_h_att, s_h, s_a, 0.5, 0.5)
            self.matches_df.at[index, 'home_rating'] = home_rating
            self.matches_df.at[index, 'away_rating'] = away_rating

            self.matches_df.at[index, 'home_home_att_power'] =i_h_att
            self.matches_df.at[index, 'home_home_def_power'] =i_h_def
            self.matches_df.at[index, 'home_away_att_power'] =i_a_att
            self.matches_df.at[index, 'home_away_def_power'] =i_a_def

            self.matches_df.at[index, 'away_home_att_power'] =j_h_att
            self.matches_df.at[index, 'away_home_def_power'] =j_h_def
            self.matches_df.at[index, 'away_away_att_power'] =j_a_att
            self.matches_df.at[index, 'away_away_def_power'] =j_a_def
            self.powers["{}h_att".format(self.matches_df.loc[index, 'home_team'])] = i_h_att
            self.powers["{}h_def".format(self.matches_df.loc[index, 'home_team'])] = i_h_def
            self.powers["{}a_att".format(self.matches_df.loc[index, 'home_team'])] = i_a_att
            self.powers["{}a_def".format(self.matches_df.loc[index, 'home_team'])] = i_a_def


            self.powers["{}h_att".format(self.matches_df.loc[index, 'away_team'])] = j_h_att
            self.powers["{}h_def".format(self.matches_df.loc[index, 'away_team'])] = j_h_def
            self.powers["{}a_att".format(self.matches_df.loc[index, 'away_team'])] = j_a_att
            self.powers["{}a_def".format(self.matches_df.loc[index, 'away_team'])] = j_a_def
            #print(self.powers["{}h_att".format(self.matches_df.loc[index, 'home_team'])])
            #print(self.powers["{}h_att".format(self.matches_df.loc[index, 'away_team'])])
        #print(self.powers)
    def get_data(self):
        return self.matches_df, self.teams_df, self.teams_dict, self.powers
    
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

# Użycie fabryki do tworzenia instancji różnych metod obliczania rankingu
#elo_calculator = RatingFactory.create_rating("Elo", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)
#berrar_calculator = RatingFactory.create_rating("Berrar", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)
#gap_calculator = RatingFactory.create_rating("GAP", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)
#pi_calculator = RatingFactory.create_rating("PI", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)