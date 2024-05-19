import time
import sys
import pandas as pd
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

def get_team_id(team_name):
    team_ids = {
        '1. FC Union Berlin' : 157,
        '1. FC Koeln' : 164,
        'Werder Brema' : 166,
        'Bochum' : 167,
        'VfB Stuttgart' : 169,
        'FC Schalke 04' : 170,
        'Hertha Berlin' : 171,
        'Arminia Bielefeld' : 172,
        'Furth' : 173,
        'Düsseldorf' : 174,
        'Paderborn' : 175,
        'Hannover' : 176,
        '1. FC Nürnberg' : 177,
        'Hamburger SV' : 178,
        'Ingolstadt' : 179,
        'Darmstadt' : 180,
        'Braunschweig' : 181,
        'Kiel' : 182,
        'Heidenheim' : 183,
        'Wehen' : 184,
        'St. Pauli' : 185,
        'Karlsruher' : 186,
        'Kaiserslautern' : 187,
        'Magdeburg' : 188,
        'Rostock' : 189,
        'Regensburg' : 190,
        'Sandhausen' : 191,
        'Dresden' : 192,
        'Aue' : 193,
        'Ingolstadt' : 179,
        'Osnabruck' : 194,
        'Wurzburger Kickers' : 195,
        'Duisburg' : 196,
        'Monachium 1860' : 197
    }
    return team_ids[team_name]

def parse_match_date(match_date):
    date_object = datetime.strptime(match_date, "%d.%m.%Y %H:%M")

    date_formatted = date_object.strftime("%Y-%m-%d %H:%M")

    return date_formatted

def get_match_id(link, driver, matches_df, league_id, season_id):
    id = -1
    driver.get(link)
    time.sleep(2)
    match_info = []
    match_data = {
        'league': 0,
        'season': 0,
        'home_team' : 0,
        'away_team' : 0,
        'game_date' : 0}
    # Znajdź wszystkie divy o klasie '_row_1csk6_9'
    stat_divs = driver.find_elements(By.CLASS_NAME, "_row_1csk6_9")
    # Znajdź wszystkie divy o klasie 'duelParticipant__startTime'
    time_divs = driver.find_elements(By.CLASS_NAME, "duelParticipant__startTime")
    team_divs = driver.find_elements(By.CLASS_NAME, "participant__participantName")
    # Dodaj zawartość divów do listy danych
    for div in time_divs:
        match_info.append(div.text.strip())
    for div in team_divs:
        match_info.append(div.text.strip())

    #print(match_info)
    match_data['league'] = league_id #id ligi
    match_data['season'] = season_id #id sezonu
    match_data['home_team'] = get_team_id(match_info[1]) #nazwa gospodarzy
    match_data['away_team'] = get_team_id(match_info[3])
    match_data['game_date'] = parse_match_date(match_info[0])
    id = #ZNAJDŹ ID MECZU O POWYŻSZYCH PARAMETRACH I JE ZWRÓĆ
    if id == -1:
        print("Nie udalo sie znalezc meczu!")
    return id
def get_1x2_odds(id, link, driver):
    pass
def get_over_under_odds(id, link, driver):
    pass

def get_btts_odds(id, link, driver):
    pass

def get_handi_odds(id, link, driver):
    pass

def get_double_chance_odds(id, link, driver):
    pass

def get_correct_score_odds(id, link, driver):
    pass

def get_data(games, driver, matches_df, league_id, season_id):
    driver.get(games)
    time.sleep(15)
    game_divs = driver.find_elements(By.CLASS_NAME, "event__match", matches_df, league_id, season_id)
    for element in game_divs:
        id = element.get_attribute('id').split('_')[2]
        match_id = get_match_id('https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/kursy-1x2/koniec-meczu'.format(id), driver)
        get_1x2_odds(match_id, 'https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/kursy-1x2/koniec-meczu'.format(id), driver)
        #get_over_under_odds(match_id, 'https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/powyzej-ponizej/koniec-meczu'.format(id), driver)
        #get_btts_odds(match_id, 'https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/obie-druzyny-strzela/koniec-meczu'.format(id), driver)
        #get_handi_odds(match_id, 'https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/handicap-azjat/koniec-meczu'.format(id), driver)
        #get_double_chance_odds(match_id, 'https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/podwojna-szansa/koniec-meczu'.format(id), driver)
        #get_correct_score_odds(match_id,'https://www.flashscore.pl/mecz/KGgchU8S/#/zestawienie-kursow/correct-score/koniec-meczu'.format(id), driver)
        break


def db_connect():
    # Połączenie z bazą danych MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="PLACEHOLDER",
        database="ekstrabet"
    )
    return conn

def main():
    #WYWOŁANIE
    conn = db_connect()
    query = "SELECT * FROM matches"
    matches_df = pd.read_sql(query, conn)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Here
    driver = webdriver.Chrome(options=options)
    #Link do strony z wynikami
    #games = 'https://www.flashscore.pl/pilka-nozna/francja/ligue-1-2016-2017/wyniki/'
    league_id = int(sys.argv[1])
    season_id = int(sys.argv[2])
    games = sys.argv[3]
    games = sys.argv[1]
    get_data(games, driver, matches_df, league_id, season_id)
if __name__ == '__main__':
    main()