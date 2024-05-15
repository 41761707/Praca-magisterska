import numpy as np
import pandas as pd


class League:
    def __init__(self, matches_df, teams_df):
        self.matches_df = matches_df 
        self.teams_df = teams_df 
        print(matches_df.head)
        print(teams_df.head)
        
    
    def symulate_league(self):
        pass 

    def generate_schedule(self):
        pass

        