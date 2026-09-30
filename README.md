# Orderrapport

Det här programmet läser en CSV-fil med ordrar och gör rapporter om
försäljning och returer.

Jag har tagit ett gammalt skript och gjort om det så att koden blir tydligare.
Rapporterna ska bli precis likadana som förut. Jag har delat upp koden i
flera filer, lagt till logging och tester och gjort bättre felhantering.

Mer om det finns i `code_review.md` och `reflection.md`.

## Vad programmet gör:

Programmet sparar fyra filer i mappen `output`:

- `overview.csv` - total försäljning, antal order och antal returer
- `sales_by_category.csv` - försäljning och returer per produktkategori
- `sales_by_region.csv` - försäljning och returer per region
- `returns_by_category.csv` - hur stor andel som returneras per kategori

Försäljning räknas så här: `quantity * unit_price * (1 - discount)`.

## Installera

Du behöver Python 3.10 eller nyare. Skriv detta i terminalen, i projektmappen:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

På Windows aktiverar du miljön med `.venv\Scripts\activate`.

Programmet behöver `pandas`. Testerna behöver `pytest`. Båda installeras av
kommandot ovan. De står också i filen `pyproject.toml`.

## Köra programmet

```bash
python -m order_report
```

Då läser programmet `data/orders.csv` och sparar rapporterna i `output`.

Vill du använda en annan fil eller mapp kan du skriva så här:

```bash
python -m order_report --input min_fil.csv --output-dir rapporter
```

Programmet skriver i terminalen vad det gör. Om något går fel skriver det
vad felet är och avslutas med kod 1.

## Köra testerna

```bash
pytest
```

Testerna kontrollerar bland annat:

- att ordervärde, rabatt och summor räknas rätt
- att datan rensas rätt, till exempel `" north "` blir `North`
- att det blir fel när en kolumn saknas, filen är tom eller värden är
  orimliga
- att rapporterna blir likadana som från det gamla programmet

## Vad händer med dålig data?

Programmet **stannar med ett fel** om:

- filen saknas eller är tom
- en kolumn saknas
- `quantity` eller `unit_price` är 0 eller mindre
- `discount` är mindre än 0 eller större än 1

Programmet **fortsätter men skriver en varning** om värden saknas. Då byts
de ut på samma sätt som i det gamla programmet:

- saknat antal blir 1
- saknat pris blir medianpriset
- saknad rabatt blir 0
- saknad region eller kategori blir `Unknown`
- saknat värde i `returned` räknas som att ordern inte är returnerad

## Så här ser projektet ut

```
order_report_project/
├── README.md
├── code_review.md
├── reflection.md
├── pyproject.toml
├── data/orders.csv
├── original/order_report.py    (det gamla skriptet, bara för jämförelse)
├── src/order_report/
│   ├── main.py                 (här startar programmet)
│   ├── config.py               (inställningar)
│   ├── loading.py              (läser in datan)
│   ├── validation.py           (kontrollerar datan)
│   ├── processing.py           (rensar och räknar)
│   └── reporting.py            (sparar rapporterna)
└── tests/
    ├── test_*.py
    └── expected/               (rapporter från det gamla programmet)
```

Programmet går igenom stegen i den här ordningen:
läsa in, kontrollera kolumner, rensa, kontrollera värden, räkna, spara.