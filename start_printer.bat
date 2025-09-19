@echo off
REM Smart Batch PDF Printer Windows Launcher
REM Eenvoudige Windows launcher voor de PDF printer

title Smart Batch PDF Printer

REM Check of Python beschikbaar is
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Python is niet geïnstalleerd of niet in PATH
    echo.
    echo Download Python van: https://www.python.org/downloads/
    echo Zorg ervoor dat je "Add Python to PATH" aanvinkt tijdens installatie
    echo.
    pause
    exit /b 1
)

REM Ga naar de juiste map
cd /d "%~dp0"

REM Start de Python launcher
echo.
echo 🖨️ Smart Batch PDF Printer starten...
echo.
python start_printer_windows.py

REM Wacht op gebruiker input voor sluiten
echo.
pause
