# 🖨️ Smart Batch PDF Printer - Windows Startgids

Hier zijn alle manieren om de PDF printer te starten op Windows:

## 🚀 **Snelste opties (Aanbevolen)**

### 1. **Dubbel-klik** (Meest eenvoudig)

- Dubbel-klik op `start_printer.bat` in Windows Verkenner
- Werkt direct, geen terminal nodig

### 2. **PowerShell** (Aanbevolen voor gevorderden)

```powershell
# Basis gebruik
.\start_printer.ps1

# Direct naar GUI
.\start_printer.ps1 -Mode gui

# Direct printen van een map
.\start_printer.ps1 -Mode cli -Path "C:\YourPDFs"

# Help
.\start_printer.ps1 -Help
```

## 🔧 **Alle opstartmethoden**

### Command Prompt (CMD)

```batch
start_printer.bat
```

### PowerShell

```powershell
.\start_printer.ps1
```

### Python direct

```python
python start_printer_windows.py
```

## 📋 **Wat gebeurt er als je start?**

1. **Systeem controle** - Controleert Python, printer, etc.
2. **Menu keuze** - Kies tussen GUI, Terminal, of Command Line
3. **Interface start** - Je gekozen interface wordt geladen

## 🖥️ **Interface opties**

| Interface        | Wanneer gebruiken       | Voordelen                                               |
| ---------------- | ----------------------- | ------------------------------------------------------- |
| **GUI**          | Beginners, visueel werk | ✓ Drag & drop<br>✓ Preview<br>✓ Gebruiksvriendelijk     |
| **Interactief**  | Terminal gebruikers     | ✓ Stap-voor-stap<br>✓ Gekleurde output<br>✓ Begeleiding |
| **Command Line** | Scripts, automatisering | ✓ Snel<br>✓ Scriptbaar<br>✓ Alle opties                 |

## ⚡ **Snelle tips**

- **Eerste keer?** → Dubbel-klik `start_printer.bat`
- **Regelmatig gebruik?** → PowerShell: `.\start_printer.ps1 -Mode gui`
- **Automatisering?** → Command Line versie
- **Problemen?** → Kies optie "4. Windows Printer Setup" in het menu

## 🔍 **Probleemoplossing**

### Python niet gevonden?

1. Installeer Python van [python.org](https://www.python.org/downloads/)
2. **Belangrijk**: Vink "Add Python to PATH" aan!
3. Herstart computer
4. Test: `python --version` in CMD

### PowerShell script blocked?

```powershell
# Als administrator:
Set-ExecutionPolicy RemoteSigned
```

### Geen printer?

1. Windows Instellingen → Printers & scanners
2. Voeg printer toe
3. Stel in als standaard

## 🎯 **Snelstart voor verschillende situaties**

### **"Ik wil gewoon PDFs printen"**

→ Dubbel-klik `start_printer.bat` → Kies "1" (GUI)

### **"Ik gebruik terminal/PowerShell veel"**

→ `.\start_printer.ps1 -Mode gui`

### **"Ik wil dit in een script gebruiken"**

→ `python batch_pdf_printer_windows.py "C:\MyPDFs"`

### **"Mijn printer werkt niet"**

→ Start launcher → Kies "4" (Printer Setup)

---

**🎉 Veel printsucces!**
Voor meer hulp, start de launcher en kies "5. Help & Informatie"
