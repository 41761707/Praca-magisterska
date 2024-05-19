import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Dane do wykresów
    labels_list = [
        ['Gospodarz', 'Remis', 'Gość'],
        ['Gospodarz', 'Remis', 'Gość'],
        # Dodaj pozostałe listy etykiet dla innych wykresów
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
        # Dodaj pozostałe listy wartości dla innych wykresów
    ]

    # Kolory dla każdego wykresu
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
        # Dodaj pozostałe listy kolorów dla innych wykresów
    ]

    #Tytuły wykresów
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

    # Ustawienia wykresów
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(18, 8))  # 6 kolumn, 2 rzędy

    for i, ax in enumerate(axes.flat):
        if i < len(labels_list):
            labels = labels_list[i]
            values = values_list[i]
            colors = colors_list[i]

            # Bez sortowania
            sorted_labels, sorted_values = labels, values

            # Utwórz wykres kolumnowy z różnymi kolorami
            ax.bar(sorted_labels, sorted_values, color=colors)

            # Dodaj tytuł i etykiety osi do każdego wykresu
            ax.set_xlabel('Procent')
            ax.set_ylabel('Wynik')
            ax.set_title(titles_list[i])

    # Dostosuj układ, aby uniknąć nakładania się
    plt.tight_layout()

    # Zapisz wykresy do pliku
    plt.savefig('do_pracy/wykresy.png')
    plt.show()

if __name__ == '__main__':
    main()
