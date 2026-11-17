
# Raport defektów – SklepTO

## DEF-01 – Brak resetowania licznika nieudanych logowań

**Wymaganie:** REQ-LOG-02

**Test:** test_login_resets_failed_attempts

**Moduł:** Logowanie

**Priorytet:** Średni

### Opis defektu

Po poprawnym zalogowaniu użytkownika licznik
nieudanych prób logowania nie zostaje wyzerowany.

### Kroki odtworzenia

1. Przywrócić dane początkowe aplikacji.
2. Otworzyć stronę logowania.
3. Wprowadzić login `jan` i błędne hasło.
4. Zalogować się ponownie, używając
   loginu `jan` i hasła `Haslo123`.
5. Otworzyć panel Administracja.
6. Sprawdzić licznik nieudanych prób
   logowania użytkownika `jan`.

### Oczekiwany rezultat

Po poprawnym zalogowaniu licznik
nieudanych prób powinien wynosić 0.

### Rzeczywisty rezultat

Licznik nieudanych prób nadal wynosi 1.

### Wynik testu

FAILED – AssertionError: assert '1' == '0'

### Status

Defekt wykryty podczas testów automatycznych.
Test oznaczony jako xfail (strict=True).


---

## DEF-02 – Brak tytułu strony Kontakt

**Wymaganie:** REQ-UI-02
**Test:** test_contact_title
**Priorytet:** Średni

### Kroki odtworzenia
1. Otworzyć stronę kontakt.php.
2. Sprawdzić zawartość elementu title.

### Oczekiwany rezultat
Tytuł strony: "SklepTO – kontakt".

### Rzeczywisty rezultat
Tytuł strony jest pusty.

### Status
Defekt potwierdzony. Test oznaczony jako xfail.

---

## DEF-03 – Brak tekstu alternatywnego obrazka

**Wymaganie:** REQ-UI-03
**Test:** test_contact_image_alt
**Priorytet:** Średni

### Kroki odtworzenia
1. Otworzyć stronę kontakt.php.
2. Znaleźć obrazek na stronie.
3. Sprawdzić atrybut alt.

### Oczekiwany rezultat
Każdy obrazek posiada niepusty atrybut alt.

### Rzeczywisty rezultat
Atrybut alt obrazka jest pusty lub nieobecny.

### Status
Defekt potwierdzony. Test oznaczony jako xfail.

---

## DEF-04 – Brak etykiety pola E-mail

**Wymaganie:** REQ-UI-04
**Test:** test_contact_email_label
**Priorytet:** Średni

### Kroki odtworzenia
1. Otworzyć stronę kontakt.php.
2. Znaleźć pole E-mail.
3. Sprawdzić istnienie label[for='email'].

### Oczekiwany rezultat
Pole E-mail ma powiązaną etykietę label.

### Rzeczywisty rezultat
Nie znaleziono powiązanej etykiety.

### Status
Defekt potwierdzony. Test oznaczony jako xfail.

---

## DEF-05 – Nieprawidłowy typ pola E-mail

**Wymaganie:** REQ-UI-05
**Test:** test_contact_email_type
**Priorytet:** Średni

### Kroki odtworzenia
1. Otworzyć stronę kontakt.php.
2. Znaleźć pole o identyfikatorze email.
3. Sprawdzić atrybut type.

### Oczekiwany rezultat
Pole E-mail posiada type="email".

### Rzeczywisty rezultat
Pole posiada type="text".

### Status
Defekt potwierdzony. Test oznaczony jako xfail.


---

## DEF-06 – Nieprawidłowy rabat przy karcie i kodzie STUDENT10

**Wymagania:** REQ-KAL-03, REQ-KAL-08

**Test:** test_calculator_results

**Moduł:** Kalkulator zamówienia

**Priorytet:** Wysoki

### Opis defektu

Kalkulator nalicza rabat 20% zamiast 15%,
gdy użytkownik posiada kartę stałego klienta
i wprowadzi poprawny kod rabatowy STUDENT10.

### Kroki odtworzenia

1. Otworzyć stronę kalkulator.php.
2. Wprowadzić wartość koszyka: 150.
3. Zaznaczyć kartę stałego klienta.
4. Wprowadzić kod rabatowy: student10.
5. Wybrać dostawę: kurier.
6. Kliknąć przycisk Oblicz.
7. Sprawdzić wysokość rabatu.

### Oczekiwany rezultat

Rabat: 15%.
Koszt dostawy: 0.00 zł.
Kwota do zapłaty: 127.50 zł.

### Rzeczywisty rezultat

