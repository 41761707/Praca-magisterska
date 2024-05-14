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

    def evaluate_k(self, goal_diff):
        constant = 32 #Z gory ustalone przez autora
        if goal_diff == 2:
            constant = constant * 1/2
        elif goal_diff == 3:
            constant = constant * 3/4 
        elif goal_diff > 3:
            constant = constant * 3/4 + (goal_diff-3)/8
        return constant
    
    def rating_wrapper(self):
        starting_rating = 1500
        for team in self.teams_df.values:
            if team[0] not in self.ratings:
                self.ratings[team[0]] = starting_rating
            if team[1] not in self.teams_dict:
                self.teams_dict[team[0]] = team[1]
        for index, match in self.matches_df.iterrows():
            goal_diff = abs(match[4] - match[5])
            home_rating, away_rating = self.elo_rating(self.ratings, match[2], match[3], match[-1], goal_diff)

            self.matches_df.at[index, 'rating_home'] = home_rating
            self.matches_df.at[index, 'rating_away'] = away_rating
        #ratings_list = [(self.teams_dict[k],v) for k,v in self.ratings.items()]
        #ratings_list.sort(key=lambda x: x[1], reverse= True)
        #for item in ratings_list:
        #    print(item[0],": ", item[1])

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

class BerrarRating:
    def __init__(self, matches_df, teams_df):
        # implementacja obliczania rankingu Berrar'a
            self.matches_df = matches_df
            self.teams_df = teams_df

class GAPRating:
    def __init__(self, matches_df, teams_df):
        # implementacja obliczania rankingu GAP
            self.matches_df = matches_df
            self.teams_df = teams_df

class PIRating:
    def __init__(self, matches_df, teams_df):
        # implementacja obliczania rankingu PI
            self.matches_df = matches_df
            self.teams_df = teams_df

class RatingFactory:
    @staticmethod
    def create_rating(method, matches_df, teams_df):
        if method == "Elo":
            return EloRating(matches_df, teams_df)
        elif method == "Berrar":
            return BerrarRating(matches_df, teams_df)
        elif method == "GAP":
            return GAPRating(matches_df, teams_df)
        elif method == "PI":
            return PIRating(matches_df, teams_df)
        else:
            raise ValueError("Nieznana metoda obliczania rankingu")

# Użycie fabryki do tworzenia instancji różnych metod obliczania rankingu
#elo_calculator = RatingFactory.create_rating("Elo", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)
#berrar_calculator = RatingFactory.create_rating("Berrar", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)
#gap_calculator = RatingFactory.create_rating("GAP", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)
#pi_calculator = RatingFactory.create_rating("PI", <obiekt typu pandas z listą meczów>, <obiekt typu pandas z listą drużyn>)