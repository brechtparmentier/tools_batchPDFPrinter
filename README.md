# Smart Batch PDF Printer

Een slimme batch PDF printer die meerdere PDF bestanden in één keer kan verwerken en afdrukken met de standaard printer instellingen.

## Functies

- **Recursief zoeken**: Vindt alle PDF bestanden in een hoofdmap en alle submappen
- **Alfabetische sortering**: Sorteert eerst op mapnaam, daarna op bestandsnaam
- **Batch verwerking**: Drukt bestanden af in batches om de printer niet te overbelasten
- **Standaard printer**: Gebruikt de standaard systeemprinter met default instellingen
- **Logging**: Houdt bij welke bestanden succesvol zijn afgedrukt
- **Dry-run modus**: Bekijk wat er afgedrukt zou worden zonder daadwerkelijk af te drukken

## Vereisten

- Python 3.6+
- Linux systeem met CUPS geïnstalleerd
- Geconfigureerde standaard printer

## Installatie

```bash
# Maak het script uitvoerbaar
chmod +x batch_pdf_printer.py
```

## Gebruik

### Basis gebruik

```bash
python3 batch_pdf_printer.py /pad/naar/pdf/map
```

### Met opties

```bash
# Dry-run om te zien wat er afgedrukt zou worden
python3 batch_pdf_printer.py --dry-run /pad/naar/pdf/map

# Aangepaste batch grootte (standaard: 10 bestanden per batch)
python3 batch_pdf_printer.py --batch-size 5 /pad/naar/pdf/map

# Combinatie van opties
python3 batch_pdf_printer.py --dry-run --batch-size 20 /pad/naar/pdf/map
```

## Voorbeelden

### Voorbeeld mapstructuur
```
/home/user/documenten/
├── 2024/
│   ├── januari/
│   │   ├── factuur_001.pdf
│   │   └── factuur_002.pdf
│   └── februari/
│       └── rapport.pdf
└── archief/
    └── oud_document.pdf
```

### Afdrukvolgorde
Het script zal de bestanden in deze volgorde afdrukken:
1. `/home/user/documenten/2024/februari/rapport.pdf`
2. `/home/user/documenten/2024/januari/factuur_001.pdf`
3. `/home/user/documenten/2024/januari/factuur_002.pdf`
4. `/home/user/documenten/archief/oud_document.pdf`

## Logging

Het script maakt automatisch een logbestand aan: `batch_pdf_printer.log`

Dit bevat informatie over:
- Welke bestanden zijn gevonden
- Welke bestanden succesvol zijn afgedrukt
- Eventuele fouten tijdens het afdrukken

## Fouten oplossen

### "lp command not found"
```bash
# Installeer CUPS op Ubuntu/Debian
sudo apt-get install cups

# Start CUPS service
sudo systemctl start cups
sudo systemctl enable cups
```

### Geen standaard printer geconfigureerd
```bash
# Bekijk beschikbare printers
lpstat -p

# Stel standaard printer in
lpoptions -d printer-naam
```

### PDF bestanden worden niet gevonden
Controleer of:
- Het opgegeven pad bestaat
- Je leesrechten hebt voor de map en submappen
- De bestanden daadwerkelijk de .pdf extensie hebben

## Commando-opties

| Optie | Beschrijving | Standaard |
|-------|--------------|-----------|
| `directory` | Hoofdmap om te doorzoeken (verplicht) | - |
| `--batch-size` | Aantal bestanden per batch | 10 |
| `--dry-run` | Toon wat afgedrukt zou worden zonder af te drukken | Uit |
| `--help` | Toon hulp informatie | - |