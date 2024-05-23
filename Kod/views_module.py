import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

## @package Views
# Moduł odpowiedzialny za dostarczanie najważniejszych informacji / ciekawostek
# Ma działać jak widoki w db
# Może byc istotny z persepktywy potencjalnego GUI
class Views:
    def __init__(self, matches_df, teams_df):
        self.matches_df = matches_df
        self.teams_df = teams_df

    def graph_goals(self, input):
        results = []
        all_matches = 0
        exact_correct = 0
        ou_correct = 0
        with open(input, 'r') as file:
            for line in file:
                parts = line.strip().split(';')
                if int(parts[5]) < 20:
                    continue
                results.append([parts[0], float(parts[1]), float(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])])
                ou_correct = ou_correct + int(parts[4]) + 1
                exact_correct = exact_correct + int(parts[3]) + 1
                all_matches = all_matches + int(parts[5])
        best_exacts = sorted(results, key=lambda x: x[1])
        best_ou = sorted(results, key=lambda x: x[2])

        print("Wszystkie mecze: {}".format(all_matches))
        print("Liczba poprawnie wywnioskowanych wyników: {}, {:.2f}%".format(exact_correct, exact_correct / all_matches * 100))
        print("Liczba poprawnie wywnioskowanych OU: {}, {}%".format(ou_correct,  ou_correct / all_matches * 100))
        print("Najlepsze przewidywania dokładnych wyników: ")
        for best in best_exacts[:20]:
            print('{} - {}'.format(best[0], best[1]))
        print("Najlepsze przewidywania Over/Under: ")
        for best in best_ou[:20]:
            print('{} - {}'.format(best[0], best[2]))

    def graph_winners(self, input):
        results = []
        all_matches = 0
        exact_correct = 0
        with open(input, 'r') as file:
            for line in file:
                parts = line.strip().split(';')
                if int(parts[2]) < 20:
                    continue
                results.append([parts[0], float(parts[1]), int(parts[2])])
                exact_correct += int(float(parts[1]) * int(parts[2]) + 1)
                all_matches = all_matches + int(parts[2])
        best_exacts = sorted(results, key=lambda x: x[1], reverse=True)

        print("Wszystkie mecze: {}".format(all_matches))
        print("Liczba poprawnie wywnioskowanych wyników: {}, {:.2f}%".format(exact_correct, exact_correct / all_matches * 100))
        print("Najlepsze przewidywania dokładnych wyników: ")
        for best in best_exacts[:20]:
            print('{} - {}'.format(best[0], best[1]))

    def league_view(self, league_id):
        pass 
    
    def season_view(self, season_id):
        pass 

    def league_season_view(self, league_id, season_id):
        pass

    def country_view(self, country_id):
        pass

def main():
    graphs = Views([], [])
    #graphs.graph_goals(sys.argv[1])
    graphs.graph_winners(sys.argv[1])

if __name__ == '__main__':
    main()

'''class MyRating:
    def __init__(self, matches_df, teams_df):
        # implementacja obliczania rankingu PI
            self.matches_df = matches_df
            self.teams_df = teams_df
            self.teams_dict = {}
            self.ratings = {}

    def relax_coef(self):
        pass
    
    def shape_coef(self):
        pass

    def cards_coef(self):
        pass

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

class GAPRating:
    def __init__(self, matches_df, teams_df):
        # implementacja obliczania rankingu PI
            self.matches_df = matches_df
            self.teams_df = teams_df
            self.teams_dict = {}
            self.ratings = []
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
    
        return a_att_j, h_att_j, a_def_j, h_def_j

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
        elif method == "GAP":
            return GAPRating(matches_df, teams_df)
        else:
            raise ValueError("Nieznana metoda obliczania rankingu")'''

