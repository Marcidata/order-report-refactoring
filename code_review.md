# Code review – orderrapportering

## 1. För många ansvarsområden i samma fil

**Observation**

Originalprogrammet innehåller inläsning av data, validering, databehandling, beräkningar, rapportskapande, filsparande och felhantering i samma fil.

**Konsekvens**

Det blir svårt att förstå programmet och svårt att testa eller ändra en specifik del utan att påverka andra delar.

**Förslag**

Dela upp programmet i moduler med tydliga ansvarsområden, till exempel `data_loader.py`, `validation.py`, `processing.py` och `reports.py`.

---

## 2. Runtime-information skrivs med print()

**Observation**

Originalprogrammet använder flera `print()`-anrop för att visa programmets status och fel.

**Konsekvens**

Det blir svårare att styra och använda programmets loggar på ett professionellt sätt.

**Förslag**

Använd Python-modulen `logging` och konfigurera logging centralt i programmets startpunkt.

---

## 3. Import kan orsaka programkörning

**Observation**

Originalprogrammets huvudsakliga programflöde ligger direkt i filen och körs vid import.

**Konsekvens**

Om filen importeras från ett annat program kan den börja läsa och skriva filer direkt.

**Förslag**

Lägg programmets flöde i en `main()`-funktion och använd:

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

På så sätt körs programmet endast när filen startas direkt.

---

## 4. Begränsad validering av data

**Observation**

Originalprogrammet konverterar numeriska värden med `pd.to_numeric(..., errors="coerce")`. Det innebär att vissa felaktiga värden kan omvandlas till saknade värden utan att problemet blir tydligt.

**Konsekvens**

Ett datakvalitetsproblem kan passera utan att användaren får veta vad som hände.

**Förslag**

Lägg valideringen i en separat modul och kontrollera både obligatoriska kolumner, numeriska värden och rimliga intervall.

Kända missing-value markörer, som `unknown` i den befintliga datan, kan hanteras som saknade värden och samtidigt loggas som en warning. Andra okända ogiltiga numeriska värden ska ge ett tydligt valideringsfel.

---

## 5. Felhanteringen är för generell

**Observation**

Originalprogrammet använder ett stort `try/except Exception` runt nästan hela programmet.

**Konsekvens**

Olika typer av fel behandlas på samma sätt och det kan bli svårare att förstå vad som faktiskt gick fel.

**Förslag**

Hantera relevanta feltyper mer specifikt, till exempel saknad fil, tom CSV-fil, parserfel och valideringsfel.

---

## 6. Konfiguration och filnamn är hårdkodade

**Observation**

Sökvägar och filnamn ligger direkt i programmets kod.

**Konsekvens**

Det blir mindre tydligt och mer omständligt att ändra programmets konfiguration.

**Förslag**

Samla konfigurationen i en dataclass, `ReportConfig`, som innehåller inputfil, outputmapp och rapporternas filnamn.

---

## Reflektion

Den viktigaste förändringen var att dela upp det stora originalprogrammet i mindre delar med tydliga ansvarsområden. Det gör programmet enklare att läsa och testa.

Jag valde att använda en dataclass för `ReportConfig` eftersom programmets filvägar och rapportnamn hör ihop och kan samlas på ett tydligt ställe.

Logging var också en viktig förbättring. Information från programmets körning visas nu med logging i stället för `print()`.

Tester är viktiga eftersom de skyddar programmets viktigaste beteenden. Om någon senare ändrar exempelvis en beräkning eller validering kan testerna visa om den befintliga funktionaliteten har påverkats.

En sak som krävde extra kontroll var att refaktoreringen inte skulle ändra resultatet från originalprogrammet. Efter refaktoreringen kördes programmet mot samma `orders.csv` och rapporterna jämfördes med resultaten från originalprogrammet. Resultaten för total försäljning, antal order, returer samt rapporterna per kategori och region var oförändrade.

Den befintliga datan innehåller också `unknown` som värde i `discount`. I stället för att ändra källfilen hanteras detta som ett känt saknat värde. Programmet loggar en warning och använder sedan samma standardbeteende som originalprogrammet för saknad rabatt, alltså `0`.

Med mer tid skulle jag kunna lägga till ännu fler tester för olika typer av felaktig data och förbättra konfigurationen ytterligare.
