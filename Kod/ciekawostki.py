import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def home_team_advantage(titles_list):
    labels_list = [
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
    ]
    values_list = [
        [43.97, 29.18, 26.85],
        [45.34, 22.7,  31.95],
        [44.77, 24.83, 30.40],
        [43.44, 25.91, 30.65],
        [45.27, 26.58, 28.14],
        [42.86, 24.68, 32.46],
        [42.08, 30.80, 27.11],
        [43.31, 25.97, 30.7],
        [43.23, 27.28, 29.49],
        [40.88, 29.54, 29.58],
        [44.77, 30.74, 24.49],
        [41.46, 32.19, 26.36],
    ]
    colors_list = [
        ['blue', 'green', 'red'],
        ['purple', 'orange', 'cyan'],
        ['blue', 'green', 'red'],
        ['purple', 'orange', 'cyan'],
        ['blue', 'green', 'red'],
        ['purple', 'orange', 'cyan'],
        ['blue', 'green', 'red'],
        ['purple', 'orange', 'cyan'],
        ['blue', 'green', 'red'],
        ['purple', 'orange', 'cyan'],
        ['blue', 'green', 'red'],
        ['purple', 'orange', 'cyan'],
    ]
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(18, 8))  # 6 kolumn, 2 rzędy
    for i, ax in enumerate(axes.flat):
        if i < len(labels_list):
            labels = labels_list[i]
            values = values_list[i]
            colors = colors_list[i]
            sorted_labels, sorted_values = labels, values
            ax.bar(sorted_labels, sorted_values, color=colors)
            ax.set_xlabel('Procent')
            ax.set_ylabel('Wynik')
            ax.set_title(titles_list[i])
    plt.tight_layout()
    plt.savefig('do_pracy/wykresy.png')
    plt.show()
    #SPA2 = 0: 10.88, 1: 23.40, 2: 27.48, 3: 20.02, 4: 10.74, 5: 4.82
    #FRA2 = 0: 11.10, 1: 22.78, 2: 24.86, 3: 19.90, 4: 12.05, 5: 5.77
    #ITA2 = 0: 9.33, 1: 19.10, 2: 28.12, 3: 20.52, 4: 12.45, 5: 6.59
    #POL2 = 0: 8.34, 1: 20.01, 2: 25.38, 3: 22.36, 4: 12.96, 5: 6.29
    #ENG2 = 0: 7.58, 1: 19.92, 2: 25.15, 3: 22.63, 4: 13.54, 5: 7.08
    #ESP1 = 0: 8.18, 1: 19.39, 2: 24.83, 3: 21.49, 4: 12.90, 5: 7.40
    #ALL  = 0: 7.96, 1: 18.45, 2: 24.98, 3: 21.93, 4: 14.12, 5: 7.39
    #POL1 = 0: 8.03, 1: 18.09, 2: 24.44, 3: 21.85, 4: 14.66, 5: 7.59
    #FRA1 = 0: 7.28, 1: 17.70, 2: 24.00, 3: 22.76, 4: 14.95, 5: 8.09
    #ENG1 = 0: 6.29, 1: 16.08, 2: 23.81, 3: 22.16, 4: 16.28, 5: 9.32
    #ITA1 = 0: 6.26, 1: 16.26, 2: 23.30, 3: 23.80, 4: 15.52, 5: 8.32
    #GER2 = 0: 6.40, 1: 14.41, 2: 23.38, 3: 23.59, 4: 17.19, 5: 8.43
    #GER1 = 0: 5.44, 1: 12.04, 2: 23.42, 3: 22.22, 4: 17.82, 5: 9.71
