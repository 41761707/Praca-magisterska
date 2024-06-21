import time
import sys
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import db_module

def get_team_id(team_name):
    team_ids = {
        'Granada' : 277,
        'Las Palmas' : 284,
        'Levante' : 278,
        'Alaves' : 279,
        'Eibar' : 281,
        'Albacete' : 287,
        'Andorra' : 288,
        'R. Oviedo' : 289,
        'Cartagena' : 290,
        'Tenerife' : 291,
        'Burgos CF' : 292,
        'Racing Santander' : 293,
        'Zaragoza' : 294,
        'Leganes' : 282,
        'Huesca' : 280,
        'Mirandes' : 295,
        'Gijon' : 286,
        'Villarreal B' : 296,
        'Ponferradina' : 297,
        'UD Ibiza' : 298,
        'Lugo' : 299,
        'Malaga' : 285,
        'Almeria' : 273,
        'Valladolid' : 274,
        'Girona' : 266,
        'Amorebieta' : 300,
        'R. Sociedad B' : 301,
        'Fuenlabrada' : 302,
        'Alcorcon' : 303,
        'Espanyol' : 275,
        'Mallorca' : 265,
        'Vallecano' : 267,
        'Sabadell' : 304,
        'UD Logrones' : 305,
        'Castellon' : 306,
        'Cadiz' : 270,
        'Elche' : 276,
        'La Coruna' : 283,
        'Racing Santander' : 293,
        'Numancia' : 307,
        'Extremadura UD' : 308,
        'Osasuna' : 263,
        'Rayo Majadahonda' : 309,
        'Gimnastic': 310,
        'Cordoba' : 311,
        'Reus FCR' : 312,
        'Cultural Leonesa' : 313,
        'Barcelona B' : 314,
        'Lorca FC' : 315,
        'Sevilla B' : 316,
        'Getafe' : 271,
        'UCAM Murcia' : 317,
		'Ferrol' : 326,
		'Eldense' : 327
        
    }
    return team_ids[team_name]

def parse_match_date(match_date):
    date_object = datetime.strptime(match_date, "%d.%m.%Y %H:%M")

    date_formatted = date_object.strftime("%Y-%m-%d %H:%M")

    return date_formatted

def get_match_links(games, driver):
    links = []
    driver.get(games)
    time.sleep(15)
    game_divs = driver.find_elements(By.CLASS_NAME, "event__match")
    for element in game_divs:
        id = element.get_attribute('id').split('_')[2]
        links.append('https://www.flashscore.pl/mecz/{}/#/szczegoly-meczu/statystyki-meczu/0'.format(id))
    return links
                

