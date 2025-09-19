# Smart Batch PDF Printer Windows PowerShell Launcher
# Geavanceerde PowerShell launcher met meer controles en diagnostiek

param(
    [string]$Mode = "interactive",
    [string]$Path = "",
    [switch]$Help
)

# Kleuren instellen
$Host.UI.RawUI.WindowTitle = "Smart Batch PDF Printer"

function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Show-Banner {
    Write-Host ""
    Write-ColorText "🖨️ ====================================" "Cyan"
    Write-ColorText "   SMART BATCH PDF PRINTER" "Cyan"
    Write-ColorText "   PowerShell Versie" "Cyan"
    Write-ColorText "======================================" "Cyan"
    Write-Host ""
}

function Test-Requirements {
    $errors = @()
    $warnings = @()
    
    # Test Python
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorText "✓ Python gevonden: $pythonVersion" "Green"
        } else {
            $errors += "Python niet gevonden in PATH"
        }
    } catch {
        $errors += "Python niet geïnstalleerd"
    }
    
    # Test Windows versie
    $osVersion = [System.Environment]::OSVersion.Version
    if ($osVersion.Major -lt 10) {
        $warnings += "Windows 10/11 wordt aanbevolen"
    } else {
        Write-ColorText "✓ Windows versie: $($osVersion.Major).$($osVersion.Minor)" "Green"
    }
    
    # Test standaard printer
    try {
        $defaultPrinter = Get-WmiObject -Class Win32_Printer | Where-Object { $_.Default -eq $true }
        if ($defaultPrinter) {
            Write-ColorText "✓ Standaard printer: $($defaultPrinter.Name)" "Green"
        } else {
            $warnings += "Geen standaard printer ingesteld"
        }
    } catch {
        $warnings += "Kan printer status niet controleren"
    }
    
    # Test script bestanden
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    $requiredFiles = @("start_printer_windows.py")
    
    foreach ($file in $requiredFiles) {
        $fullPath = Join-Path $scriptPath $file
        if (Test-Path $fullPath) {
            Write-ColorText "✓ Script gevonden: $file" "Green"
        } else {
            $warnings += "Script niet gevonden: $file"
        }
    }
    
    # Rapporteer problemen
    if ($errors.Count -gt 0) {
        Write-Host ""
        Write-ColorText "❌ Fouten gevonden:" "Red"
        foreach ($error in $errors) {
            Write-ColorText "   • $error" "Red"
        }
        return $false
    }
    
    if ($warnings.Count -gt 0) {
        Write-Host ""
        Write-ColorText "⚠️ Waarschuwingen:" "Yellow"
        foreach ($warning in $warnings) {
            Write-ColorText "   • $warning" "Yellow"
        }
        Write-Host ""
    }
    
    return $true
}

function Show-Help {
    Write-Host @"

GEBRUIK:
  .\start_printer.ps1                          # Interactieve modus
  .\start_printer.ps1 -Mode gui               # Start GUI direct
  .\start_printer.ps1 -Mode cli -Path "C:\PDFs"  # Command line met pad
  .\start_printer.ps1 -Help                   # Deze hulp

PARAMETERS:
  -Mode      Kies interface: interactive, gui, cli
  -Path      PDF map voor directe verwerking (alleen bij cli)
  -Help      Toon deze hulp

VOORBEELDEN:
  # Start met grafische interface
  .\start_printer.ps1 -Mode gui
  
  # Print direct een map
  .\start_printer.ps1 -Mode cli -Path "C:\Users\Documents\PDFs"
  
  # Interactieve modus (standaard)
  .\start_printer.ps1

VEREISTEN:
  • Python 3.6+
  • Windows 10/11
  • Geconfigureerde printer
  • PowerShell 5.0+

"@
}

function Start-PythonLauncher {
    param([string]$Mode, [string]$Path)
    
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    $pythonScript = Join-Path $scriptPath "start_printer_windows.py"
    
    if (-not (Test-Path $pythonScript)) {
        Write-ColorText "❌ Python launcher niet gevonden: $pythonScript" "Red"
        return $false
    }
    
    try {
        Set-Location $scriptPath
        
        switch ($Mode.ToLower()) {
            "gui" {
                Write-ColorText "🖥️ GUI Interface starten..." "Green"
                python $pythonScript
            }
            "cli" {
                if ($Path) {
                    Write-ColorText "⚡ Command Line Interface starten met pad: $Path" "Green"
                    $cliScript = Join-Path $scriptPath "batch_pdf_printer_windows.py"
                    if (Test-Path $cliScript) {
                        python $cliScript $Path
                    } else {
                        Write-ColorText "❌ CLI script niet gevonden" "Red"
                    }
                } else {
                    Write-ColorText "❌ Pad vereist voor CLI modus" "Red"
                    Write-Host "Gebruik: .\start_printer.ps1 -Mode cli -Path `"C:\YourPDFFolder`""
                }
            }
            default {
                Write-ColorText "📱 Interactieve modus starten..." "Green"
                python $pythonScript
            }
        }
        return $true
    } catch {
        Write-ColorText "❌ Fout bij starten van Python script: $($_.Exception.Message)" "Red"
        return $false
    }
}

# Hoofdlogica
try {
    if ($Help) {
        Show-Banner
        Show-Help
        exit 0
    }
    
    Show-Banner
    
    Write-ColorText "Systeem controles uitvoeren..." "Yellow"
    if (-not (Test-Requirements)) {
        Write-ColorText "`nKan niet doorgaan vanwege fouten hierboven." "Red"
        Read-Host "Druk Enter om af te sluiten"
        exit 1
    }
    
    Write-Host ""
    Write-ColorText "Alle controles geslaagd! 🎉" "Green"
    Write-Host ""
    
    if (-not (Start-PythonLauncher $Mode $Path)) {
        Read-Host "Druk Enter om af te sluiten"
        exit 1
    }
    
} catch {
    Write-ColorText "❌ Onverwachte fout: $($_.Exception.Message)" "Red"
    Write-Host ""
    Write-ColorText "Stack trace:" "Gray"
    Write-Host $_.ScriptStackTrace -ForegroundColor Gray
    Read-Host "Druk Enter om af te sluiten"
    exit 1
}

Write-Host ""
Write-ColorText "Bedankt voor het gebruik van Smart Batch PDF Printer! 👋" "Cyan"