def goals_per_league():
    labels_list = [
        ['SPA2', 'FRA2', 'ITA2', 'POL2', 'ENG2', 'ESP1', 'ALL', 'POL1', 'FRA1', 'ENG1', 'ITA1', 'GER2', 'GER1'],
        ['SPA2', 'FRA2', 'ITA2', 'POL2', 'ENG2', 'ESP1', 'ALL', 'POL1', 'FRA1', 'ENG1', 'ITA1', 'GER2', 'GER1'],
        ['SPA2', 'FRA2', 'ITA2', 'POL2', 'ENG2', 'ESP1', 'ALL', 'POL1', 'FRA1', 'ENG1', 'ITA1', 'GER2', 'GER1'],
        ['SPA2', 'FRA2', 'ITA2', 'POL2', 'ENG2', 'ESP1', 'ALL', 'POL1', 'FRA1', 'ENG1', 'ITA1', 'GER2', 'GER1'],
        ['SPA2', 'FRA2', 'ITA2', 'POL2', 'ENG2', 'ESP1', 'ALL', 'POL1', 'FRA1', 'ENG1', 'ITA1', 'GER2', 'GER1'],
        ['SPA2', 'FRA2', 'ITA2', 'POL2', 'ENG2', 'ESP1', 'ALL', 'POL1', 'FRA1', 'ENG1', 'ITA1', 'GER2', 'GER1'],
    ]
    values_list = [
        [10.88, 11.10, 9.33, 8.34, 7.58, 8.18, 7.96, 8.03, 7.28, 6.29, 6.26, 6.40, 5.44],
        [23.40, 22.78, 19.10, 20.01, 19.92, 19.39, 18.45, 18.09, 17.70, 16.08, 16.26, 14.41, 12.04],
        [27.48, 24.86, 28.12, 25.38, 25.15, 24.83, 24.98, 24.44, 24.00, 23.81, 23.30, 23.38, 23.42],
        [20.02, 19.90, 20.52, 22.36, 22.63, 21.49, 21.93, 21.85, 22.76, 22.16, 23.80, 23.59, 22.22],
        [10.74, 12.05, 12.45, 12.96, 13.54, 12.90, 14.12, 14.66, 14.95, 16.28, 15.52, 17.19, 17.82],
        [4.82, 5.77, 6.59, 6.29, 7.08, 7.40, 7.39, 7.59, 8.09, 9.32, 8.32, 8.43, 9.71],
    ]
    title = [
        'Procent meczów z liczbą bramek 0 dla różnych lig',
        'Procent meczów z liczbą bramek 1 dla różnych lig',
        'Procent meczów z liczbą bramek 2 dla różnych lig',
        'Procent meczów z liczbą bramek 3 dla różnych lig',
        'Procent meczów z liczbą bramek 4 dla różnych lig',
        'Procent meczów z liczbą bramek 5 dla różnych lig',
    ]
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(18, 8))  # 6 kolumn, 2 rzędy
    for i, ax in enumerate(axes.flat):
        if i < len(labels_list):
            labels = labels_list[i]
            values = values_list[i]
            colors = []
            curr_color = '#ff9896'
            sorted_labels, sorted_values = zip(*sorted(zip(labels, values), key=lambda x: x[1]))
            for element in sorted_labels:
                if element == 'ALL':
                    colors.append('red')
                    curr_color = '#c5b0d5'
                else:
                    colors.append(curr_color)
            ax.barh(sorted_labels, sorted_values, color = colors)
            print(sorted_labels)
            print(sorted_values)
            ax.set_xlabel('Procent')
            #ax.set_ylabel('Wynik')
            ax.set_title(title[i])
    plt.tight_layout()
    plt.savefig('do_pracy/wykresy.png')
    plt.show()

def goals_total():
    labels_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    values = [7.96, 18.45, 24.98, 21.93, 14.11, 7.39, 3.32, 1.25, 0.47, 0.11, 0.02, 0.005]
    sorted_labels, sorted_values = zip(*sorted(zip(labels_list, values), key=lambda x: x[1]))
    print(sorted_labels)
    print(sorted_values)
    plt.barh(sorted_labels, sorted_values)
    plt.xlabel('Procent meczów')
    plt.ylabel('Liczba bramek')
    plt.title('Rozkład procentowy bramek w badanych meczach')
    plt.savefig('do_pracy/goals_total.png')
    plt.show()

