#!/usr/bin/env python3
"""
Interactive Smart Batch PDF Printer

Gebruiksvriendelijke interactieve versie van de batch PDF printer
met slimme vragen en navigatie voor een betere gebruikerservaring.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Tuple, Optional
import time


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


class InteractivePDFPrinter:
    def __init__(self):
        self.setup_logging()
        self.current_directory = os.path.expanduser("~")
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
        print(f"\n{Colors.HEADER}{'='*60}")
        print("🖨️  SLIMME BATCH PDF PRINTER")
        print("   Gebruiksvriendelijke PDF batch afdrukker")
        print(f"{'='*60}{Colors.ENDC}\n")

    def print_menu(self, title: str, options: List[str], current_selection: int = 0):
        """Print een menu met opties."""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.print_header()
        print(f"{Colors.BOLD}{title}{Colors.ENDC}\n")
        
        for i, option in enumerate(options):
            if i == current_selection:
                print(f"{Colors.OKGREEN}► {i+1}. {option}{Colors.ENDC}")
            else:
                print(f"  {i+1}. {option}")
        
        print(f"\n{Colors.OKCYAN}Gebruik pijltjestoetsen ↑↓ en Enter om te selecteren, 'q' om te stoppen{Colors.ENDC}")

    def get_user_choice(self, options: List[str], title: str = "Maak uw keuze:") -> Optional[int]:
        """Interactieve menu selectie met pijltjestoetsen."""
        try:
            import termios, tty
        except ImportError:
            # Fallback voor systemen zonder termios
            return self.get_simple_choice(options, title)
            
        current = 0
        
        while True:
            self.print_menu(title, options, current)
            
            # Lees een enkele toets
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.cbreak(fd)
                key = sys.stdin.read(1)
                
                if key == '\x1b':  # ESC sequence
                    key += sys.stdin.read(2)
                    if key == '\x1b[A':  # Up arrow
                        current = (current - 1) % len(options)
                    elif key == '\x1b[B':  # Down arrow
                        current = (current + 1) % len(options)
                elif key == '\r' or key == '\n':  # Enter
                    return current
                elif key.lower() == 'q':
                    return None
                    
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def get_simple_choice(self, options: List[str], title: str) -> Optional[int]:
        """Simpele menu keuze voor systemen zonder termios."""
        print(f"\n{Colors.BOLD}{title}{Colors.ENDC}")
        for i, option in enumerate(options):
            print(f"  {i+1}. {option}")
        
        while True:
            try:
                choice = input(f"\n{Colors.OKCYAN}Voer uw keuze in (1-{len(options)}) of 'q' om te stoppen: {Colors.ENDC}")
                if choice.lower() == 'q':
                    return None
                choice_num = int(choice) - 1
                if 0 <= choice_num < len(options):
                    return choice_num
                else:
                    print(f"{Colors.WARNING}Ongeldige keuze. Probeer opnieuw.{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.WARNING}Voer een geldig nummer in.{Colors.ENDC}")

    def browse_directory(self) -> Optional[str]:
        """Interactieve directory browser."""
        current_path = self.current_directory
        
        while True:
            try:
                # Lijst mappen en een paar recente locaties
                dirs = []
                if os.path.dirname(current_path) != current_path:  # Niet root
                    dirs.append(".. (Terug naar bovenliggende map)")
                
                try:
                    items = sorted([d for d in os.listdir(current_path) 
                                  if os.path.isdir(os.path.join(current_path, d)) and not d.startswith('.')])
                    dirs.extend(items)
                except PermissionError:
                    dirs = ["[Geen toegang tot deze map]"]
                
                # Voeg snelkoppelingen toe
                shortcuts = [
                    "📁 Deze map gebruiken",
                    "🏠 Home map",
                    "📄 Documenten",
                    "⬇️  Downloads",
                    "🖥️  Bureaublad"
                ]
                
                all_options = shortcuts + ["---"] + dirs
                
                title = f"SELECTEER MAP\nHuidige locatie: {current_path}"
                choice = self.get_user_choice(all_options, title)
                
                if choice is None:
                    return None
                elif choice == 0:  # Deze map gebruiken
                    return current_path
                elif choice == 1:  # Home
                    current_path = os.path.expanduser("~")
                elif choice == 2:  # Documenten
                    docs_path = os.path.expanduser("~/Documents")
                    if os.path.exists(docs_path):
                        current_path = docs_path
                elif choice == 3:  # Downloads
                    downloads_path = os.path.expanduser("~/Downloads")
                    if os.path.exists(downloads_path):
                        current_path = downloads_path
                elif choice == 4:  # Bureaublad
                    desktop_path = os.path.expanduser("~/Desktop")
                    if os.path.exists(desktop_path):
                        current_path = desktop_path
                elif choice >= 6:  # Directory items
                    dir_index = choice - 6
                    if dir_index < len(dirs):
                        selected = dirs[dir_index]
                        if selected == ".. (Terug naar bovenliggende map)":
                            current_path = os.path.dirname(current_path)
                        elif selected != "[Geen toegang tot deze map]":
                            current_path = os.path.join(current_path, selected)
                            
            except Exception as e:
                print(f"{Colors.FAIL}Fout bij browsen: {e}{Colors.ENDC}")
                time.sleep(2)
                return None

    def find_pdf_files(self, directory: str) -> List[Tuple[str, str]]:
        """Zoek PDF bestanden recursief."""
        pdf_files = []
        total_dirs = 0
        
        print(f"\n{Colors.OKCYAN}Zoeken naar PDF bestanden...{Colors.ENDC}")
        
        for root, dirs, files in os.walk(directory):
            total_dirs += 1
            if total_dirs % 10 == 0:
                print(f"Doorzocht: {total_dirs} mappen...")
                
            dirs.sort()
            pdf_files_in_dir = [f for f in files if f.lower().endswith('.pdf')]
            pdf_files_in_dir.sort()
            
            for pdf_file in pdf_files_in_dir:
                pdf_files.append((root, pdf_file))
        
        return pdf_files

    def show_pdf_preview(self, pdf_files: List[str]) -> bool:
        """Toon preview van gevonden PDF bestanden."""
        if not pdf_files:
            print(f"\n{Colors.WARNING}Geen PDF bestanden gevonden.{Colors.ENDC}")
            input("Druk Enter om door te gaan...")
            return False
        
        print(f"\n{Colors.OKGREEN}Gevonden PDF bestanden ({len(pdf_files)} totaal):{Colors.ENDC}\n")
        
        # Toon eerste 20 bestanden
        for i, pdf_file in enumerate(pdf_files[:20], 1):
            rel_path = os.path.relpath(pdf_file, self.current_directory)
            print(f"  {i:3d}. {rel_path}")
        
        if len(pdf_files) > 20:
            print(f"  ... en nog {len(pdf_files) - 20} bestanden meer")
        
        print(f"\n{Colors.OKCYAN}Afdrukvolgorde: Eerst per map (alfabetisch), dan per bestandsnaam (alfabetisch){Colors.ENDC}")
        
        options = ["✅ Akkoord - start met afdrukken", "⚙️  Instellingen aanpassen", "🔙 Andere map kiezen"]
        choice = self.get_user_choice(options, "WAT WILT U DOEN?")
        
        return choice == 0 if choice is not None else False

    def configure_settings(self):
        """Configureer afdrukinstellingen."""
        while True:
            options = [
                f"Batch grootte: {self.batch_size} bestanden per keer",
                "🧪 Test printer (print test pagina)",
                "📄 Droge run (toon wat afgedrukt zou worden)",
                "✅ Klaar - terug naar hoofdmenu"
            ]
            
            choice = self.get_user_choice(options, "INSTELLINGEN")
            
            if choice is None or choice == 3:
                break
            elif choice == 0:  # Batch grootte
                self.set_batch_size()
            elif choice == 1:  # Test printer
                self.test_printer()
            elif choice == 2:  # Droge run
                self.dry_run()

    def set_batch_size(self):
        """Stel batch grootte in."""
        print(f"\n{Colors.BOLD}BATCH GROOTTE INSTELLEN{Colors.ENDC}")
        print(f"Huidige waarde: {self.batch_size} bestanden per batch")
        print("Aanbeveling: 5-15 bestanden (afhankelijk van printer snelheid)")
        
        try:
            new_size = input(f"\n{Colors.OKCYAN}Nieuwe batch grootte (Enter voor {self.batch_size}): {Colors.ENDC}")
            if new_size.strip():
                size = int(new_size)
                if 1 <= size <= 100:
                    self.batch_size = size
                    print(f"{Colors.OKGREEN}Batch grootte ingesteld op {size}{Colors.ENDC}")
                else:
                    print(f"{Colors.WARNING}Gebruik een waarde tussen 1 en 100{Colors.ENDC}")
            time.sleep(1)
        except ValueError:
            print(f"{Colors.WARNING}Ongeldige invoer{Colors.ENDC}")
            time.sleep(1)

    def test_printer(self):
        """Test de printer met een test pagina."""
        print(f"\n{Colors.BOLD}PRINTER TEST{Colors.ENDC}")
        
        try:
            # Maak een simpele test tekst
            test_content = """
