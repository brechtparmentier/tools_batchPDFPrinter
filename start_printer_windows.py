#!/usr/bin/env python3
"""
Smart Batch PDF Printer Windows Launcher
Windows-versie van de PDF printer launcher
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class Colors:
    """ANSI color codes voor gekleurde terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Print welkomst banner."""
    print(f"{Colors.OKCYAN}")
    print("🖨️ ==================================")
    print("   SMART BATCH PDF PRINTER")
    print("   Windows Versie")
    print("====================================")
    print(f"{Colors.ENDC}")


def check_requirements():
    """Controleer of alle vereisten aanwezig zijn."""
    errors = []
    warnings = []
    
    # Check Python versie
    if sys.version_info < (3, 6):
        errors.append("Python 3.6+ is vereist")
    
    # Check Windows versie
    if platform.system() != "Windows":
        warnings.append("Deze versie is specifiek voor Windows")
    
    # Check tkinter voor GUI
    try:
        import tkinter
        gui_available = True
    except ImportError:
        gui_available = False
        warnings.append("tkinter niet beschikbaar - GUI interface werkt niet")
    
    # Check of we een standaard printer hebben
    try:
        result = subprocess.run(['wmic', 'printer', 'where', 'default=true', 'get', 'name'], 
                              capture_output=True, text=True, check=True)
        if not result.stdout.strip() or 'No Instance(s) Available' in result.stdout:
            warnings.append("Geen standaard printer gevonden")
        else:
            printer_name = result.stdout.strip().split('\n')[-1].strip()
            print(f"{Colors.OKGREEN}✓ Standaard printer: {printer_name}{Colors.ENDC}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        warnings.append("Kan printer status niet controleren")
    
    # Toon resultaten
    if errors:
        print(f"{Colors.FAIL}❌ Fouten gevonden:{Colors.ENDC}")
        for error in errors:
            print(f"   • {error}")
        return False
    
    if warnings:
        print(f"{Colors.WARNING}⚠️  Waarschuwingen:{Colors.ENDC}")
        for warning in warnings:
            print(f"   • {warning}")
        print()
    
    return True


def show_menu():
    """Toon het hoofdmenu."""
    print(f"{Colors.OKBLUE}Beschikbare interfaces:{Colors.ENDC}")
    print()
    print(f"{Colors.OKGREEN}1){Colors.ENDC} 🖥️  GUI Interface (Grafisch - Aanbevolen)")
    print("   - Klik en sleep interface")
    print("   - Visuele preview")
    print("   - Real-time voortgang")
    print()
    print(f"{Colors.OKGREEN}2){Colors.ENDC} 📱 Interactief Menu (Terminal)")
    print("   - Gebruiksvriendelijke navigatie")
    print("   - Stap-voor-stap begeleiding")
    print("   - Gekleurde output")
    print()
    print(f"{Colors.OKGREEN}3){Colors.ENDC} ⚡ Command Line (Geavanceerd)")
    print("   - Voor ervaren gebruikers")
    print("   - Scriptbaar en automatiseerbaar")
    print("   - Snelle directe toegang")
    print()
    print(f"{Colors.OKGREEN}4){Colors.ENDC} 🔧 Windows Printer Setup")
    print("   - Printer configuratie hulp")
    print("   - Test je printer")
    print("   - Standaard printer instellen")
    print()
    print(f"{Colors.OKGREEN}5){Colors.ENDC} ❓ Help & Informatie")
    print()
    print(f"{Colors.OKGREEN}q){Colors.ENDC} 🚪 Afsluiten")
    print()


def launch_gui():
    """Start de GUI interface."""
    try:
        import tkinter
        print(f"\n{Colors.OKGREEN}🖥️  GUI Interface starten...{Colors.ENDC}")
        subprocess.run([sys.executable, "gui_pdf_printer_windows.py"], check=True)
    except ImportError:
        print(f"{Colors.FAIL}❌ tkinter is niet beschikbaar{Colors.ENDC}")
        print("Schakel over naar interactief menu...")
        launch_interactive()
    except FileNotFoundError:
        print(f"{Colors.FAIL}❌ GUI bestand niet gevonden{Colors.ENDC}")
        print("Start eerst de Windows versie installer")


def launch_interactive():
    """Start de interactieve interface."""
    print(f"\n{Colors.OKGREEN}📱 Interactief Menu starten...{Colors.ENDC}")
    try:
        subprocess.run([sys.executable, "interactive_pdf_printer_windows.py"], check=True)
    except FileNotFoundError:
        print(f"{Colors.FAIL}❌ Interactief bestand niet gevonden{Colors.ENDC}")
        print("Start eerst de Windows versie installer")


def launch_cli():
    """Start de command line interface."""
    print(f"\n{Colors.OKGREEN}⚡ Command Line Interface{Colors.ENDC}")
    print("Gebruik: python batch_pdf_printer_windows.py [opties] <map>")
    print()
    print("Voorbeelden:")
    print("  python batch_pdf_printer_windows.py C:\\Users\\Documents")
    print("  python batch_pdf_printer_windows.py --dry-run C:\\PDFs")
    print("  python batch_pdf_printer_windows.py --batch-size 5 C:\\Work")
    print()
    print("Voor meer opties: python batch_pdf_printer_windows.py --help")
    print()
    
    pdf_path = input(f"{Colors.WARNING}Script direct uitvoeren? Voer dan het pad in (of Enter voor terug): {Colors.ENDC}")
    if pdf_path.strip():
        try:
            subprocess.run([sys.executable, "batch_pdf_printer_windows.py", pdf_path.strip()], check=True)
        except FileNotFoundError:
            print(f"{Colors.FAIL}❌ CLI bestand niet gevonden{Colors.ENDC}")
            print("Start eerst de Windows versie installer")


def printer_setup():
    """Help met printer setup."""
    print(f"\n{Colors.OKBLUE}🔧 WINDOWS PRINTER SETUP{Colors.ENDC}")
    print()
    
    print(f"{Colors.OKGREEN}Beschikbare printers:{Colors.ENDC}")
    try:
        result = subprocess.run(['wmic', 'printer', 'get', 'name,default'], 
                              capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        printers = []
        for line in lines:
            if line.strip():
                parts = line.strip().split()
                if len(parts) >= 2:
                    is_default = parts[0].upper() == 'TRUE'
                    name = ' '.join(parts[1:])
                    printers.append((name, is_default))
                    status = "🟢 (Standaard)" if is_default else "⚪"
                    print(f"  {status} {name}")
        
        if not printers:
            print(f"  {Colors.WARNING}Geen printers gevonden{Colors.ENDC}")
            print("\n📝 Installeer eerst een printer via Windows Instellingen:")
            print("   Settings → Printers & scanners → Add printer")
        
        print(f"\n{Colors.OKGREEN}Test opdrachten:{Colors.ENDC}")
        print("1. Test printer met een bestaand PDF bestand")
        print("2. Printer instellingen openen")
        print("3. Standaard printer wijzigen")
        print("4. Terug naar hoofdmenu")
        
        choice = input(f"\n{Colors.OKCYAN}Keuze (1-4): {Colors.ENDC}")
        
        if choice == "1":
            test_file = input("Pad naar test PDF bestand: ")
            if os.path.exists(test_file):
                try:
                    os.startfile(test_file, "print")
                    print(f"{Colors.OKGREEN}✓ Print opdracht verzonden{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.FAIL}❌ Fout bij printen: {e}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}❌ Bestand niet gevonden{Colors.ENDC}")
        
        elif choice == "2":
            subprocess.run(['rundll32', 'printui.dll,PrintUIEntry', '/s'])
        
        elif choice == "3":
            print("Open Windows Instellingen → Printers & scanners")
            print("Klik op gewenste printer → 'Set as default'")
            subprocess.run(['ms-settings:printers'])
            
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"{Colors.FAIL}❌ Kan printer informatie niet ophalen: {e}{Colors.ENDC}")


def show_help():
    """Toon help informatie."""
    print(f"\n{Colors.OKBLUE}📖 HELP & INFORMATIE{Colors.ENDC}")
    print()
    print(f"{Colors.WARNING}Wat doet deze tool?{Colors.ENDC}")
    print("• Zoekt recursief naar alle PDF bestanden in een map")
    print("• Sorteert ze alfabetisch (eerst per map, dan per bestand)")
    print("• Drukt ze af in batches met uw standaard printer")
    print()
    print(f"{Colors.WARNING}Windows specifieke functionaliteit:{Colors.ENDC}")
    print("• Gebruikt Windows print API in plaats van CUPS")
    print("• Ondersteunt alle Windows printers")
    print("• Integreert met Windows printer dialogen")
    print()
    print(f"{Colors.WARNING}Welke interface kiezen?{Colors.ENDC}")
    print(f"{Colors.OKGREEN}GUI Interface{Colors.ENDC} - Beste keuze voor de meeste gebruikers")
    print("  ✓ Makkelijkste bediening")
    print("  ✓ Visuele feedback")
    print("  ✓ Drag & drop ondersteuning")
    print()
    print(f"{Colors.OKGREEN}Interactief Menu{Colors.ENDC} - Voor terminal gebruikers")
    print("  ✓ Werkt via PowerShell/CMD")
    print("  ✓ Gekleurde interface")
    print("  ✓ Stap-voor-stap begeleiding")
    print()
    print(f"{Colors.OKGREEN}Command Line{Colors.ENDC} - Voor scripts en automatisering")
    print("  ✓ Scriptbaar")
    print("  ✓ Snelst voor herhaalde taken")
    print("  ✓ Alle opties beschikbaar")
    print()
    print(f"{Colors.WARNING}Vereisten:{Colors.ENDC}")
    print("• Python 3.6+")
    print("• Windows 10/11")
    print("• Geconfigureerde printer")
    print("• Voor GUI: tkinter (meestal standaard geïnstalleerd)")
    print()
    print(f"{Colors.WARNING}Problemen oplossen:{Colors.ENDC}")
    print("• Test eerst uw printer vanuit een andere applicatie")
    print("• Controleer standaard printer in Windows Instellingen")
    print("• Zorg dat PDF bestanden niet zijn vergrendeld")
    print("• Logs staan in: batch_pdf_printer.log")
    print()
    
    input(f"{Colors.OKCYAN}Druk Enter om terug te gaan...{Colors.ENDC}")


def main():
    """Hoofdfunctie."""
    print_banner()
    
    if not check_requirements():
        print(f"\n{Colors.FAIL}Kan niet doorgaan vanwege fouten hierboven.{Colors.ENDC}")
        input("Druk Enter om af te sluiten...")
        return
    
    while True:
        show_menu()
        
        choice = input(f"{Colors.OKCYAN}Voer uw keuze in (1-5, q): {Colors.ENDC}").strip().lower()
        
        if choice == '1':
            launch_gui()
        elif choice == '2':
            launch_interactive()
        elif choice == '3':
            launch_cli()
        elif choice == '4':
            printer_setup()
        elif choice == '5':
            show_help()
        elif choice in ['q', 'quit', 'exit']:
            print(f"\n{Colors.OKCYAN}👋 Tot ziens!{Colors.ENDC}")
            break
        else:
            print(f"{Colors.FAIL}❌ Ongeldige keuze. Probeer opnieuw.{Colors.ENDC}")
    
    print(f"\n{Colors.OKCYAN}Bedankt voor het gebruik van Smart Batch PDF Printer!{Colors.ENDC}")


if __name__ == "__main__":
    main()