def goals(titles_list):
    labels_list = [
    ]
    values_list = [
    ]
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(18, 8))  # 3 kolumn, 4 rzędy
    for i, ax in enumerate(axes.flat):
        if i < len(labels_list):
            labels = labels_list[i]
            values = values_list[i]
            sorted_labels, sorted_values = zip(*sorted(zip(labels_list, values), key=lambda x: x[1]))
            ax.barh(sorted_labels, sorted_values)
            ax.set_xlabel('Procent')
            ax.set_ylabel('Wynik')
            ax.set_title(titles_list[i])
    plt.tight_layout()
    plt.savefig('do_pracy/wykresy.png')
    plt.show()

def season_totals():
    years = ['2016/17', '2017/18', '2018/19', '2019/20', '2020/21', '2021/22', '2022/23', '2023/24']
    values = [2.62, 2.60, 2.62, 2.63, 2.55, 2.64, 2.56, 2.68]
    plt.plot(years, values, marker='o', linestyle='-', color='b')
    plt.xlabel('Sezon')
    plt.ylabel('Wartość')
    plt.title('Zmiana wartości wraz ze zmianą lat')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.ylim(2, 4)
    plt.ylim(2, 3)
    plt.savefig('do_pracy/line_chart.png')
    plt.show()

def seasons_goals():
    # Dane do wykresu
    years = ['2017/18', '2018/19', '2019/20', '2020/21', '2021/22', '2022/23']
    pol1 = [2.64, 2.78, 2.59, 2.45, 2.67, 2.48]
    pol2 = [2.41, 2.5, 2.64, 2.32, 2.49, 2.65]
    eng1 = [2.68, 2.82, 2.72, 2.69, 2.82, 2.85]
    eng2 = [2.54, 2.67, 2.64, 2.30, 2.51, 2.43]
    fra1 = [2.72, 2.56, 2.52, 2.76, 2.80, 2.81]
    fra2 = [2.18, 2.2, 2.22, 2.4, 2.29, 2.41]
    ger1 = [2.79, 3.17, 3.20, 3.04, 3.11, 3.17]
    ger2 = [2.75, 2.96, 2.88, 2.97, 2.90, 2.94]
    spa1 = [2.69, 2.59, 2.48, 2.51, 2.50, 2.51]
    spa2 = [2.31, 2.18, 2.27, 2.06, 2.42, 2.01]
    ita1 = [2.68, 2.68, 3.03, 3.06, 2.87, 2.57]
    ita2 = [2.54, 2.59, 2.51, 2.39, 2.48, 2.33]
    colors = [
    '#1f77b4',  # Niebieski
    '#ff7f0e',  # Pomarańczowy
    '#2ca02c',  # Zielony
    '#d62728',  # Czerwony
    '#9467bd',  # Fioletowy
    '#8c564b',  # Brązowy
    '#e377c2',  # Różowy
    '#7f7f7f',  # Szary
    '#bcbd22',  # Oliwkowy
    '#17becf',  # Turkusowy
    '#ff9896',  # Jasnoczerwony
    '#c5b0d5'   # Jasnofioletowy
]
    # Utworzenie wykresu liniowego
    plt.plot(years, pol1, marker='o', linestyle='-', color=colors[0], label = 'POL1')
    plt.plot(years, pol2, marker='o', linestyle='-', color=colors[1], label = 'POL2')
    plt.plot(years, eng1, marker='o', linestyle='-', color=colors[2], label = 'ENG1')
    plt.plot(years, eng2, marker='o', linestyle='-', color=colors[3], label = 'ENG2')
    plt.plot(years, fra1, marker='o', linestyle='-', color=colors[4], label = 'FRA1')
    plt.plot(years, fra2, marker='o', linestyle='-', color=colors[5], label = 'FRA2')
    plt.plot(years, ger1, marker='o', linestyle='-', color=colors[6], label = 'GER1')
    plt.plot(years, ger2, marker='o', linestyle='-', color=colors[7], label = 'GER2')
    plt.plot(years, spa1, marker='o', linestyle='-', color=colors[8], label = 'SPA1')
    plt.plot(years, spa2, marker='o', linestyle='-', color=colors[9], label = 'SPA2')
    plt.plot(years, ita1, marker='o', linestyle='-', color=colors[10], label = 'ITA1')
    plt.plot(years, ita2, marker='o', linestyle='-', color=colors[11], label = 'ITA2')

    # Dodanie etykiet osi
    plt.xlabel('Sezon')
    plt.ylabel('Średnia')
    plt.ylim(1.5, 3.5)
    # Ustawienie tytułu wykresu
    plt.title('Zmiana średniej liczby bramek w meczu w czasie dla każej z lig')

    # Obrócenie etykiet osi X, aby były czytelne
    plt.xticks(rotation=45)

    # Dodanie siatki dla lepszej czytelności
    plt.grid(True)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    # Zapisanie wykresu do pliku
    plt.savefig('do_pracy/line_chart.png')

    # Wyświetlenie wykresu
    plt.show()

