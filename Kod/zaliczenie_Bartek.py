import numpy as np

def skewness(dane):
    n = len(dane)
    if n == 0:
        raise ValueError("Dane nie mogą być puste")
    
    mean = np.mean(dane)
    s = np.std(dane)  # ddof=0 for population standard deviation
    
    # Calculate the third central moment
    M3 = np.mean((dane - mean) ** 3)
    
    # Calculate skewness
    g1 = M3 / s**3
    print(M3)
    print(s**3)
    return g1


def main():
    dane = np.array([1.60, 1.47, 1.16, 1.78, 1.31, 1.70, 1.25, 1.65, 1.69, 1.92, 1.75, 1.43, 1.33, 1.84, 1.36, 1.52, 1.55, 1.62, 1.57, 1.50])
    print(f"Współczynnik asymetrii: {skewness(dane)}")

if __name__ == '__main__':
    main()


'''# Dane
#data = np.array([1.60, 1.47, 1.16, 1.78, 1.31, 1.70, 1.25, 1.65, 1.69, 1.92, 1.75, 1.43, 1.33, 1.84, 1.36, 1.52, 1.55, 1.62, 1.57, 1.50])
#data = np.array([386,284,339,340,305,386,378,335,344,346])
data = np.array([[405, 420, 411, 427, 479, 440, 378, 468, 437, 452, 421, 414, 402, 422, 462, 428, 431, 414, 437, 405, 390, 425, 425, 400, 432, 447, 385, 419, 400, 425, 458, 439, 360, 405, 369, 406, 431, 412, 387, 416]])

# Średnia masa
mean = np.mean(data)

# Mediana
median = np.median(data)

# Odchylenie standardowe
std_deviation = np.std(data)

# Odchylenie przeciętne od średniej arytmetycznej
mean_deviation_from_mean = np.mean(np.abs(data - mean))

# Odchylenie przeciętne od mediany
mean_deviation_from_median = np.mean(np.abs(data - median))

# Współczynnik zmienności
coefficient_of_variation = std_deviation / mean

# Współczynnik asymetrii
#coefficient_of_skewness = skew(data)

print(mean, median, std_deviation, mean_deviation_from_mean, mean_deviation_from_median, coefficient_of_variation)#, coefficient_of_skewness)'''