PDF PRINTER TEST

Dit is een test om te controleren of uw printer werkt.

Datum: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """

Als u deze pagina kunt lezen, werkt uw printer correct.
"""
            
            test_file = "/tmp/printer_test.txt"
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            result = subprocess.run(['lp', test_file], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"{Colors.OKGREEN}✅ Test pagina verzonden naar printer!{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}❌ Fout bij printen: {result.stderr}{Colors.ENDC}")
                
            os.remove(test_file)
            
        except Exception as e:
            print(f"{Colors.FAIL}Fout bij printer test: {e}{Colors.ENDC}")
        
        input("\nDruk Enter om door te gaan...")

    def dry_run(self):
        """Toon wat er afgedrukt zou worden."""
        if not self.found_pdfs:
            print(f"{Colors.WARNING}Geen PDF bestanden om te tonen.{Colors.ENDC}")
            input("Druk Enter om door te gaan...")
            return
        
        print(f"\n{Colors.BOLD}DROGE RUN - WAT ZOU AFGEDRUKT WORDEN{Colors.ENDC}\n")
        
        batches = [self.found_pdfs[i:i + self.batch_size] 
                  for i in range(0, len(self.found_pdfs), self.batch_size)]
        
        for batch_num, batch in enumerate(batches, 1):
            print(f"{Colors.OKCYAN}Batch {batch_num}:{Colors.ENDC}")
            for pdf in batch:
                rel_path = os.path.relpath(pdf, self.current_directory)
                print(f"  - {rel_path}")
            print()
        
        print(f"Totaal: {len(batches)} batches, {len(self.found_pdfs)} bestanden")
        input(f"\n{Colors.OKCYAN}Druk Enter om terug te gaan...{Colors.ENDC}")

    def print_pdfs(self) -> bool:
        """Print de PDF bestanden."""
        if not self.found_pdfs:
            return False
        
        print(f"\n{Colors.BOLD}STARTEN MET AFDRUKKEN{Colors.ENDC}")
        print(f"Totaal: {len(self.found_pdfs)} bestanden in batches van {self.batch_size}")
        
        # Laatste bevestiging
        confirm = input(f"\n{Colors.WARNING}Type 'JA' om definitief te starten: {Colors.ENDC}")
        if confirm.upper() != 'JA':
            print(f"{Colors.OKCYAN}Afdrukken geannuleerd.{Colors.ENDC}")
            return False
        
        successful = 0
        failed = 0
        
        batches = [self.found_pdfs[i:i + self.batch_size] 
                  for i in range(0, len(self.found_pdfs), self.batch_size)]
        
        for batch_num, batch in enumerate(batches, 1):
            print(f"\n{Colors.OKCYAN}Batch {batch_num}/{len(batches)} ({len(batch)} bestanden)...{Colors.ENDC}")
            
            for pdf in batch:
                try:
                    result = subprocess.run(['lp', pdf], capture_output=True, text=True, check=True)
                    successful += 1
                    rel_path = os.path.relpath(pdf, self.current_directory)
                    print(f"  ✅ {rel_path}")
                    logging.info(f"Successfully printed: {pdf}")
                    
                except subprocess.CalledProcessError as e:
                    failed += 1
                    rel_path = os.path.relpath(pdf, self.current_directory)
                    print(f"  ❌ {rel_path} - Fout: {e.stderr}")
                    logging.error(f"Failed to print {pdf}: {e.stderr}")
            
            if batch_num < len(batches):
                print(f"  ⏳ Wacht 3 seconden voor volgende batch...")
                time.sleep(3)
        
        print(f"\n{Colors.BOLD}AFDRUKKEN VOLTOOID{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Succesvol: {successful}{Colors.ENDC}")
        if failed > 0:
            print(f"{Colors.FAIL}Mislukt: {failed}{Colors.ENDC}")
        
        input(f"\n{Colors.OKCYAN}Druk Enter om door te gaan...{Colors.ENDC}")
        return True

    def main_loop(self):
        """Hoofdmenu loop."""
        while True:
            options = [
                "📁 Map selecteren voor PDF bestanden",
                "⚙️  Instellingen",
                "❓ Help & informatie",
                "🚪 Afsluiten"
            ]
            
            choice = self.get_user_choice(options, "HOOFDMENU")
            
            if choice is None or choice == 3:
                print(f"\n{Colors.OKCYAN}Bedankt voor het gebruik van de PDF Printer!{Colors.ENDC}")
                break
            elif choice == 0:  # Map selecteren
                selected_dir = self.browse_directory()
                if selected_dir:
                    self.current_directory = selected_dir
                    pdf_tuples = self.find_pdf_files(selected_dir)
                    self.found_pdfs = [os.path.join(d, f) for d, f in sorted(pdf_tuples)]
                    
                    if self.show_pdf_preview(self.found_pdfs):
                        self.print_pdfs()
            elif choice == 1:  # Instellingen
                self.configure_settings()
            elif choice == 2:  # Help
                self.show_help()

    def show_help(self):
        """Toon help informatie."""
        help_text = f"""
{Colors.BOLD}HELP & INFORMATIE{Colors.ENDC}

{Colors.OKCYAN}Hoe werkt dit programma?{Colors.ENDC}
1. Selecteer een map waar PDF bestanden staan
2. Het programma zoekt recursief in alle submappen
3. Bekijk de preview van gevonden bestanden
4. Pas indien nodig instellingen aan
5. Start het afdrukken

{Colors.OKCYAN}Afdrukvolgorde:{Colors.ENDC}
- Eerst gesorteerd op mapnaam (alfabetisch)
- Daarna op bestandsnaam (alfabetisch)

{Colors.OKCYAN}Vereisten:{Colors.ENDC}
- CUPS printer systeem (Linux)
- Geconfigureerde standaard printer
- Python 3.6+

{Colors.OKCYAN}Problemen?{Colors.ENDC}
- Test eerst uw printer met de test functie
- Controleer of CUPS draait: systemctl status cups
- Logs staan in: batch_pdf_printer.log

{Colors.OKCYAN}Tips:{Colors.ENDC}
- Gebruik kleinere batches voor trage printers
- Doe altijd eerst een droge run bij grote hoeveelheden
- Het programma pauzeert tussen batches
"""
        
        print(help_text)
        input(f"\n{Colors.OKCYAN}Druk Enter om terug te gaan...{Colors.ENDC}")

    def run(self):
        """Start de applicatie."""
        try:
            self.main_loop()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.OKCYAN}Programma gestopt door gebruiker.{Colors.ENDC}")
        except Exception as e:
            print(f"\n{Colors.FAIL}Onverwachte fout: {e}{Colors.ENDC}")
            logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    app = InteractivePDFPrinter()
    app.run()