Kalkulator wyświetla rabat 20%
zamiast wymaganego 15%.

Test zakończył się na sprawdzeniu rabatu,
dlatego pozostałe wartości nie zostały
potwierdzone w tym uruchomieniu.

### Wynik testu

FAILED – AssertionError: assert '20%' == '15%'

Defekt występuje dla kodu "student10"
oraz kodu " STUDENT10 " ze spacjami.

### Status

Defekt potwierdzony.
Dwa przypadki testowe oznaczone jako
xfail (strict=True).


---

## DEF-07 – Akceptowanie wielkich liter w loginie

**Wymaganie:** REQ-REJ-02

**Test:** test_invalid_login_format[Abcd]

**Moduł:** Rejestracja

**Priorytet:** Średni

### Kroki odtworzenia

1. Przywrócić początkowe dane aplikacji.
2. Otworzyć stronę rejestracja.php.
3. Wpisać login: Abcd.
4. Wypełnić pozostałe pola poprawnymi danymi.
5. Zaakceptować regulamin.
6. Kliknąć Zarejestruj.

### Oczekiwany rezultat

Wyświetlenie komunikatu:
"Login musi mieć od 3 do 20 znaków
(małe litery, cyfry, _)."

### Rzeczywisty rezultat

Aplikacja nie zgłasza błędu walidacji loginu.
Login zawierający wielką literę jest akceptowany.

### Wynik testu

FAILED – oczekiwany komunikat nie został znaleziony.

### Status

Defekt potwierdzony.
Test oznaczony jako xfail (strict=True).

---

## DEF-08 – Akceptowanie wieku 100 lat

**Wymaganie:** REQ-REJ-05

**Test:** test_invalid_age[100]

**Moduł:** Rejestracja

**Priorytet:** Średni

### Kroki odtworzenia

1. Przywrócić początkowe dane aplikacji.
2. Otworzyć stronę rejestracja.php.
3. Wprowadzić poprawny login i e-mail.
4. Wpisać wiek: 100.
5. Wypełnić pozostałe pola poprawnymi danymi.
6. Zaakceptować regulamin.
7. Kliknąć Zarejestruj.

### Oczekiwany rezultat

Wyświetlenie komunikatu:
"Wiek musi być liczbą całkowitą
z zakresu 18–99."

### Rzeczywisty rezultat

Aplikacja akceptuje wiek 100 lat,
mimo że maksymalny dozwolony wiek wynosi 99.

### Wynik testu

FAILED – oczekiwany komunikat nie został znaleziony.

### Status

Defekt potwierdzony.
Test oznaczony jako xfail (strict=True).


---

## DEF-09 – Możliwość anulowania wysłanego zamówienia

**Wymagania:** REQ-ZAM-04, REQ-ZAM-05, REQ-ZAM-07

**Moduł:** Zamówienia

**Priorytet:** Wysoki

**Testy:**
- test_available_actions[3-expected_actions2]
- test_forbidden_transition[3-Wysłane-SHIPPED]

### Opis defektu

Aplikacja SklepTO umożliwia anulowanie zamówienia,
które posiada już status "Wysłane".

Zgodnie ze specyfikacją zamówienie w stanie
"Wysłane" może jedynie przejść do stanu
"Dostarczone".

### Kroki odtworzenia

1. Przywrócić dane początkowe aplikacji
   przez install.php?reset=1.
2. Zalogować się jako jan / Haslo123.
3. Otworzyć stronę zamowienia.php.
4. Znaleźć zamówienie #3 ze statusem "Wysłane".
5. Sprawdzić dostępne przyciski akcji.
6. Wywołać adres:
   akcja.php?id=3&akcja=anuluj
7. Sprawdzić komunikat i status zamówienia.

### Oczekiwany rezultat

Dla zamówienia #3 dostępna jest wyłącznie
akcja "Potwierdź dostawę".

Próba anulowania powinna wyświetlić komunikat:

"Niedozwolone przejście: Wysłane → anuluj."

Status zamówienia powinien pozostać "Wysłane".

### Rzeczywisty rezultat

Aplikacja wyświetla dodatkowy przycisk "Anuluj".

Po wywołaniu niedozwolonej akcji wyświetla:

"Zamówienie #3: Wysłane → Anulowane."

Status zamówienia zmienia się na "Anulowane".

### Wynik testów

Dwa testy wykryły ten sam defekt:

- test_available_actions – FAILED
- test_forbidden_transition – FAILED

### Status

Defekt potwierdzony.
Oba przypadki testowe oznaczone jako
xfail (strict=True).
