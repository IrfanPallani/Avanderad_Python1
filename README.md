# Orderrapport

Det här projektet handlar om att refaktorera ett befintligt Pythonprogram som arbetar med orderdata.

Programmet läser en CSV-fil med ordrar och skapar olika rapporter om försäljning och returer. Jag har utgått från det gamla programmet och försökt göra koden tydligare och lättare att förstå och testa.

Målet var inte att bygga ett nytt analysprogram, utan att förbättra hur det gamla programmet är uppbyggt.

## Vad programmet gör

Programmet läser orderdata från:

```text
data/orders.csv
```

Sedan kontrollerar och bearbetar programmet datan och skapar fyra rapporter.

Rapporterna sparas i mappen `output`:

* `overview.csv` – visar total försäljning, antal order och antal returer
* `sales_by_category.csv` – visar försäljning och returer per produktkategori
* `sales_by_region.csv` – visar försäljning och returer per region
* `returns_by_category.csv` – visar hur stor del av ordrarna som returneras per kategori

Försäljningen räknas ut med:

```text
quantity * unit_price * (1 - discount)
```

## Vad jag har ändrat

Jag har delat upp det gamla programmet i flera delar. På det sättet har varje fil ett tydligare ansvar.

Jag har bland annat:

* delat upp koden i flera moduler
* gjort tydligare namn på funktioner och variabler
* lagt till logging istället för vanlig `print()` för information om körningen
* lagt till validering av data
* lagt till bättre felhantering
* lagt till en dataclass för programmets inställningar
* skrivit automatiska tester med pytest
* jämfört resultaten med det gamla programmet

Tanken är att programmet fortfarande ska ge samma resultat som tidigare, men att koden ska vara lättare att förstå och ändra.

## Projektets struktur

Projektet är uppdelat så här:

```text
order_report_project/
│
├── README.md
├── code_review.md
├── reflection.md
├── pyproject.toml
│
├── data/
│   └── orders.csv
│
├── original/
│   └── order_report.py
│
├── src/
│   └── order_report/
│       ├── main.py
│       ├── config.py
│       ├── loading.py
│       ├── validation.py
│       ├── processing.py
│       └── reporting.py
│
└── tests/
    ├── test_*.py
    └── expected/
```

Filerna har olika uppgifter:

* `main.py` – startar programmet
* `config.py` – innehåller programmets inställningar
* `loading.py` – läser in CSV-filen
* `validation.py` – kontrollerar att datan är korrekt
* `processing.py` – rensar datan och gör beräkningar
* `reporting.py` – skapar och sparar rapporterna
* `tests/` – innehåller testerna
* `original/` – innehåller det gamla programmet för jämförelse

Programmet går alltså igenom ungefär den här ordningen:

```text
Läsa in data
     ↓
Kontrollera kolumner
     ↓
Rensa data
     ↓
Kontrollera värden
     ↓
Göra beräkningar
     ↓
Skapa rapporter
     ↓
Spara resultat
```

## Installation

Du behöver Python 3.10 eller senare.

Öppna terminalen i projektmappen och skapa en virtuell miljö:

```bash
python -m venv .venv
```

På Windows:

```bash
.venv\Scripts\activate
```

På Linux eller macOS:

```bash
source .venv/bin/activate
```

Installera sedan projektet:

```bash
pip install -e ".[dev]"
```

Projektet använder bland annat:

* `pandas` för att läsa och bearbeta data
* `pytest` för automatiska tester

Beroendena finns i `pyproject.toml`.

## Köra programmet

När installationen är klar kan programmet köras med:

```bash
python -m order_report
```

Då används:

```text
data/orders.csv
```

och rapporterna sparas i:

```text
output/
```

Det går också att ange en annan CSV-fil och en annan output-mapp:

```bash
python -m order_report --input min_fil.csv --output-dir rapporter
```

När programmet körs skriver logging ut information om vad som händer.

Om något viktigt är fel, till exempel att filen saknas eller att data inte går att använda, får man ett felmeddelande och programmet avslutas.

## Tester

Testerna körs med:

```bash
pytest
```

Jag har testat olika delar av programmet, till exempel:

* beräkning av ordervärde
* rabatt
* summeringar
* returer
* data som behöver rensas
* saknade kolumner
* tom data
* orimliga värden

Jag har både testat vanliga fall och fall där programmet ska ge ett fel.

Testerna är till för att kontrollera att programmet fortfarande fungerar om jag senare ändrar koden.

## Felaktig eller saknad data

Programmet stoppar med ett fel om:

* CSV-filen saknas
* filen är tom
* en obligatorisk kolumn saknas
* `quantity` är 0 eller mindre
* `unit_price` är 0 eller mindre
* `discount` är mindre än 0 eller större än 1

Om vissa värden saknas försöker programmet istället hantera dem på samma sätt som det gamla programmet.

Exempel:

* saknat `quantity` blir `1`
* saknat `unit_price` ersätts med medianpriset
* saknad `discount` blir `0`
* saknad region blir `Unknown`
* saknad produktkategori blir `Unknown`
* saknat värde i `returned` räknas som att ordern inte är returnerad

På det sättet behöver inte programmet stoppa bara för att någon enstaka uppgift saknas.

## Logging

Jag har bytt ut körinformation från `print()` till Python `logging`.

Logging används bland annat för att visa:

* när data läses in
* hur många rader som lästs
* när valideringen är klar
* när rapporterna skapas
* var rapporterna sparas
* varningar och fel

Jag har försökt att inte logga varje liten sak, utan bara information som är användbar när programmet körs.

## Jämförelse med originalprogrammet

Det gamla programmet finns kvar i:

```text
original/order_report.py
```

Det används för att jämföra resultaten.

Efter refaktoreringen ska rapporterna fortfarande innehålla samma beräkningar och resultat som tidigare.

Det betyder att jag har fokuserat på att ändra **hur koden är byggd**, och inte på att ändra vad programmet ska göra.

## Code review

I filen `code_review.md` har jag gått igenom originalkoden och beskrivit problem som jag hittade.

Jag har bland annat tittat på:

* ansvarsfördelning
* projektstruktur
* duplicerad kod
* namngivning
* felhantering
* logging
* testbarhet
* hårdkodade värden

För varje problem beskriver jag vad jag såg, varför det kan vara ett problem och hur jag har tänkt förbättra det.

## Reflektion

I `reflection.md` skriver jag om hur arbetet gick och vilka förändringar jag gjorde.

Jag tar bland annat upp:

* vilka problem originalprogrammet hade
* vilka förändringar som hjälpte mest
* varför jag valde den här projektstrukturen
* varför jag använder dataclass
* vad testerna hjälper till med
* vad som var svårt
* vad jag skulle kunna förbättra om jag hade mer tid

## Sammanfattning

Det viktigaste med projektet var att ta ett fungerande men ganska rörigt program och göra det mer strukturerat.

Jag har försökt göra förändringarna steg för steg så att programmet fortfarande fungerar på samma sätt som tidigare.

Resultatet är ett program där olika delar har tydligare ansvar och där det är enklare att testa, hitta fel och göra ändringar i framtiden.