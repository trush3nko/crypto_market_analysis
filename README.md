# Crypto Market Data Analysis

Ein Python-Projekt zur Sammlung und explorativen Analyse junger
Krypto-Token auf Dexscreener.

## Funktionen

-   Asynchroner Abruf von Token- und Pool-Daten
-   Filterung auf junge Pools mit `Volume 1h > 1000 USD` und
    `Liquidität > 500 USD`
-   Vermeidung doppelter Handelspaare anhand der `pair_address`
-   Speicherung der Daten im CSV-Format
-   Datenbereinigung, Feature Engineering und Visualisierung in Jupyter
    Notebook
-   Heuristische Flags zur Markierung auffälliger Handels- und
    Preismuster

## Technologien

Python, `asyncio`, `curl_cffi`, `BeautifulSoup`, `pandas`, `NumPy`,
`Matplotlib`, `Seaborn` und Jupyter Notebook.

## Projektstruktur

-   `main.py` -- startet den Datensammler
-   `functions.py` -- enthält Funktionen zum Abrufen und Speichern der
    Daten
-   `crypto.csv` -- gesammelte Marktdaten
-   `notebook.ipynb` -- Datenbereinigung, Analyse und Visualisierungen
-   `requirements.txt` -- benötigte Python-Bibliotheken

## Installation und Verwendung

Abhängigkeiten installieren:

``` bash
pip install -r requirements.txt
```

Datensammlung starten:

``` bash
python main.py
```

Für die Analyse `notebook.ipynb` in Jupyter Notebook öffnen. Das
Notebook erwartet die Datei `crypto.csv` im selben Verzeichnis.

## Hinweise

Die Analyse konzentriert sich auf eine gefilterte Stichprobe junger
Pools. Für die Auswertung wird pro Token der Pool mit der höchsten
Liquidität im gesammelten Datensatz verwendet.

Die Risikoindikatoren basieren auf heuristischen Schwellenwerten und
sind nicht als verlässliche Betrugserkennung oder Anlageberatung
gedacht. Fehlende Daten und die gewählten Filter können die Ergebnisse
beeinflussen. Die CSV-Daten sind eine Momentaufnahme und können mit der
Zeit veralten.
