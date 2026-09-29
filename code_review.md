# Kodgranskning av order_report.py

Jag körde originalprogrammet först och sparade dess resultat. Sedan läste jag
koden och provade vad som händer när något går fel. Originalskriptet ligger
kvar i mappen `original/`.

Originalet är 219 rader lång, har inga funktioner och 8 `print()`.

## 1. Allt ligger i en fil och ingen del har eget ansvar

**Observation:** Filen läser data, kontrollerar kolumner, rensar, räknar,
gör rapporter och sparar filer i ett enda stort block.

**Konsekvens:** Det går inte att testa en enda del utan att köra allt. Vill
man testa hur `discounted_value` räknas måste man ha en riktig CSV-fil och en
`output`-mapp.

**Förslag:** Dela upp i en modul för inläsning, en för kontroller, en för
beräkningar och en för att spara filer.

## 2. Programmet startar när man importerar filen

**Observation:** Det finns ingen `main()`. Koden körs direkt när filen laddas.

**Konsekvens:** Jag provade `import order_report` och då körde hela
programmet. Man kan alltså inte återanvända något i filen eller skriva tester.

**Förslag:** Lägg körningen i en `main()`-funktion med en tydlig startpunkt.

## 3. Dålig felhantering

**Observation:** Allt ligger i ett `try` med `except Exception`. Vid saknad
kolumn kastas bara `Exception("Fel data")`.

**Konsekvens:** Jag provade fyra fel: saknad indatafil, saknad kolumn, saknad
`output`-mapp och körning från fel katalog. Alla gav **exit-kod 0**, som om
allt gått bra. Meddelandet "Fel data" säger inte vilken kolumn som saknas.
Tom data kontrolleras inte alls.

**Förslag:** Egna tydliga felmeddelanden, fånga bara fel man väntar sig och
returnera en exit-kod som visar om det gick bra.

## 4. Datan rensas i tysthet och orimliga värden kontrolleras inte

**Observation:** `orders.csv` har sex rader med saknade eller ogiltiga värden,
till exempel `discount` = `"unknown"` (O0040) och saknat pris (O0062).
Originalet byter ut dem utan att säga något. Negativt antal eller rabatt över
100 % skulle inte upptäckas.

**Konsekvens:** Den som läser rapporten vet inte att en del siffror bygger på
antaganden. Order O0062 ensam är ungefär 1,3 % av total försäljning.

**Förslag:** Behåll reglerna men skriv en varning i loggen för varje kolumn
där värden bytts ut. Lägg till en kontroll av orimliga värden.

## 5. Duplicerad kod

**Observation:** `result1` (per kategori) och `result2` (per region) är
nästan exakt samma kod. `returns_by_category` upprepar grupperingen igen.
`to_csv(os.path.join(...))` och `print("Sparade ...")` står fyra gånger.

**Konsekvens:** Om man ändrar hur `return_rate` räknas måste man ändra på tre
ställen, och det är lätt att glömma ett.

**Förslag:** En funktion som tar kolumnnamnet som parameter, och en loop som
sparar filerna.

## 6. print() i stället för logging

**Observation:** All information skrivs med `print()`.

**Konsekvens:** Det går inte att skilja information från varning och fel, och
det finns ingen tid eller modulnamn i utskriften.

**Förslag:** Använd `logging`, med `logger = logging.getLogger(__name__)` i
varje modul och en enda plats där logging ställs in.

## 7. Hårdkodade sökvägar och otydliga namn

**Observation:** `"data/orders.csv"` och `"output"` står direkt i koden. Namn
som `result1`, `result2` och `data` säger inte vad de innehåller.

**Konsekvens:** Programmet fungerar bara om man startar det från rätt mapp.
Jag provade att köra från en annan mapp, och det gick inte.

**Förslag:** Samla inställningar på ett ställe och ge variablerna tydliga namn.

## 8. Inga tester och ingen dokumentation

**Observation:** Det finns inga tester, ingen README och ingen fil som säger
att programmet behöver pandas.

**Konsekvens:** Man vet inte om en ändring förstör något, och en ny person vet
inte hur man kör programmet.

---

## Vad jag gjorde åt detta

| Punkt | Lösning i den nya koden |
|-------|--------------------------|
| 1 | Egna moduler: `loading`, `validation`, `processing`, `reporting` |
| 2 | `main()` i `main.py`. Import gör ingenting |
| 3 | `ValidationError` med tydliga texter. `main()` returnerar 1 vid fel |
| 4 | Varning i loggen per kolumn, och `check_values` för orimliga värden |
| 5 | `summarize_by()` används för alla rapporter. En loop sparar filerna |
| 6 | `logging` ställs in i `main()` |
| 7 | `ReportConfig` (dataclass) och flaggorna `--input` och `--output-dir` |
| 8 | pytest-tester, `README.md` och `pyproject.toml` |

## Saker jag medvetet inte ändrade

Uppgiften säger att resultaten inte ska ändras. Därför lät jag dessa vara:

- Saknat pris ersätts med medianen för **alla** rader (inte per kategori).
- `return_rate` = antal returnerade rader / antal unika order.
- `overview.csv` visar `80.0` i stället för `80`, eftersom listan blandar
  float och int. Det är fult men filen blir då identisk med originalet.

## Hur jag vet att resultaten är lika

Jag sparade originalets fyra rapporter i `tests/expected/`. Ett test kör
nya programmet och jämför filerna. Det testet är grönt.
