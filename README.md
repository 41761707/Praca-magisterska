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

## TERMIN REALIZACJI
Zgodnie z harmonogramem planowania (https://wit.pwr.edu.pl/studenci/dyplomanci/harmonogram_dyplomowania) uzgodniona z promotorem wersja pracy
powinna zostać przesłana do systemu nie później niż **19.06.2024**. 
Ze względu na rozpoczęcie dwutygodniowych cyklów pracy z dniem **01.03.2024**, za naturalny termin ostateczny przyjąłem **07.06.2024** 
*(do ustalenia z Panem Promotorem, czy taki termin nadesłania przeze mnie pracy jest wystarczający, aby zweryfikować jej poprawność)*

## Change log
### 1 cześć realizacji: 01.03.2023 - 15.03.2023 
#### TO-DO:
  1. Przygotowanie opisu pracy wraz z wyszczególnieniem najważniejszej literatury, na której będzie się ona opierała
  2. Szkic podziału pracy na rozdziały, przygotowanie streszczenia zawierającego kluczowe informacje na temat tego, co w pracy ma się znaleźć
  3. Określenie oraz znalezienie odpowiednich zbiorów danych / API, z których będą pobierane naistotniejsze wyniki / aspekty, niezbędne do predykcji zdarzeń
  4. Przygotowanie podstawowego podziału uzyskanych danych w logiczne struktury (konkretniej: podział na tabele w relacyjnej bazie danych)
  5. Wybór technologii, w której praca będzie realizowana (silnik bazodanowy + back-end)
  6. Do przemyslenia, czy należy tworzyć jakikolwiek interfejs użytkownika (front-end)?*

### 2 część relizacji: 15.03.2023 - 29.03.2023
#### ZREALIZOWANO:
  1. Przygotowano opis pracy z wyszczególnieniem najważniejszej literatury
  2. Utworzono pierwotny szkic pracy (spis treści) z podziałem na rozdziały 
  3. Rozpoczęto organizowanie skryptów do pobrania niezbędnych danych z zebranych baz wiedzy, wyselekcjonowano zdarzenia do predykcji
  4. Utworzono podstawowy podział zebranych danych w struktury bazodanowe: tabele
  5. Wybrano technologie, w których praca zostanie zrealizowana (python + drzewa jako sposób uczenia maszynowego + mysql)
#### TO-DO:
  1. Poprawka podziału na rozdziały oraz ich nazewnictwa zgodnie z ustaleniami w trakcie spotkania
  2. Ustalenie dokładnych relacji między tabelami wystepującymi w bazie danych, ponowne zastanowienie się nad strukturą projektu (czy wszystko na pewno się zgadza)
  3. Rozpoczęcie redagowania dwóch pierwszych rozdziałów odnośnie wstępu do pracy jak i literatury
  4. Dokończenie skryptu odpowiedzialnego za zebranie niezbędnych danych, umieszczenie ich w bazie danych
  5. Rozpoczęcie analizy pracy pod kątem przygotowania systemu rankingowego

### 3 część relizacji: 29.03.2023 - 12.04.2023
#### ZREALIZOWANO: 
  1. Poprawiono podział pracy na rozdziały, wprowadzono poprawki zgodnie z wytycznymi otrzymanymi od promotora
  2. Rozpoczęto ustalanie zależności między tabelami w bazie danych, pojawiły się pewne komplikacje związane z liczbą tabel, do ustalenia
  3. Ukończono redakcję pierwszego z rozdziałów
  4. Rozpoczęto redakcję drugiego rozdziału
  5. Ukończono skrypt realizujący pobranie istotnych danych do bazy, utworzenie folderu **DDL** zawierającego wszystkie wpisy bazodanowe w razie awarii
  6. Umieszczono wszystkie niezbędne dane w bazie danych
  7. Sporządzenie szkicu systemu rankingowego, do dalszego rozwoju
#### TO-DO:
  1. Wprowdadzenie do bazy danych tabel związanych z kursami bukmacherskimi w celu porównania predykcji z rynkiem bukmacherskim
  2. Rozpoczęcie implementacji systemu rankingowego wraz z uczeniem maszynowym odpowiedzialnym za generowanie predykcji wybranych zdarzeń
  3. W drugim rozdziale: dopisać słów parę o systemach rankingowych oraz o pracach bazujących na przetwarzaniu języka naturalnego / kursach bukmacherskich
  4. Restrukturyzacja projektu (podział funkcji pythonowych na moduły zawierające klasy)
  5. Przygotowanie do generowania dokumentacji: Dodanie komentarzy w stylu doxygen po implementacji
  6. Utworzenie skryptu mającego za zadanie pobrać kursy wyselekcjonowanych zdarzeń
  7. Modyfikacja podejścia po spotkaniu: wykorzystanie uczenia głębokiem (RNN, LSTM)
### 3* część realizacji: 12.04.2023 - 26.04.2023
  Realizacja w tym terminie została zawieszona ze względu na problemy zdrowotne

### 4 część realizacji: 26.04.2023 - 10.05.2023
  #### ZREALIZOWANO:
  1. Wprowadzono do bazy danych tabele związane z kursami bukmacherskimi
  2. Rozpoczęto implementację systemu rakingowego (do ciągłego rozwoju, zapytać w ramach spotkania!)
  3. Uzupełniono drugi rozdział o brakujące elementy opisowe
  4. Uzupełniono trzeci rozdział o nazwie "Inżynieria danych", który przedstawia wyselekcjonowane dane oraz ich podział w ramach pracy
  5. Dokonano restrukturyzacji projektu (przyszłościowo pilnować, żeby nie było bałaganu!)
  6. Rozpoczęto wdrażanie odpowiednich komentarzy, temat rozwojowy tak długo, aż będzie implementowany kod
  7. Rozpoczęcie realizacji skryptu do pobierania kursów bukmacherskich
  #### TO-DO:
  1. Redagowanie pracy: rozpoczęcie (i najlepiej ukończenie) uzupełniania rozdziałów 4 i 5: Budowanie modelu i szczegóły implementacyjne
  2. Ukończenie części implementacyjnej odnośnie przewidywania głównych zdarzeń (ustalono iż główne zdarzenia to: Przewidzenie wyniku / Liczba goli / BTTS / Over/Under), 
  ukończenie sekcji odpowiedzialnej za dostrajanie parametrów uczenia
  4. Przygotowanie oprogramowania ułatwiajacego testowanie (generowanie danych, wykresów, diagramów itd.)
  5. *Utworzenie moduły dla użytkownika (dopytać, czy warto!)*
  6. Przeniesienie projektu na gita (tak jak to powinno już byc od dawna), uzupełnienie change log'a w README.md
### 5 część ralizacji: 10.05.2023 - 24.05.2023
  #### ZREALIZOWANO:
  1. Przeniesienie projektu do systemu kontroli wersji, change log, jak widać, udało się uzupełnić  
  #### TO-DO:
  1. Ukończenie etapu dostrajania modelu oraz systemu rakingowego w celu rozpoczęcia testów, usprawnianie modelu/i o zdarzenia poboczne: (kartki / spalone / rożne)
  2. Przeprowadzenie wyczerpujących i ciekawych testów sprawdzających możliwości zaimplementowanego modelu
  3. Wdrożenie modułu mającego na celu wyszukiwanie korzystnych zakładów u bukmacherów (część pracy) 
  4. Ukończenie redagowania pracy (rozdziały 4 i 6: najlepiej przed końcem czerwca!)
### 6 część realizacji: 24.05.2023 - 07.06.2023
  #### ZREALIZOWANO:
    

### PODSUMOWANIE PRACY
#### Co zrealizowano:
  TO-DO w ramach 6 części realizacji
