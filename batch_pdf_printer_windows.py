#!/usr/bin/env python3
"""
Smart Batch PDF Printer - Windows Command Line Versie

Dit script zoekt recursief naar alle PDF bestanden in een directory en subdirectories,
sorteert ze alfabetisch op directory en bestandsnaam, en print ze met de 
standaard Windows printer.
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path
from typing import List, Tuple
import time
import platform


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('batch_pdf_printer.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def check_windows_printer() -> str:
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
        
        raise RuntimeError("Geen standaard printer gevonden")
        
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        raise RuntimeError(f"Kan printer status niet controleren: {e}")


def find_pdf_files(root_directory: str, verbose: bool = False) -> List[Tuple[str, str]]:
    """
    Recursively find all PDF files in the given directory and subdirectories.
    
    Args:
        root_directory: Root directory to search for PDF files
        verbose: Print detailed progress information
        
    Returns:
        List of tuples (full_path, relative_path) for sorting
    """
    pdf_files = []
    
    if verbose:
        print(f"🔍 Zoeken naar PDF bestanden in: {root_directory}")
    
    for root, dirs, files in os.walk(root_directory):
        # Sort directories to ensure consistent order
        dirs.sort()
        
        # Find PDF files in current directory
        pdf_files_in_dir = [f for f in files if f.lower().endswith('.pdf')]
        pdf_files_in_dir.sort()  # Sort filenames alphabetically
        
        for pdf_file in pdf_files_in_dir:
            full_path = os.path.join(root, pdf_file)
            relative_path = os.path.relpath(full_path, root_directory)
            pdf_files.append((full_path, relative_path))
            
            if verbose and len(pdf_files) % 10 == 0:
                print(f"   Gevonden: {len(pdf_files)} PDF bestanden...")
    
    # Sort by directory path first, then by filename
    pdf_files.sort(key=lambda x: (os.path.dirname(x[1]).lower(), os.path.basename(x[1]).lower()))
    
    return pdf_files


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def print_pdf_file(pdf_path: str, verbose: bool = False) -> bool:
    """
    Print a single PDF file using Windows default print action.
    
    Args:
        pdf_path: Full path to PDF file
        verbose: Print detailed information
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if verbose:
            print(f"   📄 Printen: {os.path.basename(pdf_path)}")
        
        # Use Windows startfile with print action
        os.startfile(pdf_path, "print")
        
        logging.info(f"Successfully sent to printer: {pdf_path}")
        return True
        
    except Exception as e:
        error_msg = f"Failed to print {pdf_path}: {e}"
        logging.error(error_msg)
        if verbose:
            print(f"   ❌ Fout: {error_msg}")
        return False


