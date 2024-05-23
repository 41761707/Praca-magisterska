import time
import sys
import pandas as pd
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

def get_team_id(team_name):
    team_ids = { 'Śląsk Wrocław' : 1,
                 'Jagiellonia Białystok' : 2,
                 'Lech Poznań' : 3,
                 'Raków Częstochowa' : 4,
                 'Legia Warszawa' : 5,
                 'Pogoń Szczecin' : 6,
                 'Górnik Zabrze' : 7,
                 'Zagłębie Lubin' : 8,
                 'Piast Gliwice' : 9,
                 'Radomiak Radom' : 10,
                 'Stal Mielec' : 11,
                 'Widzew Łódź' : 12,
                 'Cracovia' : 13,
                 'Puszcza Niepołomice' : 14,
                 'Warta Poznań' : 15,
                 'Korona Kielce' : 16,
                 'Ruch Chorzów' : 17,
                 'ŁKS Łódź' : 18,
                 'Wisła Płock' : 19,
                 'Lechia Gdańsk' : 20,
                 'Miedź Legnica' : 21,
                 'Bruk-Bet T.' : 22,
                 'Górnik Łęczna' : 23,
                 'Wisła Kraków' : 24,
                 'Podbeskidzie B-B' : 26,
                 'Arka Gdynia' : 27,
                 'Zagłębie Sosnowiec' : 28,
                 'Sandecja Nowy Sącz' : 29
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
    record = matches_df.loc[(matches_df['home_team'] == match_data['home_team']) & (matches_df['away_team'] == match_data['away_team'])]
    id = record.iloc[0]['id']
    if id == -1:
        print("Nie udalo sie znalezc meczu!")
    return id
def get_1x2_odds(id, link, driver):
    # 1 - zwyciestwo gospodarza
    # 2 - remis
    # 3 - zwyciestwo gosci
    driver.get(link)
    time.sleep(2)
    book_divs = driver.find_elements(By.CLASS_NAME, "ui-table__row")
    bookie_dict = {
        'STS.pl' : 4,
        'eFortuna.pl': 3,
        'Betclic.pl' : 2,
        'BETFAN' : 6,
        'Etoto' : 7,
        'LV BET': 5,
        'Superbet.pl' : 1
    }
    bookies = []
    for book in book_divs:
        try:
            # Szukamy tagu img wewnątrz obecnego diva
            img_tag = book.find_element(By.TAG_NAME, "img")
            # Pobieramy wartość atrybutu title z tagu img
            title = img_tag.get_attribute("title").strip("'")
            # Dodajemy tytuł do listy
            bookies.append(title)
        except:
            # Obsługujemy przypadek, gdy tag img lub atrybut title nie jest obecny
            bookies.append(None)
    iter = 1
    for i in range(len(book_divs)):
        text = book_divs[i].text.strip()
        text_tab = text.split('\n')
        text_1 = "INSERT INTO ODDS(match, bookmaker, event, odds) VALUES({}, {}, {}, {});".format(id, bookie_dict[bookies[i]], 1, text_tab[0])
        text_2 = "INSERT INTO ODDS(match, bookmaker, event, odds) VALUES({}, {}, {}, {});".format(id, bookie_dict[bookies[i]], 2, text_tab[1])
        text_3 = "INSERT INTO ODDS(match, bookmaker, event, odds) VALUES({}, {}, {}, {});".format(id, bookie_dict[bookies[i]], 3, text_tab[2])
        print(text_1)
        print(text_2)
        print(text_3)
        
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
    time.sleep(5)
    game_divs = driver.find_elements(By.CLASS_NAME, "event__match")
    links = []
    for element in game_divs:
        id = element.get_attribute('id').split('_')[2]
        links.append('https://www.flashscore.pl/mecz/{}'.format(id))
    for link in links:
        match_id = get_match_id(link, driver, matches_df, league_id, season_id)
        get_1x2_odds(match_id, "{}{}".format(link,'#/zestawienie-kursow/kursy-1x2/koniec-meczu'), driver)
        #get_over_under_odds(match_id, 'https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/powyzej-ponizej/koniec-meczu'.format(id), driver)
        #get_btts_odds(match_id, 'https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/obie-druzyny-strzela/koniec-meczu'.format(id), driver)
        #get_handi_odds(match_id, 'https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/handicap-azjat/koniec-meczu'.format(id), driver)
        #get_double_chance_odds(match_id, 'https://www.flashscore.pl/mecz/{}/#/zestawienie-kursow/podwojna-szansa/koniec-meczu'.format(id), driver)
        #get_correct_score_odds(match_id,'https://www.flashscore.pl/mecz/KGgchU8S/#/zestawienie-kursow/correct-score/koniec-meczu'.format(id), driver)


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
    league_id = int(sys.argv[1])
    season_id = int(sys.argv[2])
    query = "SELECT * FROM matches where league = {} and season = {}".format(league_id, season_id)
    matches_df = pd.read_sql(query, conn)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Here
    driver = webdriver.Chrome(options=options)
    #Link do strony z wynikami
    #games = 'https://www.flashscore.pl/pilka-nozna/polska/pko-bp-ekstraklasa-2023-2024/wyniki/'
    #games = sys.argv[3]
    games = 'https://www.flashscore.pl/pilka-nozna/polska/pko-bp-ekstraklasa-2023-2024/wyniki/'
    get_data(games, driver, matches_df, league_id, season_id)
    conn.close()
if __name__ == '__main__':
    main()