def goals_league():
    labels = ['SPA2', 'FRA2', 'ITA2', 'POL2', 'ENG2', 'ESP1', 'ALL', 'POL1', 'FRA1', 'ENG1', 'ITA1', 'GER2', 'GER1']
    values = [2.22, 2.31, 2.43, 2.50, 2.53, 2.60, 2.61, 2.63, 2.69, 2.77, 2.83, 2.84, 3.05]
    colors = []
    for label in labels:
        if label == 'ALL':
            colors.append('red')
        elif label.endswith('2'):
            colors.append('tan')
        elif label.endswith('1'):
            colors.append('lightblue')
        else:
            colors.append('skyblue')
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color=colors)
    ax.set_xlabel('Ligi')
    ax.set_ylabel('Średnia bramek')
    ax.set_title('Wykres słupkowy przedstawiający średnią liczbę bramek w analizowanych ligach')
    plt.xticks(rotation=45, ha='right')

    # Wyświetlenie wykresu
    plt.tight_layout()
    plt.show()

def btts():
    labels = ['SPA2', 'FRA2', 'ITA2', 'POL2', 'ENG2', 'ESP1', 'ALL', 'POL1', 'FRA1', 'ENG1', 'ITA1', 'GER2', 'GER1']
    values = [46.41, 45.74, 52.58, 49.08, 50.67, 50.60, 51.66, 51.86, 51.89, 51.70, 55.25, 57.18, 58.43]
    colors = []
    fig, ax = plt.subplots(figsize=(10, 6))
    sorted_labels, sorted_values = zip(*sorted(zip(labels, values), key=lambda x: x[1]))
    for label in sorted_labels:
        if label == 'ALL':
            colors.append('red')
        elif label.endswith('2'):
            colors.append('tan')
        elif label.endswith('1'):
            colors.append('lightblue')
        else:
            colors.append('skyblue')
    bars = ax.bar(sorted_labels, sorted_values, color=colors)
    ax.set_xlabel('Ligi')
    ax.set_ylabel('Procent BTTS')
    ax.set_title('Wykres słupkowy przedstawiający liczbę meczów, w których obie drużyny strzeliły')
    plt.tight_layout()
    plt.show()
def main():
    titles_list = [
        'PKO BP Ekstraklasa',
        'Premier League',
        'Bundesliga',
        'Ligue 1',
        'LaLiga',
        'Serie A',
        'Fortuna 1 Liga',
        'Championship',
        '2. Bundesliga',
        'Ligue 2',
        'LaLiga 2',
        'Serie B'
    ]
    #home_team_advantage(titles_list)
    #goals_total(titles_list)
    #season_totals()
    #goals_league()
    #seasons_goals()
    #goals_per_league()
    btts()
if __name__ == '__main__':
    main()
