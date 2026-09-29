# Orderrapport

Ett program som läser orderdata från en CSV-fil och skapar rapporter över
försäljning och returer. Det är en förbättrad version av ett äldre skript.
Rapporterna blir samma som förut, men koden är tydligare och har tester.

Läs också `code_review.md` (granskning av originalkoden) och `reflection.md`.

## Vad programmet skapar

Fyra filer sparas i mappen `output/`:

| Fil | Innehåll |
|-----|----------|
| `overview.csv` | Total försäljning, antal order och antal returer |
| `sales_by_category.csv` | Försäljning och returer per produktkategori |
| `sales_by_region.csv` | Försäljning och returer per region |
| `returns_by_category.csv` | Returandel per produktkategori |

Försäljning räknas som `quantity * unit_price * (1 - discount)`.

## Installera

Du behöver Python 3.10 eller nyare.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Beroenden finns i `pyproject.toml`: `pandas` (programmet) och `pytest`
(tester). Testat med pandas 2.3 och 3.0.

## Köra programmet

Kör från projektets huvudmapp:

```bash
python -m order_report
```

Du kan också välja fil och mapp själv:

```bash
python -m order_report --input min_fil.csv --output-dir rapporter
```

Programmet skriver vad det gör i terminalen (logging). Om något är fel skriver
det en tydlig förklaring och avslutas med kod 1.

## Köra testerna

```bash
pytest
```

Det finns 45 tester. Viktigast:

- Beräkningar av ordervärde, rabatt, summor och sortering.
- Rensning av data (saknade värden, stora/små bokstäver, `Yes`/`ja`).
- Felfall: saknad fil, saknad kolumn, tom data och orimliga värden.
- Ett test som visar att rapporterna är likadana som från originalprogrammet.

## Hur datan hanteras

| Problem i datan | Vad programmet gör |
|-----------------|--------------------|
| Filen finns inte eller är tom | Fel |
| En kolumn saknas | Fel med namn på kolumnen |
| Inga rader | Fel |
| `quantity` eller `unit_price` är 0 eller mindre | Fel |
| `discount` är utanför 0–1 | Fel |
| Saknat antal | Blir 1 (varning i loggen) |
| Saknat pris | Blir medianpriset (varning) |
| Saknad eller ogiltig rabatt | Blir 0 (varning) |
| Saknad region eller kategori | Blir `Unknown` (varning) |
| Saknat värde i `returned` | Räknas som inte returnerad (varning) |
| `" north "`, `"SOUTH"`, `"Yes"` | Rättas till |

## Struktur

```
order_report_project/
├── README.md
├── code_review.md
├── reflection.md
├── pyproject.toml
├── data/orders.csv
├── original/order_report.py     # gamla skriptet, bara för jämförelse
├── src/order_report/
│   ├── main.py                  # STARTPUNKT (main och run)
│   ├── config.py                # inställningar (ReportConfig)
│   ├── loading.py               # läser in datan
│   ├── validation.py            # kontrollerar datan
│   ├── processing.py            # rensar och räknar
│   └── reporting.py             # sparar rapporterna
└── tests/
    ├── test_*.py
    └── expected/                # rapporter från originalet, används som facit
```

Flödet i `main.run()`:
läs in → kontrollera kolumner → rensa → kontrollera värden → räkna → spara.
