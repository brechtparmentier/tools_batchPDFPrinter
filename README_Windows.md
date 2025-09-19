# Smart Batch PDF Printer - Windows Handleiding

## 🚀 Snel starten

### Optie 1: Dubbel-klik (Eenvoudigst)

1. Dubbel-klik op `start_printer.bat`
2. Volg de instructies op het scherm

### Optie 2: PowerShell (Aanbevolen)

1. Open PowerShell in deze map
2. Voer uit: `.\start_printer.ps1`
3. Of direct GUI: `.\start_printer.ps1 -Mode gui`

### Optie 3: Command Prompt

1. Open Command Prompt in deze map
2. Voer uit: `start_printer.bat`

## 📋 Vereisten

- **Python 3.6+** - Download van [python.org](https://www.python.org/downloads/)
  - ⚠️ Vink "Add Python to PATH" aan tijdens installatie!
- **Windows 10/11**
- **Geconfigureerde printer** - Zorg dat je een standaard printer hebt ingesteld

## 🖨️ Printer instellen

1. Ga naar **Instellingen** → **Printers & scanners**
2. Klik op je gewenste printer
3. Klik **"Instellen als standaard"**
4. Test door een PDF te printen vanuit een andere applicatie

## 🎯 Interfaces

### 🖥️ GUI Interface (Grafisch)

- **Beste keuze voor beginners**
- Drag & drop ondersteuning
- Visuele preview van bestanden
- Real-time voortgangsindicator

### 📱 Interactief Menu (Terminal)

- Gebruiksvriendelijke navigatie
- Stap-voor-stap begeleiding
- Gekleurde output voor overzicht

### ⚡ Command Line (Geavanceerd)

- Voor scripts en automatisering
- Snelste optie voor herhaald gebruik
- Alle geavanceerde opties beschikbaar

## 💡 Voorbeelden

### Direct starten met PowerShell:

```powershell
# GUI starten
.\start_printer.ps1 -Mode gui

# Direct een map printen
.\start_printer.ps1 -Mode cli -Path "C:\Users\Documents\PDFs"

# Help tonen
.\start_printer.ps1 -Help
```

### Python direct aanroepen:

```batch
# GUI versie
python start_printer_windows.py

# Command line met map
python batch_pdf_printer_windows.py "C:\PDFs"

# Met opties
python batch_pdf_printer_windows.py --dry-run "C:\PDFs"
```

## 🔧 Problemen oplossen

### ❌ "Python is niet geïnstalleerd"

1. Download Python van [python.org](https://www.python.org/downloads/)
2. **Belangrijk**: Vink "Add Python to PATH" aan!
3. Herstart je computer na installatie
4. Test: open Command Prompt en typ `python --version`

### ❌ "Geen standaard printer"

1. Ga naar **Instellingen** → **Printers & scanners**
2. Klik op gewenste printer → **"Instellen als standaard"**
3. Test met een PDF uit een andere applicatie

### ❌ "Script kan niet worden uitgevoerd" (PowerShell)

1. Open PowerShell als Administrator
2. Voer uit: `Set-ExecutionPolicy RemoteSigned`
3. Kies **Y** (Yes)
4. Probeer opnieuw

### ❌ PDF bestanden worden niet afgedrukt

1. Controleer of PDFs niet zijn vergrendeld door andere programma's
2. Test handmatig printen van een PDF
3. Bekijk de log file: `batch_pdf_printer.log`

## 📁 Projectstructuur

```
tools_batchPDFPrinter/
├── start_printer.bat           # Windows batch launcher
├── start_printer.ps1           # PowerShell launcher (aanbevolen)
├── start_printer_windows.py    # Python hoofdmenu
├── gui_pdf_printer_windows.py  # GUI interface (nog te maken)
├── interactive_pdf_printer_windows.py  # Interactief menu (nog te maken)
├── batch_pdf_printer_windows.py # Command line versie (nog te maken)
├── README_Windows.md           # Deze handleiding
└── batch_pdf_printer.log      # Log bestand (wordt automatisch aangemaakt)
```

## 🆘 Hulp nodig?

1. Start een van de interfaces
2. Kies optie **"Help & Informatie"**
3. Of gebruik: `.\start_printer.ps1 -Help`

## 🎯 Tips

- **Test eerst je printer** met een bestaand PDF bestand
- **Start klein** met een paar bestanden voordat je grote batches print
- **Gebruik dry-run modus** om te controleren wat er geprint wordt
- **Bekijk de logs** als er problemen zijn

## 🔄 Migratie van Linux versie

Als je de Linux versie gebruikt hebt:

- De Windows versie gebruikt de Windows Print API in plaats van CUPS
- Alle functionaliteit blijft hetzelfde
- Alleen de printer communicatie is aangepast voor Windows

---

**🖨️ Happy Printing!** 🎉