def print_pdfs_in_batches(pdf_files: List[Tuple[str, str]], batch_size: int, 
                         delay_between_batches: int, verbose: bool = False) -> Tuple[int, int]:
    """
    Print PDF files in batches to avoid overwhelming the printer.
    
    Args:
        pdf_files: List of (full_path, relative_path) tuples
        batch_size: Number of files to print in each batch
        delay_between_batches: Seconds to wait between batches
        verbose: Print detailed progress information
        
    Returns:
        Tuple of (successful_count, error_count)
    """
    total_files = len(pdf_files)
    successful_count = 0
    error_count = 0
    
    if verbose:
        print(f"\n🖨️ Print proces gestart...")
        print(f"   Totaal bestanden: {total_files}")
        print(f"   Batch grootte: {batch_size}")
        print(f"   Pauze tussen batches: {delay_between_batches} seconden")
    
    for i, (pdf_path, relative_path) in enumerate(pdf_files):
        batch_num = (i // batch_size) + 1
        file_in_batch = (i % batch_size) + 1
        
        if verbose:
            print(f"\n[Batch {batch_num}, Bestand {file_in_batch}/{batch_size}] {relative_path}")
        
        if print_pdf_file(pdf_path, verbose):
            successful_count += 1
        else:
            error_count += 1
        
        # Wait between files (shorter delay)
        time.sleep(0.5)
        
        # Wait between batches (longer delay)
        if (i + 1) % batch_size == 0 and i + 1 < total_files:
            if verbose:
                print(f"   ⏳ Batch {batch_num} voltooid, wachten {delay_between_batches} seconden...")
            time.sleep(delay_between_batches)
    
    return successful_count, error_count


def main():
    """Main function."""
    if platform.system() != "Windows":
        print("❌ Deze versie is specifiek voor Windows")
        print("Gebruik de originele versie voor Linux/Mac")
        return 1
    
    parser = argparse.ArgumentParser(
        description="Smart Batch PDF Printer voor Windows - Print PDF bestanden in batches",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voorbeelden:
  %(prog)s C:\\Users\\Documents\\PDFs
  %(prog)s --dry-run C:\\Downloads  
  %(prog)s --batch-size 5 --delay 5 C:\\Work\\PDFs
  %(prog)s --verbose C:\\Projects
        """
    )
    
    parser.add_argument('directory', 
                       help='Root directory om recursief te doorzoeken naar PDF bestanden')
    parser.add_argument('--batch-size', 
                       type=int, 
                       default=10,
                       help='Aantal bestanden per batch (standaard: 10)')
    parser.add_argument('--delay', 
                       type=int, 
                       default=3,
                       help='Seconden wachten tussen batches (standaard: 3)')
    parser.add_argument('--dry-run', 
                       action='store_true',
                       help='Toon wat er geprint zou worden zonder daadwerkelijk te printen')
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Toon gedetailleerde voortgangsinformatie')
    parser.add_argument('--list-only',
                       action='store_true', 
                       help='Toon alleen de lijst van gevonden bestanden')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Validate directory
    if not os.path.exists(args.directory):
        print(f"❌ Fout: Directory '{args.directory}' bestaat niet")
        return 1
    
    if not os.path.isdir(args.directory):
        print(f"❌ Fout: '{args.directory}' is geen directory")
        return 1
    
    # Show header
    print("🖨️ Smart Batch PDF Printer - Windows")
    print("=" * 50)
    print(f"Platform: {platform.platform()}")
    print(f"Python: {sys.version.split()[0]}")
    
    # Check printer (unless dry-run or list-only)
    if not args.dry_run and not args.list_only:
        try:
            printer_name = check_windows_printer()
            print(f"✅ Standaard printer: {printer_name}")
        except RuntimeError as e:
            print(f"❌ Printer probleem: {e}")
            print("   Stel een standaard printer in via Windows Instellingen")
            return 1
    
    print(f"📁 Zoeken in: {args.directory}")
    
    # Find PDF files
    start_time = time.time()
    pdf_files = find_pdf_files(args.directory, args.verbose)
    search_time = time.time() - start_time
    
    if not pdf_files:
        print("⚠️  Geen PDF bestanden gevonden")
        return 0
    
    print(f"\n✅ {len(pdf_files)} PDF bestanden gevonden in {search_time:.2f} seconden")
    
    # Calculate totals
    total_size = 0
    for pdf_path, _ in pdf_files:
        try:
            total_size += os.path.getsize(pdf_path)
        except OSError:
            pass
    
    print(f"📊 Totale grootte: {format_file_size(total_size)}")
    
    # List mode
    if args.list_only:
        print(f"\n📄 Gevonden PDF bestanden:")
        for i, (pdf_path, relative_path) in enumerate(pdf_files, 1):
            try:
                size = os.path.getsize(pdf_path)
                size_str = format_file_size(size)
                print(f"   {i:3d}) {relative_path} ({size_str})")
            except OSError:
                print(f"   {i:3d}) {relative_path}")
        return 0
    
    # Dry run mode
    if args.dry_run:
        print(f"\n👁️ DRY RUN - Print preview")
        print(f"Batch grootte: {args.batch_size}")
        print(f"Pauze tussen batches: {args.delay} seconden")
        print(f"Aantal batches: {(len(pdf_files) + args.batch_size - 1) // args.batch_size}")
        
        print(f"\nPrint volgorde:")
        for i, (pdf_path, relative_path) in enumerate(pdf_files, 1):
            batch_num = (i - 1) // args.batch_size + 1
            try:
                size = os.path.getsize(pdf_path)
                size_str = format_file_size(size)
                print(f"   {i:3d}) [Batch {batch_num}] {relative_path} ({size_str})")
            except OSError:
                print(f"   {i:3d}) [Batch {batch_num}] {relative_path}")
        
        print(f"\n💡 Gebruik zonder --dry-run om daadwerkelijk te printen")
        return 0
    
    # Confirmation for actual printing
    print(f"\n⚠️  U staat op het punt om {len(pdf_files)} PDF bestanden te printen")
    print("   Dit proces kan niet ongedaan worden gemaakt!")
    
    try:
        confirm = input("\nWeet u het zeker? Typ 'JA' om door te gaan: ").strip()
        if confirm.upper() != 'JA':
            print("Print proces geannuleerd")
            return 0
    except KeyboardInterrupt:
        print("\nPrint proces geannuleerd door gebruiker")
        return 0
    
    # Start printing
    print_start_time = time.time()
    
    successful_count, error_count = print_pdfs_in_batches(
        pdf_files, 
        args.batch_size, 
        args.delay,
        args.verbose
    )
    
    print_duration = time.time() - print_start_time
    
    # Results
    print(f"\n✅ Print proces voltooid!")
    print(f"   Succesvol: {successful_count}/{len(pdf_files)} bestanden")
    if error_count > 0:
        print(f"   Fouten: {error_count} bestanden")
    print(f"   Duur: {print_duration:.1f} seconden")
    print(f"   Logs: batch_pdf_printer.log")
    
    logging.info(f"Batch print completed: {successful_count}/{len(pdf_files)} successful, {error_count} errors")
    
    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Applicatie afgesloten door gebruiker")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Onverwachte fout: {e}")
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)
