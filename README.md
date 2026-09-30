# Orderrapportering

Det här projektet är en refaktorering av ett befintligt Pythonprogram för orderrapportering.

Programmet läser orderdata från en CSV-fil, kontrollerar och förbereder datan, beräknar försäljningsvärden och skapar rapporter för försäljning och returer.

Målet med refaktoreringen är att göra programmet tydligare, mer testbart och enklare att underhålla utan att ändra betydelsen av de ursprungliga rapporterna.

## Vad programmet gör

Programmet läser:

`data/orders.csv`

och skapar följande rapporter i:

`output/`

* `overview.csv` – total försäljning, antal order och antal returer
* `sales_by_category.csv` – försäljning och returer per produktkategori
* `sales_by_region.csv` – försäljning och returer per region
* `returns_by_category.csv` – returgrad per produktkategori

Programmet använder samma grundläggande beräkningar som originalprogrammet.

## Installation

Projektet använder Python och en virtuell miljö.

Skapa och aktivera en virtuell miljö:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installera beroenden:

```powershell
pip install -r requirements.txt
```

## Köra programmet

Stå i projektets rotmapp och kör:

```powershell
python order_report.py
```

Programmet använder logging för information, varningar och fel.

Exempel på information som loggas:

* hur många rader som lästes
* när valideringen är klar
* när rapporterna har skapats
* var rapporterna sparades
* eventuella problem med datan

## Validering

Programmet kontrollerar bland annat:

* att data inte är tom
* att obligatoriska kolumner finns
* att numeriska värden kan tolkas
* att quantity är större än 0
* att unit_price inte är negativ
* att discount ligger mellan 0 och 1

Det finns också ett känt missing-value marker i datan: `unknown`.

Detta behandlas som ett saknat värde och loggas som en warning. På så sätt kan programmet hantera den befintliga datan utan att ändra CSV-filen.

Andra okända och ogiltiga numeriska värden, till exempel `not-a-number`, leder däremot till ett valideringsfel.

## Tester

Projektet använder `pytest`.

Kör alla tester med:

```powershell
pytest -v
```

Tester finns för:

* inläsning av CSV
* saknad fil
* tom fil
* ogiltig CSV
* förberedelse av data
* hantering av saknade värden
* beräkningar
* validering
* ogiltiga numeriska värden
* orimliga numeriska värden
* skapande av rapporter
* sparande av rapporter

Den nuvarande testsviten innehåller 19 tester.

## Projektstruktur

```text
order_report_project/
│
├── data/
│   └── orders.csv
│
├── output/
│   ├── overview.csv
│   ├── sales_by_category.csv
│   ├── sales_by_region.csv
│   └── returns_by_category.csv
│
├── order_report/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── processing.py
│   ├── validation.py
│   └── reports.py
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_processing.py
│   ├── test_reports.py
│   └── test_validation.py
│
├── order_report.py
├── code_review.md
├── README.md
├── requirements.txt
├── pytest.ini
└── .gitignore
```

### Ansvar för modulerna

* `config.py` – innehåller projektets konfiguration med en dataclass.
* `data_loader.py` – läser in CSV-filen och hanterar fel vid inläsning.
* `validation.py` – kontrollerar struktur och datakvalitet.
* `processing.py` – förbereder data och gör beräkningar.
* `reports.py` – skapar och sparar rapporterna.
* `order_report.py` – programmets startpunkt och övergripande flöde.
* `tests/` – automatiska tester för programmets viktigaste funktioner.

## Reflektion

### Vilka problem var viktigast i originalprogrammet?

Originalprogrammet låg i en enda fil och blandade flera olika ansvarsområden. Inläsning, validering, databehandling, beräkningar, rapportskapande och felhantering låg på samma ställe.

Det gjorde koden svårare att läsa, testa och ändra.

Originalprogrammet använde också `print()` för information under körning och hade en generell `try/except` runt nästan hela programmet.

### Vilka förbättringar var viktigast?

Den viktigaste förbättringen var att dela upp programmet i flera moduler med tydliga ansvarsområden.

Jag ersatte också runtime-`print()` med logging och lade till mer tydlig validering och felhantering.

Automatiska tester gör det enklare att upptäcka om en förändring påverkar befintlig funktionalitet.

### Varför använda projektstruktur?

När funktionerna delas upp blir varje del enklare att förstå och testa. Det blir också tydligare var en framtida ändring ska göras.

### Var används OOP/dataclass?

`ReportConfig` i `config.py` är en dataclass som samlar programmets konfiguration på ett ställe.

Det gör det enklare att se vilka filer och rapportnamn programmet använder och minskar behovet av globala konstanter.

### Vad skyddar testerna?

Tester skyddar bland annat datainläsning, validering, beräkningar och skapandet av rapporter.

Om någon senare ändrar exempelvis beräkningen av `discounted_value` kan testerna hjälpa till att upptäcka att beteendet har förändrats.

### Vad var svårast?

En svår del var att förbättra valideringen utan att ändra resultatet från originalprogrammet.

I den befintliga datan finns exempelvis värdet `unknown` i kolumnen `discount`. Jag valde att behandla detta som ett känt saknat värde och logga en warning, medan andra okända numeriska värden leder till ett fel.

### Vad skulle kunna förbättras med mer tid?

Med mer tid skulle jag kunna lägga till fler tester för olika typer av felaktig data och även göra rapporternas filnamn och inställningar ännu enklare att konfigurera.

Jag skulle också kunna förbättra loggingen med mer detaljerad information vid större datakvalitetsproblem.
