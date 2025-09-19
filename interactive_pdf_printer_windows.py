#!/usr/bin/env python3
"""
Interactive Smart Batch PDF Printer - Windows Versie

Gebruiksvriendelijke interactieve versie van de batch PDF printer
met slimme vragen en navigatie voor een betere gebruikerservaring.
Aangepast voor Windows printer ondersteuning.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Tuple, Optional
import time
import platform


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


class WindowsInteractivePDFPrinter:
    def __init__(self):
        self.setup_logging()
        self.current_directory = os.path.expanduser("~\\Documents")
        self.found_pdfs = []
        self.batch_size = 10
        
    def setup_logging(self):
        """Setup logging configuratie."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('batch_pdf_printer.log'),
            ]
        )

    def print_header(self):
        """Print welkomst header."""
        print(f"\n{Colors.HEADER}{'='*70}")
        print("🖨️  SLIMME BATCH PDF PRINTER - WINDOWS")
        print("     Interactieve versie met begeleiding")
        print(f"{'='*70}{Colors.ENDC}\n")
        
        # Toon platform info
        print(f"{Colors.OKCYAN}Platform: {platform.platform()}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Python: {sys.version.split()[0]}{Colors.ENDC}\n")

    def check_windows_printer(self) -> Optional[str]:
        """Controleer Windows printer status."""
        try:
            result = subprocess.run(['wmic', 'printer', 'where', 'default=true', 'get', 'name'], 
                                  capture_output=True, text=True, check=True, timeout=10)
            
            if result.stdout.strip() and 'No Instance(s) Available' not in result.stdout:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    printer_name = lines[-1].strip()
                    if printer_name and printer_name != 'Name':
                        return printer_name
            return None
            
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def show_printer_status(self):
        """Toon printer status informatie."""
        print(f"{Colors.OKBLUE}🖨️  PRINTER STATUS{Colors.ENDC}")
        print("=" * 50)
        
        printer = self.check_windows_printer()
        if printer:
            print(f"{Colors.OKGREEN}✅ Standaard printer: {printer}{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}⚠️  Geen standaard printer gevonden{Colors.ENDC}")
            print(f"{Colors.FAIL}   Stel een standaard printer in via Windows Instellingen{Colors.ENDC}")
        print()

    def navigate_directory(self):
        """Interactieve directory navigatie."""
        print(f"{Colors.OKBLUE}📁 DIRECTORY NAVIGATIE{Colors.ENDC}")
        print("=" * 50)
        print(f"Huidige locatie: {Colors.OKCYAN}{self.current_directory}{Colors.ENDC}")
        
        while True:
            print(f"\n{Colors.OKGREEN}Navigatie opties:{Colors.ENDC}")
            print("1) 📂 Toon inhoud van huidige map")
            print("2) 📝 Voer map pad handmatig in")
            print("3) 📋 Gebruik veel voorkomende locaties")
            print("4) ⬆️  Ga naar bovenliggende map")
            print("5) ✅ Gebruik deze map voor PDF zoeken")
            print("6) 🔙 Terug naar hoofdmenu")
            
            choice = input(f"\n{Colors.OKCYAN}Uw keuze (1-6): {Colors.ENDC}").strip()
            
            if choice == "1":
                self.show_directory_contents()
            elif choice == "2":
                self.manual_path_input()
            elif choice == "3":
                self.show_common_locations()
            elif choice == "4":
                self.go_up_directory()
            elif choice == "5":
                return True
            elif choice == "6":
                return False
            else:
                print(f"{Colors.FAIL}❌ Ongeldige keuze. Probeer opnieuw.{Colors.ENDC}")

    def show_directory_contents(self):
        """Toon inhoud van huidige directory."""
        try:
            items = os.listdir(self.current_directory)
            dirs = [item for item in items if os.path.isdir(os.path.join(self.current_directory, item))]
            files = [item for item in items if os.path.isfile(os.path.join(self.current_directory, item))]
            
            dirs.sort()
            files.sort()
            
            print(f"\n{Colors.OKBLUE}📂 Inhoud van {self.current_directory}:{Colors.ENDC}")
            
            if dirs:
                print(f"\n{Colors.OKGREEN}📁 Mappen:{Colors.ENDC}")
                for i, dir_name in enumerate(dirs[:10], 1):  # Toon max 10 items
                    print(f"   {i:2d}) 📁 {dir_name}")
                if len(dirs) > 10:
                    print(f"      ... en {len(dirs) - 10} meer")
            
            if files:
                pdf_files = [f for f in files if f.lower().endswith('.pdf')]
                if pdf_files:
                    print(f"\n{Colors.WARNING}📄 PDF bestanden in deze map:{Colors.ENDC}")
                    for i, pdf in enumerate(pdf_files[:5], 1):
                        print(f"   {i:2d}) 📄 {pdf}")
                    if len(pdf_files) > 5:
                        print(f"      ... en {len(pdf_files) - 5} meer PDF's")
                
                print(f"\n{Colors.OKCYAN}💡 Totaal: {len(dirs)} mappen, {len(files)} bestanden ({len(pdf_files)} PDF's){Colors.ENDC}")
            
            # Optie om naar submap te gaan
            if dirs:
                print(f"\n{Colors.OKGREEN}Wilt u naar een submap gaan?{Colors.ENDC}")
                folder_choice = input("Voer mapnaam in (of Enter om door te gaan): ").strip()
                if folder_choice and folder_choice in dirs:
                    self.current_directory = os.path.join(self.current_directory, folder_choice)
                    print(f"{Colors.OKGREEN}✅ Naar map gegaan: {self.current_directory}{Colors.ENDC}")
                
        except PermissionError:
            print(f"{Colors.FAIL}❌ Geen toegang tot deze map{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}❌ Fout bij lezen map: {e}{Colors.ENDC}")

    def manual_path_input(self):
        """Handmatige pad invoer."""
        print(f"\n{Colors.OKBLUE}📝 HANDMATIGE PAD INVOER{Colors.ENDC}")
        print("Voorbeelden:")
        print("  C:\\Users\\YourName\\Documents\\PDFs")
        print("  D:\\Work\\Projects\\PDF_Files")
        print("  C:\\Downloads")
        
        new_path = input(f"\n{Colors.OKCYAN}Voer volledig pad in: {Colors.ENDC}").strip()
        
        if new_path:
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_directory = new_path
                print(f"{Colors.OKGREEN}✅ Map succesvol ingesteld: {new_path}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}❌ Map bestaat niet of is geen geldige map{Colors.ENDC}")

    def show_common_locations(self):
        """Toon veel voorkomende Windows locaties."""
        print(f"\n{Colors.OKBLUE}📋 VEEL VOORKOMENDE LOCATIES{Colors.ENDC}")
        
        common_paths = {
            "1": ("Documents", os.path.expanduser("~\\Documents")),
            "2": ("Downloads", os.path.expanduser("~\\Downloads")),
            "3": ("Desktop", os.path.expanduser("~\\Desktop")),
            "4": ("Pictures", os.path.expanduser("~\\Pictures")),
            "5": ("OneDrive Documents", os.path.expanduser("~\\OneDrive\\Documents")),
            "6": ("C:\\ Drive", "C:\\"),
        }
        
        for key, (name, path) in common_paths.items():
            exists = "✅" if os.path.exists(path) else "❌"
            print(f"{key}) {exists} {name}: {path}")
        
        choice = input(f"\n{Colors.OKCYAN}Kies locatie (1-6, of Enter om over te slaan): {Colors.ENDC}").strip()
        
        if choice in common_paths:
            name, path = common_paths[choice]
            if os.path.exists(path):
                self.current_directory = path
                print(f"{Colors.OKGREEN}✅ Locatie ingesteld: {name}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}❌ Locatie bestaat niet: {path}{Colors.ENDC}")

    def go_up_directory(self):
        """Ga naar bovenliggende directory."""
        parent = os.path.dirname(self.current_directory)
        if parent != self.current_directory:  # Niet bij root
            self.current_directory = parent
            print(f"{Colors.OKGREEN}✅ Omhoog gegaan naar: {self.current_directory}{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}⚠️  Al bij de hoofdmap van het systeem{Colors.ENDC}")

    def find_pdf_files(self, root_directory: str) -> List[Tuple[str, str]]:
        """Vind alle PDF bestanden recursief."""
        pdf_files = []
        
        print(f"{Colors.OKCYAN}🔍 Zoeken naar PDF bestanden...{Colors.ENDC}")
        
        try:
            for root, dirs, files in os.walk(root_directory):
                dirs.sort()
                
                pdf_files_in_dir = [f for f in files if f.lower().endswith('.pdf')]
                pdf_files_in_dir.sort()
                
                for pdf_file in pdf_files_in_dir:
                    full_path = os.path.join(root, pdf_file)
                    rel_path = os.path.relpath(full_path, root_directory)
                    pdf_files.append((full_path, rel_path))
                
                # Toon voortgang
                if len(pdf_files) % 50 == 0 and len(pdf_files) > 0:
                    print(f"   Gevonden: {len(pdf_files)} PDF's...")
                    
        except Exception as e:
            print(f"{Colors.FAIL}❌ Fout bij zoeken: {e}{Colors.ENDC}")
        
        return pdf_files

    def search_and_list_pdfs(self):
        """Zoek en toon PDF bestanden."""
        print(f"\n{Colors.OKBLUE}🔍 PDF ZOEKEN EN PREVIEW{Colors.ENDC}")
        print("=" * 50)
        
        print(f"Zoeken in: {Colors.OKCYAN}{self.current_directory}{Colors.ENDC}")
        
        start_time = time.time()
        self.found_pdfs = self.find_pdf_files(self.current_directory)
        search_time = time.time() - start_time
        
        if not self.found_pdfs:
            print(f"\n{Colors.WARNING}⚠️  Geen PDF bestanden gevonden in deze map{Colors.ENDC}")
            print(f"{Colors.OKCYAN}💡 Tip: Controleer of er submappen zijn met PDF's{Colors.ENDC}")
            return False
        
        print(f"\n{Colors.OKGREEN}✅ {len(self.found_pdfs)} PDF bestanden gevonden in {search_time:.2f} seconden{Colors.ENDC}")
        
        # Toon eerste paar bestanden als preview
        print(f"\n{Colors.OKBLUE}📄 Preview (eerste 10 bestanden):{Colors.ENDC}")
        for i, (full_path, rel_path) in enumerate(self.found_pdfs[:10], 1):
            try:
                size = os.path.getsize(full_path)
                size_str = self.format_file_size(size)
                print(f"   {i:2d}) {rel_path} ({size_str})")
            except:
                print(f"   {i:2d}) {rel_path}")
        
        if len(self.found_pdfs) > 10:
            print(f"   ... en {len(self.found_pdfs) - 10} meer bestanden")
        
        return True

    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

    def test_windows_printer(self) -> bool:
        """Test de Windows printer."""
        print(f"\n{Colors.OKBLUE}🧪 PRINTER TEST{Colors.ENDC}")
        print("=" * 50)
        
        printer = self.check_windows_printer()
        if not printer:
            print(f"{Colors.FAIL}❌ Geen standaard printer gevonden{Colors.ENDC}")
            print(f"{Colors.WARNING}   Stel eerst een standaard printer in via Windows Instellingen{Colors.ENDC}")
            return False
        
        print(f"{Colors.OKGREEN}✅ Standaard printer: {printer}{Colors.ENDC}")
        
        # Zoek een test PDF in de gevonden bestanden
        if self.found_pdfs:
            test_file = self.found_pdfs[0][0]  # Eerste PDF
            print(f"\n{Colors.OKCYAN}Test bestand: {os.path.basename(test_file)}{Colors.ENDC}")
            
            confirm = input(f"{Colors.WARNING}Wilt u dit bestand als test printen? (j/N): {Colors.ENDC}").strip().lower()
            
            if confirm in ['j', 'ja', 'y', 'yes']:
                try:
                    print(f"{Colors.OKCYAN}🖨️ Verzenden naar printer...{Colors.ENDC}")
                    os.startfile(test_file, "print")
                    print(f"{Colors.OKGREEN}✅ Test print opdracht verzonden!{Colors.ENDC}")
                    print(f"{Colors.OKCYAN}   Controleer of het document wordt afgedrukt{Colors.ENDC}")
                    return True
                except Exception as e:
                    print(f"{Colors.FAIL}❌ Fout bij test printen: {e}{Colors.ENDC}")
                    return False
        else:
            print(f"{Colors.WARNING}⚠️  Geen PDF bestanden beschikbaar voor test{Colors.ENDC}")
            
        return False

    def configure_print_settings(self):
        """Configureer print instellingen."""
        print(f"\n{Colors.OKBLUE}⚙️  PRINT INSTELLINGEN{Colors.ENDC}")
        print("=" * 50)
        
        print(f"Huidige batch grootte: {Colors.OKGREEN}{self.batch_size}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}💡 Batch grootte bepaalt hoeveel bestanden tegelijk naar de printer gaan{Colors.ENDC}")
        print(f"{Colors.OKCYAN}   Kleinere batches = minder belasting op printer{Colors.ENDC}")
        
        while True:
            try:
                new_size = input(f"\n{Colors.OKCYAN}Nieuwe batch grootte (1-50, Enter=behouden): {Colors.ENDC}").strip()
                if not new_size:
                    break
                
                new_size = int(new_size)
                if 1 <= new_size <= 50:
                    self.batch_size = new_size
                    print(f"{Colors.OKGREEN}✅ Batch grootte ingesteld op {new_size}{Colors.ENDC}")
                    break
                else:
                    print(f"{Colors.FAIL}❌ Voer een getal tussen 1 en 50 in{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.FAIL}❌ Voer een geldig getal in{Colors.ENDC}")

    def show_print_preview(self):
        """Toon preview van print volgorde."""
        if not self.found_pdfs:
            print(f"{Colors.WARNING}⚠️  Geen PDF bestanden gevonden voor preview{Colors.ENDC}")
            return
        
        print(f"\n{Colors.OKBLUE}👁️  PRINT PREVIEW{Colors.ENDC}")
        print("=" * 50)
        print(f"Totaal bestanden: {Colors.OKGREEN}{len(self.found_pdfs)}{Colors.ENDC}")
        print(f"Batch grootte: {Colors.OKGREEN}{self.batch_size}{Colors.ENDC}")
        print(f"Aantal batches: {Colors.OKGREEN}{(len(self.found_pdfs) + self.batch_size - 1) // self.batch_size}{Colors.ENDC}")
        
        print(f"\n{Colors.OKBLUE}Print volgorde:{Colors.ENDC}")
        for i, (full_path, rel_path) in enumerate(self.found_pdfs, 1):
            batch_num = (i - 1) // self.batch_size + 1
            batch_marker = f"[Batch {batch_num}]"
            print(f"   {i:3d}) {batch_marker:10} {rel_path}")
            
            if i >= 20:  # Toon max 20 items
                print(f"   ... en {len(self.found_pdfs) - 20} meer bestanden")
                break
        
        input(f"\n{Colors.OKCYAN}Druk Enter om door te gaan...{Colors.ENDC}")

    def print_pdfs(self) -> bool:
        """Print alle gevonden PDF bestanden."""
        if not self.found_pdfs:
            print(f"{Colors.WARNING}⚠️  Geen PDF bestanden om te printen{Colors.ENDC}")
            return False
        
        print(f"\n{Colors.OKBLUE}🖨️  PDF BESTANDEN PRINTEN{Colors.ENDC}")
        print("=" * 50)
        
        # Laatste bevestiging
        print(f"{Colors.WARNING}⚠️  U staat op het punt om {len(self.found_pdfs)} PDF bestanden te printen{Colors.ENDC}")
        print(f"{Colors.WARNING}   Dit proces kan niet ongedaan worden gemaakt!{Colors.ENDC}")
        
        confirm = input(f"\n{Colors.OKCYAN}Weet u het zeker? Typ 'JA' om door te gaan: {Colors.ENDC}").strip()
        
        if confirm.upper() != 'JA':
            print(f"{Colors.OKCYAN}Print proces geannuleerd{Colors.ENDC}")
            return False
        
        # Start printing
        print(f"\n{Colors.OKGREEN}🖨️ Print proces gestart...{Colors.ENDC}")
        start_time = time.time()
        printed_count = 0
        errors = 0
        
        for i, (pdf_path, rel_path) in enumerate(self.found_pdfs, 1):
            try:
                print(f"{Colors.OKCYAN}[{i:3d}/{len(self.found_pdfs)}] Printen: {os.path.basename(pdf_path)}{Colors.ENDC}")
                
                os.startfile(pdf_path, "print")
                printed_count += 1
                
                # Pauze na elke batch
                if i % self.batch_size == 0 and i < len(self.found_pdfs):
                    print(f"{Colors.WARNING}   ⏳ Batch {(i // self.batch_size)} voltooid, wachten 3 seconden...{Colors.ENDC}")
                    time.sleep(3)
                else:
                    time.sleep(0.5)  # Korte pauze tussen bestanden
                
            except Exception as e:
                errors += 1
                print(f"{Colors.FAIL}   ❌ Fout bij printen {os.path.basename(pdf_path)}: {e}{Colors.ENDC}")
                logging.error(f"Print error for {pdf_path}: {e}")
        
        # Resultaten
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n{Colors.OKGREEN}✅ Print proces voltooid!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}   Succesvol: {printed_count}/{len(self.found_pdfs)} bestanden{Colors.ENDC}")
        if errors > 0:
            print(f"{Colors.WARNING}   Fouten: {errors} bestanden{Colors.ENDC}")
        print(f"{Colors.OKCYAN}   Duur: {duration:.1f} seconden{Colors.ENDC}")
        
        logging.info(f"Batch print completed: {printed_count}/{len(self.found_pdfs)} successful, {errors} errors")
        return True

    def main_menu(self):
        """Toon hoofdmenu en verwerk keuzes."""
        while True:
            print(f"\n{Colors.OKGREEN}HOOFDMENU - Wat wilt u doen?{Colors.ENDC}")
            print("=" * 50)
            
            options = [
                "📁 Directory kiezen en navigeren",
                "🔍 PDF bestanden zoeken in huidige map",
                "👁️  Print preview bekijken",
                "⚙️  Print instellingen configureren",
                "🧪 Printer testen",
                "🖨️  PDF bestanden printen",
                "❓ Help & informatie",
                "🚪 Afsluiten"
            ]
            
            for i, option in enumerate(options, 1):
                print(f"{i}) {option}")
            
            choice = input(f"\n{Colors.OKCYAN}Uw keuze (1-{len(options)}): {Colors.ENDC}").strip()
            
            try:
                choice_num = int(choice)
                if choice_num == 1:
                    if self.navigate_directory():
                        # Automatisch zoeken na directory selectie
                        self.search_and_list_pdfs()
                elif choice_num == 2:
                    self.search_and_list_pdfs()
                elif choice_num == 3:
                    self.show_print_preview()
                elif choice_num == 4:
                    self.configure_print_settings()
                elif choice_num == 5:
                    self.test_windows_printer()
                elif choice_num == 6:
                    if self.found_pdfs:
                        self.print_pdfs()
                    else:
                        print(f"{Colors.WARNING}⚠️  Zoek eerst naar PDF bestanden (optie 2){Colors.ENDC}")
                elif choice_num == 7:
                    self.show_help()
                elif choice_num == 8:
                    print(f"\n{Colors.OKCYAN}👋 Tot ziens! Bedankt voor het gebruik van Smart Batch PDF Printer{Colors.ENDC}")
                    break
                else:
                    print(f"{Colors.FAIL}❌ Ongeldige keuze. Kies een getal tussen 1 en {len(options)}{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.FAIL}❌ Voer een geldig getal in{Colors.ENDC}")

    def show_help(self):
        """Toon help informatie."""
        help_text = f"""
{Colors.BOLD}HELP & INFORMATIE{Colors.ENDC}

{Colors.OKBLUE}Wat doet deze applicatie?{Colors.ENDC}
• Zoekt recursief naar alle PDF bestanden in een map
• Sorteert ze alfabetisch (eerst per map, dan per bestandsnaam)  
• Print ze in batches naar uw standaard Windows printer

{Colors.OKBLUE}Hoe te gebruiken?{Colors.ENDC}
1) Kies een map met PDF bestanden (optie 1)
2) Zoek naar PDF bestanden (optie 2) 
3) Bekijk de preview (optie 3)
4) Configureer instellingen indien nodig (optie 4)
5) Test uw printer (optie 5)
6) Start het printen (optie 6)

{Colors.OKBLUE}Windows specifiek:{Colors.ENDC}
• Gebruikt Windows Print API (geen CUPS nodig)
• Werkt met alle Windows printers
• Ondersteunt Windows printer dialogen

{Colors.OKBLUE}Tips voor succesvol printen:{Colors.ENDC}
• Zorg dat uw printer aan staat en klaar is
• Test eerst met een enkel document
• Gebruik kleinere batch grootte bij problemen
• Controleer dat PDF's niet vergrendeld zijn
• Kijk in de log file bij problemen

{Colors.OKBLUE}Batch grootte:{Colors.ENDC}
• Standaard: 10 bestanden per batch
• Kleinere batches = minder printerbelasting
• Tussen batches is een pauze van 3 seconden

{Colors.OKBLUE}Problemen oplossen:{Colors.ENDC}
• Geen printer? → Windows Instellingen → Printers & scanners
• Print fouten? → Test met andere PDF viewer
• Langzaam printen? → Verklein batch grootte
• Logs bekijken? → batch_pdf_printer.log
"""
        print(help_text)
        input(f"{Colors.OKCYAN}Druk Enter om terug te gaan naar het hoofdmenu...{Colors.ENDC}")

    def run(self):
        """Start de interactieve applicatie."""
        try:
            self.print_header()
            self.show_printer_status()
            
            print(f"{Colors.OKGREEN}Welkom bij de interactieve PDF printer!{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Deze applicatie helpt u stap-voor-stap bij het batch printen van PDF's{Colors.ENDC}")
            
            self.main_menu()
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.OKCYAN}👋 Applicatie afgesloten door gebruiker{Colors.ENDC}")
        except Exception as e:
            print(f"\n{Colors.FAIL}❌ Onverwachte fout: {e}{Colors.ENDC}")
            logging.error(f"Unexpected error: {e}")


def main():
    """Hoofdfunctie."""
    if platform.system() != "Windows":
        print("❌ Deze versie is specifiek voor Windows")
        print("Gebruik de originele versie voor Linux/Mac")
        return
    
    try:
        printer = WindowsInteractivePDFPrinter()
        printer.run()
    except Exception as e:
        print(f"❌ Fout bij starten applicatie: {e}")
        input("Druk Enter om af te sluiten...")


if __name__ == "__main__":
    main()