def update_match_data(driver, league_id, season_id, link, match_id):
    stats = []
    match_info = []
    match_data = {
        'game_date' : 0,
        'home_team_goals' : 0,
        'away_team_goals' : 0,
        'home_team_xg' : 0,
        'away_team_xg' : 0,
        'home_team_bp' : 0,
        'away_team_bp' : 0,
        'home_team_sc' : 0,
        'away_team_sc' : 0,
        'home_team_sog' : 0,
        'away_team_sog' : 0,
        'home_team_fk' : 0,
        'away_team_fk': 0,
        'home_team_ck' : 0,
        'away_team_ck' : 0,
        'home_team_off' : 0,
        'away_team_off' : 0,
        'home_team_fouls' : 0,
        'away_team_fouls' : 0,
        'home_team_yc' : 0,
        'away_team_yc' : 0,
        'home_team_rc' : 0,
        'away_team_rc' : 0,
        'round' : 0,
        'result' : 0,
        'id' : 0}
    # _row_n1rcj_9 - klasa zawierająca informacje o statystykach meczowych
    # duelParticipant__startTime - czas rozegrania meczu (timestamp)
    # participant__participantName - drużyny biorące udział w meczu
    # detailScore__wrapper - wynik meczu
    driver.get(link)
    time.sleep(2) # Let the user actually see something!
    # Znajdź wszystkie divy o klasie '_row_qsznl_8'
    stat_divs = driver.find_elements(By.CLASS_NAME, "_row_qsznl_8")
    # Znajdź wszystkie divy o klasie 'duelParticipant__startTime'
    time_divs = driver.find_elements(By.CLASS_NAME, "duelParticipant__startTime")
    team_divs = driver.find_elements(By.CLASS_NAME, "participant__participantName")
    score_divs = driver.find_elements(By.CLASS_NAME, "detailScore__wrapper")
    round_divs = driver.find_elements(By.CLASS_NAME, "tournamentHeader__country")
    for div in round_divs:
        round_info = div.text.strip()
        round = round_info.split(" ")[-1]

    # Dodaj zawartość divów do listy danych
    for div in stat_divs:
        stats.append(div.text.strip())
    for div in time_divs:
        match_info.append(div.text.strip())
    for div in team_divs:
        match_info.append(div.text.strip())
    for div in score_divs:
        match_info.append(div.text.strip())

    #print(match_info)
    #match_data['league'] = league_id #id ligi
    #match_data['season'] = season_id #id sezonu
    #match_data['home_team'] = get_team_id(match_info[1]) #nazwa gospodarzy
    #match_data['away_team'] = get_team_id(match_info[3])
    match_data['game_date'] = parse_match_date(match_info[0])
    match_data['round'] = round
    score = match_info[5].split('\n')
    home_goals = int(score[0])
    away_goals = int(score[2])
    match_data['id'] = match_id
    match_data['home_team_goals'] = home_goals
    match_data['away_team_goals'] = away_goals
    if home_goals > away_goals:
        match_data['result'] = '1'
    elif home_goals == away_goals:
        match_data['result'] = 'X'
    else:
        match_data['result'] = '2'
    for element in stats:
        stat = element.split('\n')
        if(stat[1] == 'Oczekiwane bramki (xG)'):
            match_data['home_team_xg'] = stat[0]
            match_data['away_team_xg'] = stat[2]
        elif(stat[1] == 'Posiadanie piłki'):
            match_data['home_team_bp'] = int(stat[0][:-1])
            match_data['away_team_bp'] = int(stat[2][:-1])
        elif(stat[1] == 'Sytuacje bramkowe'):
            match_data['home_team_sc'] = int(stat[0])
            match_data['away_team_sc'] = int(stat[2])
        elif(stat[1] == 'Strzały na bramkę'):
            match_data['home_team_sog'] = int(stat[0])
            match_data['away_team_sog'] = int(stat[2])
        elif(stat[1] == 'Rzuty wolne'):
            match_data['home_team_fk'] = int(stat[0])
            match_data['away_team_fk'] = int(stat[2])
        elif(stat[1] == 'Rzuty rożne'):
            match_data['home_team_ck'] = int(stat[0])
            match_data['away_team_ck'] = int(stat[2])
        elif(stat[1] == 'Spalone'):
            match_data['home_team_off'] = int(stat[0])
            match_data['away_team_off'] = int(stat[2])
        elif(stat[1] == 'Faule'):
            match_data['home_team_fouls'] = int(stat[0])
            match_data['away_team_fouls'] = int(stat[2])
        elif(stat[1] == 'Żółte kartki'):
            match_data['home_team_yc'] = int(stat[0])
            match_data['away_team_yc'] = int(stat[2])
        elif(stat[1] == 'Czerwone kartki'):
            match_data['home_team_rc'] = int(stat[0])
            match_data['away_team_rc'] = int(stat[2])
    return match_data

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
    record = matches_df.loc[(matches_df['home_team'] == match_data['home_team']) & (matches_df['away_team'] == match_data['away_team'])]
    id = record.iloc[0]['id']
    if id == -1:
        print("Nie udalo sie znalezc meczu!")
    return id

def main():
    #WYWOŁANIE
    #python scrapper.py <id_ligi> <id_sezonu> <link do strony z wynikami na flashscorze>
    league_id = int(sys.argv[1])
    season_id = int(sys.argv[2])
    conn = db_module.db_connect()
    query = "SELECT * FROM matches where league = {} and season = {}".format(league_id, season_id)
    matches_df = pd.read_sql(query, conn)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Here
    driver = webdriver.Chrome(options=options)
    #Link do strony z wynikami
    #games = 'https://www.flashscore.pl/pilka-nozna/francja/ligue-1-2016-2017/wyniki/'
    games = sys.argv[3]
    links = get_match_links(games, driver)
    for link in links:
        match_id = get_match_id(link, driver, matches_df, league_id, season_id)
        match_data = update_match_data(driver, league_id, season_id, link, match_id)
        sql = '''UPDATE `ekstrabet`.`matches` SET  `game_date` = '{game_date}', \
`home_team_goals` = '{home_team_goals}', \
`away_team_goals` = '{away_team_goals}', \
`home_team_xg` = '{home_team_xg}', \
`away_team_xg` = '{away_team_xg}', \
`home_team_bp` = '{home_team_bp}', \
`away_team_bp` = '{away_team_bp}', \
`home_team_sc` = '{home_team_sc}', \
`away_team_sc` = '{away_team_sc}', \
`home_team_sog` = '{home_team_sog}', \
`away_team_sog` = '{away_team_sog}', \
`home_team_fk` = '{home_team_fk}', \
`away_team_fk` = '{away_team_fk}', \
`home_team_ck` = '{home_team_ck}', \
`away_team_ck` = '{away_team_ck}', \
`home_team_off` = '{home_team_off}', \
`away_team_off` = '{away_team_off}', \
`home_team_fouls` = '{home_team_fouls}', \
`away_team_fouls` = '{away_team_fouls}', \
`home_team_yc` = '{home_team_yc}', \
`away_team_yc` = '{away_team_yc}', \
`home_team_rc` = '{home_team_rc}', \
`away_team_rc` = '{away_team_rc}', \
`round` = '{round}', \
`result` = '{result}' \
WHERE (`id` = '{id}');'''.format(**match_data)
        print(sql)
    conn.close()
if __name__ == '__main__':
    main()