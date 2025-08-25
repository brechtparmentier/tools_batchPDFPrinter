#!/bin/bash

# Smart Batch PDF Printer Launcher
# Eenvoudige launcher voor de verschillende versies van de PDF printer

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Kleuren voor output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "🖨️ =================================="
echo "   SMART BATCH PDF PRINTER"
echo "   Kies uw gewenste interface"
echo "==================================="
echo -e "${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is niet geïnstalleerd${NC}"
    echo "Installeer met: sudo apt-get install python3"
    exit 1
fi

# Check CUPS
if ! command -v lp &> /dev/null; then
    echo -e "${YELLOW}⚠️  CUPS (lp command) niet gevonden${NC}"
    echo "Installeer met: sudo apt-get install cups"
    echo "Configureer uw printer voordat u doorgaat."
    echo ""
fi

# Menu opties
echo -e "${BLUE}Beschikbare interfaces:${NC}"
echo ""
echo -e "${GREEN}1)${NC} 🖥️  GUI Interface (Grafisch - Aanbevolen voor beginners)"
echo "   - Klik en sleep interface"
echo "   - Visuele preview"
echo "   - Real-time voortgang"
echo ""
echo -e "${GREEN}2)${NC} 📱 Interactief Menu (Terminal met menu's)"
echo "   - Gebruiksvriendelijke navigatie"
echo "   - Slimme vragen en antwoorden"
echo "   - Gekleurde output"
echo ""
echo -e "${GREEN}3)${NC} ⚡ Command Line (Geavanceerd)"
echo "   - Voor ervaren gebruikers"
echo "   - Scriptbaar en automatiseerbaar"
echo "   - Snelle directe toegang"
echo ""
echo -e "${GREEN}4)${NC} ❓ Help & Informatie"
echo ""
echo -e "${GREEN}q)${NC} 🚪 Afsluiten"
echo ""

# Keuze input
while true; do
    echo -n -e "${CYAN}Voer uw keuze in (1-4, q): ${NC}"
    read -r choice
    
    case $choice in
        1)
            echo -e "\n${GREEN}🖥️  GUI Interface starten...${NC}"
            if python3 -c "import tkinter" 2>/dev/null; then
                cd "$SCRIPT_DIR"
                python3 gui_pdf_printer.py
            else
                echo -e "${RED}❌ tkinter is niet beschikbaar${NC}"
                echo "Installeer met: sudo apt-get install python3-tk"
                echo -e "\n${YELLOW}Schakel over naar interactief menu? (j/N): ${NC}"
                read -r fallback
                if [[ $fallback =~ ^[jJyY] ]]; then
                    cd "$SCRIPT_DIR"
                    python3 interactive_pdf_printer.py
                fi
            fi
            break
            ;;
        2)
            echo -e "\n${GREEN}📱 Interactief Menu starten...${NC}"
            cd "$SCRIPT_DIR"
            python3 interactive_pdf_printer.py
            break
            ;;
        3)
            echo -e "\n${GREEN}⚡ Command Line Interface${NC}"
            echo "Gebruik: python3 batch_pdf_printer.py [opties] <map>"
            echo ""
            echo "Voorbeelden:"
            echo "  python3 batch_pdf_printer.py ~/Documents"
            echo "  python3 batch_pdf_printer.py --dry-run ~/PDFs"
            echo "  python3 batch_pdf_printer.py --batch-size 5 ~/Work"
            echo ""
            echo "Voor meer opties: python3 batch_pdf_printer.py --help"
            echo ""
            echo -e "${YELLOW}Script direct uitvoeren? Voer dan het pad in (of Enter voor terug): ${NC}"
            read -r pdf_path
            if [[ -n "$pdf_path" ]]; then
                cd "$SCRIPT_DIR"
                python3 batch_pdf_printer.py "$pdf_path"
            fi
            break
            ;;
        4)
            echo -e "\n${BLUE}📖 HELP & INFORMATIE${NC}"
            echo ""
            echo -e "${YELLOW}Wat doet deze tool?${NC}"
            echo "• Zoekt recursief naar alle PDF bestanden in een map"
            echo "• Sorteert ze alfabetisch (eerst per map, dan per bestand)"
            echo "• Drukt ze af in batches met uw standaard printer"
            echo ""
            echo -e "${YELLOW}Welke interface kiezen?${NC}"
            echo -e "${GREEN}GUI Interface${NC} - Beste keuze voor de meeste gebruikers"
            echo "  ✓ Makkelijkste bediening"
            echo "  ✓ Visuele feedback"
            echo "  ✓ Drag & drop ondersteuning"
            echo ""
            echo -e "${GREEN}Interactief Menu${NC} - Voor terminal gebruikers"
            echo "  ✓ Werkt via SSH"
            echo "  ✓ Gekleurde interface"
            echo "  ✓ Stap-voor-stap begeleiding"
            echo ""
            echo -e "${GREEN}Command Line${NC} - Voor scripts en automatisering"
            echo "  ✓ Scriptbaar"
            echo "  ✓ Snelst voor herhaalde taken"
            echo "  ✓ Alle opties beschikbaar"
            echo ""
            echo -e "${YELLOW}Vereisten:${NC}"
            echo "• Python 3.6+"
            echo "• CUPS geïnstalleerd (sudo apt-get install cups)"
            echo "• Geconfigureerde printer"
            echo "• Voor GUI: tkinter (sudo apt-get install python3-tk)"
            echo ""
            echo -e "${YELLOW}Problemen oplossen:${NC}"
            echo "• Test eerst uw printer vanuit het systeem"
            echo "• Controleer CUPS status: systemctl status cups"
            echo "• Stel standaard printer in: lpoptions -d printername"
            echo "• Logs staan in: batch_pdf_printer.log"
            echo ""
            echo -e "${CYAN}Druk Enter om terug te gaan...${NC}"
            read -r
            exec "$0"  # Restart script
            ;;
        q|Q)
            echo -e "\n${CYAN}👋 Tot ziens!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Ongeldige keuze. Probeer opnieuw.${NC}"
            ;;
    esac
done

echo -e "\n${CYAN}Bedankt voor het gebruik van Smart Batch PDF Printer!${NC}"