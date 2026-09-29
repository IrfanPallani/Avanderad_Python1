# Reflektion

**1. Vilka var de viktigaste problemen i originalkoden?**
Allt låg i en enda fil utan funktioner, så inget gick att testa. Programmet
startade också redan när man importerade filen. Felhanteringen var dålig:
alla fel fångades av ett `except Exception` och programmet gav ändå exit-kod 0.
Datan rensades dessutom utan att någon fick veta det. Sedan var det mycket
kod som upprepades, och `print()` användes i stället för logging.

**2. Vilka förändringar förbättrade programmet mest?**
Att dela upp koden i moduler var viktigast, för det gjorde att jag kunde
testa varje del. Jag tycker också att bättre felmeddelanden och varningar i
loggen gjorde stor skillnad. Nu ser man vilka värden som ersatts och varför
ett fel uppstod.

**3. Varför valde jag den projektstruktur jag använde?**
Jag följde exemplet i uppgiften: `config`, `loading`, `validation`,
`processing` och `reporting`. Varje fil motsvarar ett steg i programmet. Jag
lade till `main.py` som enda startpunkt. Jag använde `src`-mapp och
`pip install -e .` så att importerna fungerar utan `sys.path`. Jag gjorde inte
fler filer än nödvändigt.

**4. Var använde jag OOP/dataclass och varför?**
Jag använde en dataclass, `ReportConfig`, för inställningarna (sökväg till
indata och mapp för utdata). Då slipper jag lösa globala variabler, och det är
tydligt vad som styr en körning. Den är `frozen`, så den kan inte ändras av
misstag. Resten är vanliga funktioner, eftersom en klass inte skulle göra
koden enklare där.

**5. Vilka beteenden skyddar testerna?**
Testerna skyddar beräkningarna (ordervärde, rabatt, summor, sortering),
rensningen av data och kontrollerna, till exempel saknad kolumn, tom data och
orimliga värden. De testar också att programmet ger rätt exit-kod vid fel. Ett
test jämför rapporterna med originalets rapporter. Om jag eller någon annan
ändrar koden senare ser man direkt om resultatet ändrats av misstag. Jag
kontrollerade att testerna fungerar genom att medvetet lägga in fel i koden,
och då blev testerna röda.

**6. Vad var svårast?**
Att refaktorera utan att ändra resultatet. Jag hade velat rätta några saker,
till exempel att `overview.csv` visar `80.0`. Men då hade filen inte blivit
likadan som originalet, så jag lät det vara och skrev om det i
`code_review.md`. Det var också svårt att välja vad som ska ge fel och vad
som bara ska ge en varning.

**7. Vad hade jag velat förbättra med mer tid?**
- Rätta `80.0` i `overview.csv`.
- Räkna medianpris per produktkategori i stället för över alla rader.
- Kontrollera datumformatet i `order_date`.
- Köra testerna automatiskt på GitHub (GitHub Actions).
