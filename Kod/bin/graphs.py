import matplotlib.pyplot as plt

# Dane
name = 'Pavel Zacha'
event = 'Assists'
line = 0.5
data = [0.05, 1, 0.05, 1, 0.05, 0.05, 0.05, 1, 2]
x_values = ['TOR1', 'TOR2', 'TOR3', 'TOR4', 'TOR5', 'TOR6', 'TOR7', 'FLA1', 'FLA2']
line_y = [line] * len(data)  # Wartość stała dla linii

# Określenie kolorów dla słupków na podstawie ich wartości
colors = ['red' if d < line else 'green' for d in data]
print(colors)
print("Liczba danych:", len(data))
print("Liczba elementów w x_values:", len(x_values))
print("Liczba elementów w line_y:", len(line_y))
# Rysowanie wykresu słupkowego
plt.bar(x_values, data, color=colors)

# Dodanie linii z większym zakresem osi Y
plt.plot(x_values, line_y, color='black', linestyle='--')
plt.ylim(0, max(data) + 1)  # Rozszerzenie zakresu osi Y

# Ustawienie etykiet i tytułów
plt.ylabel(event)
plt.title('{} this playoff: {}'.format(event, name))


# Zapisanie wykresu do pliku
plt.savefig('{}_{}.png'.format(name, event))

# Wyświetlenie wykresu
plt.show()