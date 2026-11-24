
# CW6 – Testowanie oprogramowania

Automatyczne testy interfejsu WWW wykonane w Pythonie z użyciem **Selenium WebDriver** i **pytest**.

Testy zostały przeprowadzone na stronie:
https://the-internet.herokuapp.com/

## 1. Cel ćwiczenia

Celem ćwiczenia było poznanie i praktyczne zastosowanie automatycznego testowania aplikacji internetowych z wykorzystaniem Selenium WebDriver oraz pytest.

W ramach laboratorium przetestowano różne sposoby oczekiwania na elementy, obsługę okien JavaScript, pracę z ramkami iframe, interakcje z myszą i klawiaturą oraz wykonywanie zrzutów ekranu.

## 2. Wykorzystane technologie

- Python 3.13
- Selenium WebDriver
- pytest
- pytest-html
- Google Chrome
- PyCharm

## 3. Zakres wykonanych zadań

### Oczekiwanie na elementy
- `time.sleep()` – przykład antywzorca.
- `WebDriverWait` – oczekiwanie jawne.
- `implicitly_wait()` – oczekiwanie niejawne.
- Sprawdzanie widoczności i obecności elementów.

### Dynamiczne elementy
- Usuwanie i dodawanie checkboxa.
- Oczekiwanie na zniknięcie elementu.
- Aktywacja nieaktywnego pola tekstowego.

### Okna JavaScript
- Alert – obsługa przycisku OK.
- Confirm – obsługa OK i Cancel.
- Prompt – wprowadzanie tekstu i anulowanie.

### Ramki i okna przeglądarki
- Przełączanie między zagnieżdżonymi ramkami.
- Otwieranie i zamykanie nowych kart.
- Powrót do głównego dokumentu.

### Akcje użytkownika
- Hover – najechanie kursorem na element.
- Keys – symulowanie naciskania klawiszy.
- Context Menu – kliknięcie prawym przyciskiem myszy.
- Drag and Drop – przeciąganie elementów.
- Infinite Scroll – dynamiczne przewijanie strony.
- Dropdown – wybieranie opcji z listy rozwijanej.

### Zrzuty ekranu
- Automatyczne wykonywanie zrzutów przy błędach.
- Zapisywanie zrzutu konkretnego elementu HTML.

## 4. Zadania samodzielne

W pliku `test_self_study.py` wykonano pięć dodatkowych zadań:

1. Oczekiwanie na pojawienie się i zniknięcie wskaźnika ładowania.
2. Aktywacja pola tekstowego przyciskiem Enable i wprowadzenie danych.
3. Anulowanie okna JavaScript Prompt i sprawdzenie wyniku.
4. Odczyt tekstu z edytora TinyMCE wewnątrz iframe.
5. Przewijanie strony do załadowania co najmniej pięciu akapitów z wykorzystaniem metody `__call__`.

Wszystkie pięć testów zakończyło się pomyślnie.

## 5. Struktura projektu

```text
cw6/
├── config.py
├── conftest.py
├── pytest.ini
├── test_waits.py
├── test_dynamic_controls.py
├── test_alerts.py
├── test_frames_windows.py
├── test_actions.py
├── test_self_study.py
├── report_cw6.html
└── README.md
```

## 6. Uruchamianie testów

Instalacja wymaganych bibliotek:

```powershell
python -m pip install pytest selenium pytest-html
```

Uruchomienie wszystkich testów:

```powershell
python -m pytest -v
```

Uruchomienie testów w trybie Headless (PowerShell):

```powershell
$env:HEADLESS="1"
python -m pytest -q
Remove-Item Env:HEADLESS
```

Generowanie raportu HTML:

```powershell
python -m pytest -v --html=report_cw6.html --self-contained-html
```

## 7. Wyniki testów

Przeprowadzono łącznie **30 testów automatycznych**.

| Status | Liczba testów |
|--------|--------------|
| PASSED | 28 |
| XFAIL | 1 |
| XPASS | 1 |
| FAILED | 0 |
| SKIPPED | 0 |

**Wynik końcowy: 28 passed, 1 xfailed, 1 xpassed.**

XFAIL oznacza oczekiwaną porażkę testu związanego z implicit wait.

XPASS oznacza, że test Drag and Drop z wykorzystaniem ActionChains zakończył się powodzeniem, mimo że był oznaczony jako oczekiwany do niepowodzenia.

Testy zostały również uruchomione dwukrotnie w trybie Headless i uzyskały takie same wyniki.

Raport z testów zapisano w pliku `report_cw6.html`.

## 8. Wnioski

Podczas ćwiczenia poznano praktyczne zastosowanie Selenium WebDriver i pytest do automatycznego testowania stron internetowych.

Wykorzystanie WebDriverWait pozwala na bardziej niezawodne testowanie dynamicznych elementów niż stosowanie stałych opóźnień `time.sleep()`.

Przećwiczono również obsługę okien JavaScript, ramek iframe, interakcje z elementami strony oraz automatyczne zapisywanie zrzutów ekranu.

Wszystkie wymagane testy zostały zaimplementowane i zweryfikowane.


