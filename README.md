# Praca-magisterska
Repozytorium zawierające wszystkie kody źródłowe zaimplementowane w ramach pracy magisterskiej o prozaicznym tytule "Przewidywanie zdarzeń w piłce nożnej". Ponadto, w repozytorium, zostanie upubliczniona cała praca do wglądu dla czytelnika w formacie .pdf ~~oraz .tex~~, zgodna ze standardami obowiązującymi na Politechnice Wrocławskiej, na wydziale Informatyki i Telekomunikacji.

## Karta pracy
### Tytuł PL
  Przewidywanie zdarzeń w piłce nożnej
### Tytuł ENG
  Predicting events in football 
### Opis pracy
  Oglądając dowolną transmisję sportową bardzo łatwym jest zauważyć wpływ niebotycznego rozwoju technologicznego ostatnich lat na dyscypliny sportowe. W trakcie meczu widz jest zalewany rozmaitymi wykresami, grafikami bądź tabelami przedstawiającymi różnorodne statystyki odnośnie danej drużyny bądź danego zawodnika,  a także prognozy wydarzeń opartych na tychże danych. Wsłuchując się w komentarz w trakcie spotkania słuchacz notorycznie natrafia na uwagi typu "Zawodnik X wygrał 9 na 10 spotkań, gdy strzelił bramkę w pierwszym kwadransie meczu", bądź "Drużyna Y w meczach domowych nie traci więcej niż dwóch bramek". Tego rodzaju analizy znacząco wpływają na postrzeganie meczu przez kibica, który może mylnie wnioskować, że "skoro Zawodnik X już strzelił gola, to na pewno nie przegramy, prawda?". Podobne mechanizmy funkcjonują w świecie zakładów bukmacherskich, które notują najwyższe notowania w historii, dzięki ogromnemu zainteresowaniu sportem, szeroką gamą możliwych do obstawienia zakładów oraz łatwością w realizacji całego procesu. Przeglądając dostępne na rynku oferty oraz potencjalne możliwe do uzyskania wygrane wielu śmiałków przy pomocy dostępnych danych oraz analiz próbuje swojego szczęścia z nadzieją na łatwe i przejmne pomnożenie swojego majątku, jednakże do jakiego stopnia "suche dane" są w stanie zagwarantować hazardziście życie w luksusie? Przecież nawet największa seria zwycięstw kiedyś musi ujrzeć jarzmo porażki. 
### Cel pracy
  Celem niniejszej pracy jest stworzenie modelu, który, bazując na starannie dobranych danych, będzie w stanie prognozować z najwyższą dokładnością pewne wydarzenia związane z piłką nożną. Głównym analizowanym zdarzeniem, najistotniejszym z perpsektywy jakiejkolwiek konkurencji, będzie zwycięstwo konkretnej drużyny, jednakże praca przewiduje ustalanie prawdopodobieństwa dla takich zdarzeń jak
  - więcej/mniej niż X bramek w meczu
  - więcej/mniej niż Y rożnych w meczu
  - więcej/mniej niż Z kartek w meczu
Otrzymane wyniki zostaną poddane analizie względem innych prac dostępnych na rynku jak i również względem prognoz ekspertów oraz bukmacherów.
### Zakres pracy
  - Przegląd dostępnej literatury naukowej
  - Wybór odpowiednich technologii
  - Wyselekcjonowanie zbiorów danych oraz cech, według których realizowane będą dalsze analizy
  - Prowadzenie oraz dokumentowanie licznych testów przygotowanych modeli, generowanie niezbędnych wykresów oraz tabel
  - Analiza oraz porównywanie wyników z innymi narzędziami dostępnymi na rynku
### Literatura
  1.  C. Constantinou. Dolores: a model that predicts football match outcomes from all over the world. Machine Learning, 108:49–75, 2018
  2.  C. Yeung, R. Bunker, R. Umemoto, K. Fujii. Evaluating soccer match prediction models: A deep learning approach and feature optimization for gradient-boosted trees, 2023.
  3.  L. Hervert, T. Matis, N. Hernández-Gress. Prediction learning model for soccer matches outcomes. strony 63–69, 10 2018


## Streszczenie
  Obiektem badań niniejszej pracy jest sprawdzenie możliwości przewidywania wybranych zdarzeń w meczach piłkarskich. Eksperyment obejmuje prognozowanie różnorodnych zdarzeń, począwszy od podstawowych, takich jak wynik meczu czy zwycięstwo drużyny, aż po bardziej szczegółowe aspekty, takie jak liczba rzutów rożnych danej drużyny.

  Praca ta składa się z obszernego opisu procesu projektowania, jak i wdrażania modelu predykcyjnego dla elementów piłkarskiego widowiska, w szczególności skupiając się na wykorzystaniu technik maszynowego głebokiego uczenia (Deep Learning, DL). Dodatkowo zawiera liczne przykłady zastosowań modelu, szczegóły implementacyjne oraz porównanie otrzymanych wyników z rzeczywistymi rezultatami oraz innymi powszechnie stosowanymi rozwiązaniami dostępnymi w literaturze naukowej.

  Dodatkowym aspektem pracy jest opracowanie metodologii umożliwiającej rywalizację w zakładach bukmacherskich poprzez wykrywanie rozbieżności między ustalonym prawdopodobieństwem wystąpienia zdarzenia, a kursem oferowanym przez wybranych bukmacherów. Przedstawiono także definicje umożliwiające czytelnikowi zapoznanie się z nomenklaturą używaną w zakładach bukmacherskich. 
## Abstract 
  The main goal of the research is to investigate the possibility of predicting selected events in soccer matches. The experiment involves the predicition of a variety of events, ranging from basic ones, such as the result of a match or a given team's victory, to more detailed aspects, such as the number of corner kicks of a given team.

  Presented thesis consists of comprehensive description of the process of designing, as well as implementing, a predicitve model for elements of the soccer game, particularly focusing on the usage of machine learning techniques, such as deep learning (Deep Learning, DL). Additionally, thesis includes numerous examples of the model's application, implementation details and a comparison of the results obtained with actual results of games and other commonly used solutions available in the scientific literature.

  An additional aspect of the work is the development of a methodology that enables competitive betting by detecting discrepancies between the established probability of an event and the odds offered by the selected bookmakers. All needed definitions are provided in order for the reader to become familiar with the nomenclature used in betting's world.

## Co zrealizowano w ramach pracy
1. Utworzenie bazy danych zawierającą informacje o poszczególnych meczach, klubach oraz ligach piłkarskich
2. Utworzenie modelu nauczania głębokiego z wykorzystaniem rekurencyjnych sieci neuronowych (RNN / LSTM) do przewidywania zdarzeń w piłce nożnej
3. Utworzenie programu rozruchowego pozwalającego na (drobną, ale jednak!) integrację z użytkownikiem. Sposób uruchomienia znajduje się w pliku .pdf
4. Utworzenie licznych testów zaimplementowanej metodologii
5. Zredagowanie pracy magisterskiej podsumowująćej zrealizowane działania

## UWAGA
Praca magisterska została w pełni zrealizowana. Owoc ów pracy można zobaczyć zapoznająć się z plikiem *Przewidywanie_zdarzeń_w_piłce_nożnej.pdf*. Od tego momentu projekt jest stale kontynuowany w repozytorium o nazwie **EkstraBet**
